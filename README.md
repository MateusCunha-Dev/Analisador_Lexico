# Analisador Léxico e Sintático
Disciplina: Compiladores  
Linguagem utilizada: Python  
Autor: Mateus Myller  

## 📚 Fontes Utilizadas

- **Stopwords**: [Gist de alopes](https://gist.github.com/alopes/5358189)
- **Similaridade entre strings**: [`difflib.SequenceMatcher`](https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher)

---

## ⚙️ Funcionalidades

### Analisador Léxico
1. **Validação léxica**: aceita apenas letras latinas (com acentuação), números e símbolos do teclado brasileiro.
2. **Verificação de caracteres inválidos**: qualquer caractere fora do padrão gera erro com posição e tipo.
3. **Stopwords**: ignora palavras irrelevantes da língua portuguesa usando um arquivo `stopwords.txt`.
4. **Similaridade com tolerância a erros**: identifica variações ortográficas com até 20% de diferença.
5. **Tabela de Símbolos**: armazena palavras relevantes e únicas.
6. **Fila de Tokens**: contém os tokens relevantes (palavras válidas, números e pontuações).

### Analisador Sintático
1. **Reconhecimento de estruturas**:
   - 5 tipos de perguntas sobre documentos (formato, tamanho, título, autor, palavra-chave)
   - 5 tipos de respostas correspondentes
2. **Tratamento de incompletudes**:
   - Identifica elementos faltantes em perguntas/respostas
   - Mantém contexto entre interações
3. **Sistema de recuperação**:
   - Tenta completar estruturas incompletas com respostas subsequentes
4. **Inferência de tipos**:
   - Classifica palavras extras em categorias semânticas (formato, título, etc)

---

## 🧠 Estrutura de Arquivos

- `main.py`: ponto de entrada da aplicação
- `analisador_lexico.py`: lógica principal da análise léxica
- `analisador_sintatico.py`: reconhecimento de estruturas gramaticais  
- `stopwords.txt`: lista de palavras ignoradas (como "de", "a", "é")
- `utils.py`: funções auxiliares de validação e comparação

---

## 📝 Gramática Implementada

```bnf
<pergunta> ::= "Qual documento está no" <formato> "?"
             | "Qual tamanho tem" <formato> "?"
             | "Qual documento tem" <titulo> "?"
             | "Quem escreveu o documento" <titulo> "?"
             | "Qual documento contém a palavra" <palavra> "?"

<resposta> ::= "O formato é" <formato> "."
             | "O tamanho é" <numero> "."
             | "O título é" <titulo> "."
             | "Quero tamanho maior que" <numero> "."
             | "O documento contém a palavra" <palavra> "."