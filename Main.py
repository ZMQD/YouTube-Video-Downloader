import tkinter as tk
from tkinter import filedialog, ttk
from pytube import YouTube, Playlist
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import threading

def progress(stream, chunk, bytes_remaining):
    current = ((stream.filesize - bytes_remaining)/stream.filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50-progress)
    progress_label.config(text='[{0}] {1}%'.format(status, percent))

def download_video():
    # Create a new thread for the download process
    download_thread = threading.Thread(target=download_video_thread)
    # Start the new thread
    download_thread.start()

def download_video_thread():
    url = url_entry.get()
    output_path = path_entry.get()
    quality = quality_combo.get()

    if 'playlist' in url:
        playlist = Playlist(url)
        for video_url in playlist.video_urls:
            download(video_url, output_path, quality)
    else:
        download(url, output_path, quality)

def download(url, output_path, quality):
    video = YouTube(url, on_progress_callback=progress)
    
    if quality == 'Highest resolution':
        video_stream = video.streams.get_highest_resolution()
    elif quality == 'Lowest resolution':
        video_stream = video.streams.get_lowest_resolution()
    else:
        video_stream = video.streams.get_by_itag(18)  # 360p

    audio_stream = video.streams.get_audio_only()

    video_file = video_stream.download(output_path, filename_prefix='video_')
    audio_file = audio_stream.download(output_path, filename_prefix='audio_')

    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path + '/' + video.title + '.mp4')

    os.remove(video_file)
    os.remove(audio_file)

root = tk.Tk()
root.configure(bg='black')

url_label = tk.Label(root, text="YouTube URL:", bg='black', fg='white')
url_label.pack()
url_entry = tk.Entry(root, width=50, bg='gray')
url_entry.pack(padx=10, pady=10)

path_label = tk.Label(root, text="Output Path:", bg='black', fg='white')
path_label.pack()
path_entry = tk.Entry(root, width=50, bg='gray')
path_entry.pack(padx=10, pady=10)

quality_label = tk.Label(root, text="Select Quality:", bg='black', fg='white')
quality_label.pack()
quality_combo = ttk.Combobox(root, values=['Highest resolution', 'Medium resolution', 'Lowest resolution'])
quality_combo.pack()

download_button = tk.Button(root, text="Download Video", command=download_video)
download_button.pack()

progress_label = tk.Label(root, text="", bg='black', fg='white')
progress_label.pack()

root.mainloop()
