import os
from PIL import Image, ImageTk
from tkinter import Label, Tk, Canvas, Scrollbar, Frame, Button, messagebox

def confirm_selection():
    selected_image = canvas.itemcget(canvas.find_withtag("current"), "image")
    messagebox.showinfo("Selection", f"You selected: {selected_image}")
    root.destroy()

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

root = Tk()
root.title("Image Selection")
root.geometry("400x300")

canvas = Canvas(root, width=380, height=280, bg="white")
canvas.pack(side="left", fill="both", expand=True)

scrollbar = Scrollbar(root, command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind_all("<MouseWheel>", on_mousewheel)

frame = Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

script_dir = os.path.dirname(os.path.realpath(__file__))
image_dir = os.path.join(script_dir, "assets", "item")

for filename in os.listdir(image_dir):
    if filename.endswith(".png"):
        image_path = os.path.join(image_dir, filename)
        image = Image.open(image_path).resize((30, 30))
        photo = ImageTk.PhotoImage(image)
        label = Label(frame, image=photo, text=filename)
        label.pack()

confirm_button = Button(root, text="Confirm Selection", command=confirm_selection)
confirm_button.pack(pady=5)

root.mainloop()
