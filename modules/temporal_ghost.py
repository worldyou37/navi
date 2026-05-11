import time
import socket
import struct
import statistics
from style.ansi_colors import Colors

class TemporalGhost:
    def __init__(self, target):
        self.target = target
        self.latencies = []
        self.ttl = None

    def _medir_eco(self):
        """Mede a latência e tenta capturar o TTL via conexão TCP."""
        try:
            # Criamos um socket TCP para medir o tempo de resposta
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            
            inicio = time.perf_counter()
            # Conecta na porta 80 ou 443 para medir o round-trip
            result = s.connect_ex((self.target, 443 if 443 else 80))
            fim = time.perf_counter()
            
            # Captura o TTL do pacote de resposta (nível de IP)
            # Nota: Em alguns SOs, o acesso ao TTL do socket exige permissões específicas
            try:
                self.ttl = s.getsockopt(socket.IPPROTO_IP, socket.IP_TTL)
            except:
                self.ttl = 64 # Fallback padrão Linux

            s.close()
            
            if result == 0:
                return (fim - inicio) * 1000 # Convert para ms
        except:
            return None
        return None

    def analisar(self, amostras=5):
        """Realiza múltiplas medições para calcular estabilidade e distância."""
        print(f"{Colors.CYAN}Sincronizando eco temporal com a Wired...{Colors.RESET}")
        
        for _ in range(amostras):
            lat = self._medir_eco()
            if lat:
                self.latencies.append(lat)
            time.sleep(0.1)

        if not self.latencies:
            return {"status": "erro", "msg": "Alvo não responde aos pulsos temporais."}

        avg_lat = sum(self.latencies) / len(self.latencies)
        jitter = statistics.stdev(self.latencies) if len(self.latencies) > 1 else 0
        
        # Dedução de distância (Hops)
        # TTLs comuns de saída: 64 (Linux), 128 (Windows), 255 (Cisco)
        if self.ttl <= 64: base = 64
        elif self.ttl <= 128: base = 128
        else: base = 255
        hops = base - self.ttl

        return {
            "status": "sucesso",
            "avg": avg_lat,
            "jitter": jitter,
            "hops": hops,
            "ttl": self.ttl
        }

    def exibir_relatorio(self, dados):
        if dados["status"] == "erro":
            print(f"  {Colors.RED}[!] {dados['msg']}{Colors.RESET}")
            return

        # Lógica de detecção de Escudo (WAF/CDN)
        # Se o jitter for muito alto ou a latência suspeitosamente baixa/estável demais
        is_ghost = "Detectado" if dados["jitter"] > (dados["avg"] * 0.5) or dados["avg"] < 15 else "Negativo"
        cor_ghost = Colors.RED if is_ghost == "Detectado" else Colors.GREEN

        print(f"\n{Colors.MAGENTA}[TEMPORAL GHOST]{Colors.RESET}")
        print(f"  {Colors.WHITE}Latência Média:  {Colors.RESET}{dados['avg']:.2f}ms")
        print(f"  {Colors.WHITE}Instabilidade:   {Colors.RESET}{dados['jitter']:.2f}ms (Jitter)")
        print(f"  {Colors.WHITE}Distância Wired: {Colors.RESET}{dados['hops']} saltos (Hops)")
        print(f"  {Colors.WHITE}Escudo Ativo:    {cor_ghost}{is_ghost}{Colors.RESET}")
        
        if is_ghost == "Detectado":
            print(f"  {Colors.GRAY}↳ Aviso: Alvo projetando imagem via Proxy/CDN.{Colors.RESET}")
        print(f"{Colors.GRAY}─{'─'*40}─{Colors.RESET}")

def executar(alvo):
    ghost = TemporalGhost(alvo)
    resultado = ghost.analisar()
    ghost.exibir_relatorio(resultado)
