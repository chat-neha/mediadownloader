import os
import yt_dlp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.utils import platform

# Set FFmpeg path dynamically
if platform == "android":
    from android.storage import app_storage_path
    FFMPEG_PATH = os.path.join(app_storage_path(), "ffmpeg.exe")
else:
    FFMPEG_PATH = r"C:\ffmpeg\bin"

# Ensure FFmpeg is available
os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_PATH)


class DownloaderApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.url_input = TextInput(hint_text="Enter YouTube URL", multiline=False, size_hint=(1, 0.2))
        layout.add_widget(self.url_input)

        self.status_label = Label(text="Ready", size_hint=(1, 0.2))
        layout.add_widget(self.status_label)

        # MP4 Download Button
        mp4_button = Button(text="Download as MP4", size_hint=(1, 0.2))
        mp4_button.bind(on_press=self.download_video)
        layout.add_widget(mp4_button)

        # MP3 Download Button
        mp3_button = Button(text="Download as MP3", size_hint=(1, 0.2))
        mp3_button.bind(on_press=self.download_audio)
        layout.add_widget(mp3_button)

        return layout

    def download_video(self, instance):
        self.start_download('mp4')

    def download_audio(self, instance):
        self.start_download('mp3')

    def start_download(self, format_type):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "Error: Enter a valid URL!"
            return

        self.status_label.text = f"Downloading {format_type.upper()}..."
        ydl_opts = self.get_download_options(format_type)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.text = f"{format_type.upper()} Download Complete!"
        except Exception as e:
            self.status_label.text = f"Download Failed: {str(e)}"

    def get_download_options(self, format_type):
        if format_type == 'mp4':
            return {
                'ffmpeg_location': FFMPEG_PATH,
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': '%(title)s.mp4',
                'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
            }
        elif format_type == 'mp3':
            return {
                'ffmpeg_location': FFMPEG_PATH,
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.mp3',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            }


if __name__ == "__main__":
    DownloaderApp().run()
