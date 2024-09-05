import tkinter as tk
import helpers.helpersWindows as hw
from PIL import ImageTk, Image
from tkinter import ttk
from subWindows.WindowPotholes import PotholeDetectionApp
from subWindows.WindowLitter import LitterDetectionApp


class MainWindow:
    def __init__(self, mode="Light"):
        self.root = tk.Tk()
        self.root.title('Urban Scan')
        self.root.resizable(False, False)
        hw.center_window(self.root, 500, 500)

        self.current_mode = mode

        self.frame = tk.Frame(self.root, bg='white')
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()
        self.current_mode = mode
        self.set_mode(mode)

    def create_widgets(self):
        # Canvas for logo
        self.canvas = tk.Canvas(self.frame, bg="white", width=200, height=200, bd=0, highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        # Load and display logo
        image_path = 'assets//logo.png'
        photo = Image.open(image_path)
        photo = photo.resize((200, 200))
        self.logo = ImageTk.PhotoImage(photo)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.logo)

        # Potholes Detection button
        self.button_potholes = tk.Button(self.frame,
                                         text="Pothole Detection",
                                         bg="purple",
                                         fg="white",
                                         activebackground="#4375b7",
                                         activeforeground="white",
                                         highlightcolor="red",
                                         highlightthickness=2,
                                         border=0,
                                         font=("Arial", 8, "bold"),
                                         command=self.open_pothole_window)
        self.button_potholes.place(relx=0.5, rely=0.57, anchor=tk.CENTER, width=120, height=40)

        # Litter Detection button
        self.button_litter = tk.Button(self.frame,
                                       text="Litter Detection",
                                       bg="purple",
                                       fg="white",
                                       activebackground="#4375b7",
                                       activeforeground="white",
                                       highlightcolor="red",
                                       highlightthickness=2,
                                       border=0,
                                       font=("Arial", 8, "bold"),
                                       command=self.open_litter_window)
        self.button_litter.place(relx=0.5, rely=0.70, anchor=tk.CENTER, width=120, height=40)

        # Theme selection combo
        self.combo = ttk.Combobox(
            self.root,
            state="readonly",
            values=["Light", "Dark"],
            width=10
        )
        self.combo.set(self.current_mode)
        self.combo.place(relx=0.8, rely=0.9)
        self.combo.bind("<<ComboboxSelected>>", self.selection_changed)

    def set_theme(self, mode):
        self.current_mode = mode
        self.set_mode(mode)
    def set_mode(self, mode):
        if mode == "Light":
            self.frame.config(bg="white")
            self.canvas.config(bg="white")
        else:
            self.frame.config(bg="#191a1b")
            self.canvas.config(bg="#191a1b")

    def selection_changed(self, event):
        self.current_mode = self.combo.get()
        self.set_mode(self.current_mode)

    def open_litter_window(self):
        self.root.withdraw()  # Ascunde fereastra principală
        litter_window = LitterDetectionApp(self, self.current_mode)  # Transmite tema curentă și self
        litter_window.window.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(litter_window))
        litter_window.window.mainloop()

    def open_pothole_window(self):
        self.root.withdraw()  # Hide the main window
        pothole_window = PotholeDetectionApp(self, self.current_mode)  # Pass the current theme mode
        pothole_window.window.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(pothole_window))
        pothole_window.window.mainloop()

    def on_child_close(self, child_window):
        child_window.window.destroy()
        self.root.deiconify()

    def run(self):
        self.root.mainloop()


# Usage
if __name__ == "__main__":
    app = MainWindow(mode="Light")
    app.run()
