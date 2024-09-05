import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from helpers import helpers_potholes as hp, helpersWindows as hw
import numpy as np
import cv2
from tkinter import ttk
import threading


class PotholeDetectionApp:
    def __init__(self,master, mode="Light"):
        self.master = master
        self.window = tk.Tk()
        self.window.title("Pothole Detection")
        hw.center_window(self.window, width=1000, height=600)
        self.window.resizable(False, False)

        self.cale_poza = ""
        self.cale_videoclip = ""
        self.test_photo = None
        self.detect_photo_resized = None
        self.detect_photo = None

        self.current_mode = mode

        self.frame = tk.Frame(self.window)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()
        self.set_mode(mode)

    def create_widgets(self):
        # Title
        self.title = tk.Label(self.frame, text="Pothole Detection", font=("Arial", 16, "bold"))
        self.title.place(relx=0.05, rely=0.03)

        # Canvases
        self.pozaCanvas = tk.Canvas(self.frame, bg="#535659", width=600, height=250)
        self.pozaCanvas.place(relx=0.05, rely=0.08)

        self.rezultatCanvas = tk.Canvas(self.frame, bg="#535659", width=600, height=250)
        self.rezultatCanvas.place(relx=0.05, rely=0.52)

        # Buttons
        self.buton_alege = self.create_button("Choose Image", self.imageUpload, relx=0.675, rely=0.10)
        self.buton_detect = self.create_button("Detect Potholes", self.detectPotholes, relx=0.675, rely=0.20)
        self.buton_show = self.create_button("Show Image", self.show_image, relx=0.675, rely=0.30)
        self.buton_salveaza_imaginea = self.create_button("Save Image", self.save_image, relx=0.675, rely=0.40)
        self.buton_alege_video = self.create_button("Choose Video", self.select_video, relx=0.675, rely=0.55)
        self.buton_preview_videoclip = self.create_button("Preview Video", self.preview_video, relx=0.675, rely=0.65)
        self.buton_detectie_videoclip = self.create_button("Detect Potholes in Video", self.detect_video, relx=0.675, rely=0.75)
        self.buton_preview_detectie = self.create_button("View Last Detection", self.preview_detection, relx=0.675, rely=0.85)

        # Video Label
        self.video_label = tk.Label(self.frame, text="Video Loaded", font=("Arial", 8, "bold"))

        # Combo for mode selection
        self.combo = ttk.Combobox(
            self.window,
            state="readonly",
            values=["Light", "Dark"],
            width=10,
            font=("Arial", 8)
        )
        self.combo.set(self.current_mode)
        self.combo.place(relx=0.9, rely=0.95)
        self.combo.bind("<<ComboboxSelected>>", self.selection_changed)

    def create_button(self, text, command, relx, rely, width=160, height=40):
        button = tk.Button(self.frame, text=text,
                           bg="purple", fg="white",
                           activebackground="#4375b7",
                           activeforeground="white",
                           highlightcolor="red",
                           highlightthickness=2,
                           border=0,
                           font=("Arial", 8, "bold"),
                           command=command)
        button.place(relx=relx, rely=rely, width=width, height=height)
        return button

    def set_mode(self, mode):
        if mode == "Light":
            self.frame.config(bg="white")
            self.title.config(bg="white", foreground="black")
            self.video_label.config(bg="white", foreground="black")
        else:
            self.frame.config(bg="#191a1b")
            self.title.config(bg="#191a1b", foreground="white")
            self.video_label.config(bg="#191a1b", foreground="white")

    def selection_changed(self, event):
        self.set_mode(self.combo.get())
        self.master.set_theme(self.combo.get())

    def imageUpload(self):
        fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
        self.cale_poza = filedialog.askopenfilename(filetypes=fileTypes)

        if self.cale_poza:
            photo = Image.open(self.cale_poza)
            photo = photo.resize((600, 250))
            self.test_photo = ImageTk.PhotoImage(photo, master=self.window)
            self.pozaCanvas.create_image(0, 0, anchor=tk.NW, image=self.test_photo)

    def detectPotholes(self):
        if not self.cale_poza:
            messagebox.showerror("Error", "No image selected.")
            return

        self.detect_photo = hp.detect_and_annotate_image(self.cale_poza)

        if isinstance(self.detect_photo, np.ndarray):
            self.detect_photo = Image.fromarray(cv2.cvtColor(self.detect_photo, cv2.COLOR_BGR2RGB))
            self.detect_photo_resized = self.detect_photo.resize((600, 250))
            self.detect_photo_resized = ImageTk.PhotoImage(self.detect_photo_resized, master=self.window)
            self.rezultatCanvas.create_image(0, 0, anchor=tk.NW, image=self.detect_photo_resized)

    def show_image(self):
        if self.detect_photo:
            self.open_image_pil(self.detect_photo)
        else:
            messagebox.showerror("Error", "No detected image.")

    def save_image(self):
        if self.detect_photo:
            self.save_image_pil(self.detect_photo)
        else:
            messagebox.showerror("Error", "No detected image.")

    def select_video(self):
        file_types = [("Video files", "*.mp4")]
        self.cale_videoclip = filedialog.askopenfilename(filetypes=file_types)
        if self.cale_videoclip:
            self.video_label.place(relx=0.86, rely=0.570)
        else:
            self.video_label.place_forget()

    def preview_video(self):
        if self.cale_videoclip:
            self.play_video(self.cale_videoclip)
        else:
            messagebox.showerror("Error", "No video selected.")

    def detect_video(self):
        if self.cale_videoclip:
            hp.process_video(self.cale_videoclip, "../Results")
        else:
            messagebox.showerror("Error", "No video selected.")

    def preview_detection(self):
        self.play_video("../Results/results_pothole.mp4")

    def open_image_pil(self, image_pil):
        def resize_image(event):
            new_width = event.width - 2 * margin
            new_height = event.height - 2 * margin
            resized_image_pil = image_pil.resize((new_width, new_height))
            photo_img = ImageTk.PhotoImage(resized_image_pil, master=self.window)
            label.config(image=photo_img)
            label.image = photo_img

        window_img = tk.Toplevel(self.window)

        width, height = image_pil.size
        margin = 20

        screen_width = window_img.winfo_screenwidth()
        screen_height = window_img.winfo_screenheight()
        window_width = min(width + margin, screen_width)
        window_height = min(height + margin, screen_height)

        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2

        window_img.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        photo_img = ImageTk.PhotoImage(image_pil, master=self.window)

        label = tk.Label(window_img, image=photo_img)
        label.image = photo_img
        label.pack(fill=tk.BOTH, expand=True)

        window_img.bind("<Configure>", resize_image)

    def save_image_pil(self, image_pil):
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            try:
                image_pil.save(save_path)
                messagebox.showinfo("Save", f"Image saved to: {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")

    def play_video(self, video_path):
        import os

        if not os.path.isfile(video_path):
            messagebox.showerror("Error", f"Video '{video_path}' does not exist.")
            return

        def video_player():
            cap = cv2.VideoCapture(video_path)
            window_name = 'Video Player'
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                cv2.imshow(window_name, frame)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

        # Run video playback in a separate thread
        thread = threading.Thread(target=video_player)
        thread.start()

    def run(self):
        self.window.mainloop()

# # Usage
# app = PotholeDetectionApp(mode="Dark")  # or "Dark"
# app.run()