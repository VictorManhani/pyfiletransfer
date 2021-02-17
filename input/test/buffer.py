
class Buffer:
    def __init__(self, s, buffer_size=4096):
        '''Buffer a pre-created socket.
        '''
        self.sock = s
        self.buffer_size = buffer_size

    def get_bytes(self, f, progress=None):
        """Write the new file at progress with buffer size"""
        data = self.sock.recv(self.buffer_size)
        while data:
            f.write(data)
            data = self.sock.recv(self.buffer_size)

            # update the progress bar if progress not None
            if progress:
                progress.update(len(data))

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

            # update the progress bar if progress not None
            if progress:
                progress.update(len(bytes_read))
        
        print('File sended successfully.')

    def get_utf8(self):
        """Get file metadata from client and decode to utf-8 string."""
        received = self.sock.recv(self.buffer_size).decode("ISO-8859-1")
        return received

    def put_utf8(self, meta):
        """Send file metadata as bytes."""
        self.sock.send(meta.encode())