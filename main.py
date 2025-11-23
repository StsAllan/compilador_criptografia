import customtkinter as ctk
import string
import base64
import threading
import time

# Verificação de Dependência (Dicionário)
try:
    from spellchecker import SpellChecker
    HAS_SPELLCHECKER = True
except ImportError:
    HAS_SPELLCHECKER = False

# ==================================================================
#  1. CORE DO COMPILADOR (Backend)
# ==================================================================

# --- TOKENS ---
TT_KEYWORD = 'PALAVRA_CHAVE'
TT_STRING  = 'TEXTO'
TT_INT     = 'NUMERO'
TT_EOF     = 'FIM_ARQUIVO'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    def __repr__(self): return f'{self.type}:{self.value}'

# --- LEXER (Leitor) ---
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in ' \t\n\r':
                self.advance()
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
            elif self.current_char.isalpha() or self.current_char in '=+/': 
                tokens.append(self.make_identifier())
            else:
                return [], f"Erro Léxico: O caractere '{self.current_char}' é inválido fora de aspas."
        tokens.append(Token(TT_EOF))
        return tokens, None

    def make_string(self):
        string_content = ''
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            string_content += self.current_char
            self.advance()
        self.advance()
        return Token(TT_STRING, string_content)

    def make_number(self):
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return Token(TT_INT, int(num_str))

    def make_identifier(self):
        id_str = ''
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit() or self.current_char in '=+/'):
            id_str += self.current_char
            self.advance()
        return Token(TT_KEYWORD, id_str.upper())

# --- PARSER (Gramática) ---
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok = None
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        if self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'DETECTAR':
            return self.parse_detection()
        else:
            return self.parse_action()

    def parse_detection(self):
        self.advance()
        if self.current_tok.type != TT_STRING:
            return None, "Erro Sintático: Esperado texto entre aspas após DETECTAR."
        text = self.current_tok.value
        self.advance()
        return {'action': 'DETECTAR', 'text': text}, None

    def parse_action(self):
        if self.current_tok.type != TT_KEYWORD or self.current_tok.value not in ['ENCRIPTAR', 'DESENCRIPTAR']:
            return None, "Erro: Comando desconhecido. Use ENCRIPTAR, DESENCRIPTAR ou DETECTAR."
        action = self.current_tok.value
        self.advance()

        if self.current_tok.type != TT_STRING: return None, "Erro: Esperado texto entre aspas."
        text = self.current_tok.value
        self.advance()

        if self.current_tok.value != 'USANDO': return None, "Erro: Esperado 'USANDO'."
        self.advance()

        if self.current_tok.type != TT_KEYWORD: return None, "Erro: Esperado algoritmo."
        method = self.current_tok.value
        self.advance()

        if self.current_tok.value != 'COM': return None, "Erro: Esperado 'COM'."
        self.advance()

        if self.current_tok.value != 'CHAVE': return None, "Erro: Esperado 'CHAVE'."
        self.advance()

        if self.current_tok.type not in [TT_INT, TT_STRING]: return None, "Erro: Chave inválida (Use numero ou texto entre aspas)."
        key = self.current_tok.value
        self.advance()

        return {'action': action, 'text': text, 'method': method, 'key': key}, None

