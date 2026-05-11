import socket
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from style.ansi_colors import Colors
from style import glitch
from modules import fingerprint

class Pulse:
    def __init__(self, target, threads=500):
        self.target = target
        self.threads = threads
        self.open_ports = []
        self.anomalias = []
        self.handshakes = self._load_handshakes()
        self.ghost_detected = False

    def _load_handshakes(self):
        """Carrega os payloads de handshake da wordlist."""
        handshake_path = 'wordlists/service_handshake.txt'
        payloads = []
        if os.path.exists(handshake_path):
            try:
                with open(handshake_path, 'r') as f:
                    for line in f:
                        if ':' in line and not line.startswith('#'):
                            parts = line.strip().split(':', 1)
                            payload = parts[1]
                            bytes_payload = bytes(payload, "utf-8").decode("unicode_escape").encode("latin-1")
                            payloads.append(bytes_payload)
            except: pass
        return payloads

    def _grab_banner(self, sock, port):
        """Captura o banner. Se o serviço for mudo após handshakes, retorna None."""
        try:
            sock.settimeout(2.0)
            # Tentativa Passiva
            try:
                banner = sock.recv(2048).decode(errors='ignore').strip()
                if banner: return banner.replace('\n', ' ').replace('\r', '')
            except: pass

            # Tentativa Ativa (Handshakes)
            for payload in self.handshakes:
                try:
                    sock.send(payload)
                    response = sock.recv(1024).decode(errors='ignore').strip()
                    if response: return response.replace('\n', ' ').replace('\r', '')
                except: continue
            return None
        except: return None

    def _scan_port(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            is_tor = hasattr(socket, 'socksocket') 
            s.settimeout(2.5 if is_tor else 1.2)
            
            result = s.connect_ex((self.target, port))
            
            if result == 0:
                banner = self._grab_banner(s, port)
                s.close()
                
                service_name = "Unknown"
                analise = None
                is_ghost = False
                
                if banner:
                    analise = fingerprint.analisar_banner(banner)
                    if analise:
                        service_name = analise[0].get('software', 'Unknown') if isinstance(analise, list) else analise.get('software', 'Unknown')
                else:
                    # Se não tem banner e é uma porta alta (>1024), há chance de ser Ghost
                    if port > 1024:
                        is_ghost = True
                    try:
                        service_name = socket.getservbyport(port).upper()
                    except:
                        service_name = "Unknown/Custom"

                # Feedback em tempo real
                if not is_ghost:
                    sys.stdout.write(f"\r\033[K{Colors.MAGENTA}  ›{Colors.RESET} Porta {Colors.BOLD}{port}{Colors.RESET} [{service_name}] {Colors.GREEN}ABERTA{Colors.RESET}\n")
                    sys.stdout.flush()
                
                return (port, service_name, banner, analise, is_ghost)
            s.close()
        except: pass
        return None

    def executar(self, full_scan=True):
        start, end = (1, 65535) if full_scan else (1, 1024)
        total_portas = end - start + 1
        
        print(f"\n{Colors.CYAN}Iniciando Interrogatório de Pulso em {Colors.BOLD}{self.target}{Colors.RESET}...")
        
        ordem_scan = list(range(start, end + 1))
        portas_processadas = 0
        ghost_count = 0

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self._scan_port, p): p for p in ordem_scan}
            
            for future in as_completed(futures):
                portas_processadas += 1
                if portas_processadas % 50 == 0:
                    glitch.exibir_barra_real(portas_processadas, total_portas, "Sincronizando")
                
                res = future.result()
                if res:
                    port, service, banner, analise, is_ghost = res
                    if is_ghost:
                        ghost_count += 1
                        # Se detectarmos mais de 15 portas mudas aleatórias, o host está mentindo
                        if ghost_count > 15 and not self.ghost_detected:
                            print(f"\n{Colors.YELLOW}[!] Anomalia detectada: Port Spoofing / Firewall Labirinto ativo.{Colors.RESET}")
                            self.ghost_detected = True
                    else:
                        self.open_ports.append((port, service))
                        if analise:
                            self.anomalias.append({'porta': port, 'banner_completo': banner, 'info': analise})

        self.open_ports.sort()
        self.reportar_final()
        return self.open_ports

    def _exibir_detalhe_anomalia(self, inf):
        sw = inf.get('software', '???') if isinstance(inf, dict) else str(inf)
        am = inf.get('ameaca', 'Low') if isinstance(inf, dict) else "Low"
        im = inf.get('impacto', 'N/A') if isinstance(inf, dict) else "N/A"
        cor = Colors.RED if am.upper() == "HIGH" else Colors.YELLOW if am.upper() == "MEDIUM" else Colors.GREEN
        print(f"  {Colors.WHITE}Software:{Colors.RESET} {sw}\n  {Colors.WHITE}Ameaça: {Colors.RESET}  {cor}{am}{Colors.RESET}\n  {Colors.WHITE}Impacto: {Colors.RESET}  {Colors.GRAY}{im}{Colors.RESET}")

    def reportar_final(self):
        if not self.open_ports:
            print(f"\n{Colors.RED}[!] Nenhum pulso real detectado.{Colors.RESET}")
            return

        print(f"\n{Colors.GREEN}PULSO CONCLUÍDO - MAPA DE ACESSO REFINADO{Colors.RESET}")
        if self.ghost_detected:
            print(f"{Colors.YELLOW}[AVISO] Portas fantasmas (Spoofing) foram filtradas da lista.{Colors.RESET}")
            
        print(f"{Colors.GRAY}┌{'─'*10}┬{'─'*20}┬{'─'*25}┐{Colors.RESET}")
        print(f"{Colors.GRAY}│{Colors.RESET} {'PORTA':<8} {Colors.GRAY}│{Colors.RESET} {'SERVIÇO':<18} {Colors.GRAY}│{Colors.RESET} {'STATUS':<23} {Colors.GRAY}│{Colors.RESET}")
        print(f"{Colors.GRAY}├{'─'*10}┼{'─'*20}┼{'─'*25}┤{Colors.RESET}")
        for port, service in self.open_ports:
            display_service = (service[:17] + '..') if len(service) > 18 else service
            print(f"{Colors.GRAY}│{Colors.RESET} {port:<8} {Colors.GRAY}│{Colors.RESET} {display_service:<18} {Colors.GRAY}│{Colors.RESET} {Colors.GREEN}{'OPEN':<23}{Colors.RESET} {Colors.GRAY}│{Colors.RESET}")
        print(f"{Colors.GRAY}└{'─'*10}┴{'─'*20}┴{'─'*25}┘{Colors.RESET}")

        if self.anomalias:
            print(f"\n{Colors.RED}{Colors.BOLD}ANÁLISE DE VULNERABILIDADES (WIRED LEAKS){Colors.RESET}")
            for item in self.anomalias:
                print(f"{Colors.MAGENTA}[PORTA {item['porta']}]{Colors.RESET} {Colors.GRAY}{item['banner_completo'][:60]}...{Colors.RESET}")
                info = item['info']
                if isinstance(info, list):
                    for entry in info: self._exibir_detalhe_anomalia(entry)
                else: self._exibir_detalhe_anomalia(info)
                print(f"{Colors.GRAY}{'-'*70}{Colors.RESET}")
