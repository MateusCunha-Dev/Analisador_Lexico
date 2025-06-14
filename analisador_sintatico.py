class AnalisadorSintatico:
    def __init__(self):
        self.contexto_anterior = None

        self.palavras_funcionais = {
            "qual", "está", "no", "quando", "quem", "com", "de", "o", "a", "é"
        }

        self.regras_perguntas = {
            "qual documento está no": "<formato>",
            "qual tamanho tem": "<formato>",
            "qual documento tem": "<titulo>",
            "quem escreveu o documento": "<titulo>",
            "qual documento contém a palavra": "<palavra>"
        }

        self.regras_respostas = {
            "o formato é": "<formato>",
            "o tamanho é": "<numero>",
            "o título é": "<titulo>",
            "quero tamanho maior que": "<numero>",
            "o documento contém a palavra": "<palavra>"
        }

        self.terminais = {
            '<formato>': {'pdf', 'docx', 'txt', 'html'},
            '<palavra>': {'documento', 'relatório', 'técnico', 'orçamento', 'dados', 'informação',
                          'manual', 'contrato', 'proposta', 'pesquisa', 'vendas', 'compra',
                          'financeiro', 'projeto', 'desenvolvimento'},
            '<numero>': None,
            '<titulo>': None
            }

    def reconhecer_estrutura(self, tokens):
        tokens_sem_pontuacao = [t for t in tokens if t not in {'.', '?', '!'}]
        frase = " ".join(tokens_sem_pontuacao).lower()

        if self.contexto_anterior:
            tipo_anterior, estrutura_anterior = self.contexto_anterior
            status, resultado = self.tentar_completar_regra(estrutura_anterior, frase)
            if status.endswith("completada"):
                self.contexto_anterior = None
                return status, resultado
            elif status == "erro_completar":
                return "erro", "Não entendi a resposta."

        for padrao, elemento in self.regras_respostas.items():
            if frase.startswith(padrao.lower()):
                if len(tokens_sem_pontuacao) == len(padrao.split()) + 1:
                    ultimo_token = tokens_sem_pontuacao[-1]
                    if self._validar_terminal(ultimo_token, elemento):
                        return "resposta", padrao
                    else:
                        return "resposta_invalida", padrao
                return "resposta_incompleta", padrao

        for padrao, elemento in self.regras_perguntas.items():
            if frase.startswith(padrao):
                return self._avaliar_estrutura(tokens, padrao, elemento, "pergunta")

        for padrao, elemento in self.regras_respostas.items():
            if frase.startswith(padrao):
                return self._avaliar_estrutura(tokens, padrao, elemento, "resposta")

        return self._lidar_com_erro(tokens)

    def _avaliar_estrutura(self, tokens, padrao, elemento, tipo):
        partes_padrao = padrao.split()

        if len(tokens) == len(partes_padrao) + 1:
            ultimo_token = tokens[-1]
            if self._validar_terminal(ultimo_token, elemento):
                return tipo, padrao
            else:
                return f"{tipo}_invalido", padrao

        palavras_extras = tokens[len(partes_padrao):]
        if palavras_extras:
            return self._lidar_com_excesso(tokens, padrao, elemento, tipo)

        return self._lidar_com_falta(padrao, elemento, tipo)

    def _validar_terminal(self, token, tipo_terminal):
        if tipo_terminal == '<numero>':
            return token.isdigit()
        elif tipo_terminal == '<titulo>':
            return all(palavra.isalpha() for palavra in token.split())
        elif self.terminais.get(tipo_terminal):
            return token.lower() in self.terminais[tipo_terminal]
        return True

    def _lidar_com_excesso(self, tokens, padrao, elemento, tipo):
        palavras_extras = tokens[len(padrao.split()):]
        extras_analisadas = self.analisar_palavras_extras(palavras_extras, padrao)

        estrutura = {
            'tipo': f"{tipo}_incompleta",
            'padrao': padrao,
            'elemento_esperado': elemento,
            'palavras_extras': palavras_extras,
            'extras_analisadas': extras_analisadas
        }
        self.contexto_anterior = (f"{tipo}_incompleta", padrao)
        return f"{tipo}_incompleta", estrutura

    def perguntar_elemento_faltando(self):
        if self.contexto_anterior:
            tipo, estrutura = self.contexto_anterior
            if isinstance(estrutura, dict):
                return estrutura.get('mensagem')
        return None

    def _lidar_com_falta(self, padrao, elemento, tipo):
        self.contexto_anterior = (f"{tipo}_incompleta", padrao)
        mensagem = self._gerar_mensagem_falta(elemento)
        return f"{tipo}_incompleta", {
            'padrao': padrao,
            'falta': elemento,
            'mensagem': mensagem,
            'str': f"{padrao} <{elemento}>"
        }

    def _lidar_com_erro(self, tokens):
        if self.contexto_anterior:
            return "erro_contexto", "Não entendi a resposta para a pergunta anterior."
        return "erro", "Não entendi."

    def _gerar_mensagem_falta(self, elemento):
        mensagens = {
            '<formato>': "De qual formato você está falando? (PDF, DOCX, TXT ou HTML)",
            '<titulo>': "Qual é o título do documento?",
            '<numero>': "Qual número?",
            '<palavra>': "Qual palavra-chave?"
        }
        return mensagens.get(elemento, f"Qual {elemento.strip('<>')}?")

    def tentar_completar_regra(self, estrutura_anterior, resposta):
        if isinstance(estrutura_anterior, dict):
            padrao = estrutura_anterior.get('padrao', '')
            elemento = estrutura_anterior.get('falta', '')
        else:
            padrao = estrutura_anterior
            elemento = None

        valor = resposta.strip()
        for chave, esperado in self.regras_respostas.items():
            if resposta.startswith(chave.lower()):
                partes = resposta.split()
                if len(partes) > len(chave.split()):
                    valor = partes[-1]
                break

        frase_completa = f"{padrao} {valor}".lower()

        for chave, esperado in self.regras_perguntas.items():
            regra_esperada = f"{chave.lower()} {esperado}"
            if regra_esperada == frase_completa:
                return "pergunta_completada", frase_completa

        for chave, esperado in self.regras_respostas.items():
            regra_esperada = f"{chave.lower()} {esperado}"
            if regra_esperada == frase_completa:
                return "resposta_completada", frase_completa

        return "erro_completar", frase_completa

    def analisar_palavras_extras(self, tokens, estrutura_detectada):
        if isinstance(estrutura_detectada, dict):
            padrao = estrutura_detectada.get('padrao', '')
        else:
            padrao = estrutura_detectada

        palavras_extras = tokens[len(padrao.split()):] if padrao else tokens

        elementos_identificados = []
        formatos = {"pdf", "docx", "txt", "html"}
        palavras_titulo = {"documento", "relatório", "técnico", "orçamento", "dados", "informação", "joão", "silva"}

        for palavra in palavras_extras:
            if palavra.lower() in self.palavras_funcionais:
                continue

            if palavra.lower() in formatos:
                elementos_identificados.append((palavra, "<formato>"))
            elif palavra.lower() in palavras_titulo:
                elementos_identificados.append((palavra, "<titulo>"))
            elif palavra.isdigit():
                elementos_identificados.append((palavra, "<numero>"))
            else:
                elementos_identificados.append((palavra, "<palavra>"))

        return elementos_identificados
