import json
import os
import re
from style.ansi_colors import Colors

def carregar_base_conhecimento():
    """Carrega o banco de dados Omega da Wired."""
    # Sobe um nível para encontrar a pasta /data fora de /modules
    caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge_base.json'))
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        # Silencioso no scan, mas útil para debug se necessário
        return None

def analisar_banner(banner):
    """
    Analisa um banner capturado e cruza com a base de dados de vulnerabilidades.
    Retorna uma lista de anomalias detectadas.
    """
    if not banner:
        return None

    db = carregar_base_conhecimento()
    if not db:
        return None

    banner_clean = banner.strip().lower()
    correspondencias = []

    # Percorre todas as categorias de segurança no JSON
    for categoria, softwares in db.get("security_categories", {}).items():
        for sw in softwares:
            nome_sw = sw['name'].lower()
            
            # 1. Verifica se o nome do software (ex: Nginx) está no banner
            if nome_sw in banner_clean:
                # 2. Verifica se alguma versão vulnerável listada bate com o banner
                for versao in sw.get("versions", []):
                    # Se for "All" ou a versão específica for encontrada na string do banner
                    if versao.lower() in banner_clean or (versao == "All"):
                        # Mapeamento para as chaves que o pulse.py utiliza no relatório final
                        resultado = {
                            "software": f"{sw['name']} {versao if versao != 'All' else ''}".strip(),
                            "ameaca": sw['risk'],  # Ex: "High", "Critical"
                            "impacto": sw['desc'], # Descrição da falha
                            "cves": sw.get("cve", [])
                        }
                        correspondencias.append(resultado)
    
    # Se identificamos o software mas nenhuma versão específica bateu,
    # retornamos um aviso genérico de risco baixo para manter o rastro.
    if not correspondencias:
        for categoria, softwares in db.get("security_categories", {}).items():
            for sw in softwares:
                if sw['name'].lower() in banner_clean:
                    return [{
                        "software": sw['name'],
                        "ameaca": "Low",
                        "impacto": "Software identificado, mas versão não consta no Omega DB.",
                        "cves": []
                    }]

    return correspondencias

def reportar_anomalia(correspondencias):
    """Exibe os resultados da análise com a estética do script (usado em debug/standalone)."""
    if not correspondencias:
        return

    for match in correspondencias:
        # Define a cor baseada no risco contido no match
        risco = match.get('ameaca', 'Low')
        cor_risco = Colors.RED if risco in ['Critical', 'High'] else Colors.YELLOW
        
        print(f"\n{Colors.MAGENTA}[ANOMALIA DETECTADA]{Colors.RESET}")
        print(f"{Colors.WHITE}Software: {Colors.BOLD}{match['software']}{Colors.RESET}")
        print(f"{Colors.WHITE}Ameaça: {cor_risco}{risco}{Colors.RESET}")
        print(f"{Colors.WHITE}Impacto: {match['impacto']}{Colors.RESET}")
        
        cves = match.get('cves', [])
        if cves:
            print(f"{Colors.CYAN}Exploits conhecidos: {', '.join(cves)}{Colors.RESET}")
        print(f"{Colors.GRAY}------------------------------------------------------------{Colors.RESET}")
