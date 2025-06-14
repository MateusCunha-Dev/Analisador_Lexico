# Compiladores (2025.01) - Atividade 2A (Atualizado)

**Autor: Mateus Myller**

## Gramática da Linguagem Natural

<interacao> ::= <pergunta> | <resposta>

### Perguntas (5 regras)

<pergunta> ::= <pergunta_formato>
             | <pergunta_tamanho>
             | <pergunta_titulo>
             | <pergunta_autor>
             | <pergunta_palavra_chave>

<pergunta_formato> ::= "Qual documento está no" <formato> "?"
<pergunta_tamanho> ::= "Qual tamanho tem" <formato> "?"
<pergunta_titulo> ::= "Qual documento tem" <titulo> "?"
<pergunta_autor> ::= "Quem escreveu o documento" <titulo> "?"
<pergunta_palavra_chave> ::= "Qual documento contém a palavra" <palavra> "?"

### Respostas (5 regras)

<resposta> ::= <resposta_formato>
             | <resposta_tamanho>
             | <resposta_titulo>
             | <resposta_desejo_tamanho>
             | <resposta_palavra_chave>

<resposta_formato> ::= "O formato é" <formato> "."
<resposta_tamanho> ::= "O tamanho é" <numero> "."
<resposta_titulo> ::= "O título é" <titulo> "."
<resposta_desejo_tamanho> ::= "Quero tamanho maior que" <numero> "."
<resposta_palavra_chave> ::= "O documento contém a palavra" <palavra> "."

### Terminais

<formato> ::= "PDF" | "DOCX" | "TXT" | "HTML"
<titulo> ::= <palavra> | <palavra> <titulo>
<numero> ::= <digito> | <digito> <numero>
<palavra> ::= "documento" | "relatório" | "técnico" | "orçamento" | "dados" | "informação"
<digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

### Exemplo Válido

Pergunta: Qual documento está no PDF?
Resposta: O formato é DOCX.