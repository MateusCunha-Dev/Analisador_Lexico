class AnalisadorSintatico:
    def __init__(self):
        self.regra_incompleta = None

        self.regras_perguntas = {
            "qual documento está no": "<formato>",
            "qual tamanho tem": "<formato>",
            "qual documento tem": "<titulo>",
            "existe documento com título": "<titulo>",
            "quantos documentos estão no formato": "<formato>",
            "quem escreveu o documento": "<titulo>",
            "quando foi criado o documento": "<titulo>",
            "qual documento contém a palavra": "<palavra>"
        }

        self.regras_respostas = {
            "o formato é": "<formato>",
            "o tamanho é": "<numero>",
            "o título é": "<titulo>",
            "quero tamanho maior que": "<numero>",
            "o documento está na pasta": "<titulo>",
            "o autor é": "<titulo>",
            "a data de criação é": "<numero>",
            "o documento contém a palavra": "<palavra>"
        }

        FORMATOS_VALIDOS = {"pdf", "docx", "txt", "html"}  # Do seu BNF original
        PALAVRAS_VALIDAS = {"documento", "relatório", "técnico", "orçamento"}  # Exemplos do seu BNF

    def reconhecer_estrutura(self, tokens):
        frase = " ".join(tokens).lower()

        # Verifica perguntas exatas do seu BNF
        for pergunta, elemento in [
            ("qual documento está no", "<formato>"),
            ("qual tamanho tem", "<formato>"),
            ("qual documento tem", "<titulo>"),
            ("existe documento com título", "<titulo>"),
            ("quantos documentos estão no formato", "<formato>"),
            ("quem escreveu o documento", "<titulo>"),
            ("quando foi criado o documento", "<titulo>"),
            ("qual documento contém a palavra", "<palavra>")
        ]:
            if frase.startswith(pergunta):
                if len(tokens) == len(pergunta.split()) + 1:  # Pergunta completa
                    return "pergunta", pergunta
                return "pergunta_incompleta", pergunta  # Falta o elemento

        # Verifica respostas exatas do seu BNF
        for resposta, elemento in [
            ("o formato é", "<formato>"),
            ("o tamanho é", "<numero>"),
            ("o título é", "<titulo>"),
            ("quero tamanho maior que", "<numero>"),
            ("o documento está na pasta", "<titulo>"),
            ("o autor é", "<titulo>"),
            ("a data de criação é", "<numero>"),
            ("o documento contém a palavra", "<palavra>")
        ]:
            if frase.startswith(resposta):
                if len(tokens) == len(resposta.split()) + 1:  # Resposta completa
                    return "resposta", resposta
                return "resposta_incompleta", resposta  # Falta o elemento

        return "erro", None

    def perguntar_elemento_faltando(self):
        if self.regra_incompleta:
            tipo, estrutura, esperado = self.regra_incompleta
            # Mapeamento mais específico baseado no seu BNF
            mensagens = {
                "<formato>": "De qual formato? (PDF, DOCX, TXT ou HTML)",
                "<titulo>": "Qual é o título do documento?",
                "<numero>": "Qual número?",
                "<palavra>": "Qual palavra-chave deseja buscar?"
            }
            return mensagens.get(esperado, f"Qual {esperado.strip('<>')}?")
        return None

    def tentar_completar_regra(self, estrutura_anterior, resposta_usuario):
        frase_completa = f"{estrutura_anterior} {resposta_usuario}".lower().strip("?.!")

        for chave, esperado in self.regras_perguntas.items():
            regra_esperada = f"{chave.lower()} {esperado}"
            if regra_esperada == frase_completa:
                return "pergunta_completada", frase_completa

        for chave, esperado in self.regras_respostas.items():
            regra_esperada = f"{chave.lower()} {esperado}"
            if regra_esperada == frase_completa:
                return "resposta_completada", frase_completa

        return "falha_completar", frase_completa

    def analisar_palavras_extras(self, tokens, estrutura_detectada):
        elementos_identificados = []
        palavras_extras = tokens[len(estrutura_detectada.split()):]

        formatos = {"pdf", "docx", "txt", "html"}
        palavras_titulo = {"documento", "relatório", "técnico", "orçamento", "joão", "silva"}

        for palavra in palavras_extras:
            if palavra.lower() in formatos:
                elementos_identificados.append((palavra, "<formato>"))
            elif palavra.lower() in palavras_titulo:
                elementos_identificados.append((palavra, "<titulo>"))
            elif palavra.isdigit():
                elementos_identificados.append((palavra, "<numero>"))
            else:
                elementos_identificados.append((palavra, "<palavra>"))  # default: palavra-chave

        return elementos_identificados
    
