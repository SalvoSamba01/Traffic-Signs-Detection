import os
from PIL import Image

def resize_images_in_place(folder, size=(640, 640)):
    for filename in os.listdir(folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
            img_path = os.path.join(folder, filename)
            img = Image.open(img_path)
            img_resized = img.resize(size)
            img_resized.save(img_path)
            print(f'Immagine {filename} ridimensionata e salvata.')

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()

    folder_selected = filedialog.askdirectory(title="Seleziona la cartella delle immagini")

    if folder_selected:
        resize_images_in_place(folder_selected)
    else:
        print("Nessuna cartella selezionata.")
