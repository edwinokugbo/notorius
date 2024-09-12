import tkinter as tk
from tkinter import Text, messagebox, filedialog
from tkinter import Toplevel, Label, Button
import utils, globals
import os
import json

# Global variables to keep track of the search state
search_query = None
start_pos = "1.0"
# Track if there are any unsaved changes
is_text_modified = False

# Recent Files Feature

RECENT_FILES_PATH = "recent_files.json"

def add_to_recent_files(file_path):
    # Load recent files from the JSON file
    if os.path.exists(RECENT_FILES_PATH):
        with open(RECENT_FILES_PATH, 'r') as f:
            recent_files = json.load(f)
    else:
        recent_files = []

    # Ensure the list is unique
    if file_path in recent_files:
        recent_files.remove(file_path)

    # Add the new file to the beginning of the list
    recent_files.insert(0, file_path)

    # Keep only the last 10 files
    recent_files = recent_files[:10]

    # Save the updated list back to the JSON file
    with open(RECENT_FILES_PATH, 'w') as f:
        json.dump(recent_files, f)

def load_recent_files():
    if os.path.exists(RECENT_FILES_PATH):
        with open(RECENT_FILES_PATH, 'r') as f:
            return json.load(f)
    return []

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            globals.text_area.delete(1.0, tk.END)
            globals.text_area.insert(tk.END, file.read())
        add_to_recent_files(file_path)
        root.title(f"{os.path.basename(file_path)} - Notorius")

def open_recent_file(file_path):
    with open(file_path, "r") as file:
        globals.text_area.delete(1.0, tk.END)
        globals.text_area.insert(tk.END, file.read())
    add_to_recent_files(file_path)
    root.title(f"{os.path.basename(file_path)} - Notorius")

def update_recent_files_menu():
    recent_files_menu.delete(0, tk.END)  # Clear the menu
    recent_files = load_recent_files()
    if recent_files:
        for file in recent_files:
            recent_files_menu.add_command(label=file, command=lambda f=file: open_recent_file(f))
    else:
        recent_files_menu.add_command(label="No recent files", state=tk.DISABLED)

# End Recent Files Feature

