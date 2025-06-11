import re
from collections import deque
from utils import carregar_stopwords, validar_palavra_portugues, validar_token, similaridade_levenshtein

class AnalisadorLexico:
    def __init__(self):
        self.stopwords = carregar_stopwords('stopwords.txt')
        self.palavras_reservadas = {
            "qual", "quando", "quem", "documento", "tamanho", "formato",
            "título", "autor", "contém", "palavra", "pasta", "criado",
            "está", "no", "com", "é", "o", "a", "os", "as", "na", "do",
            "tem", "que", "estão", "foi", "de"
        }

        self.caracteres_validos = re.compile(
            r'^[a-zA-Z0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s\.,;:!?()\-_\+*=@#%&\[\]\{\}\'"$\/]+$'
        )
        self.regex_tokens = re.compile(r'([a-zA-ZÀ-ÿ0-9]+|[\.,;:!?()\-_\+*=@#%&\[\]\{\}\'"$\/])')
        self.tabela_simbolos = {}  # palavra -> tipo
        self.fila_tokens = deque()
        self.caracteres_invalidos = []

    def encontrar_caracteres_invalidos(self, texto):
        self.caracteres_invalidos = []
        for i, char in enumerate(texto):
            if not self.caracteres_validos.fullmatch(char):
                if ord(char) < 32 or ord(char) > 126:
                    self.caracteres_invalidos.append((i, f'{char} [ASCII: {ord(char)}]'))
                else:
                    self.caracteres_invalidos.append((i, char))

    def processar_texto(self, texto):
        self.encontrar_caracteres_invalidos(texto)
        self.tabela_simbolos.clear()
        self.fila_tokens.clear()

        tokens = self.regex_tokens.findall(texto)
        for token in tokens:
            if not validar_token(token):
                continue

            if re.match(r'^[0-9]+$', token) or re.match(r'^[^\wÀ-ÿ]+$', token):
                self.fila_tokens.append(token.lower())
            elif validar_palavra_portugues(token.lower()):
                token_lower = token.lower()
                if token_lower not in self.stopwords or token_lower in self.palavras_reservadas:
                    palavra_existente = None
                    for palavra in self.tabela_simbolos:
                        if similaridade_levenshtein(palavra, token_lower):
                            palavra_existente = palavra
                            break

                    if palavra_existente:
                        self.fila_tokens.append(palavra_existente)
                    else:
                        tipo_inferido = self.inferir_tipo(token_lower)
                        self.tabela_simbolos[token_lower] = tipo_inferido
                        self.fila_tokens.append(token_lower)

        return True, "Análise concluída"

    def inferir_tipo(self, palavra):
        formatos = {"pdf", "docx", "txt", "html"}
        palavras_titulo = {"documento", "relatório", "técnico", "orçamento", "joão", "silva"}

        if palavra in formatos:
            return "<formato>"
        elif palavra in palavras_titulo:
            return "<titulo>"
        elif palavra.isdigit():
            return "<numero>"
        else:
            return "<palavra>"

    def get_resultados(self):
        return {
            'tabela_simbolos': dict(self.tabela_simbolos),
            'fila_tokens': list(self.fila_tokens),
            'caracteres_invalidos': sorted(self.caracteres_invalidos, key=lambda x: x[0])
        }

