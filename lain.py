import sys
import os
import time
from style.ansi_colors import Colors
from style import glitch, banners
from modules import (
    pulse, ghost_dns, portal_ftp, synapse_smb, 
    echo_telnet, specter_web, aura_ssl, recursion, 
    osint_leak, cloaking_tor, neural_link, temporal_ghost
)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def opening_sequence():
    clear_screen()
    glitch.ruido_terminal(3)
    time.sleep(0.5)
    
    print(f"\n{Colors.GRAY}PRESENT DAY...{Colors.RESET}")
    time.sleep(1.2)
    print(f"{Colors.BOLD}PRESENT TIME...{Colors.RESET}")
    time.sleep(1.2)
    print(f"{Colors.MAGENTA}{Colors.BLINK}HAHAHAHAHA!{Colors.RESET}\n")
    time.sleep(1.5)
    
    clear_screen()
    print(banners.MAIN_BANNER)
    
    glitch.efeito_digitacao("Navi OS v1.0.3 - Protocolo 'Lain' Ativo", velocidade=0.02, cor=Colors.GRAY)
    glitch.efeito_digitacao("Sincronizando consciência com a Wired...", velocidade=0.05, cor=Colors.CYAN)
    print(f"{Colors.MAGENTA}{'═'*60}{Colors.RESET}")

def portal_de_entrada(alvo, recursivo=True):
    """
    Coordena a infiltração nas camadas da Wired.
    """
    is_sub = os.getenv("LAIN_RECURSION") == "1"
    
    if not is_sub:
        glitch.observacao_lain("inicio")
    else:
        print(f"\n{Colors.MAGENTA}[RECURSÃO]: Analisando fragmento {alvo}...{Colors.RESET}")

    # --- FASE 0: TEMPORAL GHOST (Sonar de Rede) ---
    # Ativado para sentir a distância e a presença de escudos (WAF/CDN)
    temporal_ghost.executar(alvo)
    print(f"{Colors.MAGENTA}{'─'*60}{Colors.RESET}")

    # --- FASE 1: PULSO (Scanner de Portas + Análise de Vulnerabilidades) ---
    scanner = pulse.Pulse(alvo, threads=500)
    portas_abertas = scanner.executar()
    
    if not portas_abertas:
        return

    lista_portas = [p[0] for p in portas_abertas]
    print(f"{Colors.MAGENTA}{'─'*60}{Colors.RESET}")

    # --- FASE 2: GHOST DNS (Mapeamento de Subdomínios) ---
    subs = []
    if not is_sub:
        dns_scanner = ghost_dns.executar(alvo)
        subs = [s[0] for s in dns_scanner] if dns_scanner else []
        print(f"{Colors.MAGENTA}{'─'*60}{Colors.RESET}")

    # --- FASE 3: AURA SSL ---
    if 443 in lista_portas:
        scanner_ssl = aura_ssl.AuraSSL(alvo)
        scanner_ssl.extrair_aura()
        print(f"{Colors.MAGENTA}{'─'*60}{Colors.RESET}")

    # --- FASE 4: MÓDULOS DE SERVIÇO (Infiltração Específica) ---
    if any(p in lista_portas for p in [21, 23, 445]):
        print(f"{Colors.CYAN}Explorando protocolos de comunicação legados...{Colors.RESET}")
        if 21 in lista_portas: portal_ftp.executar(alvo)
        if 23 in lista_portas: echo_telnet.executar(alvo)
        if 445 in lista_portas: synapse_smb.executar(alvo)
        print(f"{Colors.MAGENTA}{'─'*60}{Colors.RESET}")
    
    # --- FASE 5: SPECTER WEB & NEURAL LINK ---
    if 80 in lista_portas or 443 in lista_portas:
        print(f"{Colors.CYAN}Infiltrando-se no Espectro Web...{Colors.RESET}")
        web_fuzzer = specter_web.SpecterWeb(alvo)
        fragmentos_web = web_fuzzer.executar()
        specter_web.reportar_espectro(fragmentos_web)
        
        # Ativação do Neural Link para arquivos sensíveis encontrados
        if fragmentos_web:
            print(f"\n{Colors.CYAN}Ativando Neural Link: Analisando fragmentos de dados...{Colors.RESET}")
            n_link = neural_link.NeuralLink()
            for frag in fragmentos_web:
                extensoes_alvo = ('.pdf', '.doc', '.docx', '.jpg', '.png', '.txt', '.bak', '.env')
                if frag.endswith(extensoes_alvo):
                    res = n_link.analisar_arquivo(frag) 
                    n_link.exibir_resultado(res)

        print(f"{Colors.MAGENTA}{'─'*60}{Colors.RESET}")

    # --- FASE 6: OSINT LEAK ---
    if not is_sub:
        osint_leak.executar(alvo)

    # --- Lógica de Recursão ---
    if recursivo and subs:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}>>> {len(subs)} sub-identidades detectadas.{Colors.RESET}")
        decisao = input(f"{Colors.CYAN}Deseja mergulhar na recursão de fragmentos? (s/n): {Colors.RESET}").lower()
        
        if decisao == 's':
            os.environ["LAIN_RECURSION"] = "1"
            recursion.iniciar_recursao(alvo, subs, portal_de_entrada)
            if os.getenv("LAIN_RECURSION") == "1":
                del os.environ["LAIN_RECURSION"]

def main():
    try:
        opening_sequence()
        
        print(f"{Colors.GRAY}Rastreando origem da conexão atual...{Colors.RESET}")
        cloaking_tor.geolocalizar_ip()
        
        confirmacao = input(f"\n{Colors.CYAN}Ativar protocolo de ocultação (Tor)? (s/n): {Colors.RESET}").lower()
        
        cloak = cloaking_tor.Cloaking()
        if confirmacao == 's':
            for i in range(101):
                glitch.carregar_consciencia(i/100)
                time.sleep(0.02)
            
            if cloak.ativar():
                sys.stdout.write(f"\n{Colors.MAGENTA}Identidade camuflada na Wired.{Colors.RESET}\n")
                cloaking_tor.geolocalizar_ip()
            else:
                sys.stdout.write(f"\n{Colors.RED}[!] Falha ao estabelecer túnel. Modo exposto ativo.{Colors.RESET}\n")
        else:
            print(f"{Colors.RED}[!] Alerta: Seu IP real está visível na Wired.{Colors.RESET}")
        
        banners.separador_psicodelico()

        prompt = f"{Colors.GREEN}wired@navi{Colors.RESET}:{Colors.MAGENTA}~/lain{Colors.RESET}$ "
        alvo = input(f"{prompt}digite o endereço do alvo: ").strip()
        
        if not alvo:
            print(f"{Colors.RED}Nenhum sinal detectado. Encerrando.{Colors.RESET}")
            return

        banners.pulse_animation(duracao=1)
        
        # O fluxo agora inicia pelo portal_de_entrada que inclui o Temporal Ghost
        portal_de_entrada(alvo)
        
        print(f"\n{Colors.MAGENTA}{'═'*60}{Colors.RESET}")
        glitch.observacao_lain("final")
        print(f"{Colors.GRAY}Conexão encerrada. O corpo físico espera por você.{Colors.RESET}\n")

    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Desconexão forçada da Wired. Adeus.{Colors.RESET}")
        sys.exit()

if __name__ == "__main__":
    main()
