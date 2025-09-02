from multiprocessing import current_process
from ctypes import cdll, byref, create_string_buffer

def setProcName(procname):
    """https://stackoverflow.com/questions/51521320/tkinter-python-how-to-give-process-name"""
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(len(procname) + 1)
    buff.value = procname

    libc.prctl(15, byref(buff), 0, 0, 0)


if __name__ == '__main__':
    new_procname = b'##### This is a long proc name #####\x00' # Null terminated
    setProcName(new_procname)

    input()
