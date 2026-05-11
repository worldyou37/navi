import socket
import json
import urllib.request
import urllib.parse
from style.ansi_colors import Colors
from style.glitch import efeito_digitacao, observacao_lain, ruido_terminal

class OSINTLeak:
    def __init__(self, domain):
        self.domain = domain
        self.api_key = "4a26b0f103bff671864ca02ba710fc2d"
        self.url = "https://leak-lookup.com/api/search"

    def consultar_vazamentos(self):
        """Consulta a API do Leak-Lookup por e-mails vazados no domínio."""
        efeito_digitacao(f"Sincronizando com a base de dados de identidades perdidas...", velocidade=0.03)
        ruido_terminal(1)

        # Prepara os dados para a requisição POST
        # Tipo 'domain' busca todos os e-mails associados àquele domínio
        params = {
            'key': self.api_key,
            'type': 'domain',
            'query': self.domain
        }
        
        data = urllib.parse.urlencode(params).encode()
        
        try:
            req = urllib.request.Request(self.url, data=data, method='POST')
            req.add_header('User-Agent', 'Navi/Lain-Protocol-1.0.2')
            
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode())

            if res_data.get('error') == 'false':
                self.exibir_resultados(res_data.get('message', {}))
            else:
                print(f"{Colors.GRAY}Nenhum eco de vazamento encontrado para {self.domain}.{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.RED}[!] Erro na conexão com Leak-Lookup: {e}{Colors.RESET}")

    def exibir_resultados(self, leaks):
        """Organiza e exibe as credenciais encontradas na Wired."""
        if not leaks:
            print(f"{Colors.GRAY}O banco de dados retornou um silêncio absoluto.{Colors.RESET}")
            return

        total = len(leaks)
        print(f"\n{Colors.MAGENTA}--- [ IDENTIDADES EXPOSTAS: {total} ] ---{Colors.RESET}")
        observacao_lain("vazio")

        # Exibimos os primeiros resultados para não sobrecarregar o terminal
        count = 0
        for email, sources in leaks.items():
            if count >= 10:
                print(f"{Colors.YELLOW}  ... e mais {total - 10} outros fragmentos.{Colors.RESET}")
                break
            
            print(f"  {Colors.WHITE}» {Colors.BOLD}{email}{Colors.RESET}")
            # Lista os nomes dos bancos de dados onde esse e-mail apareceu
            fontes = ", ".join(sources) if isinstance(sources, list) else str(sources)
            print(f"    {Colors.GRAY}Fontes: {fontes}{Colors.RESET}")
            count += 1

        print(f"\n{Colors.RED}[!] Recomenda-se busca por senhas em bases locais ou ferramentas de dump.{Colors.RESET}")

def executar(domain):
    leak = OSINTLeak(domain)
    leak.consultar_vazamentos()
