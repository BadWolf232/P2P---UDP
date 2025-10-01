import sys
import json
import threading
import watchdog.observers 
from servidor_UDP import servidorUDP 
from cliente_UDP import clienteUDP
from organizador import organizador  
from monitoramento import FileChangeHandler

# Integração dos componentes no peer
class Peer:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.port = self.config["port"]
        self.peers_list = self.config["peers"]
        self.directory = self.config["directory"]
        self.host = '127.0.0.1'
        
        #Componentes cliente, servidor e organizador
        self.organizadores = organizador(self.directory)
        self.client = clienteUDP(self.port)
        self.server = servidorUDP(self, self.port, self.organizadores, self.peers_list)
        
        # Monitoramento
        self.observer = watchdog.observers.Observer()
        self.event_handler = FileChangeHandler(self, self.organizadores)

    def load_config(self, filename):
        with open(filename, "r") as f:
            return json.load(f)

    def get_address(self):
        return f"{self.host}:{self.port}"
        
    # Métodos de propagação (Envia mudanças locais para a rede)
    def propagate_file(self, file_name):
        #Prepara e envia um arquivo para todos os outros peers.
        content = self.organizadores.get_file_content(file_name)
        if content:
            # Codifica o conteúdo para ser seguro na string UDP
            encoded_content = content.decode('latin-1') 
            msg = f"FILE:{file_name}:{encoded_content}"
            self.client.broadcast_message(msg, self.peers_list)
            print(f"[Peer] Arquivo {file_name} propagado para a rede.")

    def propagate_delete(self, file_name):
        #Envia um comando de exclusão para todos os outros peers.
        msg = f"DELETE:{file_name}"
        self.client.broadcast_message(msg, self.peers_list)
        print(f"[Peer] Comando DELETE:{file_name} propagado para a rede.")

    def propagate_rename(self, old_name, new_name):
        #Envia um comando de renomeação para todos os outros peers.
        msg = f"RENAME:{old_name}:{new_name}"
        self.client.broadcast_message(msg, self.peers_list)
        print(f"[Peer] Comando RENAME:{old_name} propagado para a rede.")


    def start(self):
        #Inicia o servidor e o monitor de diretório.
        print(f"==========================================")
        print(f"Iniciando PEER na porta {self.port}...")
        print(f"==========================================")

        
        # 1. Inicia o servidor em uma thread separada (Recebimento)
        server_thread = threading.Thread(target=self.server.run, daemon=True)
        server_thread.start()
        
        # 2. Inicia o monitor de diretório em uma thread separada (Envio/Sincronização Local)
        self.observer.schedule(self.event_handler, self.directory, recursive=True)
        self.observer.start()
        print(f"Monitorando diretório: {self.directory}")
        
        # 3. Loop principal para manter o peer ativo e pronto para interação
        try:
            while True:
                print('='*40)
                command = input("\nDigite 'L' para listar ou 'S' para sair: ").strip().lower()
                if command == 'l':
                    print('\n','*'*40)
                    self.organizadores.list_files() 
                    print('\n','*'*40)
                elif command == 's':
                    break
                else:
                    print("Comando inválido. Tente algum das letras correspondentes.")
                
        except KeyboardInterrupt:
            print("\nEncerrando o peer.")
        finally:
            self.observer.stop()
            self.observer.join()
            # server_thread (daemon) será encerrada com o programa
            
        print(f"Peer {self.port} encerrado.")
        
    
# Ponto de entrada para execução direta do peer
if __name__ == "__main__":
    import sys
    
    # Recebe o nome do arquivo de configuração como argumento
    if len(sys.argv) != 2:
        print("Uso: python peer_sync.py <arquivo_de_configuracao.json>")
        print("Exemplo: python peer_sync.py peer1.json")
        sys.exit(1)
        
    config_file = sys.argv[1]
    
    # Cria a instância do Peer e inicia
    peer_node = Peer(config_file)
    peer_node.start()


