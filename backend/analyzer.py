def guess_os(open_ports):
    """
    Estima o sistema operativo com base nas portas abertas encontradas.
    """
        
    ports = [item["port"] for item in open_ports]

    if 3389 in ports or 445 in ports:
        return "Possível Windows"
    elif 22 in ports and 80 in ports:
        return "Possível Linux/Servidor Web"
    elif 22 in ports:
        return "Possível Linux/Unix"
    elif 80 in ports or 443 in ports:
        return "Possível servidor Web"
    else:
        return "Sistema não identificado"