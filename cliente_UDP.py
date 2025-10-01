import socket

#classe cliente UDP 
class clienteUDP:
    def __init__(self, my_port):
        self.my_port = my_port

  #Envia uma mensagem para um peer específico.
    def send_message(self, msg, host, port):
        if port == self.my_port:
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            data = f"SRC:{self.my_port}|{msg}".encode('utf-8')
            sock.sendto(data, (host, port))
        except Exception as e:
            print('='*20)
            print(f"[Cliente] Erro ao enviar para {host}:{port}: {e}")
            print('='*20)

        finally:
            sock.close()

    def broadcast_message(self, msg, peers_list):
        for peer_info in peers_list:
            self.send_message(msg, peer_info["host"], peer_info["port"])