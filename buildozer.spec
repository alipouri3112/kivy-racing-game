[app]
title = Racing Game
package.name = racinggame
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy==2.3.0

[buildozer]
log_level = 2

android.permissions = INTERNET
android.api = 30
android.minapi = 21
android.ndk = 25b
android.sdk = 30
android.gradle_dependencies = 

[app]
android.entrypoint = org.kivy.android.PythonActivity
android.add_src = src/main/python
android.add_jars = src/main/jars
android.add_aars = src/main/aars
android.archs = arm64-v8a, armeabi-v7a
android.gradle_dependencies = 
android.enable_androidx = True
android.add_compile_options = "sourceCompatibility JavaVersion.VERSION_1_8", "targetCompatibility JavaVersion.VERSION_1_8"
android.enable_jetifier = True
