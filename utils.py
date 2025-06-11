import re
from difflib import SequenceMatcher

def carregar_stopwords(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return set(line.strip().lower() for line in f if line.strip())

def validar_palavra_portugues(palavra):
    return re.match(r'^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ0-9]+$', palavra)

def validar_token(token):
    if re.match(r'^[0-9]+$', token):
        return True
    if re.match(r'^[\.,;:!?()\-_\+*=@#%&\[\]\{\}\'"$\/]$', token):
        return True
    return validar_palavra_portugues(token)

def similaridade_levenshtein(p1, p2, limite=0.8):
    return SequenceMatcher(None, p1.lower(), p2.lower()).ratio() >= limite
