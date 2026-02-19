import environment
import os, time, threading, traceback
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.clock import Clock
from kivy.utils import platform
from kivy.logger import Logger
from kivy.uix.camera import Camera

LIVE_PATH = "/sdcard/Download/prenses_live/live_code.py" if platform == 'android' else "live_code.py"

class PrensesEngine(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        
        self.last_mtime = 0
        self.reload_cooldown = 0.8
        self.last_reload_time = 0
        self.stop_event = threading.Event() # Thread durdurma kontrolü
        
        # Ana İskelet
        self.root_layout = MDBoxLayout(orientation='vertical')
        
        # Üst Panel (Başlık ve Manuel Reload)
        top_bar = MDBoxLayout(adaptive_height=True, padding="10dp")
        top_bar.add_widget(MDLabel(text="PRENSES ENGINE PRO", font_style="H6", theme_text_color="Primary"))
        top_bar.add_widget(MDIconButton(icon="refresh", on_release=lambda x: self.reload_content()))
        
        # Preview Alanı (Sabit Container)
        self.preview_area = MDBoxLayout()
        
        # Alt Log Paneli
        self.log_panel = MDLabel(
            text="Sistem Hazır",
            theme_text_color="Secondary",
            font_style="Caption",
            halign="center",
            size_hint_y=None,
            height="30dp"
        )
        
        self.root_layout.add_widget(top_bar)
        self.root_layout.add_widget(self.preview_area)
        self.root_layout.add_widget(self.log_panel)
        
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA, Permission.RECORD_AUDIO,
                Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE
            ], self.start_engine)
        else:
            self.start_engine()
            
        return self.root_layout

    def start_engine(self, *args):
        # Güvenli Thread Yönetimi
        self.watcher_thread = threading.Thread(target=self.file_watcher_logic, daemon=True)
        self.watcher_thread.start()
        self.update_log("Watcher aktif.")

    def file_watcher_logic(self):
        while not self.stop_event.is_set():
            if os.path.exists(LIVE_PATH):
                try:
                    mtime = os.path.getmtime(LIVE_PATH)
                    curr = time.time()
                    if mtime > self.last_mtime and (curr - self.last_reload_time) > self.reload_cooldown:
                        self.last_mtime = mtime
                        self.last_reload_time = curr
                        Clock.schedule_once(self.reload_content, 0)
                except:
                    pass
            time.sleep(1) # Dosya sistemi kontrol periyodu

    def reload_content(self, *args):
        self.update_log("Yükleniyor...")
        try:
            if not os.path.exists(LIVE_PATH):
                self.show_simple_error("live_code.py bulunamadı!")
                return

            with open(LIVE_PATH, "r", encoding='utf-8') as f:
                code = f.read()

            if "# SIG: EFENDIM" not in code:
                self.show_simple_error("HATA: # SIG: EFENDIM eksik!")
                return

            exec_globals = {
                'app': self, 'MDBoxLayout': MDBoxLayout, 
                'Camera': Camera, 'platform': platform, 'Logger': Logger
            }
            
            exec(code, exec_globals)
            
            if 'create_content' in exec_globals:
                new_ui = exec_globals['create_content'](self)
                self.preview_area.clear_widgets()
                self.preview_area.add_widget(new_ui)
                self.update_log("Başarıyla güncellendi.")
        except Exception:
            self.show_simple_error(traceback.format_exc())

    def update_log(self, msg):
        self.log_panel.text = f"[{time.strftime('%H:%M:%S')}] {msg}"

    def show_simple_error(self, err):
        self.preview_area.clear_widgets()
        self.preview_area.add_widget(MDLabel(
            text=f"[color=ff5555]HATA[/color]\n\n{err}",
            halign="center", markup=True, font_style="Caption"
        ))
        self.update_log("Hata oluştu.")

    def on_stop(self):
        # Uygulama kapanırken thread'i durdur
        self.stop_event.set()
        Logger.info("PrensesEngine: Motor durduruldu.")

if __name__ == '__main__':
    PrensesEngine().run()
