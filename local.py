from os.path import abspath, join, dirname

client_host = "localhost"

server_host = "0.0.0.0"

port = 5001

buffer_size = 4096

separator = "<SEPARATOR>"

app_path = dirname(abspath(__file__))

client_path = join(app_path, "input")

server_path = join(app_path, "output")