import time
import os
import watchdog.events

#Detecta adições, modificações e exclusões locais e notifica o Peer.
class FileChangeHandler(watchdog.events.FileSystemEventHandler):
   
    def __init__(self, peer_instance, file_manager):
        self.peer = peer_instance
        self.file_manager = file_manager
        # Define um tempo de espera para evitar processar eventos temporários ou duplicados
        self.last_event_time = {}

    def on_any_event(self, event):
        # Ignora eventos de diretório
        if event.is_directory:
            return
        
        # Simple throttling: espera 1 segundo entre eventos no mesmo arquivo
        # Isso ainda é importante para evitar loops rápidos
        current_time = time.time()
        if event.src_path in self.last_event_time and current_time - self.last_event_time[event.src_path] < 1:
            return
        self.last_event_time[event.src_path] = current_time
        
        file_name = os.path.basename(event.src_path)
        
        # Eventos principais:
        if event.event_type == 'created' or event.event_type == 'modified':
            print('='*40)
            print(f"\n[Monitor] Mudança detectada: {file_name} foi criado/modificado.")
            print('='*40)

            self.peer.propagate_file(file_name)
            
        elif event.event_type == 'deleted':
            print(f"\n[Monitor] Mudança detectada: {file_name} foi deletado.")
            self.peer.propagate_delete(file_name)
            
        elif event.event_type == 'moved':
            # Trata renomeação/movimentação
            print(f"\n[Monitor] Mudança detectada: {event.src_path} movido para {event.dest_path}.")
            old_name = os.path.basename(event.src_path)
            new_name = os.path.basename(event.dest_path)
            self.peer.propagate_rename(old_name, new_name)
            
        else:
            # Caso contrário, pode ser um evento 'closed' ou outro que pode ser ignorado.
            pass
