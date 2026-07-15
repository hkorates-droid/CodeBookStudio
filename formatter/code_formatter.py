# ==============================================================================
# CodeBook Studio - RTF Code Formatter Module
# Developed by Halil KORATEŞ & Gemini
# 
# This module generates high-fidelity RTF tables designed to preserve exact 
# line heights, vertical centering, and custom padding inside Microsoft Word 
# and Adobe InDesign, with full Unicode/Turkish character support.
# ==============================================================================

import os
from pygments import lex
from pygments.token import Token
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

class CodeFormatter:
    """
    CodeBook Studio için RTF kod renklendirme ve biçimlendirme sınıfı.
    Developed by Halil KORATEŞ & Gemini.
    """
    def __init__(self, theme_manager):
        self.theme_manager = theme_manager

    def detect_language(self, code):
        """Dosya içeriğine bakarak dil tahmini yapar."""
        code_lower = code.lower()
        if "void setup()" in code_lower or "void loop()" in code_lower:
            return "Arduino IDE"
        elif "#include" in code_lower:
            if "serial.print" in code_lower:
                return "Arduino IDE"
            return "C++"
        elif "def " in code_lower or "import " in code_lower:
            return "Python"
        elif "sub " in code_lower or "dim " in code_lower:
            return "mikroBasic"
        return "Python"

    def _hex_to_rtf_color(self, hex_str):
        """#RRGGBB formatındaki rengi RTF renk tablosu formatına çevirir."""
        hex_str = hex_str.lstrip('#')
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return f"\\red{r}\\green{g}\\blue{b}"

    def _escape_rtf_text(self, text):
        r"""
        Türkçe karakterleri ve RTF özel karakterlerini (\, {, }) 
        InDesign'ın hatasız okuyacağı Unicode biçimine (\uXXXX? formatına) dönüştürür.
        """
        escaped = []
        for char in text:
            if char == '\\':
                escaped.append('\\\\')
            elif char == '{':
                escaped.append('\\{')
            elif char == '}':
                escaped.append('\\}')
            elif char == '\t':
                escaped.append('    ')
            else:
                ord_val = ord(char)
                # ASCII dışı (Türkçe ve diğer özel) karakterleri Unicode RTF formatına çeviriyoruz
                if ord_val > 127:
                    if ord_val > 32767:
                        ord_val -= 65536
                    escaped.append(f"\\u{ord_val}?")
                else:
                    escaped.append(char)
        return "".join(escaped)

    def generate_rtf(self, code, lang, font_name, font_size, theme_name, show_line_numbers=True, use_zebra=True, padding=90, table_width_mm=160):
        """
        InDesign orijinal satır yüksekliğini koruyan, Türkçe karakter destekli,
        hücre içi dikey ortalamayı ve dolguları (padding) hatasız sağlayan RTF tablosu üretir.
        """
        theme = self.theme_manager.get_theme(theme_name)
        
        # 1. Lexer Belirleme
        lexer_map = {
            "Python": "python",
            "Arduino IDE": "arduino",
            "C": "c",
            "C++": "cpp",
            "mikroBasic": "basic"
        }
        try:
            lexer = get_lexer_by_name(lexer_map.get(lang, "python"))
        except ClassNotFound:
            lexer = get_lexer_by_name("python")

        tokens = list(lex(code, lexer))

        # 2. Satır Satır Gruplama
        lines_tokens = []
        current_line = []
        for tok_type, tok_val in tokens:
            parts = tok_val.split('\n')
            for i, part in enumerate(parts):
                if part:
                    current_line.append((tok_type, part))
                if i < len(parts) - 1:
                    lines_tokens.append(current_line)
                    current_line = []
        if current_line:
            lines_tokens.append(current_line)

        # 3. RTF Renk Tablosu Hazırlama
        color_map = {}
        rtf_colors = []

        def register_color(hex_color):
            if hex_color not in color_map:
                color_map[hex_color] = len(rtf_colors) + 1
                rtf_colors.append(self._hex_to_rtf_color(hex_color))
            return color_map[hex_color]

        bg_idx = register_color(theme["background"])
        fg_idx = register_color(theme["foreground"])
        ln_idx = register_color(theme["line_numbers"])
        zebra_even_idx = register_color(theme["zebra_even"])
        zebra_odd_idx = register_color(theme["zebra_odd"])

        token_color_indices = {}
        for key, val in theme["tokens"].items():
            token_color_indices[key] = register_color(val)

        color_table_str = ";".join(rtf_colors) + ";"

        # 4. RTF Başlığı (Header)
        rtf_header = (
            "{\\rtf1\\ansi\\deff0"
            f"{{\\fonttbl{{\\f0\\fnil\\fcharset0 {font_name};}}}}"
            f"{{\\colortbl;{color_table_str}}}"
            f"\\viewkind4\\uc1\\nolang\\lang1024\\f0\\fs{int(font_size * 2)} "
        )

        # 5. Dinamik Sütun Genişlikleri Hesaplama (cm -> Twips Dönüşümü)
        total_width_twips = int(table_width_mm * 56.7)

        total_lines = len(lines_tokens)
        num_digits = len(str(total_lines))
        
        # Satır numarası kolon genişliği
        char_width_twips = font_size * 12
        padding_twips = 300
        line_col_width = int((num_digits * char_width_twips) + padding_twips)
        line_col_width = max(500, line_col_width)
        
        if not show_line_numbers:
            line_col_width = 0

        # Kod kolon genişliği
        code_col_width = total_width_twips - line_col_width

        rtf_body = []
        
        # Word'ün dikey ortalamayı bozmaması için hücre içi padding'i sıfırlıyoruz.
        # Bunun yerine padding değerini paragraf öncesi (\sb) ve sonrası (\sa) komutlarına dağıtıyoruz.
        # Yazı tipinin taban çizgisi (baseline) kaymasını telafi etmek amacıyla üst boşluğu (\sb) biraz daha geniş tutuyoruz.
        p_top = int(padding * 1.1)
        p_bottom = padding

        for line_idx, line_toks in enumerate(lines_tokens, start=1):
            if use_zebra:
                row_bg_idx = zebra_odd_idx if (line_idx % 2 == 0) else zebra_even_idx
            else:
                row_bg_idx = bg_idx

            no_borders = (
                "\\clbrdrt\\brdrnone"
                "\\clbrdrb\\brdrnone"
                "\\clbrdrl\\brdrnone"
                "\\clbrdrr\\brdrnone"
            )

            # Hücre içi padding parametrelerini temizledik (\clpadft0), tüm dikey hizalamayı paragrafa devrediyoruz.
            cell_align = "\\clvertalc\\clpadt0\\clpadft0\\clpadb0\\clpadfb0"
            row_setup = f"\\trowd\\trgaph70\\trleft0"
            
            if show_line_numbers:
                row_setup += f"{no_borders}{cell_align}\\clftsWidth3\\clwWidth{line_col_width}\\clcbpat{row_bg_idx}\\clcbpatraw{row_bg_idx}\\cellx{line_col_width}"
                row_setup += f"{no_borders}{cell_align}\\clftsWidth3\\clwWidth{code_col_width}\\clcbpat{row_bg_idx}\\clcbpatraw{row_bg_idx}\\cellx{total_width_twips}"
            else:
                row_setup += f"{no_borders}{cell_align}\\clftsWidth3\\clwWidth{total_width_twips}\\clcbpat{row_bg_idx}\\clcbpatraw{row_bg_idx}\\cellx{total_width_twips}"

            rtf_body.append(row_setup)

            # --- SÜTUN 1: SATIR NUMARASI İÇERİĞİ ---
            if show_line_numbers:
                # \sb (space before) ve \sa (space after) ile dolguyu paragraf düzeyinde tam simetrik dağıttık
                rtf_body.append(f"\\pard\\intbl\\ql\\f0\\fs{int(font_size * 2)}\\sb{p_top}\\sa{p_bottom}\\sl240\\slmult1\\cf{ln_idx} {line_idx}\\cell")

            # --- SÜTUN 2: KOD İÇERİĞİ ---
            code_parts = []
            for t_type, t_val in line_toks:
                escaped = self._escape_rtf_text(t_val)
                
                color_idx = fg_idx
                is_italic = False
                
                if t_type in Token.Keyword:
                    color_idx = token_color_indices.get("Keyword", fg_idx)
                elif t_type in Token.String or t_type in Token.Literal.String:
                    color_idx = token_color_indices.get("String", fg_idx)
                elif t_type in Token.Comment:
                    color_idx = token_color_indices.get("Comment", fg_idx)
                    is_italic = False 
                elif t_type in Token.Number:
                    color_idx = token_color_indices.get("Number", fg_idx)
                elif t_type in Token.Name.Function or t_type in Token.Name.Class:
                    color_idx = token_color_indices.get("Function", fg_idx)
                elif t_type in Token.Operator:
                    color_idx = token_color_indices.get("Operator", fg_idx)

                if is_italic:
                    code_parts.append(f"\\cf{color_idx}\\i {escaped}\\i0")
                else:
                    code_parts.append(f"\\cf{color_idx} {escaped}")

            line_content = "".join(code_parts) if code_parts else " "
            # Aynı şekilde kod hücresinde de paragraf dolgusu uygulandı
            rtf_body.append(f"\\pard\\intbl\\ql\\f0\\fs{int(font_size * 2)}\\sb{p_top}\\sa{p_bottom}\\sl240\\slmult1 {line_content}\\cell\\row")
            
        rtf_footer = "}"
        
        return rtf_header + "".join(rtf_body) + rtf_footer