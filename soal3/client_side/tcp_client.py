import sys
import socket
import json
import logging
import xmltodict
import ssl
import os
import threading
import time
import datetime

server_address = ('172.16.16.101', 12000)
#server_address = ('172.16.16.102', 12000)

def make_socket(destination_address='localhost',port=12000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        return sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def make_secure_socket(destination_address='localhost',port=10000):
    try:
        #get it from https://curl.se/docs/caextract.html

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode=ssl.CERT_OPTIONAL
        context.load_verify_locations(os.getcwd() + '/domain.crt')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        secure_socket = context.wrap_socket(sock,server_hostname=destination_address)
        logging.warning(secure_socket.getpeercert())
        return secure_socket
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

#mengubah data dari JSON ke objek
def deserialize(s):
    logging.warning(f"deserialize {s.strip()}")
    return json.loads(s)
    
def send_command(command_str,is_secure=True):
    alamat_server = server_address[0]
    port_server = server_address[1]
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# gunakan fungsi diatas
    if is_secure == True:
        sock = make_secure_socket(alamat_server,port_server)
    else:
        sock = make_socket(alamat_server,port_server)

    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = deserialize(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as ee:
        logging.warning(f"error during data receiving {str(ee)}")
        return False


def getdatapemain(nomor=0,is_secure=True):
    cmd=f"getdatapemain {nomor}\r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    return hasil

def lihatversi(is_secure=True):
    cmd=f"versi \r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    return hasil
    
#mengikuti contoh pada progjar 3
#untuk menghitung latency 
def ambil_data(numbersofrequests):
    texec = dict()

    catat_awal = datetime.datetime.now()
    for k in range(numbersofrequests):
	#bagian ini merupakan bagian yang mengistruksikan eksekusi pengambilan data pemain secara multithread
        texec[k] = threading.Thread(target=getdatapemain, args=(k+1,))
        texec[k].start()

    #setelah menyelesaikan tugasnya, dikembalikan ke main thread dengan join    
    for k in range(numbersofrequests):
        texec[k].join()
    
    catat_akhir = datetime.datetime.now()
    selesai = catat_akhir - catat_awal
    print(f"Latency: {selesai}")

if __name__=='__main__':
    ambil_data(1)
