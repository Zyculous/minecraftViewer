import tkinter as tk
import os
from PIL import Image, ImageTk
from tkinter import Label, Toplevel



slots = {
    #offhand
    -106: (175, 155),
    #hotbar
    0: (20, 345),
    1: (65, 345),
    2: (105, 345),
    3: (145, 345),
    4: (185, 345),
    5: (225, 345),
    6: (265, 345),
    7: (305, 345),
    8: (350, 345),
    #inventory
    9: (20, 205),
    10: (60, 205),
    11: (100, 205),
    12: (140, 205),
    13: (180, 205),
    14: (220, 205),
    15: (260, 205),
    16: (300, 205),
    17: (345, 205),
    #2nd row
    18: (20, 250),
    19: (60, 250),
    20: (100, 250),
    21: (140, 250),
    22: (180, 250),
    23: (220, 250),
    24: (260, 250),
    25: (300, 250),
    26: (345, 250),
    #3rd row
    27: (20, 295),
    28: (60, 295),
    29: (100, 295),
    30: (140, 295),
    31: (180, 295),
    32: (220, 295),
    33: (260, 295),
    34: (300, 295),
    35: (345, 295),
    #armor slots
    100: (20, 155),
    101: (20, 110),
    102: (20, 65),
    103: (20, 20)    
}

def insert_nbt_data(tree, parent, nbt_data, canvas):
    if isinstance(nbt_data, dict):
        for key, value in nbt_data.items():
            if key == "Inventory" and isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):                
                        # Get the directory of the script
                        script_dir = os.path.dirname(os.path.realpath(__file__))

                        # Get the filename of the ID
                        id_filename = str(item.get('id', '')).split(":")[1]
                        
                        
                        # Construct the file path
                        model_path = os.path.join(script_dir, os.pardir, "assets", "itemModels", id_filename + ".json")
                        if os.path.exists(model_path):
                            with open(model_path, "r") as f:
                                lines = f.readlines()
                            for line in lines:
                                if line.startswith("parent"):
                                    id_filename = line.split("/")[1].split(".")[0] + ".png"
                                    break

                        file_path = os.path.join(script_dir, os.pardir, "assets", "itemTextures", id_filename + ".png")
                        # Check if the file exists
                        if not os.path.exists(file_path):
                            print(f"File does not exist: {file_path}")
                            file_path = os.path.join(script_dir, "assets", "not_found_icon.png")
                        else:
                            try:
                                
                                
                                # Load and display the image
                                image = Image.open(file_path).resize((30, 30))
                                photo = ImageTk.PhotoImage(image)
                                # Display the image in the canvas
                                slot = int(item.get('Slot', ""))
                                if slots.__contains__(slot):
                                    row, col = slots[slot]
                                    image = canvas.create_image(row, col, anchor=tk.NW, image=photo)
                                    canvas.tag_bind(image, "<Button-1>", lambda e, i=image: canvas.delete(i))
                                    
                                    label = tk.Label(image=photo, text=id_filename)
                                    label.image = photo # keep a reference!
                                else:
                                    print(f"Slot {slot} not found")
                            except Exception as e:
                                print(f"An error occurred while loading the image: {e}")
            elif isinstance(value, dict):
                id = tree.insert(parent, 'end', text=key)
                insert_nbt_data(tree, id, value, canvas)
            else:
                tree.insert(parent, 'end', text=f"{key}: {value}")
    else:
        tree.insert(parent, 'end', text=str(nbt_data))
        
def show_inv(frame, window):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    image_dir = os.path.join(script_dir, os.pardir, "assets", "item")
    
    # Create a scrollable canvas
    canvas_frame = tk.Frame(frame)
    canvas_frame.pack(fill="both", expand=True)
    canvas = tk.Canvas(canvas_frame, width=400, height=400, bg="white")
    canvas.pack(side="left", fill="both", expand=True)
    
    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Bind the scrollbar to the canvas
    def on_canvas_hover(event):
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    def on_canvas_leave(event):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", on_canvas_hover)
    canvas.bind("<Leave>", on_canvas_leave)
    x = 5
    y = 0
    window.photos = []
    for filename in os.listdir(image_dir):
        if filename.endswith(".png"):
            print(filename)
            image_path = os.path.join(image_dir, filename)
            image = Image.open(image_path).resize((30, 30))
            photo = ImageTk.PhotoImage(image)
            window.photos.append(photo)
            label = Label(canvas, image=photo, text=filename)
            img = canvas.create_image(x, y, anchor=tk.NW, image=photo)
            c = tk.Canvas(frame, width=30, height=30, bg="white")
            canvas.tag_bind(img, "<Button-1>", lambda e, p=photo, f=filename:selectPhoto(window, c, p, f))
            
            if x < 360:
                x += 30
            else:
                x = 5
                y += 30
    # Configure the canvas scroll region
    canvas.configure(scrollregion=canvas.bbox("all"))

def selectPhoto(window, canvas, photo, text):
    canvas.delete("all")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.create_text(35,0 , anchor=tk.NW, text=text)
    window.selected_photo = photo
    