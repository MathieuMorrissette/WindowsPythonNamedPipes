import win32file

bufferSize = 4096

def ConnectPipe(name):
    handle = win32file.CreateFile(
    '\\\\.\\pipe\\' + name,
    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
    0,
    None,
    win32file.OPEN_EXISTING,
    0,
    None)
    return handle

def Read(pipe):
    win32file.SetFilePointer(pipe, 0, win32file.FILE_BEGIN)
    result, data = win32file.ReadFile(pipe, bufferSize, None) 

    buf = data
    while len(data) == bufferSize:            
        result, data = win32file.ReadFile(pipe, bufferSize, None)
        buf += data
    return buf

def Write(pipe, data):
    win32file.WriteFile(pipe, data)

pipe = ConnectPipe("Foo")

data = Read(pipe)
Write(pipe, b"hello from the other side")


print(data)


input("Done")




#reference 
# https://stackoverflow.com/questions/48542644/python-and-windows-named-pipes
# https://stackoverflow.com/questions/29910861/python-read-file-using-win32file-readfile


