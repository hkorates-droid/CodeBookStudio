from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from pygments import lex
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.token import Token
from pygments.util import ClassNotFound

class PySideHighlighter(QSyntaxHighlighter):
    """Pygments motorunu kullanarak PySide6 QTextEdit alanını anlık olarak renklendirir."""
    
    def __init__(self, parent, theme_manager):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.current_lang = "Python"
        self.current_theme_name = "Thonny"
        self.lexer = get_lexer_by_name("python")

    def set_config(self, lang: str, theme_name: str):
        """Kullanıcının seçtiği dil ve temayı günceller ve ekranı yeniden boyatır."""
        self.current_theme_name = theme_name
        self.current_lang = lang
        
        lexer_map = {
            "Python": "python",
            "Arduino IDE": "arduino",
            "C": "c",
            "C++": "cpp",
            "mikroBasic": "basic"
        }
        
        try:
            self.lexer = get_lexer_by_name(lexer_map.get(lang, "python"))
        except ClassNotFound:
            self.lexer = get_lexer_by_name("python")
            
        self.rehighlight() # Tüm dökümanı yeniden boyamaya zorlar

    def highlightBlock(self, text):
        """Metin kutusundaki her satır değiştikçe PySide6 tarafından otomatik çağrılır."""
        if not text:
            return

        theme = self.theme_manager.get_theme(self.current_theme_name)
        
        # Pygments ile bu satırdaki token'ları ayrıştırıyoruz
        # Not: lexer satır bazlı çalışırken bazen durum koruması isteyebilir ancak
        # bu yöntem performans açısından en kararlı ve hızlı olanıdır.
        tokens = lex(text, self.lexer)
        
        current_position = 0
        for token_type, token_value in tokens:
            token_len = len(token_value)
            
            # newline karakterini renklendirme dışı bırakıyoruz
            if token_value == '\n':
                current_position += token_len
                continue
                
            # Temadan bu token tipine ait rengi buluyoruz
            hex_val = theme["foreground"]
            is_bold = False
            
            if token_type in Token.Keyword:
                hex_val = theme["tokens"].get("Keyword", hex_val)
                is_bold = True
            elif token_type in Token.String or token_type in Token.Literal.String:
                hex_val = theme["tokens"].get("String", hex_val)
            elif token_type in Token.Comment:
                hex_val = theme["tokens"].get("Comment", hex_val)
            elif token_type in Token.Number:
                hex_val = theme["tokens"].get("Number", hex_val)
            elif token_type in Token.Name.Function or token_type in Token.Name.Class:
                hex_val = theme["tokens"].get("Function", hex_val)
                is_bold = True
            elif token_type in Token.Operator:
                hex_val = theme["tokens"].get("Operator", hex_val)
            else:
                hex_val = theme["tokens"].get("Generic", hex_val)

            # PySide biçimlendirme formatını oluştur
            char_format = QTextCharFormat()
            char_format.setForeground(QColor(hex_val))
            if is_bold:
                char_format.setFontWeight(QFont.Bold)
                
            # Belirlenen aralığı boya
            self.setFormat(current_position, token_len, char_format)
            current_position += token_len