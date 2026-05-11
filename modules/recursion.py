import os
from style.ansi_colors import Colors
from style.glitch import efeito_digitacao, observacao_lain, carregar_consciencia

def iniciar_recursao(principal, subdominios, funcao_scan):
    """
    principal: o domínio alvo original
    subdominios: lista de achados (ex: www.bancocn.com)
    funcao_scan: a função portal_de_entrada do lain.py
    """
    if not subdominios:
        return

    # Lain comenta sobre o mergulho profundo
    observacao_lain("vazio")
    efeito_digitacao(f"Expandindo consciência para {len(subdominios)} novas entidades...", velocidade=0.03)

    for i, sub in enumerate(subdominios):
        # Limpa o nome caso venha com espaços ou protocolos
        sub = sub.strip()
        
        # Evita re-escanear o alvo principal se ele estiver na lista de subs
        if sub == principal:
            continue

        print(f"\n{Colors.MAGENTA}{'═'*60}")
        print(f"{Colors.BOLD}MERGULHO RECURSIVO NO FRAGMENTO: {sub}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'═'*60}\n")
        
        # Executa o scan no subdomínio
        # Passamos recursivo=False para que o subdomínio não peça outra recursão
        # evitando loops infinitos de camadas.
        funcao_scan(sub, recursivo=False)
        
        # Mostra o progresso da árvore de recursão
        carregar_consciencia((i + 1) / len(subdominios))
    
    print(f"\n{Colors.CYAN}A Wired estabilizou. Todos os fragmentos foram processados.{Colors.RESET}")
