import tkinter as tk
import os
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from customElements.playerElements import invBox 
from nbtParser import parse_nbt_file  

def insert_nbt_data(tree, parent, nbt_data):
    if isinstance(nbt_data, dict):
        for key, value in nbt_data.items():
            if key == "Inventory" and isinstance(value, list):
                for i, item in enumerate(value):
                    if i < len(elements):
                        j = 0
                        while j < 9:
                            if isinstance(item, dict):
                                element.delete(0, tk.END)                  
                                # Get the directory of the script
                                script_dir = os.path.dirname(os.path.realpath(__file__))

                                # Get the filename of the ID
                                id_filename = str(item.get('id', '')).split(":")[1] + ".png"

                                # Construct the file path
                                file_path = os.path.join(script_dir, "assets", "item", id_filename)

                                # Check if the file exists
                                if not os.path.exists(file_path):
                                    print(f"File does not exist: {file_path}")
                                    file_path = os.path.join(script_dir, "assets", "not_found_icon.png")
                                else:
                                    try:
                                        # Load and display the image
                                        image = Image.open(file_path)
                                        image = image.resize((50, 50))  # Resize the image if needed
                                        photo = ImageTk.PhotoImage(image)
                                        element.image = photo  # Store a reference to the image
                                        # Display the image in the grid_box
                                        label = ttk.Label(grid_box, image=photo)
                                        label.grid(row=i, column=j, padx=5, pady=5)
                                    except Exception as e:
                                        print(f"An error occurred while loading the image: {e}")
                            print(id_filename)
                            j += 1
            elif isinstance(value, dict):
                id = tree.insert(parent, 'end', text=key)
                insert_nbt_data(tree, id, value)
            else:
                tree.insert(parent, 'end', text=f"{key}: {value}")
    else:
        tree.insert(parent, 'end', text=str(nbt_data))

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:  # Check that a file was selected
        # Parse the file
        try:
            data = parse_nbt_file(file_path)
            
            # Clear the tree view
            for i in tree.get_children():
                tree.delete(i)
            
            # Insert the parsed data into the tree view
            insert_nbt_data(tree, '', data)
        except Exception as e:
            print(f"An error occurred while parsing the file: {e}")

# Create the main window
window = tk.Tk()

#tree viewer for player nbt data
tree = ttk.Treeview(window)
tree.pack(fill=tk.BOTH, expand=True)  # Resize the tree to fit its children
tree.pack()

#visual inventory viewer
# Create a 9x4 grid box
grid_box = ttk.Frame(window)
grid_box.pack()

# Create a list to hold the elements in each square
elements = []

# Add elements to each square
for i in range(4):
    row = []
    for j in range(9):
        element = ttk.Entry(grid_box)
        element.grid(row=i, column=j, padx=5, pady=5)
        row.append(element)
    elements.append(row)


# Create a button to open the file chooser
open_button = tk.Button(window, text="Open File", command=open_file)
open_button.pack()

# Start the main event loop
window.mainloop()
