import socket
import ssl
from style.ansi_colors import Colors
from style.glitch import efeito_digitacao, observacao_lain, ruido_terminal

class PhantomHeaders:
    def __init__(self, target, ip):
        self.target = target
        self.ip = ip
        # Headers de segurança essenciais
        self.security_headers = {
            "Strict-Transport-Security": "Protege contra downgrade de protocolo (HSTS).",
            "Content-Security-Policy": "Define quais fontes de conteúdo são confiáveis (anti-XSS).",
            "X-Frame-Options": "Impede que o site seja colocado em um iframe (anti-Clickjacking).",
            "X-Content-Type-Options": "Força o navegador a seguir o MIME type (anti-Sniffing).",
            "Referrer-Policy": "Controla quanta informação de origem é enviada em links.",
            "Permissions-Policy": "Restringe o uso de câmera, microfone e geolocalização."
        }

    def analisar(self, port=443):
        """Analisa a armadura de cabeçalhos do alvo."""
        efeito_digitacao(f"Lendo a aura de segurança de {self.target}...", velocidade=0.02)
        
        request = f"HEAD / HTTP/1.1\r\nHost: {self.target}\r\nConnection: close\r\n\r\n"
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)

            if port == 443:
                context = ssl.create_default_context()
                s = context.wrap_socket(s, server_hostname=self.target)

            s.connect((self.ip, port))
            s.send(request.encode())
            response = s.recv(4096).decode(errors='ignore')
            s.close()

            # Extração de headers (case-insensitive)
            found_headers = {}
            lines = response.split("\r\n")
            for line in lines:
                if ":" in line:
                    key, val = line.split(":", 1)
                    found_headers[key.strip().lower()] = val.strip()

            self.exibir_relatorio(found_headers)

        except Exception:
            print(f"{Colors.GRAY}Não foi possível ler os reflexos de segurança na porta {port}.{Colors.RESET}")

    def exibir_relatorio(self, found_headers):
        """Exibe o que está presente e o que está ausente na consciência do servidor."""
        print(f"\n{Colors.MAGENTA}--- [ RELATÓRIO DE PHANTOM HEADERS ] ---{Colors.RESET}")
        
        ausentes = []
        
        for header, desc in self.security_headers.items():
            if header.lower() in found_headers:
                print(f"{Colors.GREEN}[V] {header}:{Colors.RESET} {Colors.GRAY}Ativo.{Colors.RESET}")
            else:
                print(f"{Colors.RED}[X] {header}{Colors.RESET}")
                ausentes.append((header, desc))

        if ausentes:
            ruido_terminal(1)
            observacao_lain("pergunta")
            print(f"\n{Colors.YELLOW}Vulnerabilidades na estrutura detectadas:{Colors.RESET}")
            for h, d in ausentes:
                print(f"  {Colors.WHITE}» {h}:{Colors.RESET} {Colors.GRAY}{d}{Colors.RESET}")
        else:
            print(f"\n{Colors.CYAN}A consciência deste servidor parece estar blindada.{Colors.RESET}")

def executar(target, ip, active_ports):
    phantom = PhantomHeaders(target, ip)
    # Tenta HTTPS primeiro, depois HTTP
    if 443 in active_ports:
        phantom.analisar(443)
    elif 80 in active_ports:
        phantom.analisar(80)
