import sys
import time
import random
from style.ansi_colors import Colors

def efeito_digitacao(texto, velocidade=0.04, cor=Colors.CYAN):
    """Simula a digitação de um terminal Navi com flutuações de sinal."""
    for char in texto:
        if random.random() < 0.03:
            sys.stdout.write(Colors.MAGENTA + random.choice(["@", "#", "§", "Ø"]) + Colors.RESET)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b") 

        sys.stdout.write(cor + char + Colors.RESET)
        sys.stdout.flush()
        time.sleep(velocidade)
    print()

def texto_instavel(texto):
    """Retorna uma versão visualmente corrompida do texto."""
    glitches = ["!", "@", "#", "$", "%", "*", "Ø", "X", "⚡", "†"]
    chars = list(texto)
    for _ in range(random.randint(1, 2)):
        pos = random.randint(0, len(chars)-1)
        if chars[pos] != " ":
            chars[pos] = random.choice(glitches)
    return "".join(chars)

def ruido_terminal(linhas=1):
    """Gera uma linha de ruído estático, como interferência na Wired."""
    for _ in range(linhas):
        estatico = "".join(random.choice([" ", "░", "▒", "▓", "█", "║", "•"]) for _ in range(40))
        print(f"{Colors.GRAY}{estatico}{Colors.RESET}")
        time.sleep(0.05)

def observacao_lain(contexto):
    """Lain manifesta pensamentos sobre o estado da rede e do usuário."""
    frases = {
        "inicio": "Não importa onde você esteja, todos estão sempre conectados.",
        "alvo_encontrado": "Encontrei uma presença física. Mas... ela realmente existe?",
        "ftp_aberto": "Uma porta deixada aberta. As pessoas são tão descuidadas com as suas memórias.",
        "smb_sucesso": "Eu vejo as camadas da consciência coletiva deles agora.",
        "telnet_alerta": "Um protocolo antigo... ecos de um passado que se recusa a morrer.",
        "dns_revelado": "O nome deles é apenas um rótulo na Wired. Eu sei quem eles são.",
        "erro": "A Wired está se distorcendo. A culpa é sua?",
        "final": "Você não precisa de um corpo aqui. Você entende agora?",
        "vazio": "Se você não for lembrado, você nunca existiu."
    }
    
    msg = frases.get(contexto, "...")
    print(f"\n{Colors.MAGENTA}[LAIN]: {Colors.BOLD}{msg}{Colors.RESET}\n")
    time.sleep(1.2)

def alerta_psicodelico(msg):
    """Exibe um alerta que parece piscar entre a realidade e o código."""
    for _ in range(3):
        sys.stdout.write(f"\r{Colors.RED}{Colors.BOLD}!! {msg.upper()} !!{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.write(f"\r{' ' * (len(msg) + 10)}")
        sys.stdout.flush()
        time.sleep(0.1)
    print(f"\r{Colors.YELLOW}{msg}{Colors.RESET}")

def carregar_consciencia(progresso):
    """Barra de carregamento simples para transições de menu."""
    largura = 20
    preenchido = int(largura * progresso)
    barra = "█" * preenchido + "░" * (largura - preenchido)
    sys.stdout.write(f"\r{Colors.GRAY}Sincronizando PSI: [{Colors.MAGENTA}{barra}{Colors.GRAY}] {int(progresso*100)}%{Colors.RESET}")
    sys.stdout.flush()

def exibir_barra_real(atual, total, tarefa, cor_barra=Colors.CYAN):
    """
    Exibe o progresso real de forma persistente.
    Usa \r para retornar ao início e \033[K para limpar apenas a linha da barra.
    """
    largura = 30
    percentagem = int((atual / total) * 100)
    preenchido_tamanho = int(largura * atual / total)
    
    # Efeito de oscilação de cor (glitch visual)
    cor_dinamica = cor_barra if atual % 4 != 0 else Colors.MAGENTA
    
    barra = "█" * preenchido_tamanho + "░" * (largura - preenchido_tamanho)
    
    # \r garante que a barra sobrescreva a si mesma na linha atual.
    # \033[K limpa qualquer caractere residual que tenha sobrado na linha.
    sys.stdout.write(f"\r  {Colors.GRAY}{tarefa}: [{cor_dinamica}{barra}{Colors.GRAY}] {percentagem}% \033[K")
    sys.stdout.flush()
    
    if atual >= total:
        # Finaliza a linha para o relatório final não sobrescrever a barra concluída
        sys.stdout.write(f" {Colors.GREEN}CONCLUÍDO{Colors.RESET}\n")
        sys.stdout.flush()
