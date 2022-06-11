import socket
from threading import Thread


class Client:
    def __init__(self, name, host, port, max_size):
        """ Initializing client socket
            Takes 3 arguments: name, host, port and max size of message
        """

        if name.strip():
            self._name = name
        else:
            raise ValueError('Name cannot be empty string')

        self._host = host
        self._port = int(port)
        self._max_size = int(max_size)

        self.__server = (self._host, self._port)

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.__receiving_thread = Thread(target=self.__receive)

    def send_message(self, message):
        """ Sends message to server """
        message = f'[Nickname - {self._name}]: {message}'
        try:
            self.__client.sendto(message.encode('utf-8'), self.__server)
        except Exception as ex:
            print(ex)

    def __send_initial_message(self):
        try:
            self.__client.sendto(self._name.encode('utf-8'), self.__server)
        except Exception as ex:
            print(ex)

    def __receive(self):
        while True:
            data, address = self.__client.recvfrom(self._max_size)
            print(data.decode('utf-8'))

    def start_work(self):
        """ Starts work of client """
        self.__send_initial_message()
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
            name = input('Input nickname:')
            if not name.strip():
                print('Incorrect name!')
            else:
                break

        client = Client(name, ip, port, max_size)

        print('Client is initialized')
        print('Connect to server? [y/n]')

        while True:
            choice = input().lower()
            if choice in 'yn':
                break
            else:
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
