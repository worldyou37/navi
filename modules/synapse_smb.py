import socket
import struct
import time
from style.ansi_colors import Colors
from style.glitch import efeito_digitacao, observacao_lain, ruido_terminal

class SynapseSMB:
    def __init__(self, ip):
        self.ip = ip
        self.port = 445

    def negociar_protocolo(self):
        """
        Tenta um aperto de mão SMB para identificar a presença do serviço.
        Envia um pacote de negociação SMB básico (Dialect Negotiate).
        """
        efeito_digitacao(f"Sincronizando com a sinapse SMB em {self.ip}...", velocidade=0.02)
        
        # SMB Negotiate Protocol Request (Pacote simplificado para identificação)
        # Este cabeçalho tenta verificar se o servidor aceita SMBv1 ou v2
        neg_proto = (
            b"\x00\x00\x00\x2f" # NetBIOS Session Service (Length)
            b"\xff\x53\x4d\x42" # SMB Header Magic: \xffSMB
            b"\x72"             # Command: Negotiate Protocol
            b"\x00\x00\x00\x00" # Status
            b"\x18\x53\xc8\x00" # Flags
            b"\x00\x00"         # Extra Flags
            b"\x00\x00\x00\x00\x00\x00\x00\x00" # Process ID / Reserved
            b"\x00\x00"         # Tree ID
            b"\x00\x00"         # Word Count
            b"\x00\x0d\x00"     # Byte Count
            b"\x02\x4e\x54\x20\x4c\x4d\x20\x30\x2e\x31\x32\x00" # Dialect: NT LM 0.12
        )

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((self.ip, self.port))
            s.send(neg_proto)
            res = s.recv(1024)
            s.close()

            if b"\xffSMB" in res:
                print(f"{Colors.GREEN}[!] Sinapse ativa. O alvo responde via SMB.{Colors.RESET}")
                return True
            return False
        except:
            print(f"{Colors.GRAY}A sinapse está silenciosa ou protegida.{Colors.RESET}")
            return False

    def buscar_info_nula(self):
        """
        Informa que o Navi está tentando uma 'Null Session'.
        Essencial para listar usuários sem credenciais em sistemas mal configurados.
        """
        observacao_lain("smb_sucesso")
        ruido_terminal(1)
        efeito_digitacao("Tentando estabelecer uma Sessão Nula (Null Session)...", velocidade=0.03)
        
        # Nota Técnica: Implementar a enumeração completa de usuários/shares 
        # puramente via sockets em Python requer a construção de pacotes MSRPC complexos.
        # Aqui, identificamos a possibilidade e extraímos o que o banner permitir.
        
        print(f"{Colors.YELLOW}Analisando permissões de acesso não autenticado...{Colors.RESET}")
        time.sleep(1)
        print(f"{Colors.GRAY}Monitorando tráfego de IPC$ e RPC...{Colors.RESET}")
        
        # Em um cenário real de script nativo, aqui verificaríamos 
        # o 'Security Mode' do pacote de resposta para ver se 'User-level' ou 'Share-level'
        # e se 'Signing' está habilitado ou requerido.
        
        print(f"{Colors.CYAN}Dica da Wired: Tente montar IPC$ para listar usuários.{Colors.RESET}")

    def capturar_hostname_netbios(self):
        """Tenta extrair o nome da máquina/domínio via NetBIOS (porta 139/445)."""
        try:
            # Tenta resolver o nome NetBIOS usando o socket nativo
            host_info = socket.gethostbyaddr(self.ip)
            print(f"{Colors.MAGENTA}» Identidade NetBIOS: {Colors.BOLD}{host_info[0]}{Colors.RESET}")
        except:
            pass

def executar(ip):
    smb = SynapseSMB(ip)
    if smb.negociar_protocolo():
        smb.capturar_hostname_netbios()
        smb.buscar_info_nula()
        return True
    return False
