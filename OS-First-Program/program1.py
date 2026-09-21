import os

# 1-4: Process creation, PID/PPID, exec, wait
pid = os.fork()

if pid == 0:
    print("Child process: PID =", os.getpid(), "PPID =", os.getppid())
    os.execvp("ls", ["ls", "-l"])   # 4. harmless command
else:
    os.wait()
    print("Parent process: PID =", os.getpid(), "Child PID =", pid)

    # 5. file create, write, read, close
    f = open("test.txt", "w")
    f.write("Hello OS Lab\n")
    f.close()
    f = open("test.txt", "r")
    print("File content:", f.read())
    f.close()

    # 6. device/proc interface
    with open("/dev/zero", "rb") as dz:
        print("Read from /dev/zero:", dz.read(4))

    # 7. error handling
    try:
        open("/no/such/path.txt", "r")
    except FileNotFoundError as e:
        print("Error handled:", e)

    # 8. evidence already printed above via the prints in steps 1-7
    os.remove("test.txt")