# references
# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
# https://www.csestack.org/python-oserror-winerror-10022-invalid-argument-was-supplied/
# https://stackoverflow.com/questions/53136368/sending-multiple-files-python-using-socket
# https://linuxhint.com/python_socket_file_transfer_send/
# https://stackoverflow.com/questions/1325581/how-do-i-check-if-im-running-on-windows-in-python
# https://stackoverflow.com/questions/13162372/using-absolute-unix-paths-in-windows-with-python
# https://stackoverflow.com/questions/25146960/python-convert-back-slashes-to-forward-slashes
# https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
# https://stackabuse.com/creating-and-deleting-directories-with-python/
# https://stackoverflow.com/questions/49284015/how-to-check-if-folder-is-empty-with-python
# https://www.guru99.com/python-check-if-file-exists.html
# https://stackoverflow.com/questions/2212643/python-recursive-folder-read
# https://stackoverflow.com/questions/5552555/unicodedecodeerror-invalid-continuation-byte
# https://stackoverflow.com/questions/56453782/utf-8-codec-cant-decode-byte-0xe2-invalid-continuation-byte-error

# [APP NAME]: FILE TRANSFER

from threading import Thread
from time import sleep

from server import FileServer
from client import FileClient

def fileserver():
    # init file server
    fs = FileServer(host="0.0.0.0", port=5001)
    # listen client's files
    fs.bulk_receive_file()

def fileclient():
    # init file client
    fc = FileClient(host="localhost", port=5001)
    # send bulk files to server
    fc.bulk_send_file()

thread_server = Thread(target=fileserver)
thread_server.start()

sleep(5)

thread_server = Thread(target=fileclient)
thread_server.start()

