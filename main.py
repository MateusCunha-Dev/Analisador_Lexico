from analisador_lexico import AnalisadorLexico

def main():
    analisador = AnalisadorLexico()
    print("=== ANALISADOR LÉXICO ===")

    while True:
        texto = input("\nDigite um texto (ou 'sair' para encerrar):\n> ")
        if texto.lower() == 'sair':
            break

        sucesso, msg = analisador.processar_texto(texto)
        resultados = analisador.get_resultados()

        print(f"\nStatus: {msg}")
        print("\nTabela de Símbolos:", ", ".join(resultados['tabela_simbolos']))
        print("\nFila de Tokens:", " -> ".join(resultados['fila_tokens']))

        if resultados['caracteres_invalidos']:
            print("\nCaracteres inválidos encontrados:")
            for pos, char in resultados['caracteres_invalidos']:
                print(f"Posição {pos}: {char}")
        else:
            print("\nNenhum caractere inválido encontrado.")

if __name__ == "__main__":
    main()
