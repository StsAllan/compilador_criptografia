# 🔒 CryptoLang IDE

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Completed-success)

**CryptoLang** é uma IDE e Compilador de Criptografia desenvolvido com foco educacional. O projeto implementa um pipeline completo de engenharia de compiladores (Lexer, Parser e Interpreter) para processar uma linguagem de domínio específico (DSL) criada para operações de segurança da informação.

O sistema permite encriptar e desencriptar mensagens usando diversos algoritmos clássicos, além de possuir uma funcionalidade de **Criptoanálise Automática** que utiliza análise estatística e dicionários para identificar e quebrar cifras desconhecidas.

---

## 📸 Interface Visual

> *[Insira aqui uma captura de tela da sua aplicação rodando]*
>
> *Interface moderna com tema escuro, editor de código e console de saída integrado.*

---

## ✨ Funcionalidades Principais

### 1. Compilador Dedicado
Diferente de scripts comuns, este projeto processa comandos através de fases reais de compilação:
- **Análise Léxica:** Tokenização do código fonte.
- **Análise Sintática:** Validação gramatical e construção da AST (Árvore de Sintaxe Abstrata).
- **Interpretação:** Execução lógica dos nós da árvore.

### 2. Algoritmos Suportados
- **Cifra de César:** Deslocamento simples de caracteres.
- **Cifra de Vigenère:** Cifra polialfabética usando chave de texto.
- **XOR Cipher:** Operação bit-a-bit (segurança computacional).
- **Base64:** Codificação de dados binários em texto.
- **Substituição:** Troca de alfabeto completa baseada em chave de 26 caracteres.

### 3. 🕵️ Detecção Automática (Smart Detect)
O sistema possui um módulo de inteligência que analisa textos cifrados sem saber a chave ou o método.
- Realiza ataques de força bruta inteligentes.
- Utiliza a biblioteca `pyspellchecker` para validar palavras em **Português** e **Inglês**.
- Retorna o algoritmo provável, a chave encontrada e o nível de confiança (%).

### 4. Interface Gráfica (GUI)
- Desenvolvida com **CustomTkinter**.
- Design moderno, responsivo e com modo escuro nativo.
- Feedback visual de erros de sintaxe e execução.