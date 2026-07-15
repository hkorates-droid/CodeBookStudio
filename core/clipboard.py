import ctypes
from ctypes import wintypes

GMEM_MOVEABLE = 0x0002
GMEM_ZEROINIT = 0x0040

class WindowsClipboard:
    """Windows Pano API'sini doğrudan manipüle ederek InDesign uyumlu kopyalama sağlar."""
    
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
        self.user32.OpenClipboard.argtypes = [wintypes.HWND]
        self.user32.OpenClipboard.restype = wintypes.BOOL
        self.user32.EmptyClipboard.restype = wintypes.BOOL
        self.user32.CloseClipboard.restype = wintypes.BOOL
        self.user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
        self.user32.SetClipboardData.restype = wintypes.HANDLE
        
        self.kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
        self.kernel32.GlobalAlloc.restype = wintypes.HGLOBAL
        self.kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
        self.kernel32.GlobalLock.restype = wintypes.LPVOID
        self.kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
        self.kernel32.GlobalUnlock.restype = wintypes.BOOL
        
        self.CF_RTF = self.user32.RegisterClipboardFormatW("Rich Text Format")
        self.CF_UNICODETEXT = 13

    def copy(self, plain_text: str, rtf_text: str) -> bool:
        """Panoya düz metni ve RTF'i Türkçe yerel kodlamasıyla kararlı şekilde yazar."""
        if not self.user32.OpenClipboard(0):
            return False
            
        try:
            self.user32.EmptyClipboard()
            
            # 1. Düz Metin Yazma (CF_UNICODETEXT)
            unicode_bytes = plain_text.encode('utf-16-le') + b'\x00\x00'
            h_uni_mem = self.kernel32.GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, len(unicode_bytes))
            if h_uni_mem:
                p_uni_mem = self.kernel32.GlobalLock(h_uni_mem)
                if p_uni_mem:
                    ctypes.memmove(p_uni_mem, unicode_bytes, len(unicode_bytes))
                    self.kernel32.GlobalUnlock(h_uni_mem)
                    self.user32.SetClipboardData(self.CF_UNICODETEXT, h_uni_mem)

            # 2. RTF Yazma (CF_RTF)
            # RTF metnini yerel Türkçe CP1254 ile kodlayarak InDesign/Word'e %100 uyumlu hale getiriyoruz
            rtf_bytes = rtf_text.encode('cp1254', errors='replace') + b'\x00'
            h_rtf_mem = self.kernel32.GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, len(rtf_bytes))
            if h_rtf_mem:
                p_rtf_mem = self.kernel32.GlobalLock(h_rtf_mem)
                if p_rtf_mem:
                    ctypes.memmove(p_rtf_mem, rtf_bytes, len(rtf_bytes))
                    self.kernel32.GlobalUnlock(h_rtf_mem)
                    self.user32.SetClipboardData(self.CF_RTF, h_rtf_mem)
                    
            return True
        except Exception as e:
            print(f"Pano Hatası: {e}")
            return False
        finally:
            self.user32.CloseClipboard()