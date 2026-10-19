cd ~/vyrux-repo

cat << 'EOF' > README.md
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
- **Human-in-the-Loop (HITL):** Nenhum comando do sistema operacional é executado sem a confirmação e autorização explícita do operador ( `s/N` ).
- **Whitelist de Segurança:** Restrição estrita de execução aos comandos de diagnóstico de rede permitidos ( `ping` , `nmap` , `dig` , `traceroute` , `curl` ).
- **Baixa Latência:** Extração otimizada via Expressão Regular (Regex) das tags `<cmd>`, garantindo respostas em poucos segundos.

---

## 🧪 Ambiente de Testes (CyberLab)

A PoC foi validada em um ambiente virtualizado e isolado no VirtualBox:

- **Agente (Vyrux):** Ubuntu Guest OS ( `192.168.100.1` )
- **Alvo de Testes:** Metasploitable2 ( `192.168.100.2` )
- **Rede:** Rede Interna Isolada ( `CyberLab` ) com IPs estáticos e modo promíscuo ativado.

---

## ⚙️ Pré-requisitos do Sistema

Certifique-se de que o sistema possui as seguintes ferramentas instaladas antes de prosseguir:

- **Pacotes Base do Sistema (Python e Git):**
  - Comando: `sudo apt update && sudo apt install -y python3 python3-venv python3-pip git`
- **Ferramentas de Diagnóstico de Rede:**
  - Comando: `sudo apt install -y nmap iputils-ping dnsutils traceroute curl`
- **Ollama (Engine LLM Local):**
  - Instalação: `curl -fsSL https://ollama.com/install.sh | sh`
  - Download do modelo: `ollama pull llama3.2:1b`

---

## 🛠️ Guia de Instalação e Configuração

Siga os passos abaixo para preparar e executar o ambiente do Vyrux:

- **Passo 1: Clonar o Repositório**
  - `git clone https://github.com/Brenosspc/vyrux-agent.git`
  - `cd vyrux-agent`
- **Passo 2: Criar e Ativar o Ambiente Virtual Python**
  - `python3 -m venv vyrux-env`
  - `source vyrux-env/bin/activate`
- **Passo 3: Instalar as Dependências**
  - `pip install -r requirements.txt`

---

## 📖 Como Utilizar o Vyrux

- **1. Verificar o Serviço do Ollama:**
  - Certifique-se de que o Ollama está ativo rodando: `ollama list`
- **2. Iniciar o Agente:**
  - Execute o script principal com o ambiente virtual ativo: `python vyrux.py`
- **3. Exemplos de Prompts em Linguagem Natural:**
  - **Varredura de Rede:** `"Faça um scan de portas no IP 192.168.100.2 e me diga os serviços ativos."`
  - **Teste de Conectividade:** `"Verifique se o IP 192.168.100.2 está acessível na rede."`
  - **Dúvidas Conceituais:** `"O que é o serviço vsftpd 2.3.4 e por que ele é considerado vulnerável?"`
- **4. Fluxo de Autorização de Comandos (HITL):**
  - Quando o Vyrux sugere um comando (ex: `[Vyrux] Comando sugerido: nmap -sV 192.168.100.2`), confirme com `s` para aprovar ou `n` para recusar.
- **5. Encerrar o Agente:**
  - Digite `sair` ou `exit` a qualquer momento para fechar o programa.

---

## 📂 Estrutura do Repositório

- **`vyrux.py`:** Script principal contendo a lógica do agente, Regex e validação HITL.
- **`requirements.txt`:** Ficheiro de dependências Python do projeto ( `ollama` ).
- **`README.md`:** Documentação completa do projeto.

---

## 🔧 Troubleshooting (Solução de Problemas)

- **Erro `Connection Refused` ao conectar ao Ollama:**
  - O serviço do Ollama não está rodando. Abra outro terminal e execute `ollama serve`.
- **Comando não executado pelo Vyrux:**
  - O comando solicitado não está na *whitelist*. Apenas `ping`, `nmap`, `dig`, `traceroute` e `curl` são permitidos.
- **Erro de permissão no Nmap:**
  - Varreduras avançadas exigem `root`. Use varreduras padrão de serviços ( `nmap -sV` ) ou rode com `sudo`.

---

## 📝 Aprendizados e Limitações Identificadas

- **Ajuste de System Prompt:** Modelos locais menores necessitam de prompts estritos para evitar formatação excessiva quando a saída precisa ser consumida por scripts.
- **Raciocínio Encadeado:** Modelos de 1B parâmetros são excelentes para tradução direta de intenção para comando (*Text-to-CLI*), mas apresentam limitações ao tentar gerenciar fluxos complexos de auditoria de forma 100% autônoma.

---
*Projeto desenvolvido para fins educacionais e de pesquisa em cibersegurança.*
EOF

git add README.md
git commit -m "style: padroniza todo o README com estilo de marcadores e inline code"
git push
