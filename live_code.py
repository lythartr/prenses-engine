# SIG: EFENDIM
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

def create_content(app):
    layout = MDBoxLayout(orientation='vertical', padding="20dp")
    layout.add_widget(MDLabel(
        text="PRENSES ENGINE AKTIF\n\nLive Code Modu Calisiyor",
        halign="center",
        font_style="H5",
        theme_text_color="Custom",
        text_color=(0, 1, 1, 1)
    ))
    return layout
