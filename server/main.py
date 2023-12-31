import sys
import socket
import logging
import signal
from threading import Thread
from socket_handler import handler
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from ftp_handler import SQLiteAuthorizer

# Config part
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
port = 7979


def signal_handler(signal, frame):
    # Add SIGINT handler for killing the threads
    logging.info("Caught Ctrl+C, shutting down...")
    fileserver.close_all()
    server.close()
    sys.exit()


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))  # Bind to all address
    server.listen()

    host = socket.gethostbyname(socket.gethostname())
    logging.info("Listen at %s:%d", host, port)
    logging.info("Server started...")

    signal.signal(signal.SIGINT, signal_handler)

    FTPhandler = FTPHandler
    FTPhandler.authorizer = SQLiteAuthorizer()
    fileserver = FTPServer(("", port + 1), FTPhandler)  # win 下 FTPD 监听有问题 请改成本机地址
    ftp_thread = Thread(target=fileserver.serve_forever, daemon=True)
    ftp_thread.start()

    while True:
        conn, addr = server.accept()
        socket_thread = Thread(target=handler, daemon=True,
                               args=(conn, addr))
        socket_thread.start()
