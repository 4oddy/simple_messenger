import time
import socket


class Server:
    def __init__(self, host, port, max_size):
        self._host = host
        self._port = port
        self._max_size = max_size

        self.__clients = list()
        self.__running = True

        self.__server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.__alert_new_client_default = '[{}][Nickname - {}]: Client {}-{} has connected'

    def start_server(self):
        """Binds server after initializing
           
           You need to use this method before server_forever method
           
        """
        print(f'[{self.__get_now_local_time()}] - ({self._host}, {self._port}) Server has been started')
        self.__server.bind((self._host, self._port))

    def serve_forever(self):
        """ Main loop of server
            
            To use this method, you have to complete start_server() command
            
        """
        while self.__running:
            try:
                data, address = self.__server.recvfrom(self._max_size)

                nickname = data.decode('utf-8').split()[0]

                if address not in self.__clients:
                    self.__clients.append(address)

                    print(self.__alert_new_client_default.format(self.__get_now_local_time(), nickname,
                                                                 address[0], address[1]))

                    self.__send_message(address, self.__alert_new_client_default.format(self.__get_now_local_time(),
                                                                                        nickname, address[0],
                                                                                        address[1]).encode('utf-8'))
                else:
                    data = data.decode('utf-8')
                    self.__send_message(address,
                                        f'[{self.__get_now_local_time()}]{data}'
                                        .encode('utf-8'))

            except Exception:
                print(f'[{self.__get_now_local_time()}] - Somebody has left chat')
                self.__running = False

    def __send_message(self, address, message):
        for client in self.__clients:
            if client != address:
                self.__server.sendto(message, client)

    def __get_now_local_time(self):
        return time.strftime('%Y-%m-%d|%H:%M:%S', time.localtime())


if __name__ == '__main__':
    import os
    import sys
    from ipaddress import ip_address
    from colorama import init, Fore

    DEFAULT_MAX_SIZE = 1024
    FILE_NAME = 'settings.conf'

    init()

    print(Fore.GREEN + 'Welcome!')

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as file:
            data = file.read().split()
            ip = data[0]
            port = int(data[1])
            max_size = int(data[2])

    else:
        while True:
            try:
                print(Fore.WHITE + 'Input your IP:')
                ip = input()
                ip_check = ip_address(ip)
                break
            except Exception:
                print('This is not correct IP!')

        while True:
            try:
                print('Input your port:')
                port = int(input())
                break
            except Exception:
                print('This is not correct port!')

        with open(FILE_NAME, 'w') as file:
            max_size = DEFAULT_MAX_SIZE

            file.write(f'{ip} {port} {max_size}')

    serv = Server(ip, port, max_size)

    print(Fore.WHITE + 'Server has been initialized')
    print('Start server? [y/n]')

    while True:
        try:
            choice = input().lower()
            if choice not in 'y n'.split():
                raise ValueError()
            break
        except ValueError:
            print('Not correct choice!')

    if choice == 'y':
        serv.start_server()
        serv.serve_forever()
    else:
        sys.exit()
