import socket
from threading import Thread
from ipaddress import ip_address


class Client:
    def __init__(self, name, host, port, max_size):
        """ Initializing client socket
            Takes 3 arguments: name, host, port and max size of message
        """

        try:
            _ = ip_address(host)
            self._host = host
        except Exception as ex:
            print(ex)
        else:
            try:
                if isinstance(port, int) and 0 < port <= 65535:
                    self._port = port
                else:
                    raise ValueError("This is not correct port!")
            except ValueError as ex:
                print(ex)

        self._name = name
        self._max_size = max_size

        self.__server = (self._host, self._port)

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.__receiving_thread = Thread(target=self.__receive)

    def send_message(self, message):
        """ Sends message to server """
        if message != self._name:
            message = f'[Nickname - {self._name}]: {message}'
        try:
            self.__client.sendto(message.encode('utf-8'), self.__server)
        except Exception as e:
            print(e)

    def __receive(self):
        while True:
            data, address = self.__client.recvfrom(self._max_size)
            print(data.decode('utf-8'))

    def start_work(self):
        """ Starts work of client """
        self.send_message(self._name)
        self.__receiving_thread.start()


if __name__ == '__main__':
    import os
    import sys

    FILE_NAME = 'settings.conf'

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as file:
            data = file.read().split()
            ip = data[0]
            port = int(data[1])
            max_size = int(data[2])

        while True:
            try:
                name = input('Input Nickname:')
                if not name:
                    raise ValueError()
                break
            except ValueError:
                print('This is empty string!')

        client = Client(name, ip, port, max_size)

        print('Client is initialized')
        print('Connect to server? [y/n]')

        while True:
            try:
                choice = input().lower()
                if choice not in 'y n'.split():
                    raise ValueError()
                break
            except ValueError:
                print('Not correct choice!')

        if choice == 'y':
            client.start_work()

            while True:
                message = input()
                client.send_message(message)

        else:
            sys.exit()

    else:
        raise FileNotFoundError(f'File {FILE_NAME} not found.')
