from analisador_lexico import AnalisadorLexico
from analisador_sintatico import AnalisadorSintatico

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

        # Etapa 1: Análise Léxica
        sucesso, _ = analisador_lexico.processar_texto(texto)
        resultados = analisador_lexico.get_resultados()
        tokens = [t for t in resultados['fila_tokens'] if t not in {'?', '.', '!'}]


        if not tokens:
            print("⚠ Nenhum token válido encontrado.")
            continue

        if resultados['caracteres_invalidos']:
            print("⚠ Caracteres inválidos encontrados:")
            for pos, char in resultados['caracteres_invalidos']:
                print(f"  Posição {pos}: {char}")
            continue

        print("Tokens:", tokens)

        # Etapa 2: Análise Sintática
        tipo, estrutura = analisador_sintatico.reconhecer_estrutura(tokens)

        if tipo == "pergunta":
            print(f"✅ Pergunta reconhecida: '{estrutura}'")
            contexto_anterior = ("pergunta", estrutura)

        elif tipo == "resposta":
            print(f"✅ Resposta reconhecida: '{estrutura}'")
            if contexto_anterior:
                tipo_ant, estrutura_ant = contexto_anterior
                status, resultado = analisador_sintatico.tentar_completar_regra(estrutura_ant, " ".join(tokens))
                if status.endswith("completada"):
                    print(f"✅ Estrutura anterior completada com resposta: '{resultado}'")
                    contexto_anterior = None
            else:
                contexto_anterior = ("resposta", estrutura)

        elif tipo.endswith("_incompleta"):
            print(f"🟡 Estrutura incompleta reconhecida: '{estrutura}'")
            falta = analisador_sintatico.perguntar_elemento_faltando()
            if falta:
                print(f"> {falta}")
            contexto_anterior = (tipo.replace("_incompleta", ""), estrutura)

        elif tipo == "erro":
            if contexto_anterior:
                status, resultado = analisador_sintatico.tentar_completar_regra(contexto_anterior[1], " ".join(tokens))
                if status.endswith("completada"):
                    print(f"✅ Estrutura completada com sucesso: '{resultado}'")
                    contexto_anterior = None
                else:
                    print("❌ Ainda não entendi. Estrutura continua incorreta.")
            else:
                print("❌ Não entendi.")

if __name__ == "__main__":
    main()
