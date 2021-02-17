from os import name
from os.path import expanduser, normpath, basename

def fix_path(path):
    """fix path """
    path = normpath(expanduser(path))
    if path.startswith("\\"): return "C:" + path
    return path

def convert_path(path):
    path = fix_path(path)
    if not name == 'nt':
        path = path.replace('\\','/') 
    return path

if __name__ == "__main__":
    # path = r"C:\Users\vmanhani\Desktop\file-transfer\input\abc.txt"
    # path = "C:\\Users\\vmanhani\\Desktop\\file-transfer\\input\\abc.txt"
    # path = "/mnt/c/Users/vmanhani/Desktop/file-transfer/abc.txt"
    # path = "~/blob_files/myfile.blob"
    path = "hello\\world.txt"
    path = convert_path(path)
    print(path)
    print(basename(path))

