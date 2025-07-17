def compilar_para_L1(tabela_simbolos):
    """
    Gera uma URL da linguagem L1 (Pergamum) com base na tabela de símbolos.
    """
    base_url = "https://catalogobiblioteca.ufmg.br/pesquisa_avancada?"

    titulo = []
    autor = ""
    assunto = ""

    for termo, tipo in tabela_simbolos.items():
        if tipo == "<titulo>":
            titulo.append(termo)
        elif tipo == "<autor>" and not autor:
            autor = termo
        elif tipo == "<palavra>" and not assunto:
            assunto = termo

    parametros = (
        f"for=TITULO&q={' '.join(titulo)}"
        f"&condition=AND&for2=AUTOR&q2={autor}"
        f"&condition2=AND&for3=ASSUNTO&q3={assunto}"
        f"&keyword_type=P"
    )
    return base_url + parametros