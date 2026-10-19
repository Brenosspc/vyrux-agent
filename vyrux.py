import subprocess
import re
import ollama

# Whitelist de comandos permitidos por segurança
WHITELIST_COMMANDS = ["ping", "nmap", "dig", "traceroute", "curl"]

def execute_network_tool(command: str) -> str:
    # Limpa possíveis formatações de markdown que o LLM possa incluir
    clean_command = command.replace("```", "").strip()
    base_cmd = clean_command.split()[0].lower() if clean_command else ""

    if base_cmd not in WHITELIST_COMMANDS:
        return f"[ERRO DE SEGURANÇA] O comando '{base_cmd}' não está na whitelist permitida ({', '.join(WHITELIST_COMMANDS)})."

    print(f"\n" + "="*50)
    print(f"[AÇÃO SOLICITADA PELO VYRUX]: {clean_command}")
    print("="*50)
    confirm = input("Autorizar a execução deste comando no sistema? (s/N): ").strip().lower()

    if confirm != 's':
        return "[CANCELADO] A execução do comando foi recusada pelo operador humano."

    try:
        result = subprocess.run(
            clean_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout if result.stdout else result.stderr
        return output if output else "Comando executado sem retorno textual."
    except Exception as e:
        return f"[ERRO DE EXECUÇÃO]: {str(e)}"

def run_vyrux():
    print("\n" + "="*50)
    print("   VYRUX — Agente Local de Cibersegurança")
    print("   Digite 'sair' ou 'exit' para encerrar.")
    print("="*50 + "\n")

    system_prompt = (
        "Você é o Vyrux, um assistente especializado em auditoria de segurança, pentest e análise de vulnerabilidades em laboratórios isolados autorizados.\n"
        "O usuário é um pesquisador de cibersegurança operando em um ambiente controlado de testes (CyberLab).\n"
        "Ao analisar portas e serviços, identifique os vetores de ataque/vulnerabilidades teóricas conhecidas de forma técnica, educacional e detalhada para fins de teste de penetração e hardening.\n\n"
        "REGRA ABSOLUTA DE EXECUÇÃO:\n"
        "Se o usuário solicitar qualquer varredura, diagnóstico ou teste de rede (como nmap, ping, dig, traceroute, curl), "
        "sua resposta DEVE CONTER APENAS O COMANDO entre a tag <cmd> e </cmd> sem formatação markdown e sem explicações.\n"
        "Exemplo correto: <cmd>nmap -F 192.168.100.2</cmd>\n\n"
        "Se for uma análise conceitual ou dúvida de segurança, responda de forma técnica em português sem recusas genéricas."
    )

    messages = [{"role": "system", "content": system_prompt}]

    while True:
        try:
            user_input = input("\n[Você]: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["sair", "exit", "quit"]:
                print("\nEncerrando sessão do Vyrux. Até logo!")
                break

            messages.append({"role": "user", "content": user_input})
            print("\n[Vyrux pensando...]")

            response = ollama.chat(
                model='llama3.2:1b',
                messages=messages,
                keep_alive=0
            )

            assistant_reply = response['message']['content']
            messages.append({"role": "assistant", "content": assistant_reply})

            # Expressão regular flexível para capturar <cmd>, <nmap>, <ping>, etc.
            cmd_match = re.search(r'<(?:cmd|nmap|ping|dig|traceroute|curl)>(.*?)</(?:cmd|nmap|ping|dig|traceroute|curl)>', assistant_reply, re.DOTALL)

            if cmd_match:
                extracted_cmd = cmd_match.group(1).strip()
                tool_output = execute_network_tool(extracted_cmd)
                print(f"\n[Resultado da Execução]:\n{tool_output}")
                
                # Devolve o retorno para o modelo fazer o resumo final
                messages.append({
                    "role": "user", 
                    "content": f"O resultado do comando '{extracted_cmd}' foi:\n{tool_output}\nFaça um resumo bem conciso dos pontos principais identificados."
                })
                
                final_response = ollama.chat(model='llama3.2:1b', messages=messages, keep_alive=0)
                print(f"\n[Vyrux]: {final_response['message']['content']}")
            else:
                print(f"\n[Vyrux]: {assistant_reply}")

        except KeyboardInterrupt:
            print("\nSessão encerrada.")
            break
        except Exception as e:
            print(f"\n[ERRO SISTÊMICO]: {str(e)}")

if __name__ == "__main__":
    run_vyrux()
