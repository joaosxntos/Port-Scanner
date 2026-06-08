O Port Scanner é uma ferramenta de recolha de informação de rede desenvolvida em Python.

O programa permite:

* Descobrir hosts ativos numa rede;
* Identificar portas abertas;
* Identificar serviços associados às portas;
* Recolher banners dos serviços;
* Estimar o sistema operativo dos hosts;
* Gerar relatórios em TXT, JSON e HTML.

## Estrutura do Projeto

```
.
├── backend/
│   ├── analyzer.py
│   ├── common_ports.py
│   ├── report.py
│   └── scanner.py
├── relatorios/
├── common_ports.json
├── main.py
└── README.md
```

## Requisitos

* Python 3.10 ou superior

## Como Executar

```
python main.py
```

## Etapas

Descoberta de hosts ativos através de pedidos ICMP (ping).

Análise de portas abertas nos hosts identificados.

Identificação de serviços e estimativa do sistema operativo.

Criação de relatórios em:

* TXT
* JSON
* HTML
