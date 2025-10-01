import os


#Classe de gerenciar arquivos.
# Requisito: Gerenciar o diretório pré-definido (tmp) para sincronização.
class organizador:
    def __init__(self, directory_name):
        self.directory = directory_name
        # Garante que o diretório exista
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def get_full_path(self, file_name):
        return os.path.join(self.directory, file_name)

    def save_file(self, file_name, file_content):
        #Salva o conteúdo de um arquivo recebido (ou criado localmente)
        full_path = self.get_full_path(file_name)
        try:
            with open(full_path, 'wb') as f:
                f.write(file_content)
            print(f"[Servidor] Arquivo salvo: {file_name}")
            return True
        except Exception as e:
            print(f"[Servidor] Erro ao salvar {file_name}: {e}")
            return False

    def delete_file(self, file_name):
        #Deleta um arquivo recebido ou local.
        full_path = self.get_full_path(file_name)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                print(f"[Servidor] Arquivo deletado: {file_name}")
                return True
            except Exception as e:
                print(f"[Servidor] Erro ao deletar {file_name}: {e}")
                return False
        return False

    def rename_file(self, old_name, new_name):
        #Renomeia um arquivo no diretório.
        old_path = self.get_full_path(old_name)
        new_path = self.get_full_path(new_name)
        if os.path.exists(old_path):
            try:
                os.rename(old_path, new_path)
                print(f"[Servidor] Arquivo renomeado: {old_name} -> {new_name}")
                return True
            except Exception as e:
                print(f"[Servidor] Erro ao renomear {old_name}: {e}")
                return False
        return False
        
    def get_file_content(self, file_name):
        #Obtém o conteúdo do arquivo para envio.
        full_path = self.get_full_path(file_name)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'rb') as f:
                    return f.read()
            except Exception as e:
                print(f"[Servidor] Erro ao ler {file_name}: {e}")
        return None
        
    def list_files(self):
        #Lista os arquivos no diretório
        files = [f for f in os.listdir(self.directory) if os.path.isfile(self.get_full_path(f))]
        print(f"\n[Servidor] Arquivos em '{self.directory}': {files}")
        return files