def show_about_dialog():
    # Create a new top-level window
    about_window = Toplevel(root)
    about_window.title("About")
    about_window.geometry("300x150")
    
    # Disable resizing the About window
    about_window.resizable(False, False)
    
    # Add a label with the "About" information
    about_label = Label(about_window, text="Notorius Text Editor\nVersion 1.0\n\nCreated by Edwin Mebele Okugbo", padx=10, pady=10)
    about_label.pack(expand=True)
    
    # Add an OK button to close the dialog
    ok_button = Button(about_window, text="OK", command=about_window.destroy)
    ok_button.pack(pady=10)
    
    # Center the dialog on the screen
    about_window.update_idletasks()
    width = about_window.winfo_width()
    height = about_window.winfo_height()
    x = (about_window.winfo_screenwidth() // 2) - (width // 2)
    y = (about_window.winfo_screenheight() // 2) - (height // 2)
    about_window.geometry(f'{width}x{height}+{x}+{y}')
    
    # Make sure the About dialog is centered on the parent window
    about_window.transient(root)
    about_window.grab_set()
    root.wait_window(about_window)

def on_text_modified(event=None):
    global is_text_modified
    is_text_modified = True

def check_unsaved_changes():
    global is_text_modified
    if is_text_modified:
        response = messagebox.askyesnocancel("Unsaved Changes", 
                                             "You have unsaved changes. Do you want to save before exiting?")
        if response:  # Yes, save changes
            utils.save_file()
            return True
        elif response is None:  # Cancel, do not exit
            return False
    return True  # No unsaved changes or user chose not to save    

def on_closing():
    if check_unsaved_changes():
        root.destroy()    

# Functionality to exit the application
def exit_app():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Notorius Pad")

# Create the text area for typing
globals.text_area = Text(root, wrap='word', undo=True)
globals.text_area.pack(expand='yes', fill='both')

# Create a menu bar
menu_bar = tk.Menu(root)

# Function to apply the black theme
def apply_black_theme():
    root.configure(bg="#2e2e2e")
    globals.text_area.configure(bg="#1e1e1e", fg="#d4d4d4", insertbackground="#ffffff", 
                        selectbackground="#555555", selectforeground="#ffffff", 
                        font=("Consolas", 12), wrap=tk.WORD, undo=True)
    menu_bar.configure(bg="#2e2e2e", fg="#ffffff")
    for menu in menu_bar.winfo_children():
        menu.configure(bg="#2e2e2e", fg="#ffffff")

# Function to apply the white (default) theme
def apply_white_theme():
    root.configure(bg="#f0f0f0")
    globals.text_area.configure(bg="#ffffff", fg="#000000", insertbackground="#000000", 
                        selectbackground="#cce5ff", selectforeground="#000000", 
                        font=("Consolas", 12), wrap=tk.WORD, undo=True)
    menu_bar.configure(bg="#f0f0f0", fg="#000000")
    for menu in menu_bar.winfo_children():
        menu.configure(bg="#f0f0f0", fg="#000000")        

# File menu with options: New, Open, Save, Exit
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", accelerator="Ctrl+N", command=utils.new_file)
file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
file_menu.add_command(label="Save", accelerator="Ctrl+S", command=utils.save_file)
file_menu.add_separator()
# Create the Recent Files submenu
recent_files_menu = tk.Menu(file_menu, tearoff=False)
file_menu.add_cascade(label="Recent Files", menu=recent_files_menu)
# Add the Import submenu
import_menu = tk.Menu(file_menu, tearoff=0)
import_menu.add_command(label="Import Text", command=utils.import_text)
import_menu.add_command(label="Import PDF", command=utils.import_pdf)
import_menu.add_command(label="Import MS Word", command=utils.import_msword)
import_menu.add_command(label="Import From Link", command=utils.import_from_link)

file_menu.add_cascade(label="Import", menu=import_menu)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

# Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", command=utils.new_file)
edit_menu.add_command(label="Redo", command=utils.new_file)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=utils.select_all)
edit_menu.add_command(label="Copy", command=utils.copy)
edit_menu.add_command(label="Cut", command=utils.cut)
edit_menu.add_command(label="Paste", command=utils.paste)
edit_menu.add_separator()
edit_menu.add_command(label="Find", accelerator="Ctrl+F", command=utils.find_text)
edit_menu.add_command(label="Find Next", accelerator="F3", command=utils.find_next)
edit_menu.add_command(label="Find Previous", accelerator="Shift+F3", command=utils.find_previous)
edit_menu.add_command(label="Replace", command=utils.new_file)
edit_menu.add_command(label="Replace Next", command=utils.new_file)
edit_menu.add_command(label="Replace Previous", command=utils.new_file)
edit_menu.add_separator()
edit_menu.add_command(label="Go to...", accelerator="Ctrl+G", command=utils.go_to_line)

# Help Menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Switch To WhiteTheme", command=apply_white_theme)
help_menu.add_command(label="Switch To Black Theme", command=apply_black_theme)
help_menu.add_separator()
help_menu.add_command(label="Spell Check", command=utils.spell_check)
help_menu.add_command(label="Clear Spell Check", command=utils.clear_spell_check)
help_menu.add_separator()
help_menu.add_command(label="About", command=show_about_dialog)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Create the context menu
globals.context_menu = tk.Menu(root, tearoff=0)
globals.context_menu.add_command(label="Select All", command=utils.select_all)
globals.context_menu.add_command(label="Cut", command=utils.cut)
globals.context_menu.add_command(label="Copy", command=utils.copy)
globals.context_menu.add_command(label="Paste", command=utils.paste)
globals.context_menu.add_separator()
globals.context_menu.add_command(label="Find", command=utils.find_text)
globals.context_menu.add_command(label="Replace", command=utils.replace)
globals.context_menu.add_separator()
globals.context_menu.add_command(label="Calculate", command=utils.calculate_from_text)
globals.context_menu.add_command(label="Reformat to List", command=utils.reformat_to_list)
globals.context_menu.add_command(label="Reformat to Table", command=utils.format_to_table)
globals.context_menu.add_command(label="Save Selected Text", command=utils.save_selected_text)

# Bind the right-click to show the context menu
globals.text_area.bind("<Button-3>", utils.show_context_menu)
# Bind events to update the status bar continuously
globals.text_area.bind('<KeyRelease>', utils.update_status_bar)
globals.text_area.bind('<Button-1>', utils.update_status_bar)
globals.text_area.bind('<ButtonRelease-1>', utils.update_status_bar)  # Update on mouse release
globals.text_area.bind('<<Modified>>', utils.on_text_change)  # Update on any text change
# Bind the text area to detect modifications
globals.text_area.bind("<<Modified>>", on_text_modified)

# Apply the black theme
# apply_black_theme()

# Configure the window to use the menu
root.config(menu=menu_bar)

root.bind('<Control-n>', lambda event: utils.new_file())
root.bind('<Control-o>', lambda event: utils.open_file())
root.bind('<Control-s>', lambda event: utils.save_file())
root.bind('<Control-f>', lambda event: utils.find_text())
root.bind('<F3>', lambda event: utils.find_next())
root.bind('<Shift-F3>', lambda event: utils.find_previous())
root.bind('<Control-g>', lambda event: utils.go_to_line())

# Create a status bar
globals.status_text = tk.StringVar()
globals.status_text.set("Line: 1 | Column: 1")

status_bar = tk.Label(root, textvariable=globals.status_text, bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Update status bar on startup
utils.update_status_bar()

# Override the default window close behavior
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the application
# root.mainloop()

if __name__ == "__main__":
    # Update the recent files menu on startup
    update_recent_files_menu()
    
    root.mainloop()
