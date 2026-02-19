[app]
title = Prenses Engine Pro
package.name = prensesengine
package.domain = org.efendim
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Gerekli Kütüphaneler
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,sdl2_ttf

orientation = portrait
fullscreen = 1

# İzinler
android.permissions = CAMERA, RECORD_AUDIO, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 33

# Mimari (Modern telefonlar için)
android.archs = arm64-v8a, armeabi-v7a

# Log ayarları
log_level = 2
warn_on_root = 0
