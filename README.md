# 💻 CodeBook Studio

**CodeBook Studio**, teknik kitap yazarları, akademisyenler ve öğretmenler için geliştirilmiş; kaynak kodları Microsoft Word ve Adobe InDesign gibi kelime işlemcilere biçimlendirmesi korunmuş (RTF) tablolar halinde aktaran masaüstü kod biçimlendirme aracıdır.

---

## 🇹🇷 Türkçe Açıklama

### 🌟 Öne Çıkan Özellikler
- **Zengin RTF Tablo Çıktısı:** Kodlarınızı satır numaraları, zebra satır renklendirmesi ve özelleştirilebilir kenar boşlukları (padding) ile doğrudan Word/InDesign uyumlu RTF formatına dönüştürür.  
- **Akıllı Dil Algılama:** Yazdığınız kodu analiz ederek hangi programlama diline ait olduğunu otomatik tespit eder.  
- **Özel Temalar:** Ders kitapları ve teknik yayın standartlarına uygun, göz yormayan özel renk temaları (Örn: *Maarif Pastel*).  
- **Kolay Kurulum:** Kodlama bilmeyen kullanıcılar için derlenmiş `.exe` sürümüyle doğrudan çalıştırılabilir.  

### 🛠️ Teknik Altyapı
- **Arayüz:** PySide6 (Qt framework)  
- **Syntax Highlighter:** Pygments kütüphanesi  
- **Platform:** Windows (Doğrudan `.exe` olarak çalıştırılabilir)  

### 🚀 Kurulum ve Kullanım

#### Yöntem 1: Doğrudan Çalıştırın (Derlemeden)
1. Bu depoyu ZIP olarak indirin veya bilgisayarınıza klonlayın.  
2. `dist` klasörünün içine girin.  
3. **CodeBook Studio.exe** dosyasına çift tıklayarak uygulamayı başlatın.  

#### Yöntem 2: Python ile Çalıştırma (Geliştiriciler İçin)
Projeyi yerelde çalıştırmak veya geliştirmek isterseniz:  
Masaüstünüzde yeni bir klasör oluşturun
```bash
mkdir Test_CodeBook
````
```bash
cd Test_CodeBook
````
#### Depoyu klonlayın
```bash
git clone https://github.com/hkorates-droid/CodeBookStudio.git
````
```bash
cd CodeBookStudio
 ````

#### Gerekli kütüphaneleri yükleyin
```bash
pip install -r requirements.txt
 ````


#### Uygulamayı başlatın
python main.py


## 🇬🇧 English Description
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

Double-click CodeBook Studio.exe to launch the application instantly.

Method 2: Run with Python (For Developers)
If you want to run or develop the project locally:
# Create a new folder on your desktop
mkdir Test_CodeBook
cd Test_CodeBook

# Clone the repository
git clone https://github.com/hkorates-droid/CodeBookStudio.git
cd CodeBookStudio

# Install required libraries
pip install -r requirements.txt

# Start the application
python main.py

