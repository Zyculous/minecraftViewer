import tkinter as tk
import os
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from nbtParser import parse_nbt_file  
from inventory.playerInvTree import insert_nbt_data

def open_file(canvas):
    canvas.delete("all")
    img = ImageTk.PhotoImage(Image.open("assets/inventory.png").resize((400, 400)))
    canvas.background = img
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    file_path = filedialog.askopenfilename()
    if file_path:  # Check that a file was selected
        # Parse the file
        try:
            data = parse_nbt_file(file_path)
            
            # Clear the tree view
            for i in tree.get_children():
                tree.delete(i)
            
            # Insert the parsed data into the tree view
            insert_nbt_data(tree, '', data, canvas)
        except Exception as e:
            print(f"An error occurred while parsing the file: {e}")

# Create the main window
window = tk.Tk()

#tree viewer for player nbt data
tree = ttk.Treeview(window)
tree.pack(fill="x", expand=True)  # Resize the tree to fit its children

#visual inventory viewer
# Create a 9x4 grid box
canvas = tk.Canvas(window, width=400, height=400, bg="white")
canvas.pack(fill="both", expand=True)


img = ImageTk.PhotoImage(Image.open("assets/inventory.png").resize((400, 400)))
canvas.background = img
canvas.create_image(0, 0, anchor=tk.NW, image=img)

# Create a button to open the file chooser
open_button = tk.Button(window, text="Open File", command=lambda:open_file(canvas))
open_button.pack()

# Start the main event loop
window.mainloop()
