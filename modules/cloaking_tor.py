import socket
import requests
import socks
import time
from style.ansi_colors import Colors
from style.glitch import efeito_digitacao

class Cloaking:
    def __init__(self, proxy_host="127.0.0.1", proxy_port=9050, control_port=9051):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.control_port = control_port
        self.proxy_url = f"socks5h://{proxy_host}:{proxy_port}"
        self.is_active = False

    def verificar_tor(self):
        """Verifica se o serviço Tor está escutando na porta configurada."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3) # Timeout levemente maior para verificar o serviço
        try:
            s.connect((self.proxy_host, self.proxy_port))
            s.close()
            return True
        except (socket.timeout, ConnectionRefusedError):
            return False

    def rotacionar_identidade(self):
        """
        Envia o sinal NEWNYM para trocar o IP.
        Removido do fluxo de recursão automática para priorizar estabilidade.
        Pode ser chamado manualmente se necessário.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.proxy_host, self.control_port))
                s.sendall(b'AUTHENTICATE ""\r\n')
                response = s.recv(1024)
                if b"250" in response:
                    s.sendall(b'SIGNAL NEWNYM\r\n')
                    response = s.recv(1024)
                    if b"250" in response:
                        print(f"{Colors.MAGENTA}[LAIN]: Mudando de pele... Nova identidade sendo forjada na Wired.{Colors.RESET}")
                        time.sleep(5) # O Tor precisa de tempo para estabilizar o novo circuito
                        return True
                else:
                    print(f"{Colors.RED}[!] Erro de autenticação na ControlPort do Tor.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Falha ao rotacionar IP: {e}{Colors.RESET}")
        return False

    def ativar(self):
        """
        Estabelece a camada de anonimato persistente.
        O DNS é resolvido remotamente (rdns=True) para evitar leaks.
        """
        if not self.verificar_tor():
            print(f"{Colors.RED}[!] Erro: Serviço Tor não detectado em {self.proxy_host}:{self.proxy_port}.{Colors.RESET}")
            print(f"{Colors.GRAY}Certifique-se de que o Tor está rodando: 'sudo service tor start'{Colors.RESET}")
            return False

        try:
            # Aumenta o timeout padrão do socket global para lidar com a latência do Tor
            socket.setdefaulttimeout(15)

            # Aplica o Monkey Patch Global para Sockets
            # Isso garante que ghost_dns.py e outros módulos usem o Tor automaticamente
            socks.set_default_proxy(socks.SOCKS5, self.proxy_host, self.proxy_port, rdns=True)
            socket.socket = socks.socksocket
            
            # Configuração para a biblioteca requests (usada em geolocalização e headers)
            proxies = {
                'http': self.proxy_url,
                'https': self.proxy_url
            }
            
            efeito_digitacao(f"Sincronizando com a rede Tor... Estabelecendo túnel na Wired.", cor=Colors.GREEN)
            
            # Captura do IP de saída para confirmar a ativação
            # Usamos uma URL que retorna apenas o IP para ser rápido
            tentativas = 0
            nova_identidade = None
            while tentativas < 3:
                try:
                    nova_identidade = requests.get(
                        'https://api.ipify.org', 
                        proxies=proxies, 
                        timeout=15
                    ).text.strip()
                    break
                except:
                    tentativas += 1
                    time.sleep(2)

            if nova_identidade:
                self.is_active = True
                print(f"{Colors.CYAN}Identidade Única Ativa: {Colors.BOLD}{nova_identidade}{Colors.RESET}")
                return True
            else:
                raise Exception("Não foi possível validar o IP de saída.")
            
        except Exception as e:
            print(f"{Colors.RED}[!] Falha crítica no roteamento: {e}{Colors.RESET}")
            # Tenta restaurar o socket original em caso de falha catastrófica
            import importlib
            importlib.reload(socket)
            return False

def geolocalizar_ip():
    """
    Obtém a localização em tempo real através do túnel estabelecido.
    """
    proxies = {
        'http': "socks5h://127.0.0.1:9050",
        'https': "socks5h://127.0.0.1:9050"
    }

    try:
        url = "http://ip-api.com/json/"
        response = requests.get(url, proxies=proxies, timeout=15)
        data = response.json()
        
        if data.get('status') == 'success':
            print(f"{Colors.GRAY}Localização na Wired: {Colors.WHITE}{data.get('city')}, {data.get('country')}{Colors.RESET}")
            print(f"{Colors.GRAY}Provedor de Saída: {Colors.WHITE}{data.get('isp')}{Colors.RESET}")
            return data
        else:
            print(f"{Colors.YELLOW}[!] Detalhes de localização indisponíveis no momento.{Colors.RESET}")
    except Exception:
        print(f"{Colors.RED}[!] Erro ao rastrear coordenadas na Wired (Timeout).{Colors.RESET}")
    return None
