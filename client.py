import socket
from os import listdir
from os.path import abspath, join, dirname, getsize, exists
from buffer import Buffer

class FileClient:
    connection = None

    def __init__(self, *args, **kwargs):
        # separator
        self.separator = "<SEPARATOR>"

        # send 4096 bytes each time step
        self.buffer_size = 4096

        # the ip address or hostname of the server, the receiver
        self.host = kwargs.get("host", "localhost") # "192.168.1.101"

        # the port, let's use 5001 as default
        self.port = kwargs.get("port", 5001)

        # absolute path
        self.app_abspath = dirname(abspath(__file__))

        # input path
        self.input_path = join(self.app_abspath, "input")

        self.get_connection()

    def get_connection(self):
        if self.connection:
            self.connection.close()

        # create the client socket
        self.connection = socket.socket()
        print(f"[+] Connecting to {self.host}:{self.port}")
        # connecting to the server:

    def file_print(self, filename, filepath, filesize):
        print("\n[FILE NAME]:", filename)
        print("[FILE PATH]:", filepath)
        print("[FILE SIZE]:", filesize, "\n")

    def send_file(self, filename):
        # join input path with filename
        filepath = join(self.input_path, filename)
        
        if not exists(filepath):
            print(f"[ERROR]: file {filepath} doesn't exist")
            return

        # get the file size
        filesize = getsize(filepath)
        
        self.connection.connect((self.host, self.port))
        print("[+] Connected.")

        sbuf = Buffer(self.connection, self.buffer_size)
        sbuf.put_utf8(f"{filepath}{self.separator}{filesize}")

        # pretty print at terminal
        self.file_print(filename, filepath, filesize)

        # start sending the file
        # import tqdm
        # progress = tqdm.tqdm(
        #     range(filesize), f"Sending {filepath}", unit="B", 
        #     unit_scale=True, unit_divisor=1024)

        with open(filepath, "rb") as file_:
            sbuf.put_bytes(file_)
            self.connection.close()
            self.get_connection()

    def bulk_send_file(self):
        for filename in listdir(self.input_path):
            self.send_file(filename)

if __name__ == "__main__":
    from local import client_host

    # if host not set, the default is localhost
    fc = FileClient(host=client_host)
    # fc.send_file("abc.txt")
    fc.bulk_send_file() # send all files from input path to server
