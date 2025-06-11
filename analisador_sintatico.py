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

    def reconhecer_estrutura(self, tokens):
        frase = " ".join(tokens).lower().strip("?.!")

        for chave, esperado in self.regras_perguntas.items():
            if frase.startswith(chave):
                if len(tokens) == len(chave.split()) + 1:
                    return "pergunta", chave
                else:
                    self.regra_incompleta = ("pergunta", chave, esperado)
                    return "pergunta_incompleta", chave

        for chave, esperado in self.regras_respostas.items():
            if frase.startswith(chave):
                if len(tokens) == len(chave.split()) + 1:
                    return "resposta", chave
                else:
                    self.regra_incompleta = ("resposta", chave, esperado)
                    return "resposta_incompleta", chave

        return "erro", None

    def perguntar_elemento_faltando(self):
        if self.regra_incompleta:
            tipo, estrutura, esperado = self.regra_incompleta
            perguntas = {
                "<formato>": "Qual formato você deseja saber?",
                "<titulo>": "Qual título você deseja indicar?",
                "<numero>": "Qual número você deseja especificar?",
                "<palavra>": "Qual palavra-chave você está buscando?"
            }
            return perguntas.get(esperado)
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

