[app]
title = DownloaderApp
package.name = downloader
package.domain = org.kivy
source.include_exts = py,kv
source.exclude_exts = spec
version = 1.0
requirements = python3,kivy,yt-dlp
android.permissions = android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_EXTERNAL_STORAGE, android.permission.INTERNET
android.api = 31
android.minapi = 21
android.ndk = 23b
android.arch = arm64-v8a
android.storage = true
android.gradle_dependencies = 'com.android.support:support-v4:27.1.1'

# FFmpeg Setup
android.presplash_color = "#000000"
android.allow_backup = True
p4a.branch = master
p4a.local_recipes = ./recipes
android.meta_data = android.permission.INTERNET, android.permission.ACCESS_NETWORK_STATE

[buildozer]
log_level = 2
warn_on_root = 1
