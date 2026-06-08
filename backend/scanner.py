import socket
import ipaddress
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor


def ping_host(ip):
    """
    Envia um pedido de ping para verificar se o host está ativo.
    """

    # Identifica o sistema operativo para adaptar o comando ping.
    system = platform.system().lower()

    # Comando ping para Windows.
    if system == "windows":
        command = ["ping", "-n", "1", "-w", "500", str(ip)]

    # Comando ping para Linux/macOS.
    else:
        command = ["ping", "-c", "1", "-W", "1", str(ip)]

    # Executa o ping sem mostrar o output no terminal.
    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Código 0 significa que o host respondeu ao ping.
    return result.returncode == 0


def scan_network(network):
    """
    Percorre todos os endereços da rede e identifica os hosts ativos.
    """

    active_hosts = []

    # Converte a rede recebida numa estrutura manipulável pelo Python.
    ip_net = ipaddress.ip_network(network, strict=False)

    print(f"\n[+] Rede alvo: {network}")

    # Usa threads para testar vários hosts em simultâneo.
    with ThreadPoolExecutor(max_workers=50) as executor:

        # Executa a função ping_host para todos os hosts da rede.
        results = executor.map(ping_host, ip_net.hosts())

        # Associa cada IP ao respetivo resultado do ping.
        for ip, is_active in zip(ip_net.hosts(), results):

            # Se o host respondeu ao ping, é considerado ativo.
            if is_active:
                print(f"[ATIVO] {ip}")
                active_hosts.append(str(ip))

    return active_hosts


def get_banner(ip, port):
    """
    Tenta obter o banner do serviço para identificar aplicações e versões.
    """

    try:
        # Cria um socket TCP.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define o tempo máximo de espera pela resposta do serviço.
        sock.settimeout(1)

        # Estabelece ligação ao IP e porta indicados.
        sock.connect((ip, port))

        try:
            # Envia uma quebra de linha para tentar provocar resposta do serviço.
            sock.send(b"\r\n")

            # Recebe até 1024 bytes enviados pelo serviço.
            banner = sock.recv(1024).decode(errors="ignore").strip()

        except:
            # Alguns serviços não devolvem banner.
            banner = ""

        # Fecha a ligação ao serviço.
        sock.close()

        return banner

    except:
        # Se não for possível ligar ou obter resposta, devolve string vazia.
        return ""


def scan_port(ip, port, common_ports):
    """
    Verifica se uma porta está aberta e recolhe informação do serviço associado.
    """

    try:
        # Cria um socket TCP para testar a ligação à porta.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define timeout curto para evitar esperas longas.
        sock.settimeout(0.5)

        # Tenta ligar à porta. O valor 0 indica que a porta está aberta.
        result = sock.connect_ex((ip, port))

        # Fecha o socket depois do teste.
        sock.close()

        if result == 0:

            # Obtém o nome do serviço com base no ficheiro common_ports.json.
            service = common_ports.get(port, "Desconhecido")

            # Tenta obter o banner do serviço.
            banner = get_banner(ip, port)

            # Devolve a informação recolhida sobre a porta aberta.
            return {
                "port": port,
                "service": service,
                "banner": banner
            }

    except:
        # Ignora erros de ligação para manter o scan a decorrer.
        pass

    # Se a porta estiver fechada ou ocorrer erro, não devolve resultado.
    return None


def scan_ports(ip, ports, common_ports):
    """
    Analisa múltiplas portas de um host e devolve as que se encontram abertas.
    """

    open_ports = []

    # Usa múltiplas threads para analisar várias portas em simultâneo.
    with ThreadPoolExecutor(max_workers=100) as executor:

        # Executa scan_port para cada porta indicada.
        results = executor.map(
            lambda port: scan_port(ip, port, common_ports),
            ports
        )

        # Percorre apenas os resultados que indicam portas abertas.
        for result in results:

            if result:
                print(f"[-] Porta {result['port']} aberta ({result['service']})")

                # Guarda a porta aberta na lista de resultados.
                open_ports.append(result)

    return open_ports