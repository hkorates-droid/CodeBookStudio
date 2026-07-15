import sys
import os
import json  # Yapılandırma ayarlarını kaydetmek için ekledik
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTextEdit, QComboBox, QSpinBox, 
                             QPushButton, QCheckBox, QGroupBox, QApplication,
                             QFileDialog, QPlainTextEdit)
from PySide6.QtCore import Qt, QTimer, QRect, QSize
from PySide6.QtGui import QFont, QColor, QPalette, QSyntaxHighlighter, QTextCharFormat, QPainter

from formatter.code_formatter import CodeFormatter
from core.theme_manager import ThemeManager

try:
    from core.clipboard import WindowsClipboard
except ImportError:
    try:
        from utils.clipboard import WindowsClipboard
    except ImportError:
        from clipboard import WindowsClipboard


# =============================================================================
# SATIR NUMARASI ALANI YARDIMCI BİLEŞENİ
# =============================================================================
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


# =============================================================================
# GELİŞMİŞ VE DİNAMİK KOD EDİTÖRÜ (SOL PANEL İÇİN)
# =============================================================================
class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)

        # Görünüm Bayrakları (Dinamik olarak değiştirilebilir)
        self.show_line_numbers = True
        self.use_zebra = True

        # Varsayılan Tema Renkleri
        self.theme_bg = QColor("#FFFFFF")
        self.theme_fg = QColor("#000000")
        self.theme_ln = QColor("#A0A0A0")
        self.theme_zebra_even = QColor("#FFFFFF")
        self.theme_zebra_odd = QColor("#F9F9F9")

        # Sinyal Bağlantıları
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        # Viewport arka planının tamamen ezilebilmesi için saydamlık ayarı
        self.viewport().setAttribute(Qt.WA_OpaquePaintEvent, False)

        self.update_line_number_area_width(0)

    def update_theme_colors(self, bg, fg, ln, zebra_even, zebra_odd):
        """Tema değişiminde renkleri günceller."""
        self.theme_bg = QColor(bg)
        self.theme_fg = QColor(fg)
        self.theme_ln = QColor(ln)
        self.theme_zebra_even = QColor(zebra_even)
        self.theme_zebra_odd = QColor(zebra_odd)
        
        # Editör temel palet arka planını saydam yapıyoruz ki paintEvent altından zebra renkleri görünebilsin
        palette = self.palette()
        palette.setColor(QPalette.Base, Qt.transparent)
        palette.setColor(QPalette.Text, self.theme_fg)
        self.setPalette(palette)
        
        self.viewport().update()
        self.line_number_area.update()

    def line_number_area_width(self):
        if not self.show_line_numbers:
            return 0
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num /= 10
            digits += 1
        space = 15 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def paintEvent(self, event):
        # Arka planı ve zebra satırlarını elle çiziyoruz
        painter = QPainter(self.viewport())
        
        if self.use_zebra:
            # Varsayılan arka planı doldur
            painter.fillRect(event.rect(), self.theme_bg)
            
            block = self.firstVisibleBlock()
            block_number = block.blockNumber()
            offset = self.contentOffset()
            top = int(self.blockBoundingGeometry(block).translated(offset).top())
            bottom = top + int(self.blockBoundingRect(block).height())
            
            while block.isValid() and top <= event.rect().bottom():
                if block.isVisible() and bottom >= event.rect().top():
                    rect = QRect(0, top, self.viewport().width(), bottom - top)
                    # Alternatif satır renklendirmesi (Zebra)
                    color = self.theme_zebra_odd if (block_number + 1) % 2 == 0 else self.theme_zebra_even
                    painter.fillRect(rect, color)
                
                block = block.next()
                top = bottom
                bottom = top + int(self.blockBoundingRect(block).height())
                block_number += 1
        else:
            painter.fillRect(event.rect(), self.theme_bg)
            
        painter.end()
        super().paintEvent(event)

    def line_number_area_paint_event(self, event):
        if not self.show_line_numbers:
            return
            
        painter = QPainter(self.line_number_area)
        # Satır numarası alanının arka planını zebra boyamadan ayırmak için hafif koyu tonda boyuyoruz
        painter.fillRect(event.rect(), self.theme_bg.darker(103))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = int(self.blockBoundingGeometry(block).translated(offset).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        painter.setPen(self.theme_ln)
        font = self.font()
        painter.setFont(font)

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, top, self.line_number_area.width() - 8, 
                                 self.blockBoundingRect(block).height(),
                                 Qt.AlignRight | Qt.AlignVCenter, number)
            
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1
            
        painter.end()


