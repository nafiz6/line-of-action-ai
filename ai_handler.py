
import subprocess

class AI_Handler():
    def __init__(self, size):
        self.p = None
        self.size = size
        self.end = False
        p =subprocess.Popen("javac AI_Handler.java")
        p.communicate()

        self.process = subprocess.Popen("java AI_Handler",stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.write(size)
        print(self.read())
        #self.stdout, self.stderr = self.p.communicate(self.size.encode('utf-8'))
    
    def write(self, msg):
        self.process.stdin.write(msg.encode('utf-8'))
        self.process.stdin.flush()
    
    def read(self):
        msg = self.process.stdout.readline()
        return msg.decode('utf-8')

