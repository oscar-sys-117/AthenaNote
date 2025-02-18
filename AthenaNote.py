import tkinter as tk
from tkinter import filedialog, messagebox

# AthenaNote Class
class AthenaNote(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("AthenaNote")
        self.geometry("400x300")
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        
        self.frames = {}
        for page in (Menu, TextEditor):
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("Menu")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class Menu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # GUI
        label = tk.Label(self, text="Menu", bd=4)
        button1 = tk.Button(self, text="Create Folder", width=12, command=lambda:CreateFolder()) 
        button2 = tk.Button(self, text="Open Folder", width=12, command=lambda:OpenFolder())
        label.grid(row = 0, column = 0) #(pady=10)
        button1.grid(row = 1, column = 0) #(side="top", pady=(0, 10))
        button2.grid(row = 2, column = 0) #(side="top", pady=(10, 0))

        # Functionality
        def NameValid(name):
            invalid_chars = ("\\", "/", ":", "*", "?", "\"", "<", ">", "|")
            for char in name:
                if char in invalid_chars:
                    messagebox.showinfo("Invalid Char", f"Invalid char {char} in name.")
                    return False
            return True
                
        def CreateFolder():
            directory_path = filedialog.askdirectory(title="Select a Directory")
            new_folder_name = # dialog for folder name
            if (directory_path != '') and NameValid(directory_path) and NameValid(new_folder_name):
                controller.show_frame("TextEditor")
            else:
                controller.show_frame("Menu")
                
        def OpenFolder():
            directory_path = filedialog.askdirectory(title="Select a Directory")
            controller.show_frame("TextEditor")

class TextEditor(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = tk.Label(self, text="TextEditor")
        label.pack(pady=10)
        
        button = tk.Button(self, text="Menu", 
                            command=lambda: controller.show_frame("Menu"))
        button.pack(pady=10)

# Initializing AthenaNote
if __name__ == "__main__":
    app = AthenaNote()
    app.mainloop()