# --- CRIPTOANALISTA (Inteligência) ---
class Cryptanalyst:
    def __init__(self):
        self.loaded = False
        self.spell_pt = None
        self.spell_en = None
        self.status_msg = "Dicionários não carregados."

    def load_dicts(self):
        if not HAS_SPELLCHECKER: 
            self.status_msg = "Biblioteca 'pyspellchecker' ausente."
            return
        
        # Carrega em background
        try:
            self.spell_pt = SpellChecker(language='pt')
            self.spell_en = SpellChecker(language='en')
            self.loaded = True
            self.status_msg = "Dicionários PT/EN Prontos."
            print("Dicionários carregados com sucesso!")
        except Exception as e:
            self.status_msg = f"Erro ao carregar dicionários: {e}"

    def score(self, text):
        if not self.loaded: return 0
        words = text.split()
        if len(words) == 0: return 0
        valid = 0
        for w in words:
            clean = ''.join(filter(str.isalpha, w)).lower()
            if not clean: continue
            if (clean in self.spell_pt) or (clean in self.spell_en):
                valid += 1
        return (valid / len(words)) * 100

    def detect(self, text):
        if not HAS_SPELLCHECKER: return "Erro: Instale 'pyspellchecker' para usar detecção."
        if not self.loaded: return "Erro: Dicionários ainda carregando... Tente em 5 segundos."
        
        candidates = []
        
        # 1. Base64
        try:
            b64 = base64.b64decode(text).decode('utf-8')
            if all(c in string.printable or c.isspace() for c in b64):
                pts = self.score(b64)
                if pts > 20: candidates.append((pts+10, "BASE64", 0, b64))
        except: pass

        # 2. Cesar
        for k in range(1, 26):
            dec = ""
            for c in text:
                if c.isalpha():
                    start = 65 if c.isupper() else 97
                    dec += chr((ord(c) - start - k) % 26 + start)
                else: dec += c
            pts = self.score(dec)
            if pts > 30: candidates.append((pts, "CESAR", k, dec))

        if not candidates: return "Resultado: Não foi possível identificar o padrão automaticamente."
        
        candidates.sort(key=lambda x: x[0], reverse=True)
        best = candidates[0]
        return f"🔎 DETECTADO: {best[1]}\n🔑 CHAVE: {best[2]}\n📊 CONFIANÇA: {best[0]:.1f}%\n----------------------\n📜 TRADUÇÃO: {best[3]}"

# --- INTERPRETER (Executor) ---
class Interpreter:
    def __init__(self, analyst):
        self.analyst = analyst

    def visit(self, node):
        if node['action'] == 'DETECTAR': return self.analyst.detect(node['text'])
        
        m, t, k, a = node['method'], node['text'], node['key'], node['action']

        try:
            if m == 'CESAR': return self.caesar(t, k, a)
            elif m == 'VIGENERE': return self.vigenere(t, k, a)
            elif m == 'XOR': return self.xor(t, k, a)
            elif m == 'BASE64': return self.b64(t, a)
            elif m == 'SUBSTITUICAO': return self.subst(t, k, a)
            else: return f"Erro: Método '{m}' desconhecido."
        except Exception as e:
            return f"Erro de Execução: {str(e)}"

    def caesar(self, t, k, a):
        if not isinstance(k, int): return "Erro: Chave Cesar deve ser número."
        res = ""
        if a == 'DESENCRIPTAR': k = -k
        for c in t:
            if c.isalpha():
                s = 65 if c.isupper() else 97
                res += chr((ord(c)-s+k)%26+s)
            else: res += c
        return res

    def vigenere(self, t, k, a):
        if not isinstance(k, str): return "Erro: Chave Vigenere deve ser texto."
        res = []; idx = 0; k = k.upper()
        for c in t:
            if c.isalpha():
                sh = ord(k[idx%len(k)])-65
                if a == 'DESENCRIPTAR': sh = -sh
                s = 65 if c.isupper() else 97
                res.append(chr((ord(c)-s+sh)%26+s))
                idx += 1
            else: res.append(c)
        return "".join(res)

    def xor(self, t, k, a):
        if not isinstance(k, int): return "Erro: Chave XOR deve ser número."
        return "".join([chr(ord(c)^k) for c in t])

    def b64(self, t, a):
        try:
            if a == 'ENCRIPTAR': return base64.b64encode(t.encode()).decode()
            else: return base64.b64decode(t.encode()).decode()
        except: return "Erro: Texto não é Base64 válido."

    def subst(self, t, k, a):
        if len(k)!=26: return "Erro: Chave Substituição deve ter 26 letras."
        abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        k = k.upper()
        if a == 'ENCRIPTAR': tbl = str.maketrans(abc+abc.lower(), k+k.lower())
        else: tbl = str.maketrans(k+k.lower(), abc+abc.lower())
        return t.translate(tbl)


