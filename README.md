# Port Scanner

O Port Scanner é uma ferramenta de recolha de informação de rede desenvolvida em Python.

O programa permite:

* Descobrir hosts ativos numa rede;
* Identificar portas abertas;
* Identificar serviços associados às portas;
* Recolher banners dos serviços;
* Estimar o sistema operativo dos hosts;
* Gerar relatórios em TXT, JSON e HTML.

## Clonar o Projeto

```bash
git clone https://github.com/joaosxntos/Port-Scanner.git
cd Port-Scanner
```

## Estrutura do Projeto

```text
.
├── backend/
│   ├── analyzer.py
│   ├── common_ports.py
│   ├── report.py
│   └── scanner.py
├── relatorios/
├── common_ports.json
├── main.py
├── README.md
└── .gitignore
```

## Requisitos

* Python 3.10 ou superior

## Como Executar

```bash
python main.py
```

## Configuração das Portas Comuns

O ficheiro `common_ports.json` contém a lista de portas e serviços utilizados quando o utilizador seleciona a opção **portos comuns**.

Este ficheiro pode ser alterado sem necessidade de modificar o código Python, permitindo adicionar, remover ou alterar portas e serviços.

Exemplo:

```json
{
    "22": "SSH",
    "80": "HTTP",
    "443": "HTTPS"
}
```

## Etapas

### Parte 1

Descoberta de hosts ativos através de pedidos ICMP (ping).

### Parte 2

Análise de portas abertas nos hosts identificados.

### Parte 3

Identificação de serviços, recolha de banners e estimativa do sistema operativo.

### Parte 4

Criação de relatórios em:

* TXT
* JSON
* HTML

## Aviso Legal e Ético

Esta ferramenta foi desenvolvida exclusivamente para fins académicos e de aprendizagem no âmbito da unidade curricular de Programação Aplicada à Cibersegurança.

A sua utilização deve ser limitada a redes, sistemas ou equipamentos para os quais exista autorização explícita do proprietário ou administrador.

O autor não se responsabiliza por qualquer utilização indevida da aplicação em ambientes não autorizados.
