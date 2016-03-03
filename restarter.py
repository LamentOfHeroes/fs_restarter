
import telnetlib
import socket
import threading
import socketserver

listening_port = 3000
password = "test"

class Restarter(socketserver.BaseRequestHandler):
    def tell(self, message):
        self.request.sendall(bytes(message, 'ascii'))
    
    def get(self):
        return str(self.request.recv(1024))
    
    def restart_fs(self):
        os.system("kill -9 `cat ~nuku/fs/game/protomuck.pid` ; ~nuku/fs/game/restart")
    
    def fs_down(self):
        try:
            con = telnetlib.Telnet("localhost", 2000, 5)
        except ConnectionRefusedError:
            return "connection refused\n"
        return False
    
    def attempt_reboot():
        self.tell("Checking to see if the server is up.")
        server_down = fs_down()
        if server_down:
            self.tell("Server is down due to: {}\n".format(server_down))
            self.restart_fs()
        else:
            self.tell("Server is already up and running.\n")
    
    def handle(self):
        self.tell("To restart FS, please enter the password:\n")
        user_password = self.request.recv(1024).decode('ascii').strip()
        print(user_password)
        if user_password == password:
            self.tell("Password correct.\n")
            self.attempt_reboot()
        else:
            self.tell("Password incorrect.\n")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    server = ThreadedTCPServer(("localhost", listening_port), Restarter)
    server.serve_forever()
