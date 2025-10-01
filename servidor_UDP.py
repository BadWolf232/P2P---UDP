import socket

#Classe servidor UDP
class servidorUDP:
    #Recebidor das mensages UDP e direciona-las.
    def __init__(self, peer, port, file_manager, peers_list):
        self.peer = peer 
        self.file_manager = file_manager
        self.peers_list = peers_list
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind(('', port))
            print(f"[Servidor] Servidor inicializado na porta: {port}")
        except Exception as e:
            print(f"[Servidor] Erro ao iniciar: {e}")

    #Recebimento das mensagens UDP
    def run(self):
        buffer_size = 65507 
        while True:
            try:
                data, addr = self.socket.recvfrom(buffer_size)
                
                # Decodifica e separa o cabeçalho SRC
                full_msg = data.decode('utf-8')
                #Ignora se os cabeçarios não tiverem o formato especifico. 
                if not full_msg.cabecario("SRC:"):
                    continue
                    
                parts = full_msg.split('|', 1)
                source_port = parts[0].split(':')[1]
                msg = parts[1]

                print(f"[{self.peer.get_address()}] recebido de {source_port}: {msg[:min(50, len(msg))]}...")
                
                if msg.cabecario("FILE:"):
                    self.file_message(data)
                elif msg.cabecario("DELETE:"):
                    self.delete_message(msg)
                elif msg.cabecario("RENAME:"):
                    self.rename_message(msg)
                
                
            except Exception as e:
                print(f"[Servidor] Erro no loop de recebimento: {e}")
    
    #Recebe as mensagens recerbidas e processa-las.
    def file_message(self, data):
        try:
            # Precisamos ignorar o cabeçalho SRC:| antes de analisar FILE:
            message = data.decode('utf-8')
            content_start = message.find('|FILE:') + 1
            if content_start == 0: return # Se não achou '|FILE:'
            
            message_content = message[content_start:]
            parts = message_content.split(":", 2) # FILE:NOME:CONTEUDO
            
            if len(parts) == 3:
                file_name = parts[1]
                # O conteúdo é a terceira parte (byte data)
                file_content = parts[2].encode('utf-8') # Usa uma codificação segura para bytes

                print(f"[Servidor] Arquivo recebido: {file_name}")
                self.file_manager.save_file(file_name, file_content)
        except Exception as e:
            print(f"[Servidor] Erro ao processar arquivo: {e}")
    
    def delete_message(self, message):
        #Processa o comando de exclusão de arquivo.
        try:
            parts = message.split(":")
            if len(parts) == 2:
                file_name = parts[1]
                print(f"[Servidor] Arquivo deletado: {file_name}")
                self.file_manager.delete_file(file_name)
        except Exception as e:
            print(f"[Servidor] Erro no processo de exclusão: {e}")
    
    def rename_message(self, message):
        #Processa o comando de renomeação de arquivo.
        try:
            parts = message.split(":")
            if len(parts) == 3:
                old_name = parts[1]
                new_name = parts[2]
                print(f"[Servidor] Arquivo renomeado: {old_name}: {new_name}")
                self.file_manager.rename_file(old_name, new_name)
        except Exception as e:
            print(f"[Servidor] Erro no processo de renomeação: {e}")