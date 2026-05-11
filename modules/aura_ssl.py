import socket
import ssl
from style.ansi_colors import Colors

class AuraSSL:
    def __init__(self, target):
        self.target = target

    def extrair_aura(self):
        """
        Realiza um handshake SSL/TLS para capturar os metadados do certificado.
        Funciona através do Tor se o patch global de socket estiver ativo.
        """
        print(f"\n{Colors.CYAN}Sintonizando frequência SSL/TLS de {Colors.BOLD}{self.target}{Colors.RESET}...")
        
        # Criamos um contexto SSL padrão
        # CERT_NONE é usado para garantir que capturemos os dados mesmo de certificados 
        # auto-assinados ou expirados (comum em servidores de infraestrutura).
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        try:
            # Estabelece a conexão de baixo nível (socket)
            # Se o Tor estiver ativo, o socket.create_connection usará o proxy SOCKS5
            with socket.create_connection((self.target, 443), timeout=5) as sock:
                # Envolve o socket com a camada SSL
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    # Obtém o certificado binário e o decodifica
                    decoded_cert = ssock.getpeercert()
                    
                    # Se o cert vier vazio (comum com CERT_NONE em algumas versões), 
                    # tentamos pegar os dados da conexão peer
                    if not decoded_cert:
                        # Fallback para capturar dados brutos se necessário
                        print(f"{Colors.YELLOW}[!] Handshake realizado, mas os dados do certificado estão ocultos.{Colors.RESET}")
                        return None

                    print(f"{Colors.GREEN}[+] Conexão Criptografada Estabelecida.{Colors.RESET}")
                    
                    # Extração de campos específicos (Subject e Issuer)
                    subject = dict(x[0] for x in decoded_cert.get('subject', []))
                    issuer = dict(x[0] for x in decoded_cert.get('issuer', []))

                    # Exibição formatada com a estética Lain
                    print(f"  {Colors.MAGENTA}› Identidade (Subject):{Colors.RESET} {Colors.WHITE}{subject.get('commonName', 'Desconhecido')}{Colors.RESET}")
                    print(f"  {Colors.MAGENTA}› Organização:{Colors.RESET} {Colors.WHITE}{subject.get('organizationName', 'N/A')}{Colors.RESET}")
                    print(f"  {Colors.MAGENTA}› Emissor (CA):{Colors.RESET} {Colors.WHITE}{issuer.get('commonName', 'N/A')}{Colors.RESET}")
                    print(f"  {Colors.MAGENTA}› Validade (Até):{Colors.RESET} {Colors.WHITE}{decoded_cert.get('notAfter', 'N/A')}{Colors.RESET}")
                    
                    return decoded_cert

        except socket.timeout:
            print(f"{Colors.RED}[!] Tempo de resposta esgotado (Timeout). O servidor pode estar bloqueando scans.{Colors.RESET}")
        except ConnectionRefusedError:
            print(f"{Colors.RED}[!] Conexão recusada na porta 443. SSL não disponível.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Falha ao ler a aura SSL: {str(e)}{Colors.RESET}")
            
        return None
