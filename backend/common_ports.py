import json
import os

def load_common_ports():
    """
    Carrega do ficheiro JSON a lista de portas e serviços mais comuns.
    """
        
    base_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, "common_ports.json")

    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return {
            int(port): service
            for port, service in data.items()
        }

    except FileNotFoundError:
        print("[ERRO] Ficheiro common_ports.json não encontrado.")
        return {}

    except json.JSONDecodeError:
        print("[ERRO] O ficheiro common_ports.json tem JSON inválido.")
        return {}