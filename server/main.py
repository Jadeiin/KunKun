import sys
import socket
import logging
import signal
from threading import Thread

# Config part
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")
port = 7979


def handler(conn, addr):
    message = conn.recv(1024).decode().rstrip("\r\n")
    logging.debug("%s from %s", message, addr)


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))  # Bind to all address
    server.listen()

    host = socket.gethostbyname(socket.gethostname())
    logging.debug("Listen at %s:%d", host, port)
    logging.info("Server started...")

    def signal_handler(signal, frame):
        # Add SIGINT handler for killing the threads
        logging.info("Caught Ctrl+C, shutting down...")
        server.close()
        sys.exit()

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        conn, addr = server.accept()
        thread = Thread(target=handler, daemon=True, args=(conn, addr))
        thread.start()
