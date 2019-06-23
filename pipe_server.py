import win32pipe, win32file

bufferSize = 4096

def CreateNamedPipe(name):
    pipe = win32pipe.CreateNamedPipe(
    '\\\\.\\pipe\\' + name,
    win32pipe.PIPE_ACCESS_DUPLEX,
    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
    1, 65536, 65536,
    0,
    None)

    return pipe

def Open(pipe_handle):
    win32pipe.ConnectNamedPipe(pipe_handle, None)

def WritePipe(pipe, data):
    win32file.WriteFile(pipe, data)

def ReadPipe(pipe):
    win32file.SetFilePointer(pipe, 0, win32file.FILE_BEGIN)
    result, data = win32file.ReadFile(pipe, bufferSize, None) 

    buf = data
    while len(data) == bufferSize:            
        result, data = win32file.ReadFile(pipe, bufferSize, None)
        buf += data
    return buf

def Close(pipe):
    win32file.CloseHandle(pipe)

pipe = CreateNamedPipe("Foo")

# this will wait for a client
print("Waiting for client!")
Open(pipe)
print("Received client!")

WritePipe(pipe, b'hello im am the server with lot of data')


data = ReadPipe(pipe)
print(data)

input("Press enter to close pipe")
Close(pipe)

#reference 
# https://stackoverflow.com/questions/48542644/python-and-windows-named-pipes
# https://stackoverflow.com/questions/29910861/python-read-file-using-win32file-readfile