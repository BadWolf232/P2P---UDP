##  Visão Geral do Projeto

Este é um projeto para a cadeira de Redes de Computadores: Aplicação e transporte em que tem como objetivo estabelecer um sistema de atualização de arquivos **Peer-to-Peer (P2P)** utilizando o **protocolo UDP (User Datagram Protocol)**. 

Cada nó (peer) na rede atua simultaneamente como **servidor** e **cliente**, garantindo que um diretório pré-definido (`tmp_peerX`) seja **sincronizado** com todos os arquivos presentes em cada peer da rede.

## 🛠️ Tecnologias Utilizadas

* **Linguagem de Programação:** Python 3.x
* **Protocolo de Transporte:** UDP
* **Bibliotecas Principais:**
    * `socket`: Para a comunicação UDP (cliente e servidor).
    * `watchdog`: Para o monitoramento de eventos no sistema de arquivos local (adição, modificação, exclusão).
    * `threading`: Para executar o servidor de recebimento em *background*.
    * `json`: Para leitura dos arquivos de configuração dos peers.

---

## ⚙️ Estrutura da Rede e Configuração

[cite_start]A rede é **estática** (os peers são conhecidos) e definida por arquivos de configuração JSON. Esta configuração permitiu adicionar novas peers, adicionando apenas mais uma linha com o endereço e ip das máquinas. Na demonstração é utilizado o padrão mínimo estabelecido pelo trabalho de três peers.

### **Configurações de Exemplo**

| Peer | Porta | Diretório Monitorado | Peers Conectados |
| :--- | :--- | :--- | :--- |
| **Peer 1** | 5000 | `tmp_peer1` | Peer 2 (5001), Peer 3 (5002) |
| **Peer 2** | 5001 | `tmp_peer2` | Peer 1 (5000), Peer 3 (5002) |
| **Peer 3** | 5002 | `tmp_peer3` | Peer 1 (5000), Peer 2 (5001) |

### **Detalhes dos Arquivos**

| Arquivo | Descrição |
| :--- | :--- |
| `peer.py` | Classe principal (`Peer`) que integra todas as funcionalidades (servidor, cliente, monitor e organizador). |
| `servidor_UDP.py` | Lógica para **receber** mensagens UDP (comandos FILE, DELETE, RENAME). |
| `cliente_UDP.py` | Lógica para **enviar** mensagens UDP a outros peers. |
| `organizador.py` | Gerencia o diretório local (`tmp_peerX`), com funções de salvar, deletar, renomear e listar arquivos. |
| `monitoramento.py` | Utiliza `watchdog` para detectar mudanças locais (criação, modificação, exclusão, renomeação) e notificar o Peer. |
| `peerX.json` | Arquivos de configuração que definem a porta local e a lista de peers da rede. |

---

## ▶️ Como Executar

### **Pré-requisitos**

É necessário ter o Python 3 e a biblioteca `watchdog` instalada:

```bash
pip install watchdog

**ponto importante**

Caso a biblioteca não consiga ser instalada, é necessário estabelecer um ambiente virtual para que a aplicação possa ser instalada. 

Segue os comandos para a criação do ambiente virtual padrão python: 

```bash 
python3 -m venv venv

**Para Linux/Mac 

```bash 
source venv/bin/activate

**Para Windows
venv\Scripts\activate


Após a ativação do ambiente virtual, basta instalar a biblioteca.  


### **Execução** 

**Primeira máquina**

```bash 
python peer.py peer1.json

**Segunda máquina**

```bash 
python peer.py peer2.json

**Terceira máquina**

```bash 
python peer.py peer3.json
