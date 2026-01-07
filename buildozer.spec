[app]
title = Math Titan
package.name = mathtitan
package.domain = org.bhai
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# GitHub build ke liye requirements
requirements = python3,kivy==2.3.0,kivymd==1.2.0,sympy,pillow

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.allow_backup = True
p4a.branch = master