# =============================================================================
# CANLI RENKLENDİRME İÇİN HIGHLIGHTER (SOL PANEL İÇİN)
# =============================================================================
class PygmentsHighlighter(QSyntaxHighlighter):
    def __init__(self, parent, theme_manager):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.current_theme_name = "Maarif Pastel"
        self.rules = []
        self.update_rules()

    def set_theme(self, theme_name):
        self.current_theme_name = theme_name
        self.update_rules()
        self.rehighlight()

    def update_rules(self):
        self.rules.clear()
        theme = self.theme_manager.get_theme(self.current_theme_name)
        tokens = theme.get("tokens", {})

        def make_format(color_hex, bold=False, italic=False):
            fmt = QTextCharFormat()
            fmt.copyTo = None # redundant, just using simple creation
            fmt.setForeground(QColor(color_hex))
            if bold:
                fmt.setFontWeight(QFont.Bold)
            if italic:
                fmt.setFontItalic(False) # Ana form üzerindeki italik yazıları kapat
            return fmt

        kw_format = make_format(tokens.get("Keyword", "#0000FF"), bold=True)
        str_format = make_format(tokens.get("String", "#A31515"))
        com_format = make_format(tokens.get("Comment", "#008000"), italic=True)
        num_format = make_format(tokens.get("Number", "#098658"))
        fn_format = make_format(tokens.get("Function", "#795E28"))

        keywords = [
            r'\bclass\b', r'\bdef\b', r'\bif\b', r'\belse\b', r'\belif\b', r'\bfor\b',
            r'\bwhile\b', r'\breturn\b', r'\bimport\b', r'\bfrom\b', r'\btry\b', r'\bexcept\b',
            r'\bint\b', r'\bfloat\b', r'\bdouble\b', r'\bchar\b', r'\bvoid\b', r'\bconst\b',
            r'\bunsigned\b', r'\blong\b', r'\bshort\b', r'\bstruct\b', r'\bsetup\b', r'\bloop\b',
            r'\b#include\b', r'\b#define\b', r'\b#ifdef\b', r'\b#ifndef\b', r'\b#endif\b'
        ]

        for kw in keywords:
            self.rules.append((kw, kw_format))

        self.rules.append((r'\b[0-9]+\b', num_format))
        self.rules.append((r'\b0x[0-9a-fA-F]+\b', num_format))
        self.rules.append((r'"[^"\\]*(\\.[^"\\]*)*"', str_format))
        self.rules.append((r"'[^'\\]*(\\.[^'\\]*)*'", str_format))
        self.rules.append((r'\b[A-Za-z0-9_]+(?=\()', fn_format))
        self.rules.append((r'//[^\n]*', com_format))
        self.rules.append((r'#[^\n]*', com_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            import re
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)


# =============================================================================
# ANA PENCERE (MAIN WINDOW)
# =============================================================================
class MainWindow(QMainWindow):
    def __init__(self, theme_manager=None):
        super().__init__()
         
        if theme_manager is None:
            self.theme_manager = ThemeManager()
        else:
            self.theme_manager = theme_manager
            
        self.formatter = CodeFormatter(self.theme_manager)
        self.clipboard_helper = WindowsClipboard()
        
        self.init_ui()
        self.highlighter = PygmentsHighlighter(self.code_input.document(), self.theme_manager)
        
        # Önce varsayılan tema ve ayarları yükle/uygula
        self.apply_editor_theme()
        
        # Eğer varsa önceki kayıtlı config ayarlarını yükle
        self.load_config()

        # İlk açılışta başlığı "Yeni Dosya" ve geliştirici isimlerimizle kuruyoruz[cite: 5]
        self.update_window_title(None)
        
    def init_ui(self):
        # Varsayılan başlık update_window_title ile ezileceği için geçici atanabilir[cite: 5]
        self.setWindowTitle("CodeBook Studio")
        self.resize(1100, 700)

        # Menü[cite: 5]
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Dosya")
        open_action = file_menu.addAction("Dosya Aç...")
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        exit_action = file_menu.addAction("Çıkış")
        exit_action.triggered.connect(self.close)

        # Ana Widget ve Düzen[cite: 5]
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Sol Panel[cite: 5]
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        header_layout = QHBoxLayout()
        self.lbl_code = QLabel("Biçimlendirilecek Kod:")
        self.lbl_code.setStyleSheet("font-weight: bold;")
        
        self.btn_open_file = QPushButton("Dosya Seç...")
        self.btn_open_file.setFixedWidth(100)
        self.btn_open_file.setStyleSheet("height: 22px; font-size: 11px;")
        self.btn_open_file.clicked.connect(self.open_file)
        
        header_layout.addWidget(self.lbl_code)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_open_file)
        
        # Yeni Gelişmiş Dinamik Editör Bileşeni[cite: 5]
        self.code_input = CodeEditor()
        self.code_input.setPlaceholderText("Kodunuzu buraya yapıştırın veya yukarıdan dosya seçin...")
        
        left_layout.addLayout(header_layout)
        left_layout.addWidget(self.code_input)
        main_layout.addWidget(left_panel, stretch=3)

        # Sağ Panel (Ayarlar)[cite: 5]
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 0, 0, 0)

        settings_group = QGroupBox("Biçimlendirme Ayarları")
        settings_layout = QVBoxLayout(settings_group)
        settings_layout.setSpacing(8)

        # 1. Dil Seçimi[cite: 5]
        settings_layout.addWidget(QLabel("Yazılım Dili:"))
        self.combo_lang = QComboBox()
        self.combo_lang.addItems(["Otomatik Algıla", "Python", "Arduino IDE", "C", "C++", "mikroBasic"])
        self.combo_lang.currentIndexChanged.connect(self.save_config)  # Değişiklikte kaydet
        settings_layout.addWidget(self.combo_lang)

        # 2. Font Seçimi[cite: 5]
        settings_layout.addWidget(QLabel("Yazı Tipi (Font):"))
        self.combo_font = QComboBox()
        self.combo_font.addItems([
            "Consolas", "Courier New", "Arial", "Calibri", "Segoe UI", 
            "Fira Code", "Source Code Pro", "JetBrains Mono", "Lucida Console"
        ])
        self.combo_font.currentTextChanged.connect(self.apply_editor_theme)
        self.combo_font.currentTextChanged.connect(self.save_config)  # Değişiklikte kaydet
        settings_layout.addWidget(self.combo_font)

        # 3. Yazı Boyutu ve Satır Aralığı[cite: 5]
        size_layout = QHBoxLayout()
        
        v_size = QVBoxLayout()
        v_size.addWidget(QLabel("Yazı Punto (pt):"))
        self.spin_font_size = QSpinBox()
        self.spin_font_size.setRange(6, 48)
        self.spin_font_size.setValue(10)
        self.spin_font_size.valueChanged.connect(self.apply_editor_theme)
        self.spin_font_size.valueChanged.connect(self.save_config)  # Değişiklikte kaydet
        v_size.addWidget(self.spin_font_size)
        
        v_pad = QVBoxLayout()
        v_pad.addWidget(QLabel("Satır Aralığı (Padding):"))
        self.spin_padding = QSpinBox()
        self.spin_padding.setRange(10, 500)
        self.spin_padding.setValue(90)
        self.spin_padding.setToolTip("Satırlar arası dikey boşluk (Twips cinsinden)")
        self.spin_padding.valueChanged.connect(self.save_config)  # Değişiklikte kaydet
        v_pad.addWidget(self.spin_padding)
        
        size_layout.addLayout(v_size)
        size_layout.addLayout(v_pad)
        settings_layout.addLayout(size_layout)

        # Tablo Genişliği[cite: 5]
        settings_layout.addWidget(QLabel("Tablo Genişliği (mm):"))
        self.spin_table_width = QSpinBox()
        self.spin_table_width.setRange(50, 300)
        self.spin_table_width.setValue(160)
        self.spin_table_width.setToolTip("Word/InDesign'daki tablonun sütun genişliğini belirler.")
        self.spin_table_width.valueChanged.connect(self.save_config)  # Değişiklikte kaydet
        settings_layout.addWidget(self.spin_table_width)

        # 4. Tema Seçimi[cite: 5]
        settings_layout.addWidget(QLabel("Renk Teması:"))
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(self.theme_manager.get_theme_names())
        self.combo_theme.currentTextChanged.connect(self.apply_editor_theme)
        self.combo_theme.currentTextChanged.connect(self.save_config)  # Değişiklikte kaydet
        settings_layout.addWidget(self.combo_theme)

        # 5. Seçenek Kutuları (Zebra ve Satır No)[cite: 5]
        options_layout = QVBoxLayout()
        self.chk_line_numbers = QCheckBox("Satır Numaralarını Göster")
        self.chk_line_numbers.setChecked(True)
        self.chk_line_numbers.stateChanged.connect(self.update_preview_options)
        self.chk_line_numbers.stateChanged.connect(self.save_config)  # Değişiklikte kaydet
        options_layout.addWidget(self.chk_line_numbers)

        self.chk_zebra = QCheckBox("Zebra Satır Boyama (Alternatif)")
        self.chk_zebra.setChecked(True)
        self.chk_zebra.stateChanged.connect(self.update_preview_options)
        self.chk_zebra.stateChanged.connect(self.save_config)  # Değişiklikte kaydet
        options_layout.addWidget(self.chk_zebra)
        
        settings_layout.addLayout(options_layout)
        right_layout.addWidget(settings_group)

        # İşlem Butonları[cite: 5]
        self.btn_copy = QPushButton("RTF Tablo Olarak Kopyala")
        self.btn_copy.setStyleSheet("background-color: #2ca02c; color: white; font-weight: bold; height: 40px;")
        self.btn_copy.clicked.connect(self.on_copy_clicked)
        right_layout.addWidget(self.btn_copy)

        self.btn_clear = QPushButton("Temizle")
        self.btn_clear.clicked.connect(self.clear_editor)
        right_layout.addWidget(self.btn_clear)

        right_layout.addStretch()
        main_layout.addWidget(right_panel, stretch=1)

    # =============================================================================
    # CONFIG (YAPILANDIRMA) KAYDETME VE OKUMA METOTLARI
    # =============================================================================
    def get_config_path(self):
        """
        Uygulamanın çalıştığı dizinde 'config.json' dosyası yolunu döner.
        PyInstaller (.exe) uyumludur; config her zaman exe'nin yanına kaydedilir.
        """
        if getattr(sys, 'frozen', False):
            # Eğer uygulama derlenmiş bir .exe ise, exe'nin bulunduğu gerçek klasör
            base_dir = os.path.dirname(sys.executable)
        else:
            # Standart Python scripti olarak çalışıyorsa, scriptin bulunduğu klasör
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
        return os.path.join(base_dir, "config.json")

    def save_config(self):
        """Arayüzdeki güncel ayarları JSON dosyasına kaydeder."""
        config_data = {
            "language": self.combo_lang.currentText(),
            "font_family": self.combo_font.currentText(),
            "font_size": self.spin_font_size.value(),
            "padding": self.spin_padding.value(),
            "table_width": self.spin_table_width.value(),
            "theme": self.combo_theme.currentText(),
            "show_line_numbers": self.chk_line_numbers.isChecked(),
            "use_zebra": self.chk_zebra.isChecked()
        }
        try:
            with open(self.get_config_path(), "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Config kaydedilirken hata oluştu: {e}")

    def load_config(self):
        """Uygulama açılırken config.json dosyasını okur ve arayüze yükler."""
        config_path = self.get_config_path()
        if not os.path.exists(config_path):
            return  # Dosya henüz yoksa varsayılan ayarlarla başla

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)

            # Sinyalleri geçici olarak engelleyelim ki yükleme sırasında 
            # save_config fonksiyonu tekrar tekrar tetiklenmesin.
            self.blockSignals(True)

            if "language" in config_data:
                self.combo_lang.setCurrentText(config_data["language"])
            if "font_family" in config_data:
                self.combo_font.setCurrentText(config_data["font_family"])
            if "font_size" in config_data:
                self.spin_font_size.setValue(config_data["font_size"])
            if "padding" in config_data:
                self.spin_padding.setValue(config_data["padding"])
            if "table_width" in config_data:
                self.spin_table_width.setValue(config_data["table_width"])
            if "theme" in config_data:
                self.combo_theme.setCurrentText(config_data["theme"])
            if "show_line_numbers" in config_data:
                self.chk_line_numbers.setChecked(config_data["show_line_numbers"])
            if "use_zebra" in config_data:
                self.chk_zebra.setChecked(config_data["use_zebra"])

            self.blockSignals(False)

            # Temayı ve görünüm opsiyonlarını editöre anında yansıt
            self.apply_editor_theme()
            self.update_preview_options()

        except Exception as e:
            print(f"Config yüklenirken hata oluştu: {e}")
            self.blockSignals(False)

    # =============================================================================
    # MEVCUT ARAYÜZ FONKSİYONLARI
    # =============================================================================
    def update_window_title(self, file_path=None):
        """
        Pencere başlığını ortak geliştirici isimlerimiz, aktif dosya adı ve dosya yoluyla günceller.
        """
        base_title = "CodeBook Studio - Developed by Halil KORATEŞ & Gemini"
        
        if file_path:
            normalized_path = os.path.abspath(file_path)
            file_name = os.path.basename(normalized_path)
            self.setWindowTitle(f"{base_title} - [{file_name}] ({normalized_path})")
        else:
            self.setWindowTitle(f"{base_title} - [Yeni Dosya]")

    def clear_editor(self):
        """Editörü temizler ve pencere başlığını 'Yeni Dosya' olarak sıfırlar."""
        self.code_input.clear()
        self.update_window_title(None)

    def update_preview_options(self):
        """Checkbox'lar tıklandığında editörün anlık görünümünü günceller."""
        self.code_input.show_line_numbers = self.chk_line_numbers.isChecked()
        self.code_input.use_zebra = self.chk_zebra.isChecked()
        
        # Kenar boşluklarını ve numaralandırma alanını yeniden hesaplatıp çizdiriyoruz
        self.code_input.update_line_number_area_width(0)
        self.code_input.viewport().update()
        self.code_input.line_number_area.update()

    def apply_editor_theme(self):
        theme_name = self.combo_theme.currentText()
        theme = self.theme_manager.get_theme(theme_name)
        
        bg_hex = theme.get("background", "#FFFFFF")
        fg_hex = theme.get("foreground", "#000000")
        ln_hex = theme.get("line_numbers", "#A0A0A0")
        zebra_even_hex = theme.get("zebra_even", bg_hex)
        zebra_odd_hex = theme.get("zebra_odd", bg_hex)
        
        # Gelişmiş editör bileşenine tema renklerini pasla
        self.code_input.update_theme_colors(
            bg=bg_hex,
            fg=fg_hex,
            ln=ln_hex,
            zebra_even=zebra_even_hex,
            zebra_odd=zebra_odd_hex
        )
        
        # Font güncellemesi
        font_name = self.combo_font.currentText()
        font_size = self.spin_font_size.value()
        self.code_input.setFont(QFont(font_name, font_size))

        if hasattr(self, 'highlighter'):
            self.highlighter.set_theme(theme_name)

    def open_file(self):
        file_filter = "Kod Dosyaları (*.py *.ino *.c *.cpp *.h *.txt);;Tüm Dosyalar (*.*)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Kod Dosyası Seç", "", file_filter)
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.code_input.setPlainText(content)
                
                # Başlığı açılan dosyaya ve tam yoluna göre güncelle
                self.update_window_title(file_path)
                
                ext = os.path.splitext(file_path)[1].lower()
                if ext == ".py":
                    self.combo_lang.setCurrentText("Python")
                elif ext in [".ino", ".pde"]:
                    self.combo_lang.setCurrentText("Arduino IDE")
                elif ext in [".c", ".h"]:
                    self.combo_lang.setCurrentText("C")
                elif ext in [".cpp", ".hpp"]:
                    self.combo_lang.setCurrentText("C++")
                else:
                    self.combo_lang.setCurrentText("Otomatik Algıla")
                    
            except Exception as e:
                self.code_input.setPlainText(f"Dosya okunurken bir hata oluştu:\n{str(e)}")

    def on_copy_clicked(self):
        code = self.code_input.toPlainText()
        if not code.strip():
            return

        selected_lang = self.combo_lang.currentText()
        if selected_lang == "Otomatik Algıla":
            selected_lang = self.formatter.detect_language(code)

        font_name = self.combo_font.currentText()
        font_size = self.spin_font_size.value()
        padding = self.spin_padding.value()
        table_width_mm = self.spin_table_width.value()
        theme_name = self.combo_theme.currentText()
        show_lines = self.chk_line_numbers.isChecked()
        use_zebra = self.chk_zebra.isChecked()

        rtf_data = self.formatter.generate_rtf(
            code=code,
            lang=selected_lang,
            font_name=font_name,
            font_size=font_size,
            theme_name=theme_name,
            show_line_numbers=show_lines,
            use_zebra=use_zebra,
            padding=padding,
            table_width_mm=table_width_mm
        )

        success = self.clipboard_helper.copy(code, rtf_data)
        
        if success:
            self.btn_copy.setText("✓ Kopyalandı!")
        else:
            self.btn_copy.setText("⚠️ Pano Hatası!")
            
        QTimer.singleShot(1500, lambda: self.btn_copy.setText("RTF Tablo Olarak Kopyala"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.argv[0] = "CodeBook Studio"  # İşletim sistemi düzeyinde isim düzeltmesi
    sys.exit(app.exec())