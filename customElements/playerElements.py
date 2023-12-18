import tkinter as tk
from PIL import ImageTk, Image

class invBox(tk.Frame):
    def __init__(self, master=None, image=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.entry = tk.Entry(self)
        self.entry.pack(side=tk.LEFT)
        
        if image:
            self.image = image
            self.image_label = tk.Label(self, image=self.image)
            self.image_label.pack(side=tk.LEFT)
    def delete(self, start, end):
        self.entry.delete(start, end)
    def get(self):
        return self.entry.get()
    
    def set(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def focus(self):
        self.entry.focus_set()
