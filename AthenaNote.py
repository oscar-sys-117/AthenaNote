import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class AthenaNoteApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("AthenaNote")
        self.geometry("400x300")
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.current_path = ''
        self.current_file_path = ''
        self.frames = {}
        self.BuildFrames()
        self.ShowFrame("Menu")

    # Frame Methods 
    def BuildFrames(self):
        self.frames["Menu"] = self.BuildMenuFrame()
        self.frames["TextEditor"] = self.BuildTextEditorFrame()

    def ShowFrame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()        
    
    def BuildMenuFrame(self):
        frame = tk.Frame(self.container)
        label = tk.Label(frame, text="Menu", bd=4)
        button1 = tk.Button(frame, text="Create Folder", width=12, command=lambda:self.CreateFolder())
        button2 = tk.Button(frame, text="Open Folder", width=12, command=lambda:self.OpenFolder())
        label.grid(row=0, column=0)
        button1.grid(row=1, column=0)
        button2.grid(row=2, column=0)
        frame.grid(row=0, column=0, sticky="nsew")

        '''frame = tk.Frame(self.container, padx=20, pady=20)  # Add padding around the frame
        label = tk.Label(frame, text="Menu", font=("Arial", 16, "bold")) # Styling the label
        label.grid(row=0, column=0, sticky="ew")  # Make label stretch horizontally
        button1 = tk.Button(frame, text="Create Folder", width=15, command=lambda:self.CreateFolder(),  # Increased width
                        font=("Arial", 12), pady=5)  # Styling the button
        button1.grid(row=1, column=0, sticky="ew", pady=(5,0)) # Make button stretch horizontally and add padding
        button2 = tk.Button(frame, text="Open Folder", width=15, command=lambda:self.OpenFolder(),
                            font=("Arial", 12), pady=5)  # Styling the button
        button2.grid(row=2, column=0, sticky="ew", pady=(5,0)) # Make button stretch horizontally and add padding
        # Configure grid to make the frame expand nicely
        frame.columnconfigure(0, weight=1)  # Make column 0 expand
        frame.rowconfigure(0, weight=0) # Make row 0 not expand, since it contains the title
        frame.rowconfigure(1, weight=0) # Make row 1 not expand, since it contains a button
        frame.rowconfigure(2, weight=0) # Make row 2 not expand, since it contains a button
        frame.rowconfigure(3, weight=1) # Make row 3 expand, to center the elements
        return frame'''

    def BuildTextEditorFrame(self):
        frame = tk.Frame(self.container)
        
        self.files_frame = tk.Frame(frame)
        self.entry = tk.Text(frame)
        label = tk.Label(frame, text="TextEditor")
        save_button = tk.Button(frame, text="Save", width=12, command=lambda:self.SaveFile(self.current_file_path))
        new_file_button = tk.Button(frame, text="New File", width=12, command=lambda:self.NewFile(self.current_path))
        
        self.files_frame.grid(column=0, row=0, rowspan=3)
        self.entry.grid(column=1, row=2, columnspan=2)
        label.grid(column=1, row=0, columnspan=2)
        save_button.grid(column=1, row=3)
        new_file_button.grid(column=2, row=3)
        
        frame.grid(row=0, column=0, sticky="nsew")
        return frame
    
    # Menu Methods
    def CreateFolder(self):
        directory_path = self.GetDirectoryPath()
        if directory_path: 
            new_folder_name = self.GetNewFolderName()
            if new_folder_name and self.NameCheck(new_folder_name):
                new_folder_path = os.path.join(directory_path, new_folder_name)
                try:
                    os.makedirs(new_folder_path)
                    self.InitializeTextEditor(new_folder_path)
                    self.ShowFrame("TextEditor")
                    self.current_path = new_folder_path
                except OSError as e:
                    messagebox.showerror("Error", f"Could not create new folder: {e}")
    
    def OpenFolder(self):
        directory_path = self.GetDirectoryPath()
        if directory_path:
            self.InitializeTextEditor(directory_path)
            self.ShowFrame("TextEditor")
            self.current_path = directory_path

    # TextEditor Methods
    def InitializeTextEditor(self, path):
        files_frame = self.files_frame
        for widget in files_frame.winfo_children():
            widget.destroy()
        try:
            files = os.listdir(path)
            txt_files = [filename for filename in files if filename.lower().endswith(".txt")]
            for txt_file in txt_files:
                txt_file_button = tk.Button(files_frame, width=24, text=txt_file, command=lambda filepath=os.path.join(path, txt_file): self.FileButton(filepath))
                txt_file_button.pack(side='top')
        except FileNotFoundError:
            messagebox.showerror("Error", "Folder not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occured: {e}")
    
    def FileButton(self, filepath):
        try:
            with open(filepath, 'r') as file:
                content = file.read()
                self.entry.delete("1.0", tk.END)
                self.entry.insert(tk.END, content)
            self.current_file_path = filepath
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occured: {e}")

    def GetDirectoryPath(self):
        self.directory_path = filedialog.askdirectory(title="Select a Directory")
        return self.directory_path
    
    def GetNewFolderName(self):
        new_folder_name = simpledialog.askstring(title="New Folder Name", prompt="Enter the New Folder's Name")
        return new_folder_name
    
    def GetNewFileName(self):
        new_file_name = simpledialog.askstring(title="New File Name", prompt="Enter the New File's Name")
        return new_file_name
    
    def NewFile(self, path):
        if not self.current_path:
            messagebox.showinfo("Info", "Please open or create a folder first.")
            return
        new_file_name = self.GetNewFileName() + ".txt"
        if new_file_name: 
            new_file_path = os.path.join(path, new_file_name)
            try:
                with open(new_file_path, 'w') as file:
                    file.write(f"New File {new_file_name} Created")
                    self.InitializeTextEditor(self.current_path)
                messagebox.showinfo("Success", "File created successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occured: {e}")
    
    def SaveFile(self, path):
        if not self.current_file_path:
            messagebox.showinfo("Info", "Please open or create a file to save.")
            return
        try:
            with open(path, 'w') as file:
                file.write("")
                contents = self.entry.get("1.0", tk.END)
                file.write(contents)
            messagebox.showinfo("Success", "File saved sucessfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occured: {e}")

    def NameCheck(self, name):
        invalid_chars = ("\\", "/", ":", "*", "?", "\"", "<", ">", "|")
        for char in name:
            if char in invalid_chars:
                messagebox.showinfo("Invalid Char", f"Invalid char {char} in {name}.")
                return False
        return True

# Initializing AthenaNote
if __name__ == "__main__":
    app = AthenaNoteApp()
    app.mainloop()

# Better UI
