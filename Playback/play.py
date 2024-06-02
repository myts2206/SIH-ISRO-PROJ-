import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from threading import Thread
from pathlib import Path
from vlc import MediaPlayer

def is_scrambled(file_path):
    # Check if the file is scrambled/encrypted
    output = subprocess.check_output(
        f"ffprobe -v error -show_entries stream_tags:stream=encryption -of default=noprint_wrappers=1:nokey=1 {file_path}", shell=True)
    return "encrypted" in output.decode()

def extract_streams(file_path, output_folder):
    if is_scrambled(file_path):
        messagebox.showinfo("Info", "The file is encrypted/scrambled.")
        return

    num_streams = int(subprocess.check_output(
        f"ffprobe -v error -select_streams v -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {file_path} | wc -l", shell=True))
    for i in range(num_streams):
        try:
            result = subprocess.call(f"ffmpeg -err_detect ignore_err -copy_unknown -analyzeduration 2147483647 -probesize 2147483647 -i {file_path} -map v:{i}? -c copy {output_folder}/output_video_{i}.mp4", shell=True)
            if result != 0:
                messagebox.showinfo("Info", f"Failed to extract stream {i}.")
        except Exception as e:
            messagebox.showinfo("Info", f"Error occurred while extracting stream {i}: {str(e)}")

def play_video(file_path):
    player = MediaPlayer(file_path)
    player.play()

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("TS files", "*.ts")])
    if file_path:
        output_folder = Path(file_path).parent / 'folder11111'
        output_folder.mkdir(exist_ok=True)
        Thread(target=extract_streams, args=(file_path, output_folder)).start()
        messagebox.showinfo("Info", "Extraction started. Please refresh the list after a while.")

def refresh_list():
    folder_path = filedialog.askdirectory()
    if folder_path:
        listbox.delete(0, tk.END)
        for file in os.listdir(folder_path):
            if file.endswith(".mp4"):
                listbox.insert(tk.END, os.path.join(folder_path, file))

def on_select(event):
    selected_file = listbox.get(listbox.curselection())
    Thread(target=play_video, args=(selected_file,)).start()

root = tk.Tk()
root.title("TS Stream Extractor")

browse_button = tk.Button(root, text="Browse TS File", command=browse_file)
browse_button.pack()

refresh_button = tk.Button(root, text="Refresh List", command=refresh_list)
refresh_button.pack()

listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH, expand=1)
listbox.bind('<<ListboxSelect>>', on_select)

root.mainloop()
