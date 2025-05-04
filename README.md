# Analisador Léxico
Disciplina: Compiladores

Linguagem utilizada: Python

Autor: Mateus Myller
## 📚 Fontes Utilizadas

- **Stopwords**: [Gist de alopes](https://gist.github.com/alopes/5358189)
- **Similaridade entre strings**: [`difflib.SequenceMatcher`](https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher)

---

## ⚙️ Funcionalidades

Este analisador léxico realiza as seguintes etapas:

1. **Validação léxica**: aceita apenas letras latinas (com acentuação), números e símbolos do teclado brasileiro.
2. **Verificação de caracteres inválidos**: qualquer caractere fora do padrão gera erro com posição e tipo.
3. **Stopwords**: ignora palavras irrelevantes da língua portuguesa usando um arquivo `stopwords.txt`.
4. **Similaridade com tolerância a erros**: identifica variações ortográficas com até 20% de diferença.
5. **Tabela de Símbolos**: armazena palavras relevantes e únicas.
6. **Fila de Tokens**: contém os tokens relevantes (palavras válidas, números e pontuações).

---

## 🧠 Estrutura de Arquivos

- `main.py`: ponto de entrada da aplicação.
- `utils.py`: funções auxiliares de validação e comparação.
- `analisador_lexico.py`: lógica principal da análise léxica.
- `stopwords.txt`: lista de palavras ignoradas (como “de”, “a”, “é”, etc).

---

## 💻 Exemplo de Entrada

```txt
📚 Hoje eu visitei a biblioteca para estudar programação, estudei programação por duas horas, 2 horas.

Saíde esperada:
Tabela de Símbolos: Hoje, visitei, biblioteca, estudar, programação, estudei, duas, horas

Fila de Tokens: Hoje -> visitei -> biblioteca -> estudar -> programação -> , -> estudei -> programação -> duas -> horas -> , -> 2 -> horas -> .

Caracteres inválidos encontrados:
Posição 0: 📚 [ASCII: 128218]