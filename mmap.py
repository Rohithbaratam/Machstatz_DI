#Python’s mmap provides memory-mapped file input and output (I/O). It allows you to take advantage of lower-level operating system functionality to read files as if they were one large string or array. 
#This can provide significant performance improvements in code that requires a lot of file I/O.



from multiprocessing import Process
from multiprocessing import shared_memory

def modify(buf_name):
    shm = shared_memory.SharedMemory(buf_name)
    shm.buf[0:50] = b"b" * 50
    shm.close()

if __name__ == "__main__":
    shm = shared_memory.SharedMemory(create=True, size=100)

    try:
        shm.buf[0:100] = b"a" * 100
        proc = Process(target=modify, args=(shm.name,))
        proc.start()
        proc.join()
        print(bytes(shm.buf[:100]))
    finally:
        shm.close()
        shm.unlink()
        
  
 

'''Memory mapping is an alternative approach to file I/O that’s available to Python programs through the mmap module. 
Memory mapping uses lower-level operating system APIs to store file contents directly in physical memory. 
This approach often results in improved I/O performance because it avoids many costly system calls and reduces expensive data buffer transfers.
'''
