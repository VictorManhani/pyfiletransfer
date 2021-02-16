# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
# https://www.csestack.org/python-oserror-winerror-10022-invalid-argument-was-supplied/
# https://stackoverflow.com/questions/53136368/sending-multiple-files-python-using-socket
# https://linuxhint.com/python_socket_file_transfer_send/
# https://stackoverflow.com/questions/1325581/how-do-i-check-if-im-running-on-windows-in-python
# https://stackoverflow.com/questions/13162372/using-absolute-unix-paths-in-windows-with-python
# https://stackoverflow.com/questions/25146960/python-convert-back-slashes-to-forward-slashes
# https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f

# [APP NAME]: FILE TRANSFER

from os import system
from time import sleep

system("py server.py")

sleep(5)

system("py client.py")