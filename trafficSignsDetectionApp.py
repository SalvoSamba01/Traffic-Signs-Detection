import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from collections import Counter
from ultralytics import YOLOv10

# Definisci la dimensione massima per le immagini
MAX_IMAGE_SIZE = (400, 400)

# Funzione per ridimensionare l'immagine mantenendo il rapporto d'aspetto
def resize_image(image, max_size):
    image.thumbnail(max_size, Image.ANTIALIAS)
    return image

# Funzione per caricare l'immagine ground truth
def load_ground_truth():
    global gt_img
    if img_path:
        gt_img_path = img_path.replace("/images", "/groundThruthAnnotations")

        try:
            gt_img = cv2.imread(gt_img_path)
            if gt_img is not None:
                gt_img_rgb = cv2.cvtColor(gt_img, cv2.COLOR_BGR2RGB)
                gt_img_pil = Image.fromarray(gt_img_rgb)
                gt_img_pil = resize_image(gt_img_pil, MAX_IMAGE_SIZE)
                gt_img_tk = ImageTk.PhotoImage(gt_img_pil)
                img_panel_middle.config(image=gt_img_tk)
                img_panel_middle.image = gt_img_tk
                title_middle.grid()  # Mostra il titolo "Ground-truth boxes"
            else:
                messagebox.showerror("Error", "Ground truth image not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Ground truth image loading error: {str(e)}")

# Funzione per caricare un'immagine
def load_image():
    global img, img_path
    remove_prediction()  # Rimuovi la predizione e il titolo precedente se presente
    img_path = filedialog.askopenfilename()
    if img_path:
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = resize_image(img_pil, MAX_IMAGE_SIZE)
        img_tk = ImageTk.PhotoImage(img_pil)
        img_panel_left.config(image=img_tk)
        img_panel_left.image = img_tk
        title_left.grid()  # Mostra il titolo "Original image"
        load_ground_truth()

# Funzione per rimuovere l'immagine attuale e i relativi titoli
def remove_images():
    global img, gt_img
    img_panel_left.config(image='')
    img_panel_middle.config(image='')
    img_panel_right.config(image='')
    title_left.grid_remove()
    title_middle.grid_remove()
    title_right.grid_remove()
    prediction_listbox.pack_forget()  # Nascondi la listbox delle predizioni
    prediction_listbox.delete(0, tk.END)  # Svuota la lista delle predizioni
    img = None
    gt_img = None

# Funzione per rimuovere la predizione e il titolo
def remove_prediction():
    img_panel_right.config(image='')
    title_right.grid_remove()
    prediction_listbox.pack_forget()  # Nascondi la listbox delle predizioni

# Funzione per caricare il modello YOLO
def load_model(event):
    global model
    model_name = selected_model.get()
    try:
        if model_name == "YOLOv10n":
            model = YOLOv10("./YOLOv10nTRAINED/weights/best.pt")
        elif model_name == "YOLOv10s":
            model = YOLOv10("./YOLOv10sTRAINED/weights/best.pt")
        elif model_name == "YOLOv10m":
            model = YOLOv10("./YOLOv10mTRAINED/weights/best.pt")
        messagebox.showinfo("Model loaded", f"{model_name} model loaded!")
    except Exception as e:
        messagebox.showerror("Error", f"Error in model loading: {str(e)}")

