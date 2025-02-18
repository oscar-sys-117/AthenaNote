import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

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
        button1 = tk.Button(self, text="Create Folder", width=12, command=lambda:CreateFolderButtonFunctionality()) 
        button2 = tk.Button(self, text="Open Folder", width=12, command=lambda:OpenFolderButtonFunctionality())
        label.grid(row = 0, column = 0) #(pady=10)
        button1.grid(row = 1, column = 0) #(side="top", pady=(0, 10))
        button2.grid(row = 2, column = 0) #(side="top", pady=(10, 0))

        # Functions
        def NameCheck(name):
            invalid_chars = ("\\", "/", ":", "*", "?", "\"", "<", ">", "|")
            for char in name:
                if char in invalid_chars:
                    messagebox.showinfo("Invalid Char", f"Invalid char {char} in {name}.")
                    return False
            return True
        def GetDirectoryPath():
            directory_path = filedialog.askdirectory(title="Select a Directory")
            return directory_path
        def GetNewFolderName():
            new_folder_name = simpledialog.askstring(title="New Folder Name", prompt="Enter the New Folders Name")
            return new_folder_name
        def InitializeTextEditor():
            print()
        # Button Functionality
        def CreateFolderButtonFunctionality():
            directory_path = GetDirectoryPath
            new_folder_name = GetNewFolderName
            if (directory_path != '') and NameCheck(new_folder_name):
                new_folder_path = os.path.join(directory_path, new_folder_name)
                InitializeTextEditor(new_folder_path)
                controller.show_frame("TextEditor")
            else:
                controller.show_frame("Menu")
        def OpenFolderButtonFunctionality():
            directory_path = GetDirectoryPath()
            if (directory_path != ""):
                InitializeTextEditor(directory_path)
            else:
                controller.show_frame("menu")

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
# Create popup to get the new folder name in CreateFolder()
# 