import tkinter as tk
import os
from PIL import Image, ImageTk

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
                        id_filename = str(item.get('id', '')).split(":")[1] + ".png"
                        
                        
                        # Construct the file path
                        file_path = os.path.join(script_dir, os.pardir, "assets", "item", id_filename)

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