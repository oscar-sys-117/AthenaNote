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
        self.current_page_name = ''
        self.current_path = ''
        self.current_file_path = ''
        self.frames = {}
        self.build_frames()
        self.show_frame("Menu")
    
    def build_frames(self):
        self.frames["Menu"] = self.build_menu_frame()
        self.frames["TextEditor"] = self.build_text_editor_frame()
    
    def show_frame(self, page_name): 
        if hasattr(self, 'current_page_name'):
            previouse_page = self.current_page_name
            if previouse_page != '':
                self.frames[previouse_page].pack_forget()

        frame = self.frames[page_name]
        frame.pack(fill="both", expand=True)
        self.current_page_name = page_name
    
    def build_menu_frame(self):
        frame = tk.Frame(self.container)
        label = tk.Label(frame, text="Menu", font=("none", 20))
        label.pack()
        create_folder_frame = tk.Frame(frame)
        create_folder_button = tk.Button(create_folder_frame, text="Create Folder", width=12, command=self.create_folder)
        create_folder_button.pack(side="left")
        create_folder_label = tk.Label(create_folder_frame, text="Create a new folder to store '.txt' files.", font=("none", 12))
        create_folder_label.pack(side='left')
        open_folder_frame = tk.Frame(frame)
        open_folder_button = tk.Button(open_folder_frame, text="Open Folder", width=12, command=self.open_folder)
        open_folder_button.pack(side='left')
        open_folder_label = tk.Label(open_folder_frame, text="Open a folder to edit and add to its existing '.txt' files.", font=("none", 12))
        open_folder_label.pack(side='left')
        create_folder_frame.pack(fill="x", expand=False, padx=10, pady=10)
        open_folder_frame.pack(fill="x", expand=False, padx=10, pady=10)
        return frame

    def build_text_editor_frame(self):
        frame = tk.Frame(self.container)
        # files_frame
        self.files_frame = tk.Frame(frame)
        self.files_frame.pack(side="left", fill="y", expand=False) 
        files_container = tk.Frame(self.files_frame)
        files_container.pack(side="left", fill='y') 
        # files_container widgets
        canvas = tk.Canvas(files_container) # not the issue
        canvas.pack(side="left", fill='y', expand=False)  
        scrollbar_y = tk.Scrollbar(files_container, command=canvas.yview)
        scrollbar_y.pack(side='left', fill='y')
        canvas.config(yscrollcommand=scrollbar_y.set)
        # canvas widgets (only one instance of self.files_inner_frame)
        self.files_inner_frame = tk.Frame(canvas)  
        canvas.create_window((0, 0), window=self.files_inner_frame, anchor="nw")
        def _configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.files_inner_frame.bind("<Configure>", _configure_canvas) 
        # content_frame
        content_frame = tk.Frame(frame)
        content_frame.pack(side="left", fill="both", expand=True)
        label = tk.Label(content_frame, text="TextEditor", font=("None", 16))
        label.pack(side="top", fill="x")
        self.entry = tk.Text(content_frame)
        self.entry.pack(side="top", fill="both", expand=True)
        button_frame = tk.Frame(content_frame)
        button_frame.pack(side="top", fill="x")
        save_button = tk.Button(button_frame, text="Save", width=12, command=self.save_file)
        save_button.pack(side="top")
        new_file_button = tk.Button(button_frame, text="New File", width=12, command=self.new_file)
        new_file_button.pack(side="top")
        return frame
    
    def create_folder(self): 
        directory_path = self.get_directory_path() 
        if directory_path:
            new_folder_name = self.get_new_folder_name()
            if new_folder_name and self.name_check(new_folder_name):
                new_folder_path = os.path.join(directory_path, new_folder_name)
                try:
                    os.makedirs(new_folder_path)
                    self.initialize_text_editor(new_folder_path) 
                    self.show_frame("TextEditor") 
                    self.current_path = new_folder_path
                except OSError as e:
                    messagebox.showerror("Error", f"Could not create folder: {e}")
    
    def open_folder(self): 
        directory_path = self.get_directory_path() 
        if directory_path:
            self.initialize_text_editor(directory_path)
            self.show_frame("TextEditor") 
            self.current_path = directory_path
    
    def initialize_text_editor(self, path):
        files_frame = self.files_inner_frame
        for widget in files_frame.winfo_children():
            widget.destroy()
        try:
            files = os.listdir(path)
            txt_files = [filename for filename in files if filename.lower().endswith(".txt")]
            for txt_file in txt_files:
                txt_file_button = tk.Button(files_frame, width=24, text=txt_file, command=lambda filepath=os.path.join(path, txt_file): self.file_button(filepath)) # Corrected method name
                txt_file_button.pack(side='top')
        except FileNotFoundError:
            messagebox.showerror("Error", "Folder not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def file_button(self, filepath): 
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
        
    def get_directory_path(self): 
        self.directory_path = filedialog.askdirectory(title="Select a Directory")
        return self.directory_path
    
    def get_new_folder_name(self): 
        new_folder_name = simpledialog.askstring(title="New Folder Name", prompt="Enter the New Folder's Name")
        return new_folder_name
    
    def get_new_file_name(self): 
        new_file_name = simpledialog.askstring(title="New File Name", prompt="Enter the New File's Name")
        return new_file_name
    
    def new_file(self): 
        if not self.current_path:
            messagebox.showinfo("Info", "Please open or create a folder first.")
            return
        new_file_name = self.get_new_file_name() 
        if new_file_name: 
            new_file_path = os.path.join(self.current_path, new_file_name + ".txt")
            try:
                with open(new_file_path, 'w') as file:
                    file.write(f"New File {new_file_name} Created")
                    self.initialize_text_editor(self.current_path)
            except Exception as e:
                messagebox.showerror("Error", f"An error occured: {e}")
            
    def save_file(self): 
        if not self.current_file_path:
            messagebox.showinfo("Info", "Please open or create a file to save.")
            return
        try:
            with open(self.current_file_path, 'w') as file:
                file.write("") 
                contents = self.entry.get("1.0", tk.END)
                file.write(contents)
                messagebox.showinfo("Success", "File saved successfully.") 
        except Exception as e: 
            messagebox.showerror("Error", f"An error occurred while saving: {e}")
        
    def name_check(self, name): 
        invalid_chars = ("\\", "/", ":", "*", "?", "\"", "<", ">", "|")
        for char in name:
            if char in invalid_chars:
                messagebox.showinfo("Invalid Char", f"Invalid char {char} in {name}.")
                return False
        return True

if __name__ == "__main__":
    app = AthenaNoteApp()
    app.mainloop()
# Add scrollbar to TextEditor