# ==================================================================
#  2. INTERFACE GRÁFICA (Frontend)
# ==================================================================

class CryptoIDE(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da Janela
        self.title("CryptoLang IDE - Compilador de Criptografia")
        self.geometry("950x650")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        # Inicializa Backend
        self.analyst = Cryptanalyst()
        self.interpreter = Interpreter(self.analyst)
        
        # Carrega dicionário em segundo plano
        threading.Thread(target=self.analyst.load_dicts, daemon=True).start()

        self.create_widgets()

    def create_widgets(self):
        # Grid Layout: Sidebar (0) e Main (1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (Ajuda) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="CryptoLang", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))

        help_txt = (
            "📚 GUIA RÁPIDO\n\n"
            "🔹 ENCRIPTAR\n"
            'ENCRIPTAR "Texto"\n'
            "USANDO [METODO]\n"
            "COM CHAVE [VALOR]\n\n"
            "🔹 DESENCRIPTAR\n"
            "(Mesma lógica)\n\n"
            "🔹 DETECTAR (Auto)\n"
            'DETECTAR "Texto cifrado"\n\n'
            "🔸 MÉTODOS & CHAVES\n"
            "• CESAR (Num ex: 3)\n"
            "• VIGENERE (Txt ex: \"ABC\")\n"
            "• BASE64 (Use 0)\n"
            "• XOR (Num ex: 123)\n"
            "• SUBSTITUICAO (Alfabeto)"
        )
        self.help_lbl = ctk.CTkLabel(self.sidebar, text=help_txt, justify="left", anchor="w", text_color="gray80")
        self.help_lbl.grid(row=1, column=0, padx=15, pady=10)

        # --- ÁREA PRINCIPAL ---
        self.main = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.main.grid_rowconfigure(1, weight=1) # Editor cresce
        self.main.grid_rowconfigure(3, weight=1) # Console cresce
        self.main.grid_columnconfigure(0, weight=1)

        # Editor
        ctk.CTkLabel(self.main, text="📝 EDITOR DE CÓDIGO", anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.editor = ctk.CTkTextbox(self.main, font=("Consolas", 14), height=150, border_width=2, border_color="#444")
        self.editor.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.editor.insert("0.0", 'ENCRIPTAR "Ola Mundo" USANDO CESAR COM CHAVE 3')

        # Botão
        self.btn = ctk.CTkButton(self.main, text="▶ EXECUTAR CÓDIGO", height=45, command=self.run, font=("Arial", 13, "bold"))
        self.btn.grid(row=2, column=0, sticky="ew", pady=10)

        # Console
        ctk.CTkLabel(self.main, text="💻 CONSOLE DE SAÍDA", anchor="w", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="nw")
        self.console = ctk.CTkTextbox(self.main, font=("Courier New", 13), fg_color="#111", text_color="#0f0", state="disabled")
        self.console.grid(row=4, column=0, sticky="nsew")

    def log(self, msg, error=False):
        self.console.configure(state="normal")
        self.console.delete("0.0", "end") # Limpa anterior
        prefix = "❌ ERRO: " if error else "✅ SUCESSO:\n"
        color = "#ff5555" if error else "#55ff55"
        self.console.configure(text_color=color)
        self.console.insert("0.0", f"{prefix}{msg}")
        self.console.configure(state="disabled")

    def run(self):
        code = self.editor.get("0.0", "end").strip()
        if not code: return

        try:
            # 1. Lexer
            lexer = Lexer(code)
            tokens, err = lexer.make_tokens()
            if err: return self.log(err, True)

            # 2. Parser
            parser = Parser(tokens)
            ast, err = parser.parse()
            if err: return self.log(err, True)

            # 3. Interpreter
            res = self.interpreter.visit(ast)
            self.log(res, error=False)

        except Exception as e:
            self.log(f"Falha crítica no sistema: {e}", True)

if __name__ == "__main__":
    app = CryptoIDE()
    app.mainloop()