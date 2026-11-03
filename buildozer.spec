[app]
title = Autism Student Learning
package.name = autismstudentlearning
package.domain = org.pujadieworks
source.dir = .
source.include_exts = py,kv,png,jpg,atlas,ttf,otf
version = 1.2.0
requirements = python3,kivy,plyer
orientation = landscape
fullscreen = 1
android.api = 35
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.private_storage = True

# For Tamil glyph support, bundle a Tamil Unicode .ttf font and configure
# Kivy labels to use that font if the tablet's default font is insufficient.
