import os

pid = os.fork()

if pid == 0:
    print("Child process: PID =", os.getpid(), "PPID =", os.getppid())
else:
    os.wait()
    print("Parent process: PID =", os.getpid(), "Child PID =", pid)