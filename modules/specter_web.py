import requests
import os
from style.ansi_colors import Colors
from concurrent.futures import ThreadPoolExecutor

class SpecterWeb:
    def __init__(self, target, threads=15):
        # Garante que o target tenha o protocolo correto
        if not target.startswith(('http://', 'https://')):
            self.target = f"http://{target}"
        else:
            self.target = target
            
        self.threads = threads
        self.bypass_file = "wordlists/bypass_payloads.txt"
        
        # Wordlist integrada com ficheiros e diretórios críticos
        self.wordlist = [
            'robots.txt', '.git/config', '.env', 'phpinfo.php', 
            'admin/', 'backup/', 'config.php', '.htaccess', 
            'wp-admin/', 'api/v1', 'docker-compose.yml', 
            '.ssh/id_rsa', 'server-status', 'dashboard/',
            'storage/', 'logs/', 'sql.sql', 'db.php'
        ]
        
        # Carrega a matriz de bypass da wordlist criada
        self.payloads = self._carregar_payloads()

    def _carregar_payloads(self):
        """Lê os payloads do arquivo bypass_payloads.txt e organiza por categoria."""
        p = {'verbs': [], 'headers': [], 'paths': []}
        if not os.path.exists(self.bypass_file):
            return p
        
        current_cat = None
        try:
            with open(self.bypass_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'): continue
                    if "[VERBS]" in line: current_cat = 'verbs'
                    elif "[HEADERS]" in line: current_cat = 'headers'
                    elif "[PATHS]" in line: current_cat = 'paths'
                    elif current_cat:
                        p[current_cat].append(line)
        except Exception:
            pass
        return p

    def _tentar_bypass(self, path):
        """Tenta forçar a entrada em fragmentos restritos usando a matriz de bypass."""
        url_base = f"{self.target.rstrip('/')}/{path}"
        
        # 1. Testar Verbos Alternativos (POST, HEAD, etc)
        for verb in self.payloads['verbs']:
            try:
                res = requests.request(verb, url_base, timeout=3, allow_redirects=False)
                if res.status_code == 200:
                    return f"Bypass: Verbo [{verb}]"
            except: pass

        # 2. Testar Cabeçalhos (X-Forwarded-For, X-Original-URL, etc)
        for header_line in self.payloads['headers']:
            try:
                h_name, h_val = header_line.split(': ', 1)
                # Injeta o path real se o payload for '/'
                final_val = f"/{path}" if h_val == '/' else h_val
                res = requests.get(url_base, headers={h_name: final_val}, timeout=3)
                if res.status_code == 200:
                    return f"Bypass: Header [{h_name}]"
            except: pass

        # 3. Testar Ofuscação de Caminho (/%2e/, /.;/, etc)
        for p_mod in self.payloads['paths']:
            url_alt = f"{self.target.rstrip('/')}{p_mod}{path}"
            try:
                res = requests.get(url_alt, timeout=3)
                if res.status_code == 200:
                    return f"Bypass: Path Mod [{p_mod}]"
            except: pass

        return None

    def _check_path(self, path):
        """Analisa o caminho e inicia incursão se encontrar um bloqueio 403."""
        url = f"{self.target.rstrip('/')}/{path}"
        try:
            response = requests.get(url, timeout=3, allow_redirects=False, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Navi/1.0.2'
            })
            
            status = response.status_code
            
            if status == 200:
                print(f"  {Colors.GREEN}[200]{Colors.RESET} Fragmento encontrado: {Colors.WHITE}/{path}{Colors.RESET}")
                return (path, "Aberto")
            
            elif status == 403:
                print(f"  {Colors.YELLOW}[403]{Colors.RESET} Restrito: {Colors.GRAY}/{path}{Colors.RESET} -> {Colors.MAGENTA}Iniciando Incursão...{Colors.RESET}")
                # Inicia o motor de bypass para este arquivo específico
                resultado_bypass = self._tentar_bypass(path)
                if resultado_bypass:
                    print(f"  {Colors.GREEN}{Colors.BLINK}[!!!]{Colors.RESET} {Colors.GREEN}SUCESSO: {resultado_bypass} em /{path}{Colors.RESET}")
                    return (path, resultado_bypass)
                else:
                    return (path, "Restrito (Bloqueado)")
                
        except requests.exceptions.RequestException:
            pass
        return None

    def executar(self):
        """Inicia a varredura multithread com lógica de bypass."""
        print(f"\n{Colors.CYAN}Iniciando varredura espectral (Web Incursion) em {Colors.BOLD}{self.target}{Colors.RESET}...")
        print(f"{Colors.GRAY}Processando {len(self.wordlist)} caminhos com {self.threads} threads...{Colors.RESET}\n")
        
        encontrados = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            resultados = executor.map(self._check_path, self.wordlist)
            for res in resultados:
                if res:
                    encontrados.append(res)
        
        if not encontrados:
            print(f"{Colors.GRAY}Nenhum rastro digital detectado nesta camada.{Colors.RESET}")
        
        return encontrados

def reportar_espectro(fragmentos):
    """Exibe o resumo das vulnerabilidades e bypasses encontrados."""
    if fragmentos:
        print(f"\n{Colors.MAGENTA}Sumário da Presença Web:{Colors.RESET}")
        for path, tipo in fragmentos:
            # Destaca se houve sucesso no bypass
            cor = Colors.GREEN if "Bypass" in tipo else Colors.WHITE
            print(f" {cor}› /{path:15} | Status: {tipo}{Colors.RESET}")
