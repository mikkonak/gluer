import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

def check_ffmpeg():
    try:
        ffmpeg_version = os.popen('ffmpeg -version').read()
        if "ffmpeg version" not in ffmpeg_version:
            raise FileNotFoundError
    except Exception:
        messagebox.showerror("Error", "ffmpeg is not installed or not found in PATH. Please install ffmpeg and add it to your system PATH.")
        return False
    return True

def merge_audio_files(folder1, folder2, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    files1 = {f.split('_')[0]: f for f in os.listdir(folder1) if f.endswith('.mp3')}
    files2 = {f.split('_')[0]: f for f in os.listdir(folder2) if f.endswith('.mp3')}

    common_keys = set(files1.keys()).intersection(set(files2.keys()))

    for key in common_keys:
        file1_path = os.path.join(folder1, files1[key])
        file2_path = os.path.join(folder2, files2[key])

        try:
            audio1 = AudioSegment.from_mp3(file1_path)
            audio2 = AudioSegment.from_mp3(file2_path)
        except CouldntDecodeError:
            messagebox.showerror("Error", f"Could not decode one of the files: {file1_path} or {file2_path}")
            return

        combined = audio1 + audio2

        new_filename = f"{files1[key].replace('.mp3', '')}_{files2[key]}"
        combined.export(os.path.join(output_folder, new_filename), format="mp3")
        print(f"Saved combined file: {new_filename}")

    messagebox.showinfo("Completed", f"All common files have been merged and saved to {output_folder}")

def browse_folder(entry):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry.delete(0, 'end')
        entry.insert(0, folder_selected)

def create_gui():
    root = Tk()
    root.title("Merge Audio Files")

    Label(root, text="Folder 1:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    folder1_entry = Entry(root, width=50)
    folder1_entry.grid(row=0, column=1, padx=10, pady=5)
    Button(root, text="Browse", command=lambda: browse_folder(folder1_entry)).grid(row=0, column=2, padx=10, pady=5)

    Label(root, text="Folder 2:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    folder2_entry = Entry(root, width=50)
    folder2_entry.grid(row=1, column=1, padx=10, pady=5)
    Button(root, text="Browse", command=lambda: browse_folder(folder2_entry)).grid(row=1, column=2, padx=10, pady=5)

    Label(root, text="Output Folder:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    output_folder_entry = Entry(root, width=50)
    output_folder_entry.grid(row=2, column=1, padx=10, pady=5)
    Button(root, text="Browse", command=lambda: browse_folder(output_folder_entry)).grid(row=2, column=2, padx=10, pady=5)

    Button(root, text="Merge Files", command=lambda: merge_audio_files(folder1_entry.get(), folder2_entry.get(), output_folder_entry.get()) if check_ffmpeg() else None).grid(row=3, columnspan=3, pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
