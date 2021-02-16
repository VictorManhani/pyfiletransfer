
class Buffer:
    def __init__(self, s, buffer_size=4092):
        '''Buffer a pre-created socket.
        '''
        self.sock = s
        self.buffer = b''
        self.buffer_size = buffer_size

    def get_bytes(self, f, progress=None):
        """Write the new file at progress with buffer size"""
        data = self.sock.recv(self.buffer_size)
        while data:
            f.write(data)
            data = self.sock.recv(self.buffer_size)
        # close the client socket
        self.sock.close()
        print('File received successfully.')

    def put_bytes(self, f, progress=None):
        while True:
            # read the bytes from the file
            bytes_read = f.read(self.buffer_size)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            self.sock.sendall(bytes_read)

            # update the progress bar
            if progress:
                progress.update(len(bytes_read))

        # self.sock.close()
        # self.sock.sendall(data)

        # 2º MODE OF DATA TRANSMISSION
        # data = f.read(self.buffer_size)
        # while data:
        #     self.sock.send(data)
        #     data = f.read(self.buffer_size)

    def get_utf8(self):
        """Get text at header"""
        # receive using client socket, not server socket
        received = self.sock.recv(self.buffer_size).decode()
        return received

    def put_utf8(self, s):
        self.sock.send(s.encode())