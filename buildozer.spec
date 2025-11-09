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
