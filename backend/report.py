import json
import os
from datetime import datetime

def save_results(results, scan_name):
    """
    Cria os ficheiros de relatório e guarda os resultados do scan.
    """
        
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(base_dir, "reports")
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    json_file = os.path.join(output_dir, f"{scan_name}_{timestamp}.json")

    txt_file = os.path.join(output_dir, f"{scan_name}_{timestamp}.txt")

    html_file = os.path.join(output_dir, f"{scan_name}_{timestamp}.html")

    save_json(results, json_file, scan_name, timestamp)

    save_txt(results, txt_file, scan_name, timestamp)

    save_html(results, html_file, scan_name, timestamp)

    print("\n[+] Relatórios guardados em:")
    print(f"    {json_file}")
    print(f"    {txt_file}")
    print(f"    {html_file}")

def save_json(results, filename, scan_name, timestamp):
    """
    Exporta os resultados do scan para formato JSON.
    """
        
    data = {
        "scan_name": scan_name,
        "scan_date": timestamp,
        "results": results
    }

    if not results:
        data["message"] = "Nenhum host ativo foi encontrado."

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def save_txt(results, filename, scan_name, timestamp):
    """
    Exporta os resultados do scan para um relatório de texto.
    """
        
    with open(filename, "w", encoding="utf-8") as file:

        file.write("Relatório\n")
        file.write("=" * 40 + "\n\n")

        file.write(f"Nome do Scan: {scan_name}\n")
        file.write(f"Data do Scan: {timestamp}\n\n")

        if not results:
            file.write("Nenhum host ativo foi encontrado.\n")
            return

        for host in results:

            file.write(f"IP: {host['ip']}\n")
            file.write(f"Sistema provável: {host['os_guess']}\n")
            file.write("Portas abertas:\n")

            if not host["open_ports"]:
                file.write("  Nenhuma porta aberta encontrada.\n")
            else:
                for port in host["open_ports"]:
                    file.write(f"  - Porta {port['port']} ({port['service']})")

                    if port["banner"]:
                        file.write(f" | Banner: {port['banner']}")

                    file.write("\n")

            file.write("\n" + "-" * 40 + "\n\n")

def save_html(results, filename, scan_name, timestamp):
    """
    Exporta os resultados do scan para um relatório em html.
    """
    with open(filename, "w", encoding="utf-8") as file:

        file.write("""
<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<title>Relatório</title>

<style>
body {
    font-family: Arial, sans-serif;
    margin: 40px;
}

h1 {
    text-align: center;
}

details {
    margin-bottom: 15px;
    border: 1px solid #ccc;
    padding: 10px;
}

summary {
    cursor: pointer;
    font-weight: bold;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}

th, td {
    border: 1px solid #ccc;
    padding: 8px;
}

th {
    background-color: #f2f2f2;
}
</style>

</head>
<body>
""")

        file.write("<h1>Relatório </h1>")

        file.write(
            f"<p><strong>Nome do Scan:</strong> "
            f"{scan_name}</p>"
        )

        file.write(
            f"<p><strong>Data do Scan:</strong> "
            f"{timestamp}</p>"
        )

        if not results:
            file.write(
                "<p>Nenhum host ativo foi encontrado.</p>"
            )

        else:

            for host in results:

                file.write(
                    f"<details>"
                    f"<summary>{host['ip']}</summary>"
                )

                file.write(
                    f"<p><strong>Sistema provável:</strong> "
                    f"{host['os_guess']}</p>"
                )

                if not host["open_ports"]:

                    file.write(
                        "<p>Nenhuma porta aberta encontrada.</p>"
                    )

                else:

                    file.write("""
<table>
<tr>
<th>Porta</th>
<th>Serviço</th>
<th>Banner</th>
</tr>
""")

                    for port in host["open_ports"]:

                        banner = (
                            port["banner"]
                            if port["banner"]
                            else "-"
                        )

                        file.write(
                            f"<tr>"
                            f"<td>{port['port']}</td>"
                            f"<td>{port['service']}</td>"
                            f"<td>{banner}</td>"
                            f"</tr>"
                        )

                    file.write("</table>")

                file.write("</details>")

        file.write("""
</body>
</html>
""")