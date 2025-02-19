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
        self.build_frames()  # Corrected method name
        self.show_frame("Menu") # Corrected method name

    def build_frames(self): # Corrected method name
        self.frames["Menu"] = self.build_menu_frame() # Corrected method name
        self.frames["TextEditor"] = self.build_text_editor_frame() # Corrected method name

    def show_frame(self, page_name): # Corrected method name
        frame = self.frames[page_name]
        frame.tkraise()

    def build_menu_frame(self): # Corrected method name
        frame = tk.Frame(self.container)
        label = tk.Label(frame, text="Menu", bd=4)
        button1 = tk.Button(frame, text="Create Folder", width=12, command=self.create_folder) # Corrected method name
        button2 = tk.Button(frame, text="Open Folder", width=12, command=self.open_folder) # Corrected method name

        label.grid(row=0, column=0)
        button1.grid(row=1, column=0)
        button2.grid(row=2, column=0)

        frame.grid(row=0, column=0, sticky="nsew")
        return frame

    def build_text_editor_frame(self): # Corrected method name
        frame = tk.Frame(self.container)

        self.files_frame = tk.Frame(frame)
        self.entry = tk.Text(frame)
        label = tk.Label(frame, text="TextEditor")
        save_button = tk.Button(frame, text="Save", width=12, command=self.save_file) # Corrected method name
        new_file_button = tk.Button(frame, text="New File", width=12, command=self.new_file) # Corrected method name

        self.files_frame.grid(column=0, row=0, rowspan=3)
        self.entry.grid(column=1, row=2, columnspan=2)
        label.grid(column=1, row=0, columnspan=2)
        save_button.grid(column=1, row=3)
        new_file_button.grid(column=2, row=3)

        frame.grid(row=0, column=0, sticky="nsew")
        return frame

    def create_folder(self): # Corrected method name
        directory_path = self.get_directory_path() # Corrected method name
        if directory_path:
            new_folder_name = self.get_new_folder_name() # Corrected method name
            if new_folder_name and self.name_check(new_folder_name): # Corrected method name
                new_folder_path = os.path.join(directory_path, new_folder_name)
                try:
                    os.makedirs(new_folder_path)
                    self.initialize_text_editor(new_folder_path) # Corrected method name
                    self.show_frame("TextEditor") # Corrected method name
                    self.current_path = new_folder_path
                except OSError as e:
                    messagebox.showerror("Error", f"Could not create folder: {e}")

    def open_folder(self): # Corrected method name
        directory_path = self.get_directory_path() # Corrected method name
        if directory_path:
            self.initialize_text_editor(directory_path) # Corrected method name
            self.show_frame("TextEditor") # Corrected method name
            self.current_path = directory_path

    def initialize_text_editor(self, path): # Corrected method name
        files_frame = self.files_frame
        for widget in files_frame.winfo_children():
            widget.destroy()
        try:
            files = os.listdir(path)
            txt_files = [filename for filename in files if filename.lower().endswith(".txt")]
            for txt_file in txt_files:
                # Corrected lambda issue: Use a default argument
                txt_file_button = tk.Button(files_frame, width=24, text=txt_file, command=lambda filepath=os.path.join(path, txt_file): self.file_button(filepath)) # Corrected method name
                txt_file_button.pack(side='top')
        except FileNotFoundError:
            messagebox.showerror("Error", "Folder not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def file_button(self, filepath): # Corrected method name
        try:
            with open(filepath, 'r') as file:
                content = file.read()
                self.entry.delete("1.0", tk.END)
                self.entry.insert(tk.END, content)
            self.current_file_path = filepath
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def get_directory_path(self): # Corrected method name
        self.directory_path = filedialog.askdirectory(title="Select a Directory")
        return self.directory_path

    def get_new_folder_name(self): # Corrected method name
        new_folder_name = simpledialog.askstring(title="New Folder Name", prompt="Enter the New Folder's Name")
        return new_folder_name

    def get_new_file_name(self): # Corrected method name
        new_file_name = simpledialog.askstring(title="New File Name", prompt="Enter the New File's Name")
        return new_file_name

    def new_file(self): # Corrected method name
        if not self.current_path:
            messagebox.showinfo("Info", "Please open or create a folder first.")
            return

        new_file_name = self.get_new_file_name() # Corrected method name
        if new_file_name:  # Check if user entered a name
            new_file_path = os.path.join(self.current_path, new_file_name + ".txt")
            try:
                with open(new_file_path, 'w') as file:
                    file.write(f"New File {new_file_name} Created")
                    self.initialize_text_editor(self.current_path)
            except Exception as e:
                messagebox.showerror("Error", f"An error occured: {e}")
    
    def save_file(self):  # Corrected method name to match button command
        if not self.current_file_path:
            messagebox.showinfo("Info", "Please open or create a file to save.")
            return
        try:
            with open(self.current_file_path, 'w') as file:
                file.write("")  # Clear the file first
                contents = self.entry.get("1.0", tk.END)
                file.write(contents)
            messagebox.showinfo("Success", "File saved successfully.") #optional, but good practice
        except Exception as e:  # Catch any potential error during file saving
            messagebox.showerror("Error", f"An error occurred while saving: {e}")

    def name_check(self, name):  # Corrected method name to match button command
        invalid_chars = ("\\", "/", ":", "*", "?", "\"", "<", ">", "|")
        for char in name:
            if char in invalid_chars:
                messagebox.showinfo("Invalid Char", f"Invalid char {char} in {name}.")
                return False
        return True

if __name__ == "__main__":
    app = AthenaNoteApp()
    app.mainloop()

# Better UI