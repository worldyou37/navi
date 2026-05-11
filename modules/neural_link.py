import subprocess
import shutil
import os
from style.ansi_colors import Colors

class NeuralLink:
    def __init__(self):
        self.interessante = ["author", "creator", "producer", "title", "directory", "path", "user", "location"]
        # Verifica se o exiftool está instalado no sistema (ferramenta padrão na Wired/Kali)
        self.exif_present = shutil.which("exiftool") is not None

    def analisar_arquivo(self, caminho_arquivo):
        """
        Extrai metadados e filtra o que é relevante para a 'Lain'.
        """
        if not os.path.exists(caminho_arquivo):
            return None

        if not self.exif_present:
            return {"erro": "ExifTool não encontrado no Navi. Instale para ler metadados."}

        try:
            # Executa exiftool para pegar metadados em formato chave: valor
            processo = subprocess.Popen(
                ["exiftool", caminho_arquivo],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            saida, _ = processo.communicate()
            
            metadados_brutos = {}
            for linha in saida.splitlines():
                if ":" in linha:
                    chave, valor = linha.split(":", 1)
                    metadados_brutos[chave.strip().lower()] = valor.strip()

            return self._filtrar_relevancia(metadados_brutos, caminho_arquivo)

        except Exception as e:
            return {"erro": str(e)}

    def _filtrar_relevancia(self, dados, path):
        """
        Filtro rigoroso: Só extrai se houver rastro humano ou de infraestrutura.
        """
        vazamentos = {}
        nome_arquivo = os.path.basename(path)

        for chave, valor in dados.items():
            # Filtra por palavras-chave interessantes e ignora valores genéricos/vazios
            if any(ref in chave for ref in self.interessante):
                if len(valor) > 2 and "unknown" not in valor.lower():
                    vazamentos[chave.capitalize()] = valor

        if vazamentos:
            return {
                "status": "relevante",
                "arquivo": nome_arquivo,
                "origem": path,
                "dados": vazamentos
            }
        else:
            return {
                "status": "limpo",
                "arquivo": nome_arquivo,
                "origem": path
            }

    def exibir_resultado(self, resultado):
        """
        Interface visual do Neural Link.
        """
        if not resultado:
            return

        if "erro" in resultado:
            print(f"{Colors.RED}[!] Neural Link Falhou: {resultado['erro']}{Colors.RESET}")
            return

        if resultado["status"] == "relevante":
            print(f"\n{Colors.CYAN}[NEURAL LINK]: Identidade fragmentada encontrada em {Colors.BOLD}{resultado['arquivo']}{Colors.RESET}")
            print(f"{Colors.GRAY} Localização: {resultado['origem']}{Colors.RESET}")
            
            for k, v in resultado["dados"].items():
                print(f"  {Colors.MAGENTA}› {k}:{Colors.RESET} {v}")
            print(f"{Colors.GRAY}─{'─'*40}─{Colors.RESET}")
        else:
            # Caso não haja nada relevante, apenas o log de existência
            print(f"{Colors.GRAY}[NEURAL LINK]: {resultado['arquivo']} analisado (Nenhum rastro detectado).{Colors.RESET}")

# Exemplo de integração rápida
if __name__ == "__main__":
    # Teste stand-alone
    nl = NeuralLink()
    # nl.exibir_resultado(nl.analisar_arquivo("documento_alvo.pdf"))
