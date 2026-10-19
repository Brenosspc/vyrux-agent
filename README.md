# 🛡️ Vyrux — Local Cybersecurity Agent (PoC)

**Vyrux** é uma Prova de Conceito (PoC) de um assistente local de cibersegurança focado na automação de diagnósticos de rede e análise de conectividade. O agente utiliza um Modelo de Linguagem Local (LLM) rodando via **Ollama** e uma interface de execução segura com autorização humana (*Human-in-the-Loop*).

---

## 📋 Sumário
- [Arquitetura e Funcionalidades](#-arquitetura-e-funcionalidades)
- [Ambiente de Testes (CyberLab)](#-ambiente-de-testes-cyberlab)
- [Pré-requisitos do Sistema](#-pré-requisitos-do-sistema)
- [Guia de Instalação e Configuração](#-guia-de-instalação-e-configuração)
- [Como Utilizar o Vyrux](#-como-utilizar-o-vyrux)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Troubleshooting (Solução de Problemas)](#-troubleshooting-solução-de-problemas)
- [Aprendizados e Limitações Identificadas](#-aprendizados-e-limitações-identificadas)

---

## 🚀 Arquitetura e Funcionalidades

- **Engine Local:** Execução 100% offline e privada utilizando **Ollama** com o modelo `llama3.2:1b`.
- **Human-in-the-Loop (HITL):** Nenhum comando do sistema operacional é executado sem a confirmação e autorização explícita do operador (`s/N`).
- **Whitelist de Segurança:** Restrição estrita de execução aos comandos de diagnóstico de rede permitidos (`ping`, `nmap`, `dig`, `traceroute`, `curl`).
- **Baixa Latência:** Extração otimizada via Expressão Regular (Regex) das tags `<cmd>`, garantindo respostas em poucos segundos.

---

## 🧪 Ambiente de Testes (CyberLab)

A PoC foi validada em um ambiente virtualizado e isolado no VirtualBox:
- **Agente (Vyrux):** Ubuntu Guest OS (`192.168.100.1`)
- **Alvo de Testes:** Metasploitable2 (`192.168.100.2`)
- **Rede:** Rede Interna Isolada (`CyberLab`) com IPs estáticos e modo promíscuo ativado.

---

## ⚙️ Pré-requisitos do Sistema

Antes de instalar o Vyrux, certifique-se de que seu sistema operacional (Linux/Ubuntu) possui os seguintes pacotes instalados:

1. **Python 3.10+** e suporte a ambiente virtual (`venv`):
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-venv python3-pip git
Ferramentas de Rede:

Bash
sudo apt install -y nmap iputils-ping dnsutils traceroute curl
Ollama (Engine LLM Local):

Instale o Ollama conforme as instruções oficiais:

Bash
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
Baixe o modelo leve llama3.2:1b:

Bash
ollama pull llama3.2:1b
🛠️ Guia de Instalação e Configuração
Siga os passos abaixo para preparar e executar o ambiente do Vyrux:

Clonar o Repositório:

Bash
git clone [https://github.com/Brenosspc/vyrux-agent.git](https://github.com/Brenosspc/vyrux-agent.git)
cd vyrux-agent
Criar e Ativar o Ambiente Virtual Python:

Bash
python3 -m venv vyrux-env
source vyrux-env/bin/activate
Instalar as Dependências:

Bash
pip install -r requirements.txt
📖 Como Utilizar o Vyrux
Garantir que o Serviço do Ollama está Ativo:
Em uma janela do terminal (ou em segundo plano), verifique se o Ollama está rodando:

Bash
ollama list
Iniciar o Agente:
Com o ambiente virtual ativado ((vyrux-env) no prompt), execute o script principal:

Bash
python vyrux.py
Exemplos de Interação:
Você pode interagir em linguagem natural. O agente identificará se precisa rodar um comando ou apenas responder com explicações técnicas:

Varredura de Rede: "Faça um scan de portas no IP 192.168.100.2 e me diga os serviços ativos."

Teste de Conectividade: "Verifique se o IP 192.168.100.2 está acessível na rede."

Dúvidas Conceituais: "O que é o serviço vsftpd 2.3.4 e por que ele é considerado vulnerável?"

Autorização de Comandos (Fluxo HITL):
Quando o Vyrux sugere a execução de um comando do terminal, ele interrompe o fluxo e solicita sua confirmação:

Plaintext
[Vyrux] Comando sugerido: nmap -sV 192.168.100.2
Deseja executar este comando? (s/N):
Digite s e pressione Enter para aprovar a execução.

Digite n (ou pressione Enter) para recusar.

Encerrar a Execução:
Para sair do agente, digite sair ou exit a qualquer momento.

📂 Estrutura do Repositório
Plaintext
vyrux-agent/
├── vyrux.py             # Script principal contendo a lógica do agente, Regex e validação HITL
├── requirements.txt     # Dependências Python do projeto (ollama)
└── README.md            # Documentação completa do projeto
🔧 Troubleshooting (Solução de Problemas)
Erro Connection Refused ao conectar ao Ollama:
Certifique-se de que o serviço do Ollama está rodando em segundo plano digitando ollama serve em outro terminal.

Comando não executado pelo Vyrux:
O comando solicitado precisa estar contido na whitelist de segurança (ping, nmap, dig, traceroute, curl). Caso contrário, a execução é bloqueada por segurança.

Erro de permissão no Nmap:
Alguns tipos de varredura avançada do Nmap exigem privilégios de superusuário (sudo). Para varreduras normais de serviços (nmap -sV), permissões de usuário padrão são suficientes.

📝 Aprendizados e Limitações Identificadas
Ajuste de System Prompt: Modelos locais menores necessitam de prompts estritos para evitar a formatação excessiva em Markdown quando a saída precisa ser consumida por scripts.

Raciocínio Encadeado: Modelos de 1B parâmetros são excelentes para tradução direta de intenção para comando (Text-to-CLI), mas apresentam limitações ao tentar gerenciar fluxos complexos e multi-etapas de auditoria de forma 100% autônoma.

Projeto desenvolvido para fins educacionais e de pesquisa em cibersegurança.
