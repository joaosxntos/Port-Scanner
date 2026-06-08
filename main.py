import os
import ipaddress
from backend.scanner import scan_network, scan_ports
from backend.analyzer import guess_os
from backend.report import save_results
from backend.common_ports import load_common_ports

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_banner():
    print("\n" + "=" * 40)
    print("O MAPA DA MINA".center(40))
    print("Scanner de Rede em Python".center(40))
    print("=" * 40)

def show_scan_start():
    print("\n" + "=" * 40)
    print("SCAN EM EXECUÇÃO".center(40))
    print("=" * 40)

def get_scan_name():
    """
    Pede ao utilizador um nome para o scan e substitui espaços por underscores.
    """
        
    scan_name = input("\nIntroduz um nome para este scan (Enter = mapa_da_mina): ").strip()

    if not scan_name:
        scan_name = "mapa_da_mina"

    return scan_name.replace(" ", "_")

def get_network():
    """
    Pede ao utilizador uma rede e valida o formato antes de avançar.
    """
        
    while True:
        network = input("\nIntroduz a rede/IP range. Ex: 192.168.1.0/24: ")

        try:
            ipaddress.ip_network(network, strict=False)
            return network

        except ValueError:
            print("\n[ERRO] Rede inválida.")
            input("Pressiona ENTER para tentar novamente...")

def get_ports(common_ports):
    """
    Permite escolher entre portas comuns (ficheiro common_ports.json) ou um intervalo personalizado.
    """
        
    while True:
        port_choice = input("Queres analisar portos comuns ou um intervalo? (comuns/intervalo): ").lower().strip()

        if port_choice in ("comuns", "intervalo"):
            break

        print("\n[ERRO] Opção inválida. Escolhe 'comuns' ou 'intervalo'.")

    if port_choice == "intervalo":
        return get_port_range()

    return common_ports.keys(), "Portos comuns"

def get_port_range():
    """
    Recebe um intervalo de portas válido e devolve as portas a analisar.
    """
        
    while True:
        try:
            start_port = int(input("Porta inicial: "))
            end_port = int(input("Porta final: "))

            if (
                1 <= start_port <= 65535 and
                1 <= end_port <= 65535 and
                start_port <= end_port
            ):
                ports = range(start_port, end_port + 1)
                port_mode = f"Intervalo {start_port}-{end_port}"
                return ports, port_mode

            print("\n[ERRO] Intervalo inválido. As portas devem estar entre 1 e 65535 e a porta inicial não pode ser superior à final.")

        except ValueError:
            print("\n[ERRO] Introduz apenas números inteiros.")

def show_scan_config(scan_name, network, port_mode):
    print("\n===== CONFIGURAÇÃO DO SCAN =====")
    print(f"Nome: {scan_name}")
    print(f"Rede: {network}")
    print(f"Portos: {port_mode}")

def run_scan(active_hosts, ports, common_ports):
    """
    Analisa os hosts ativos, identifica portas abertas e estima o sistema operativo.
    """
        
    results = []

    for ip in active_hosts:
        print(f"\n[+] A analisar host {ip}")

        open_ports = scan_ports(ip, ports, common_ports)

        if not open_ports:
            print("[-] Nenhuma porta aberta encontrada")

        os_guess = guess_os(open_ports)

        results.append({
            "ip": ip, 
            "os_guess": os_guess, 
            "open_ports": open_ports
            })

    return results

def show_summary(active_hosts, results):
    """
    Apresenta um resumo com o número de hosts e portas identificadas.
    """

    print("\n===== RESUMO DO SCAN =====")
    print(f"Hosts ativos: {len(active_hosts)}")

    total_ports = sum(
        len(host["open_ports"]) 
        for host in results
        )

    print(f"Portas abertas encontradas: {total_ports}")

def main():
    """
    Gere todas as etapas do programa, desde a recolha de dados até à criação do relatório.
    """
        
    show_banner()

    common_ports = load_common_ports()

    scan_name = get_scan_name()
    network = get_network()
    ports, port_mode = get_ports(common_ports)

    show_scan_config(scan_name, network, port_mode)

    input("\nPressiona ENTER para iniciar o scan...")

    clear_screen()
    show_scan_start()

    active_hosts = scan_network(network)

    if not active_hosts:
        print("\n[+] Nenhum host ativo encontrado.")

    results = run_scan(active_hosts, ports, common_ports)

    save_results(results, scan_name)

    print("\n[+] SCAN concluído.")

    show_summary(active_hosts, results)

if __name__ == "__main__":
    main()