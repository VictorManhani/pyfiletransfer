import socket
from os import mkdir
from os.path import basename, join, abspath, dirname
from path import convert_path
from buffer import Buffer

class FileServer:
    connection = None

    def __init__(self, *args, **kwargs):
        # if host not set, the default is 0.0.0.0
        self.host = kwargs.get("host", "0.0.0.0")
        # if port not set, the default is 5001
        self.port = kwargs.get("port", 5001)
        # receive 4096 bytes each time
        self.buffer_size = kwargs.get("buffer_size", 4096)
        # file separator
        self.separator = kwargs.get("separator", "<SEPARATOR>")
        # absolute path
        self.app_path = kwargs.get("app_path", dirname(abspath(__file__)))
        # input path
        self.path = kwargs.get("path", join(self.app_path, "output"))
        # initilize socket connection
        self.connection = self.get_connection(self.host, self.port)

    def get_connection(self, host, port):
        # create the server socket
        # TCP socket
        connection = socket.socket()
        # bind the socket to our local address
        connection.bind((host, port))
        return connection

    def file_print(self, filename, filepath, filesize):
        # hashs = (len(filename)+len(str(filesize))) * "#"
        # print("%s [FILE TRANSFER] %s" % (hashs, hashs))
        print("\n[FILE NAME]:", filename)
        print("[FILE PATH]:", filepath)
        print("[FILE SIZE]:", filesize, "\n")

    def create_folder(self, foldername):
        try:
            mkdir(foldername)
        except OSError:
            print ("Creation of the directory %s failed" % foldername)
        else:
            print ("Successfully created the directory %s " % foldername)

    def receive_file(self):
        # listen port until n requesters
        self.connection.listen(20)

        # accept connection if there is any
        client_socket, address = self.connection.accept()
        
        # if below code is executed, that means the sender is connected
        print(f"[+] {address} is connected.")

        # receive the file infos
        # receive using client socket, not server socket
        received = client_socket.recv(self.buffer_size).decode()
        filename, filesize, filetype = received.split(self.separator)
        # remove absolute path if there is
        filename = basename(filename)

        # convert to integer
        filesize = filesize or int(filesize)
        # file path
        filepath = join(self.path, filename)

        if filetype == "folder":
            self.create_folder(filepath)
            return

        # progress = tqdm.tqdm(
        #     iterable=range(filesize), desc = f"Receiving {filename}", 
        #     unit="B", unit_scale=True, unit_divisor=1024)

        # pretty print
        self.file_print(filename, filepath, filesize)

        with open(filepath, "wb") as f:
            while True:
                try:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = client_socket.recv(self.buffer_size)
                    if not bytes_read:    
                        # nothing is received
                        # file transmitting is done
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    
                    # update the progress bar
                    # progress.update(len(bytes_read))
                except KeyboardInterrupt:
                    break

        # close the client socket
        client_socket.close()

    def bulk_receive_file(self):
        """start receiving the file from the socket
        and writing to the file stream"""

        # listen port until n requesters
        self.connection.listen(20)

        while True:
            print("\nCONNECTION ACCEPT")
            # accept connection if there is any
            client_socket, address = self.connection.accept()
            # if below code is executed, that means the sender is connected
            print(f"[+] {address} is connected.")
            # generate buffer
            sbuf = Buffer(client_socket, self.buffer_size)

            while True:
                # get text from buffer
                received = sbuf.get_utf8()
                # get filename and filesize
                filename, filesize, filetype = received.split(self.separator)
                # print(filename, filesize)

                # remove absolute path if there is
                filename = basename(convert_path(filename))

                # convert to integer
                filesize = int(filesize)

                # file path
                filepath = join(self.path, filename)

                if filetype == "folder":
                    print(filetype, filepath)
                    self.create_folder(filepath)
                    return

                # pretty print
                self.file_print(filename, filepath, filesize)

                # progress = tqdm.tqdm(
                #     iterable=range(filesize), desc=f"Receiving {filename}", 
                #     unit="B", unit_scale=True, unit_divisor=1024)

                with open(filepath, "wb") as f:
                    sbuf.get_bytes(f)
                    break

            client_socket.close()

if __name__ == "__main__":
    from local import (
        server_host, port, buffer_size, separator,
        app_path, server_path
    )
    fs = FileServer(
        host=server_host, port=port, buffer_size=buffer_size,
        separator=separator, app_path=app_path, path=server_path
    )
    # fs.receive_file() # get only one file
    fs.bulk_receive_file() # listens port and receive files, saving at file path