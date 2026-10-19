# 🛡️ Vyrux — Local Cybersecurity Agent (PoC)

**Vyrux** é uma Prova de Conceito (PoC) de um assistente local de cibersegurança focado em automação de diagnósticos de rede e análise de conectividade. O agente utiliza um Modelo de Linguagem Local (LLM) integrado a uma interface de execução com autorização humana (*Human-in-the-Loop*).

---

## 🚀 Arquitetura e Funcionalidades

- **Engine Local:** Rodando via **Ollama** (`llama3.2:1b`), garantindo execução 100% offline e privada.
- **Human-in-the-Loop (HITL):** NENHUM comando do sistema é executado sem a aprovação explícita do operador (`s/N`).
- **Whitelist de Segurança:** Restrição estrita de comandos executáveis (`ping`, `nmap`, `dig`, `traceroute`, `curl`).
- **Baixa Latência:** Extração direta por Regex das tags de comando, reduzindo a latência de processamento.

---

## 🧪 Ambiente de Testes (CyberLab)

A PoC foi validada em um ambiente virtualizado e isolado no VirtualBox:
- **Agente (Vyrux):** Ubuntu Guest OS (`192.168.100.1`)
- **Alvo de Testes:** Metasploitable2 (`192.168.100.2`)
- **Rede:** Rede Interna Isolada (`CyberLab`) com IPs estáticos e modo promíscuo ativado.

---

## 🛠️ Como Executar

### Pré-requisitos
- Python 3.10+
- Ollama instalado com o modelo `llama3.2:1b`:
  ```bash
  ollama pull llama3.2:1b
