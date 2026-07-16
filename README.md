### 🇹🇷  💻 CodeBook Studio

**CodeBook Studio**, özellikle teknik kitap yazarları, akademisyenler ve öğretmenler için tasarlanmış; kaynak kodları Microsoft Word ve Adobe InDesign gibi kelime işlemcilere biçimlendirmesi korunmuş (RTF) tablolar halinde aktaran gelişmiş bir masaüstü kod biçimlendirme aracıdır.

---
AÇIKLAMA
### 🌟 Öne Çıkan Özellikler
* **Zengin RTF Tablo Çıktısı:** Kodlarınızı satır numaraları, zebra satır renklendirmesi ve özelleştirilebilir kenar boşlukları (padding) ile doğrudan Word/InDesign uyumlu RTF formatına dönüştürür.
* **Akıllı Dil Algılama:** Yazdığınız kodu analiz ederek hangi programlama diline ait olduğunu otomatik tespit eder.
* **Özel Temalar:** Ders kitapları ve teknik yayın standartlarına uygun, göz yormayan özel renk temaları (Örn: *Maarif Pastel*).
* **Kolay Kurulum:** Kodlama bilmeyen kullanıcılar için derlenmiş `.exe` sürümüyle doğrudan çalıştırılabilir.

### 🛠️ Teknik Altyapı
* **Arayüz:** PySide6 (Qt framework)
* **Syntax Highlighter:** Pygments kütüphanesi
* **Platform:** Windows (Doğrudan `.exe` olarak çalıştırılabilir)

### 🚀 Kurulum ve Kullanım

#### Yöntem 1: Doğrudan Çalıştırın (Derlemeden)
1. Bu depoyu ZIP olarak indirin veya bilgisayarınıza klonlayın.
2. `dist` klasörünün içine girin.
3. **CodeBook Studio.exe** dosyasına çift tıklayarak uygulamayı anında başlatın!

#### Yöntem 2: Python ile Çalıştırma (Geliştiriciler İçin)
Projeyi yerelde çalıştırmak veya geliştirmek isterseniz:
1-Masaüstünüzde boş bir yere sağ tıklayın ve "Yeni Klasör" oluşturup adını Deneme_CodeBook yapın.
2-Bu yeni klasörün içine girin
3-Klasörün içinde boş bir yere sağ tıklayıp "PowerShell Penceresini Buradan Açın" veya "Terminalde Aç" seçeneğini seçin
terminale şu komutu yazıp entere basın
git clone https://github.com/hkorates-droid/CodeBookStudio.git

terminale  şu komutu yazıp entere basın
cd CodeBookStudio

# Gerekli kütüphaneleri yüklemek için terminale şu komutu yazın
pip install -r requirements.txt

# Uygulamayı başlatın
python main.py


### 🇬🇧 💻 CodeBook Studio
CodeBook Studio is an advanced desktop code formatting tool designed especially for technical book authors, academics, and teachers. It exports source code into richly formatted RTF tables that preserve styling and can be directly used in Microsoft Word and Adobe InDesign.

DESCRIPTION
🌟 Key Features
Rich RTF Table Output: Converts your code into Word/InDesign-compatible RTF format with line numbers, zebra row coloring, and customizable padding.

Smart Language Detection: Automatically analyzes your code and detects the programming language.

Custom Themes: Special color themes designed for textbooks and technical publications, easy on the eyes (e.g., Maarif Pastel).

Easy Installation: Comes with a compiled .exe version for non-coders to run instantly.

🛠️ Technical Infrastructure
Interface: PySide6 (Qt framework)

Syntax Highlighter: Pygments library

Platform: Windows (runs directly as .exe)

🚀 Installation and Usage
Method 1: Run Directly (No Compilation)
Download this repository as ZIP or clone it to your computer.

Enter the dist folder.

Double-click CodeBook Studio.exe to launch the application instantly!

Method 2: Run with Python (For Developers)
If you want to run or develop the project locally:

Right-click on an empty space on your desktop and create a new folder named Test_CodeBook.

Enter this new folder.

Inside the folder, right-click on an empty space and select Open PowerShell Window Here or Open in Terminal.

Type the following command in the terminal and press Enter:
git clone https://github.com/hkorates-droid/CodeBookStudio.git

Then type the following command and press Enter:
cd CodeBookStudio


To install the required libraries, type:
pip install -r requirements.txt

Finally, start the application with:
python main.py



