import sys
import time
import random
from style.ansi_colors import Colors

# --- ESPAÇO PARA SUA ARTE ASCII ---
# Você pode usar triplas aspas para artes multilinhas.
MAIN_BANNER = """

 █████                  ███            
░░███                  ░░░             
 ░███         ██████   ████  ████████  
 ░███        ░░░░░███ ░░███ ░░███░░███ 
 ░███         ███████  ░███  ░███ ░███ 
 ░███      █ ███░░███  ░███  ░███ ░███ 
 ███████████░░████████ █████ ████ █████
░░░░░░░░░░░  ░░░░░░░░ ░░░░░ ░░░░ ░░░░░ 


"""
# ----------------------------------

def pulse_animation(duracao=15):
    """
    Animação de escaneamento psicodélico.
    Simula o Navi sintonizando frequências na Wired.
    """
    frames = [
        f"{Colors.MAGENTA}◈{Colors.RESET}---", 
        f"-{Colors.MAGENTA}◈{Colors.RESET}--", 
        f"--{Colors.MAGENTA}◈{Colors.RESET}-", 
        f"---{Colors.MAGENTA}◈{Colors.RESET}"
    ]
    
    mensagens = [
        "Sintonizando frequências...",
        "Perfurando a Camada 04...",
        "Buscando rastros de consciência...",
        "Interceptando pacotes perdidos..."
    ]
    
    msg_atual = random.choice(mensagens)
    
    for i in range(duracao):
        frame = frames[i % len(frames)]
        # A cada 5 frames, muda a mensagem para parecer processamento real
        if i % 5 == 0:
            msg_atual = random.choice(mensagens)
            
        sys.stdout.write(f"\r{Colors.GRAY}[{frame}{Colors.GRAY}] {Colors.CYAN}{msg_atual}{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(0.15)
    
    # Limpa a linha após a animação
    sys.stdout.write("\r" + " " * 60 + "\r")

def separador_psicodelico():
    """Gera uma linha divisória instável."""
    simbolos = ["═", "─", "≈", "≋", "×", "✦"]
    linha = "".join(random.choice(simbolos) for _ in range(50))
    print(f"{Colors.MAGENTA}{linha}{Colors.RESET}")
