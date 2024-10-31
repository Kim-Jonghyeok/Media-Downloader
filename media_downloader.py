import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import re
from pathlib import Path

class YouTubeDownloader:
    def __init__(self):
        self.setup_ssl()
        self.setup_gui()
        
    def setup_ssl(self):
        """SSL 설정 및 경고 비활성화"""
        urllib3.disable_warnings(InsecureRequestWarning)

    def check_ffmpeg(self):
        """ffmpeg 설치 확인 및 경로 찾기"""
        try:
            # Windows
            if os.name == 'nt':
                paths = ['C:/ffmpeg/bin/ffmpeg.exe', 'ffmpeg.exe']
                for path in paths:
                    if os.path.exists(path):
                        return path
            # Linux/Mac
            else:
                result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
            
            messagebox.showwarning("경고", "ffmpeg를 찾을 수 없습니다. 설치 후 다시 시도해주세요.")
            return None
        except Exception as e:
            messagebox.showerror("오류", f"ffmpeg 확인 중 오류 발생: {e}")
            return None

    def check_and_install_yt_dlp(self):
        """yt-dlp 설치 및 업데이트 확인"""
        try:
            subprocess.check_call([
                sys.executable,
                '-m',
                'pip',
                'install',
                '--upgrade',
                'pip',
                '--trusted-host',
                'pypi.org',
                '--trusted-host',
                'files.pythonhosted.org',
                '--no-warn-script-location'
            ])
            
            subprocess.check_call([
                sys.executable,
                '-m',
                'pip',
                'install',
                '--upgrade',
                'yt-dlp',
                '--trusted-host',
                'pypi.org',
                '--trusted-host',
                'files.pythonhosted.org',
                '--no-warn-script-location'
            ])
            return True
        except Exception as e:
            messagebox.showerror("오류", f"yt-dlp 설치/업데이트 실패: {e}")
            return False

    def validate_url(self, url):
        """YouTube URL 유효성 검사"""
        youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
        return bool(re.match(youtube_regex, url))

    def update_progress(self, d):
        """다운로드 진행률 업데이트"""
        try:
            if d['status'] == 'downloading':
                if '_percent_str' in d:
                    percent_str = d['_percent_str']
                    clean_str = re.sub(r'\x1b\[[0-9;]*m', '', percent_str)
                    progress = float(clean_str.replace('%', ''))
                elif 'downloaded_bytes' in d and 'total_bytes' in d:
                    progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                else:
                    return
                    
                self.progress_var.set(progress)
                self.root.update_idletasks()
        except Exception as e:
            print(f"진행률 업데이트 중 오류 발생: {e}")
            pass

    def download_video(self, url, path, quality_option):
        if not self.validate_url(url):
            messagebox.showwarning("경고", "올바른 YouTube URL을 입력하세요.")
            return

        if 'list=' in url:
            video_id = url.split('v=')[1].split('&')[0]
            url = f'https://www.youtube.com/watch?v={video_id}'

        ffmpeg_path = self.check_ffmpeg()
        if not ffmpeg_path:
            return

        try:
            format_id = quality_option
            
            ydl_opts = {
                'format': format_id,
                'progress_hooks': [self.update_progress],
                'ffmpeg_location': ffmpeg_path,
                'nocheckcertificate': True,
                'noplaylist': True,
                'quiet': False,
                'no_warnings': False,
                'ignoreerrors': False,
                'socket_timeout': 60,
                'retries': 30,
                'fragment_retries': 30,
                'http_chunk_size': 1048576,
                'verify': False,
                'buffersize': 1024,
                'external_downloader': 'native',
                'format_sort': ['res:2160', 'res:1440', 'res:1080', 'res:720', 'res:480', 'res:360'],
                'writethumbnail': False,
                'writesubtitles': False,
                'postprocessors': [],
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s')
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            messagebox.showinfo("성공", "다운로드가 완료되었습니다!")
            self.progress_var.set(0)
            
        except Exception as e:
            messagebox.showerror("오류", f"다운로드 중 오류 발생: {e}")
            self.progress_var.set(0)

    def setup_gui(self):
        """GUI 설정"""
        self.root = tk.Tk()
        self.root.title("YouTube 동영상 다운로더")
        self.root.geometry("600x400")

        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TEntry", padding=3)

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(main_frame, text="YouTube URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(main_frame, text="저장 경로:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.folder_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.folder_path, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="찾아보기", command=self.select_folder).grid(row=1, column=2, pady=5)

        ttk.Label(main_frame, text="화질:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value='bestvideo[height<=2160]+bestaudio/best')
        quality_options = [
            'bestvideo[height<=2160]+bestaudio/best',
            'bestvideo[height<=1440]+bestaudio/best',
            'bestvideo[height<=1080]+bestaudio/best',
            'bestvideo[height<=720]+bestaudio/best',
            'bestvideo[height<=480]+bestaudio/best',
            'bestvideo[height<=360]+bestaudio/best'
        ]
        ttk.OptionMenu(main_frame, self.quality_var, *quality_options).grid(row=2, column=1, sticky=tk.W, pady=5)

        self.progress_var = tk.DoubleVar()
        ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100).grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(main_frame, text="다운로드", command=self.start_download).grid(row=4, column=1, pady=20)

        for i in range(3):
            main_frame.columnconfigure(i, weight=1)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def start_download(self):
        url = self.url_entry.get().strip()
        path = self.folder_path.get()
        quality = self.quality_var.get()

        if not all([url, path, quality]):
            messagebox.showwarning("경고", "모든 필드를 입력해주세요.")
            return

        self.download_video(url, path, quality)

    def run(self):
        """프로그램 실행"""
        if self.check_and_install_yt_dlp():
            self.root.mainloop()

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.run()