# Funzione per eseguire la predizione
def predict():
    global img
    if img is None:
        messagebox.showerror("Error", "Load image first!")
        return
    if model is None:
        messagebox.showerror("Error", "Load a model first!")
        return

    results = model(img_path)
    class_count = Counter()  # Per contare le occorrenze delle classi

    for result in results:
        image = result.orig_img
        boxes = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = box.conf[0].item()
                class_id = int(box.cls[0].item())
                class_name = results[0].names[class_id]
                boxes.append((x1, y1, x2, y2, confidence, class_name))
                class_count[class_name] += 1  # Aggiungi al contatore della classe

        boxes = sorted(boxes, key=lambda x: x[4], reverse=True)

        for (x1, y1, x2, y2, confidence, class_name) in boxes:
            label = f'{class_name}-{confidence:.2f}'
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 0.7
            font_thickness = 1
            (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)

            text_x = int(x1 + (x2 - x1 - text_width) / 2)
            text_y = int(y1) - 10
            cv2.putText(image, label, (text_x, text_y), font, font_scale, (255, 0, 0), font_thickness)

        img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        img_pil = resize_image(img_pil, MAX_IMAGE_SIZE)
        img_tk = ImageTk.PhotoImage(img_pil)
        img_panel_right.config(image=img_tk)
        img_panel_right.image = img_tk
        title_right.grid()  # Mostra il titolo "Predictions"

        # Aggiorna la listbox con le classi predette
        prediction_listbox.delete(0, tk.END)  # Svuota la lista
        if class_count:
            prediction_listbox.insert(tk.END, "PREDICTIONS")
            for class_name, count in class_count.items():
                prediction_listbox.insert(tk.END, f"{class_name} x{count}")
            prediction_listbox.pack(side=tk.BOTTOM, fill=tk.X)  # Mostra la listbox delle predizioni
        else:
            prediction_listbox.insert(tk.END, "No traffic sign detected!")
            prediction_listbox.pack(side=tk.BOTTOM, fill=tk.X)  # Mostra la listbox delle predizioni

# Configurazione dell'interfaccia utente con tkinter
root = tk.Tk()
root.title("Traffic Sign Detection App")
root.update_idletasks()  # Assicurati che il layout sia aggiornato
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f"{width}x{height}+0+0")

# Menu a tendina per la selezione del modello
model_label = tk.Label(root, text="Select YOLO model:")
model_label.pack()

selected_model = tk.StringVar()
model_menu = ttk.Combobox(root, textvariable=selected_model)
model_menu['values'] = ('YOLOv10n', 'YOLOv10s', 'YOLOv10m')
model_menu.pack()
model_menu.bind("<<ComboboxSelected>>", load_model)

# Frame per i pulsanti di caricamento e rimozione dell'immagine
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Pulsante per caricare l'immagine
load_img_btn = tk.Button(button_frame, text="Load image", command=load_image)
load_img_btn.pack(side=tk.LEFT, padx=5)

# Pulsante per rimuovere l'immagine caricata
remove_img_btn = tk.Button(button_frame, text="Remove image", command=remove_images)
remove_img_btn.pack(side=tk.LEFT, padx=5)

# Riquadri e titoli per le immagini
frame = tk.Frame(root)
frame.pack()

title_left = tk.Label(frame, text="Original Image", font=("Courier", 10,"bold"))
title_left.grid(row=0, column=0)
title_left.grid_remove()

title_middle = tk.Label(frame, text="Ground-truth Boxes", font=("Courier", 10,"bold"))
title_middle.grid(row=0, column=1)
title_middle.grid_remove()

title_right = tk.Label(frame, text="Predictions", font=("Courier", 10,"bold"))
title_right.grid(row=0, column=2)
title_right.grid_remove()

img_panel_left = tk.Label(frame)
img_panel_left.grid(row=1, column=0, padx=10, pady=10)

img_panel_middle = tk.Label(frame)
img_panel_middle.grid(row=1, column=1, padx=10, pady=10)

img_panel_right = tk.Label(frame)
img_panel_right.grid(row=1, column=2, padx=10, pady=10)

# Listbox per mostrare le predizioni
prediction_listbox = tk.Listbox(root, height=15, width=40, font=("Courier", 10), justify="center")
prediction_listbox.pack_forget()  # Nascondi inizialmente

# Pulsante per fare la predizione
predict_btn = tk.Button(root, text="Predict", command=predict)
predict_btn.pack(pady=10)

# Variabili globali
img = None
img_path = None
gt_img = None
model = None

# Avvio dell'interfaccia
root.mainloop()