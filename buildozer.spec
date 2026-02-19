
title = Prenses Engine Pro
package.name = prensesengine
package.domain = org.efendim
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# GEREKSİNİMLER: OpenCV ve Android kütüphaneleri eklendi
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,sdl2_ttf,opencv4android,android

orientation = portrait
fullscreen = 1

# İZİNLER: Kamera, Ses ve Depolama (Android 11+ MANAGE_EXTERNAL_STORAGE dahil)
android.permissions = CAMERA, RECORD_AUDIO, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license = True

# Mimariler
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
