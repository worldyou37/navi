import socket
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from style.ansi_colors import Colors
from style import glitch

def _verificar_subdominio(alvo, sub, subdominios_encontrados):
    """Tenta resolver um subdomínio e limpa a linha da barra se encontrar algo."""
    host = f"{sub}.{alvo}"
    try:
        # Aumentamos o timeout global implicitamente via socket se o Tor estiver ativo
        ip_sub = socket.gethostbyname(host)
        
        # Limpa a linha da barra (\r\033[K), imprime o achado e pula linha
        sys.stdout.write(f"\r\033[K  {Colors.GREEN}[+]{Colors.RESET} Sub-identidade: {Colors.WHITE}{host:25}{Colors.RESET} -> {Colors.CYAN}{ip_sub}{Colors.RESET}\n")
        sys.stdout.flush()
        
        subdominios_encontrados.append((host, ip_sub))
        return True
    except (socket.gaierror, socket.timeout):
        return False
    except Exception:
        return False

def executar(alvo):
    """
    Realiza a enumeração de subdomínios com barra de progresso persistente.
    Sincronizado com o Protocolo Navi.
    """
    print(f"\n{Colors.CYAN}Mapeando espectro DNS de {Colors.BOLD}{alvo}{Colors.RESET}...")
    
    subdominios_encontrados = []
    # Caminho atualizado conforme seu dump anterior
    wordlist_path = "wordlists/dns.txt"
    
    if not os.path.exists(wordlist_path):
        print(f"{Colors.RED}[!] Wordlist não encontrada em: {wordlist_path}{Colors.RESET}")
        return []

    try:
        # 1. Resolução do IP Principal
        try:
            ip_alvo = socket.gethostbyname(alvo)
            print(f"  {Colors.MAGENTA}›{Colors.RESET} Identidade Principal: {Colors.WHITE}{ip_alvo}{Colors.RESET}")
        except socket.gaierror:
            print(f"  {Colors.YELLOW}[!] Alvo principal não resolveu IP (possível bloqueio DNS).{Colors.RESET}")

        # 2. Análise de porta 53 (AXFR Check)
        _tentar_axfr(alvo)

        # 3. Preparação da Wordlist
        with open(wordlist_path, 'r') as f:
            subs = [line.strip() for line in f if line.strip()]
        
        total = len(subs)
        processados = 0
        
        print(f"{Colors.GRAY}Infiltrando-se via dicionário DNS...{Colors.RESET}")
        
        # Inicializa a barra na base
        glitch.exibir_barra_real(0, total, "Mapeando DNS")

        # Usamos threads para não demorar uma eternidade no DNS
        # O número de workers é menor que no Pulse para evitar banimentos de DNS
        with ThreadPoolExecutor(max_workers=40) as executor:
            futures = {executor.submit(_verificar_subdominio, alvo, s, subdominios_encontrados): s for s in subs}
            
            for future in as_completed(futures):
                processados += 1
                
                # Atualiza a barra constantemente sem apagar os achados
                if processados % 5 == 0 or processados == total:
                    glitch.exibir_barra_real(processados, total, "Mapeando DNS")

    except Exception as e:
        sys.stdout.write(f"\r\033[K{Colors.RED}[!] Erro na análise DNS: {e}{Colors.RESET}\n")

    return subdominios_encontrados

def _tentar_axfr(dominio):
    """Verifica se o serviço DNS aceita conexões TCP (AXFR estético)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            result = s.connect_ex((dominio, 53))
            if result == 0:
                print(f"  {Colors.YELLOW}[!] Alerta: Porta 53 (TCP) aberta. Possível transferência de zona.{Colors.RESET}")
    except:
        pass

def reportar_dns(subs):
    """Lain manifesta sobre os resultados encontrados."""
    if subs:
        glitch.observacao_lain("dns_revelado")
