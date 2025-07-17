from analisador_lexico import AnalisadorLexico
from analisador_sintatico import AnalisadorSintatico
from compilador import compilar_para_L1

def main():
    analisador_lexico = AnalisadorLexico()
    analisador_sintatico = AnalisadorSintatico()
    contexto_anterior = None

    print("=== ANALISADOR LÉXICO E SINTÁTICO ===")
    print("Digite 'sair' para encerrar.\n")

    while True:
        texto = input("> ").strip()
        if texto.lower() == 'sair':
            break

        sucesso, _ = analisador_lexico.processar_texto(texto)
        resultados = analisador_lexico.get_resultados()
        tokens = [t for t in resultados['fila_tokens'] if t not in {'?', '.', '!'}]

        if not tokens:
            print("Nenhum token válido encontrado.")
            continue

        if resultados['caracteres_invalidos']:
            print("Caracteres inválidos encontrados:")
            for pos, char in resultados['caracteres_invalidos']:
                print(f"  Posição {pos}: {char}")
            continue

        print("Tokens:", tokens)
        print("Tabela de símbolos (com tipo inferido):")
        for palavra, tipo in resultados['tabela_simbolos'].items():
            print(f"  - {palavra}: {tipo}")

        # 🔽 NOVO BLOCO: Compilação para Linguagem L1 (Pergamum)
        print("\n--- COMPILAÇÃO PARA LINGUAGEM L1 (Pergamum) ---")
        url_l1 = compilar_para_L1(resultados['tabela_simbolos'])
        print(f"URL gerada: {url_l1}\n")

        tipo, estrutura = analisador_sintatico.reconhecer_estrutura(tokens)

        if tipo == "pergunta":
            print(f"Pergunta reconhecida: '{estrutura}'")
            contexto_anterior = ("pergunta", estrutura)

        elif tipo == "resposta":
            print(f"Resposta reconhecida: '{estrutura}'")

            if contexto_anterior and contexto_anterior[0] in {"pergunta", "pergunta_incompleta"}:
                ultimo_token = tokens[-1] if tokens else ""
                status, resultado = analisador_sintatico.tentar_completar_regra(
                    contexto_anterior[1],
                    ultimo_token
                )
                if status.endswith("completada"):
                    print(f"Estrutura completada: '{resultado}'")
                    contexto_anterior = None
                else:
                    print("Não consegui relacionar com a pergunta anterior.")
            else:
                print("Resposta registrada com sucesso.")

        elif tipo.endswith("_incompleta"):
            if isinstance(estrutura, dict):
                msg = f"Estrutura incompleta reconhecida: '{estrutura['padrao']}"
                if 'falta' in estrutura:
                    msg += f" <<{estrutura['falta']}>>"
                msg += "'"
                print(msg)

                if 'mensagem' in estrutura:
                    print(estrutura['mensagem'])
            else:
                print(f"Estrutura incompleta reconhecida: '{estrutura}'")

            if isinstance(estrutura, dict):
                extras = analisador_sintatico.analisar_palavras_extras(tokens, estrutura['padrao'])
            else:
                extras = analisador_sintatico.analisar_palavras_extras(tokens, estrutura)

            if extras:
                print("Palavras extras e funções inferidas:")
                for palavra, tipo_inf in extras:
                    print(f"  - '{palavra}': inferido como {tipo_inf}")
                    analisador_lexico.tabela_simbolos[palavra] = tipo_inf

            contexto_anterior = (tipo.replace("_incompleta", ""), estrutura)

        elif tipo == "erro":
            if contexto_anterior:
                status, resultado = analisador_sintatico.tentar_completar_regra(
                    contexto_anterior[1],
                    " ".join(tokens)
                )
                if status.endswith("completada"):
                    print(f"Estrutura completada com sucesso: '{resultado}'")
                    contexto_anterior = None
                else:
                    print("Não consegui entender.")
            else:
                print("Não entendi.")

        elif tipo == "erro_contexto":
            print("Não consegui entender a resposta para a pergunta anterior.")

if __name__ == "__main__":
    main()
