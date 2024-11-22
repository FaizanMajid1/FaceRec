import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
from PIL import Image, ImageTk

# Variable to store the admin password
#c
admin_password = "superhero"

# Function placeholders for the buttons
def register_face():
    global admin_password
    password = simpledialog.askstring("Admin Password", "Enter admin password:", show='*')
    if admin_password == password:
        print("Admin Authorized.")
        # Run the face_register.py script
        subprocess.run(["python3", "face_register.py"])
    else:
        print("Admin not Authorized.")
        messagebox.showerror("Authentication", "Incorrect Admin Password!")


def authenticate_face():
    print("Authenticate Face button clicked")
    # Run the authenticate.py script
    result = subprocess.run(["python3", "authenticate.py"], capture_output=True)
    if result.returncode == 0:
        # Clear the existing UI
        for widget in window.winfo_children():
            widget.destroy()

        # Load the image
        img = Image.open("unlocked.png")  # Replace 'example.png' with your image file path
        img = img.resize((150, 150), Image.LANCZOS)  # Resize the image if needed
        img_tk = ImageTk.PhotoImage(img)

        # Create a label to display the image
        label = tk.Label(window, image=img_tk, bg="#E6E6FA")
        label.image = img_tk  # Keep a reference to avoid garbage collection
        label.pack(expand=True)
    else:
        messagebox.showerror("Authentication", "Face not recognized. Please try again.")

# Create the main window
window = tk.Tk()
window.title("Facial Biometric System")

# Set the window size to maintain a 16:9 aspect ratio
width = 400
height = 200
window.geometry(f"{width}x{height}")

# Set the background color to light lavender
window.configure(bg="#E6E6FA")

# Create and place the "Register Face" button
register_button = tk.Button(window, text="Register Face", command=register_face, padx=20, pady=10)
register_button.pack(pady=20)

# Create and place the "Authenticate Face" button
authenticate_button = tk.Button(window, text="Authenticate Face", command=authenticate_face, padx=20, pady=10)
authenticate_button.pack(pady=20)

# Run the Tkinter event loop
window.mainloop()
