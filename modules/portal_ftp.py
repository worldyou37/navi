import socket
import time
from style.ansi_colors import Colors
from style.glitch import efeito_digitacao, observacao_lain, ruido_terminal

class PortalFTP:
    def __init__(self, ip):
        self.ip = ip
        self.port = 21

    def capturar_banner(self):
        """Extrai a versão e tecnologia do serviço FTP."""
        efeito_digitacao(f"Tentando sincronizar com a porta {self.port}...", velocidade=0.02)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((self.ip, self.port))
            
            # O FTP costuma enviar o banner assim que você conecta
            banner = s.recv(1024).decode(errors='ignore').strip()
            s.close()
            
            if banner:
                print(f"{Colors.GRAY}Frequência capturada: {Colors.MAGENTA}{banner}{Colors.RESET}")
                return banner
        except Exception as e:
            print(f"{Colors.GRAY}O portal parece estar fechado ou instável.{Colors.RESET}")
            return None

    def testar_anonymous(self):
        """Tenta infiltrar-se usando credenciais anônimas na Wired."""
        observacao_lain("ftp_aberto")
        ruido_terminal(1)
        print(f"{Colors.CYAN}Iniciando teste de acesso anônimo...{Colors.RESET}")
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((self.ip, self.port))
            s.recv(1024) # Limpa o banner inicial

            # Envia o usuário 'anonymous'
            s.send(b"USER anonymous\r\n")
            res_user = s.recv(1024).decode()
            
            if "331" in res_user: # 331 significa que precisa de senha
                # Envia um e-mail genérico como senha (padrão RFC)
                s.send(b"PASS lain@wired.jp\r\n")
                res_pass = s.recv(1024).decode()
                
                if "230" in res_pass: # 230 significa Login bem-sucedido
                    print(f"{Colors.GREEN}{Colors.BOLD}[!] ACESSO ANÔNIMO PERMITIDO.{Colors.RESET}")
                    
                    # Tenta um comando rápido para ver o SO
                    s.send(b"SYST\r\n")
                    syst_info = s.recv(1024).decode().replace("215 ", "").strip()
                    print(f"{Colors.GREEN}» Sistema Operacional Remoto: {Colors.BOLD}{syst_info}{Colors.RESET}")
                    
                    # Tenta listar o conteúdo básico (PWD)
                    s.send(b"PWD\r\n")
                    pwd_info = s.recv(1024).decode().split('"')[1]
                    print(f"{Colors.GREEN}» Diretório Atual: {Colors.BOLD}{pwd_info}{Colors.RESET}")
                else:
                    print(f"{Colors.GRAY}Login anônimo rejeitado pela Wired.{Colors.RESET}")
            else:
                print(f"{Colors.GRAY}O servidor não reconhece usuários anônimos.{Colors.RESET}")
            
            s.send(b"QUIT\r\n")
            s.close()
        except Exception as e:
            print(f"{Colors.RED}Erro na tentativa de conexão: {str(e)}{Colors.RESET}")

def executar(ip):
    ftp = PortalFTP(ip)
    banner = ftp.capturar_banner()
    if banner:
        ftp.testar_anonymous()
    return banner
