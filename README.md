# compilador_criptografia
🔒 CryptoLang IDE
CryptoLang é uma IDE e Compilador de Criptografia desenvolvido com foco educacional. O projeto implementa um pipeline completo de engenharia de compiladores (Lexer, Parser e Interpreter) para processar uma linguagem de domínio específico (DSL) criada para operações de segurança da informação.

O sistema permite encriptar e desencriptar mensagens usando diversos algoritmos clássicos, além de possuir uma funcionalidade de Criptoanálise Automática que utiliza análise estatística e dicionários para identificar e quebrar cifras desconhecidas.

📸 Interface Visual
![Exenplo - Encriptando Texto](imagens_interface/exemplo_encriptando.png)

![Exemplo - Detectando Texto](imagens_interface/exemplo_detectando.png)

✨ Funcionalidades Principais
1. Compilador Dedicado
Diferente de scripts comuns, este projeto processa comandos através de fases reais de compilação:

Análise Léxica: Tokenização do código fonte.

Análise Sintática: Validação gramatical e construção da AST (Árvore de Sintaxe Abstrata).

Interpretação: Execução lógica dos nós da árvore.

2. Algoritmos Suportados
Cifra de César: Deslocamento simples de caracteres.

Cifra de Vigenère: Cifra polialfabética usando chave de texto.

XOR Cipher: Operação bit-a-bit (segurança computacional).

Base64: Codificação de dados binários em texto.

Substituição: Troca de alfabeto completa baseada em chave de 26 caracteres.

3. 🕵️ Detecção Automática (Smart Detect)
O sistema possui um módulo de inteligência que analisa textos cifrados sem saber a chave ou o método.

Realiza ataques de força bruta inteligentes.

Utiliza a biblioteca pyspellchecker para validar palavras em Português e Inglês.

Retorna o algoritmo provável, a chave encontrada e o nível de confiança (%).

4. Interface Gráfica (GUI)
Desenvolvida com CustomTkinter.

Design moderno, responsivo e com modo escuro nativo.

Feedback visual de erros de sintaxe e execução.

🛠️ Instalação e Uso
Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina.

1. Clonar o repositório
Bash

git clone https://github.com/seu-usuario/cryptolang.git
cd cryptolang
2. Instalar dependências
Este projeto utiliza bibliotecas externas para a GUI e para o dicionário inteligente.

Bash

pip install customtkinter pyspellchecker
3. Executar o projeto
Bash

python crypto_ide.py
📘 Documentação da Linguagem
A CryptoLang foi desenhada para ser legível e intuitiva. Abaixo estão os padrões de comando:

Encriptar e Desencriptar
Sintaxe: AÇÃO "TEXTO" USANDO ALGORITMO COM CHAVE VALOR

Exemplos:

Plaintext

# Cifra de César (Chave Numérica)
ENCRIPTAR "Ataque ao amanhecer" USANDO CESAR COM CHAVE 3

# Cifra de Vigenère (Chave Texto)
ENCRIPTAR "Documento Secreto" USANDO VIGENERE COM CHAVE "SENHA"

# Base64 (Chave é ignorada, use 0)
ENCRIPTAR "Dados do Servidor" USANDO BASE64 COM CHAVE 0

# Desencriptar (Processo Inverso)
DESENCRIPTAR "Dwdtxh dr dpdqkhfhu" USANDO CESAR COM CHAVE 3
Detecção Automática
Utilize este comando quando possuir um texto cifrado e desconhecer a origem.

Sintaxe: DETECTAR "TEXTO CIFRADO"

Exemplo:

Plaintext

DETECTAR "Um texto que voce nao sabe como foi gerado"
O console exibirá o algoritmo detectado e a tradução sugerida baseada na pontuação de palavras válidas.

🧠 Arquitetura Técnica
O núcleo do projeto reside nas classes que formam o compilador:

Lexer: Lê a string de entrada caractere por caractere e gera uma lista de Tokens (ex: TT_KEYWORD, TT_STRING).

Parser: Recebe os tokens e verifica se seguem a gramática da linguagem. Se sim, produz um dicionário representando a instrução (AST).

Cryptanalyst: Módulo estatístico que carrega dicionários em memória e pontua frases baseada na frequência de palavras reais.

Interpreter: O "visitante" que percorre a AST e chama as funções matemáticas apropriadas para gerar o resultado final.

📦 Tecnologias Utilizadas
Linguagem: Python 3

GUI: CustomTkinter

Processamento de Linguagem Natural: Pyspellchecker

Core: Bibliotecas padrão (string, base64, threading)