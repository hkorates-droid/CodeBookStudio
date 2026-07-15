class ThemeManager:
    """Uygulama içinde kullanılacak Koyu ve Açık temaları yöneten sınıf."""
    
    def __init__(self):
        self.themes = {
            # =================================================================
            # LIGHT (AÇIK RENKLİ) TEMALAR - KİTAP BASIMLARI İÇİN İDEAL
            # =================================================================
            "Maarif Pastel": {
                "background": "#F9F9FB",
                "foreground": "#2C3E50",
                "line_numbers": "#7F8C8D",
                "zebra_even": "#F9F9FB",
                "zebra_odd": "#F0F1F6",
                "tokens": {
                    "Keyword": "#8E44AD",       # Mor
                    "String": "#27AE60",        # Yeşil
                    "Comment": "#7F8C8D",       # Soft Gri
                    "Number": "#D35400",        # Turuncu
                    "Function": "#2980B9",      # Mavi
                    "Operator": "#34495E",      # Koyu Gri
                    "Generic": "#2C3E50"
                }
            },
            "Yayinci Dostu": {
                "background": "#FFFFFF",
                "foreground": "#111111",
                "line_numbers": "#888888",
                "zebra_even": "#FFFFFF",
                "zebra_odd": "#F5F6F8",
                "tokens": {
                    "Keyword": "#0056B3",       # Canlı Kurumsal Mavi
                    "String": "#28A745",        # Yaprak Yeşili
                    "Comment": "#6A737D",       # Github tarzı gri
                    "Number": "#E83E8C",        # Canlı Pembe/Kırmızı
                    "Function": "#6F42C1",      # Derin Mor
                    "Operator": "#D15700",      # Canlı Turuncu
                    "Generic": "#111111"
                }
            },
            "Retro Kitap": {
                "background": "#FDFBF7",
                "foreground": "#332211",
                "line_numbers": "#8C7E6E",
                "zebra_even": "#FDFBF7",
                "zebra_odd": "#F5F0E6",
                "tokens": {
                    "Keyword": "#A01E1E",       # Sıcak Tuğla Kırmızısı
                    "String": "#1E6B3F",        # Koyu Orman Yeşili
                    "Comment": "#7A7065",       # Sıcak Toprak Grisi
                    "Number": "#B05000",        # Sıcak Tarçın
                    "Function": "#0F52BA",      # Safir Mavisi
                    "Operator": "#4A3B32",      # Çikolata
                    "Generic": "#332211"
                }
            },     
            "Thonny": {
                "foreground": "#000000",
                "background": "#FFFFFF",
                "line_numbers": "#999999",
                "zebra_even": "#F5F5F5",
                "zebra_odd": "#FFFFFF",
                "tokens": {
                    "Keyword": "#7F0055",
                    "String": "#2A00FF",
                    "Comment": "#3F7F5F",
                    "Number": "#000000",
                    "Function": "#000000",
                    "Operator": "#000000",
                    "Generic": "#000000"
                }
            },
            "Solarized Light": {
                "foreground": "#657B83",
                "background": "#FDF6E3",
                "line_numbers": "#93A1A1",
                "zebra_even": "#EEE8D5",
                "zebra_odd": "#FDF6E3",
                "tokens": {
                    "Keyword": "#859900",      # Zeytin Yeşili
                    "String": "#2AA198",       # Turkuaz
                    "Comment": "#93A1A1",      # Açık Gri
                    "Number": "#D33682",       # Magenta
                    "Function": "#268BD2",     # Okyanus Mavisi
                    "Operator": "#B58900",     # Hardal Sarısı
                    "Generic": "#657B83"
                }
            },
            "GitHub Light": {
                "foreground": "#24292E",
                "background": "#FFFFFF",
                "line_numbers": "#BABBBD",
                "zebra_even": "#FAFBFC",
                "zebra_odd": "#FFFFFF",
                "tokens": {
                    "Keyword": "#D73A49",      # Kırmızı
                    "String": "#032F62",       # Koyu Mavi
                    "Comment": "#6A737D",      # Gri
                    "Number": "#005CC5",       # Parlak Mavi
                    "Function": "#6F42C1",     # Mor
                    "Operator": "#D73A49",     # Kırmızı
                    "Generic": "#24292E"
                }
            },
            "Elegant Gray": {
                "foreground": "#333333",
                "background": "#F8F9FA",
                "line_numbers": "#A0AAB2",
                "zebra_even": "#EDEFF1",
                "zebra_odd": "#F8F9FA",
                "tokens": {
                    "Keyword": "#0052CC",      # Kurumsal Mavi
                    "String": "#008000",       # Net Yeşil
                    "Comment": "#708090",      # Slate Gri
                    "Number": "#D03A00",       # Koyu Turuncu
                    "Function": "#800080",     # Mor
                    "Operator": "#333333",     # Füme
                    "Generic": "#333333"
                }
            },
            "Maarif Klasik": {
                "foreground": "#2C3E50",
                "background": "#FAF9F5",
                "line_numbers": "#BDC3C7",
                "zebra_even": "#F2EFE9",
                "zebra_odd": "#FAF9F5",
                "tokens": {
                    "Keyword": "#E74C3C",      # Yumuşak Kırmızı
                    "String": "#27AE60",       # Doğal Yeşil
                    "Comment": "#7F8C8D",      # Orta Gri
                    "Number": "#2980B9",       # Yumuşak Mavi
                    "Function": "#8E44AD",     # Soft Mor
                    "Operator": "#34495E",     # Koyu Lacivert
                    "Generic": "#2C3E50"
                }
            },
            # =================================================================
            # DARK (KOYU RENKLİ) TEMALAR - EKRAN KULLANIMI İÇİN İDEAL
            # =================================================================
            "Monokai": {
                "foreground": "#F8F8F2",
                "background": "#272822",
                "line_numbers": "#75715E",
                "zebra_even": "#2E2F30",
                "zebra_odd": "#272822",
                "tokens": {
                    "Keyword": "#F92672",
                    "String": "#E6DB74",
                    "Comment": "#75715E",
                    "Number": "#AE81FF",
                    "Function": "#A6E22E",
                    "Operator": "#F92672",
                    "Generic": "#F8F8F2"
                }
            },
            "Dracula": {
                "foreground": "#F8F8F2",
                "background": "#282A36",
                "line_numbers": "#6272A4",
                "zebra_even": "#343746",
                "zebra_odd": "#282A36",
                "tokens": {
                    "Keyword": "#FF79C6",
                    "String": "#F1FA8C",
                    "Comment": "#6272A4",
                    "Number": "#BD93F9",
                    "Function": "#50FA7B",
                    "Operator": "#FF79C6",
                    "Generic": "#F8F8F2"
                }
            },
            "One Dark": {
                "foreground": "#ABB2BF",
                "background": "#282C34",
                "line_numbers": "#4B5263",
                "zebra_even": "#2C313C",
                "zebra_odd": "#282C34",
                "tokens": {
                    "Keyword": "#C678DD",
                    "String": "#98C379",
                    "Comment": "#5C6370",
                    "Number": "#D19A66",
                    "Function": "#61AFEF",
                    "Operator": "#56B6C2",
                    "Generic": "#ABB2BF"
                }
            },
            "Nord": {
                "foreground": "#D8DEE9",
                "background": "#2E3440",
                "line_numbers": "#4C566A",
                "zebra_even": "#3B4252",
                "zebra_odd": "#2E3440",
                "tokens": {
                    "Keyword": "#81A1C1",
                    "String": "#A3BE8C",
                    "Comment": "#4C566A",
                    "Number": "#B48EAD",
                    "Function": "#88C0D0",
                    "Operator": "#81A1C1",
                    "Generic": "#D8DEE9"
                }
            },
            "Synthwave '84": {
                "foreground": "#FFFFFF",
                "background": "#262335",
                "line_numbers": "#685E79",
                "zebra_even": "#2F2B43",
                "zebra_odd": "#262335",
                "tokens": {
                    "Keyword": "#FE4450",
                    "String": "#FF7EDB",
                    "Comment": "#848BB3",
                    "Number": "#FEDE5D",
                    "Function": "#36F9F6",
                    "Operator": "#36F9F6",
                    "Generic": "#FFFFFF"
                }
            }
        }

    def get_theme_names(self):
        """Kayıtlı tüm temaların isimlerini liste halinde döner."""
        return list(self.themes.keys())

    def get_theme(self, name):
        """İsmi verilen temanın renk paletini döner, bulunamazsa varsayılan Thonny döner."""
        return self.themes.get(name, self.themes["Thonny"])