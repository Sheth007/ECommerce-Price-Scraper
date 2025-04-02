import tkinter as tk
import subprocess
from tkinter import messagebox
import sys

# Function to run the file (script or executable)
def run_file(file_path):
    try:
        if sys.platform == "win32":
            subprocess.run([sys.executable, file_path], check=True)
        else:
            subprocess.run(["python", file_path], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run the file: {e}")

#main screen
root = tk.Tk()
root.geometry("400x200")
root.title("Price Scraper Tools")

label = tk.Label(root, text="Choose where to search 🔎", font=('Arial', 18))
label.pack(pady=50)

#put the button horizontally
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

#creating 2 buttons
button1 = tk.Button(button_frame, text="E_Commerce", width=20, command=lambda: run_file("E_Commerce.py"))
button1.pack(side=tk.LEFT, padx=20)

button2 = tk.Button(button_frame, text="Quick_Commerce", width=20, command=lambda: run_file("Quick_Commerce.py"))
button2.pack(side=tk.LEFT, padx=20)

root.mainloop()