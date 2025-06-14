import re
from collections import deque
from difflib import SequenceMatcher


class AnalisadorLexico:
    def __init__(self):
        self.stopwords = self.carregar_stopwords('stopwords.txt')
        self.palavras_reservadas = {
            "qual", "quando", "quantos", "quem", "documento", "tamanho", "formato",
            "título", "autor", "contém", "palavra", "pasta", "criado",
            "está", "no", "com", "é", "o", "a", "os", "as", "na", "do",
            "tem", "que", "estão", "foi", "de"
        }

        self.palavras_corretas = {
            "documento", "tamanho", "formato", "título", "autor",
            "relatório", "técnico", "orçamento", "pdf", "docx",
            "txt", "html", "qual", "quando", "quantos", "quem", "contém",
            "palavra", "pasta", "criado", "dados", "informação"
        }

        self.caracteres_validos = re.compile(
            r'^[a-zA-Z0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s\.,;:!?()\-_\+*=@#%&\[\]\{\}\'"$\/]+$'
        )
        self.regex_tokens = re.compile(r'([a-zA-ZÀ-ÿ0-9]+|[\.,;:!?()\-_\+*=@#%&\[\]\{\}\'"$\/])')
        self.tabela_simbolos = {}
        self.fila_tokens = deque()
        self.caracteres_invalidos = []

    @staticmethod
    def carregar_stopwords(caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return set(line.strip().lower() for line in f if line.strip())
        except FileNotFoundError:
            print(f"Arquivo de stopwords '{caminho}' não encontrado. Usando lista vazia.")
            return set()

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
            if not self.validar_token(token):
                continue

            if re.match(r'^[0-9]+$', token) or re.match(r'^[^\wÀ-ÿ]+$', token):
                self.fila_tokens.append(token.lower())
            elif self.validar_palavra_portugues(token.lower()):
                token_lower = token.lower()
                if token_lower not in self.stopwords or token_lower in self.palavras_reservadas:
                    palavra_corrigida = self.corrigir_palavra(token_lower)

                    palavra_existente = None
                    for palavra in self.tabela_simbolos:
                        if self.similaridade_levenshtein(palavra, palavra_corrigida, 0.9):
                            palavra_existente = palavra
                            break

                    if palavra_existente:
                        self.fila_tokens.append(palavra_existente)
                    else:
                        tipo_inferido = self.inferir_tipo(palavra_corrigida)
                        self.tabela_simbolos[palavra_corrigida] = tipo_inferido
                        self.fila_tokens.append(palavra_corrigida)

        return True, "Análise concluída"

    def corrigir_palavra(self, palavra):
        if palavra in self.palavras_corretas:
            return palavra

        melhor_similaridade = 0
        melhor_palavra = palavra

        for palavra_correta in self.palavras_corretas:
            similaridade = SequenceMatcher(None, palavra, palavra_correta).ratio()
            if similaridade > melhor_similaridade and similaridade >= 0.7:
                melhor_similaridade = similaridade
                melhor_palavra = palavra_correta

        return melhor_palavra

    @staticmethod
    def validar_palavra_portugues(palavra):
        return re.match(r'^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ0-9]+$', palavra)

    @staticmethod
    def validar_token(token):
        if re.match(r'^[0-9]+$', token):
            return True
        if re.match(r'^[\.,;:!?()\-_\+*=@#%&\[\]\{\}\'"$\/]$', token):
            return True
        return AnalisadorLexico.validar_palavra_portugues(token)

    @staticmethod
    def similaridade_levenshtein(p1, p2, limite=0.8):
        return SequenceMatcher(None, p1.lower(), p2.lower()).ratio() >= limite

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
