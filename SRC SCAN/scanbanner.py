# -*- coding:utf-8 -*-

from socket import *
import threading


def scan(host, port):
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.settimeout(5)
        sock.connect((host, port))
        sock.send(b'Hello\r\n')
        res = sock.recv(1024)

        print(res.decode())
    except Exception as e:
        print(e)
    finally:
        sock.close()


if __name__ == "__main__":
    jobs = []
    main_host = '114.55.65.251'
    ports = [i for i in range(45000,45999)]

    for main_port in ports:
        t = threading.Thread(target=scan, args=(main_host,main_port))
        t.start()
        jobs.append(t)

    for job in jobs:
        job.join()

