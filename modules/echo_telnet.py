import socket
import time
from style.ansi_colors import Colors
from style.glitch import efeito_digitacao, observacao_lain, ruido_terminal

class EchoTelnet:
    def __init__(self, ip):
        self.ip = ip
        self.port = 23

    def capturar_eco(self):
        """
        Tenta estabelecer uma conexão e negociar o protocolo Telnet.
        O Telnet exige resposta a comandos de negociação (IAC - Is Any Command).
        """
        efeito_digitacao(f"Escutando ecos do passado na porta {self.port}...", velocidade=0.03)
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((self.ip, self.port))
            
            # Negociação básica Telnet (responder a DO/DONT/WILL/WONT)
            # Para evitar que o servidor feche a conexão imediatamente.
            time.sleep(0.5)
            data = s.recv(1024)
            
            # Se o servidor enviar comandos IAC (começam com \xff)
            if data.startswith(b'\xff'):
                # Respondemos que não queremos opções especiais (WONT)
                # \xff (IAC) \xfc (WONT) + o comando recebido
                s.send(b'\xff\xfc' + data[2:3])
            
            banner = s.recv(1024).decode(errors='ignore').strip()
            s.close()
            
            if banner:
                print(f"{Colors.GRAY}Voz detectada no vácuo: {Colors.MAGENTA}{banner[:100]}{Colors.RESET}")
                return banner
            else:
                print(f"{Colors.GRAY}O eco retornou vazio.{Colors.RESET}")
                return None
                
        except Exception as e:
            print(f"{Colors.GRAY}A porta 23 não emite sons em {self.ip}.{Colors.RESET}")
            return None

    def analisar_vulnerabilidade(self, banner):
        """Reflexão da Lain sobre a insegurança do protocolo."""
        observacao_telnet = False
        
        # Procura por palavras-chave que indicam sistemas específicos
        keywords = ["linux", "cisco", "switch", "login:", "password:"]
        if any(key in banner.lower() for key in keywords):
            observacao_telnet = True
            
        if observacao_telnet:
            observacao_lain("telnet_alerta")
            ruido_terminal(1)
            print(f"{Colors.RED}[!] TRÁFEGO EXPOSTO: Tudo o que for dito aqui pode ser ouvido por qualquer um na Wired.{Colors.RESET}")
            print(f"{Colors.YELLOW}Recomendação: Busque por credenciais padrão ou sniffing de rede.{Colors.RESET}")

def executar(ip):
    telnet = EchoTelnet(ip)
    banner = telnet.capturar_eco()
    if banner:
        telnet.analisar_vulnerabilidade(banner)
    return banner
