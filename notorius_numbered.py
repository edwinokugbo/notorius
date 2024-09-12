import tkinter as tk
from tkinter import filedialog, Text, simpledialog, messagebox
import re


class TextWithLineNumbers(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.text_area = tk.Text(self, wrap=tk.WORD, undo=True)
        self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.line_numbers = tk.Text(self, width=4, padx=3, takefocus=0, border=0,
                                    background='lightgrey', state='disabled', wrap='none')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_area.bind('<KeyPress>', self.update_line_numbers)
        self.text_area.bind('<MouseWheel>', self.sync_scroll)
        self.text_area.bind('<Button-1>', self.update_line_numbers)
        self.text_area.bind('<KeyRelease>', self.update_line_numbers)
        self.text_area.bind('<FocusIn>', self.update_line_numbers)
        self.text_area.bind('<Configure>', self.update_line_numbers)

        # Setup scroll command
        self.text_area.config(yscrollcommand=self.sync_scroll)
        self.line_numbers.config(yscrollcommand=self.sync_scroll)

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete('1.0', tk.END)

        current_line, _ = self.text_area.index(tk.END).split('.')
        line_number_content = "\n".join(str(i) for i in range(1, int(current_line)))

        self.line_numbers.insert('1.0', line_number_content)
        self.line_numbers.config(state=tk.DISABLED)

    def sync_scroll(self, *args):
        # Sync the line number and text area scrollbars
        if len(args) == 1:
            self.line_numbers.yview_moveto(self.text_area.yview()[0])
        elif len(args) == 2:
            self.line_numbers.yview(*args)
        self.text_area.yview(*args)

# Global variables to keep track of the search state
search_query = None
start_pos = "1.0"

# Functionality to open a file
def open_file():
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())

# Functionality to save the current file
def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))

# Functionality to create a new file (clears the current text)
def new_file():
    text_area.delete(1.0, tk.END)

# Functionality to find text in the text area
def find_text():
    global search_query, start_pos
    
    # Check if there's selected text
    selected_text = text_area.selection_get() if text_area.tag_ranges("sel") else ""
    
    # Prompt the user with the selected text pre-filled
    search_query = simpledialog.askstring("Find", "Enter text to find:", initialvalue=selected_text)

    start_pos = "1.0"  # Start at the beginning of the document
    if search_query:
        start_pos = text_area.search(search_query, "1.0", stopindex=tk.END)
        if start_pos:
            end_pos = f"{start_pos}+{len(search_query)}c"
            text_area.tag_remove("found", "1.0", tk.END)
            text_area.tag_add("found", start_pos, end_pos)
            text_area.tag_config("found", background="yellow", foreground="black")
            text_area.mark_set(tk.INSERT, end_pos)
            text_area.see(tk.INSERT)
            start_pos = end_pos  # Update start_pos to the end of the found text
        else:
            messagebox.showinfo("Find", "Text not found.")
            start_pos = None  # Reset start_pos after reaching the end

def find_next():
    global start_pos
    if search_query:
        # Start searching from just after the current match (or the current cursor position)
        if start_pos:
            start_pos = text_area.index(f"{start_pos}+1c")  # Move one character forward
        else:
            start_pos = text_area.index(tk.INSERT)  # Start from the current cursor position

        pos = text_area.search(search_query, start_pos, stopindex=tk.END)
        if pos:
            end_pos = f"{pos}+{len(search_query)}c"
            text_area.tag_remove("found", "1.0", tk.END)
            text_area.tag_add("found", pos, end_pos)
            text_area.tag_config("found", background="yellow", foreground="black")
            text_area.mark_set(tk.INSERT, end_pos)
            text_area.see(tk.INSERT)
            start_pos = end_pos  # Update start_pos to the end of the found text
        else:
            messagebox.showinfo("End of Document", "No more occurrences found.")
            start_pos = None  # Reset start_pos after reaching the end

def find_previous():
    global start_pos
    if search_query:
        # Start searching from just before the current match (or the current cursor position)
        if start_pos:
            start_pos = text_area.index(f"{start_pos}-1c")  # Move one character backward
        else:
            start_pos = text_area.index(tk.INSERT)  # Start from the current cursor position

        pos = text_area.search(search_query, start_pos, stopindex="1.0", backwards=True)
        if pos:
            end_pos = f"{pos}+{len(search_query)}c"
            text_area.tag_remove("found", "1.0", tk.END)
            text_area.tag_add("found", pos, end_pos)
            text_area.tag_config("found", background="yellow", foreground="black")
            text_area.mark_set(tk.INSERT, pos)
            text_area.see(tk.INSERT)
            start_pos = pos  # Update start_pos to the start of the found text
        else:
            messagebox.showinfo("Start of Document", "No more occurrences found.")
            start_pos = None  # Reset start_pos after reaching the start

def replace():
    find_text = simpledialog.askstring("Find", "Enter text to find:")
    replace_text = simpledialog.askstring("Replace", "Enter text to replace with:")
    if find_text and replace_text:
        content = text_area.get("1.0", tk.END)
        new_content = content.replace(find_text, replace_text)
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, new_content)

def go_to_line():
    line_number = simpledialog.askinteger("Go to Line", "Enter line number:")
    if line_number is not None:
        text_area.mark_set(tk.INSERT, f"{line_number}.0")
        text_area.see(tk.INSERT)

def select_all():
    text_area.tag_add("sel", "1.0", "end")

def cut():
    text_area.event_generate("<<Cut>>")

def copy():
    text_area.event_generate("<<Copy>>")

def paste():
    text_area.event_generate("<<Paste>>")

def show_context_menu(event):
    try:
        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()

def calculate_from_text():
    # Check if there's selected text
    selected_text = text_area.selection_get() if text_area.tag_ranges("sel") else ""

    if selected_text:
        result = compute_expression(selected_text)
        print(f"The result of the expression is: {result}")

        new_content = selected_text + ' = ' + str(result)
        replace_selected_text(new_content)
    else:
        print('No Selected Text')

def compute_expression(input_string):
    # Step 1: Remove all characters that are not digits or mathematical operators
    cleaned_string = re.sub(r'[^0-9+\-*/]', '', input_string)
    
    try:
        # Step 2: Compute the mathematical result of the cleaned string
        result = eval(cleaned_string)
    except (SyntaxError, ZeroDivisionError) as e:
        return f"Error in expression: {str(e)}"

    return result

def replace_selected_text(new_text):
    try:
        # Get the current selection's start and end positions
        start_pos = text_area.index(tk.SEL_FIRST)
        end_pos = text_area.index(tk.SEL_LAST)
        
        # Delete the selected text
        text_area.delete(start_pos, end_pos)
        
        # Insert the new text at the position of the original selection
        text_area.insert(start_pos, new_text)
        
        # Optionally, re-select the new text
        text_area.tag_add("sel", start_pos, f"{start_pos}+{len(new_text)}c")
    
    except tk.TclError:
        # If there's no selection, show a message
        messagebox.showinfo("Replace", "No text selected.")

# Functionality to exit the application
def exit_app():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Notorius Pad")

# Create the text area for typing
text_area = TextWithLineNumbers(root)
text_area.pack(expand='yes', fill='both')

# Create a menu bar
menu_bar = tk.Menu(root)

# File menu with options: New, Open, Save, Exit
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", accelerator="Ctrl+N", command=new_file)
file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

# Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", command=new_file)
edit_menu.add_command(label="Redo", command=new_file)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=new_file)
edit_menu.add_command(label="Copy", command=new_file)
edit_menu.add_command(label="Cut", command=new_file)
edit_menu.add_command(label="Paste", command=new_file)
edit_menu.add_separator()
edit_menu.add_command(label="Find", accelerator="Ctrl+F", command=find_text)
edit_menu.add_command(label="Find Next", accelerator="F3", command=find_next)
edit_menu.add_command(label="Find Previous", accelerator="Shift+F3", command=find_previous)
edit_menu.add_command(label="Replace", command=new_file)
edit_menu.add_command(label="Replace Next", command=new_file)
edit_menu.add_command(label="Replace Previous", command=new_file)
edit_menu.add_separator()
edit_menu.add_command(label="Go to...", accelerator="Ctrl+G", command=go_to_line)

# Help Menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=new_file)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Create the context menu
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Select All", command=select_all)
context_menu.add_command(label="Cut", command=cut)
context_menu.add_command(label="Copy", command=copy)
context_menu.add_command(label="Paste", command=paste)
context_menu.add_separator()
context_menu.add_command(label="Find", command=find_text)
context_menu.add_command(label="Replace", command=replace)
context_menu.add_separator()
context_menu.add_command(label="Calculate", command=calculate_from_text)

# Bind the right-click to show the context menu
text_area.bind("<Button-3>", show_context_menu)

# Configure the window to use the menu
root.config(menu=menu_bar)

root.bind('<Control-n>', lambda event: new_file())
root.bind('<Control-o>', lambda event: open_file())
root.bind('<Control-s>', lambda event: save_file())
root.bind('<Control-f>', lambda event: find_text())
root.bind('<F3>', lambda event: find_next())
root.bind('<Shift-F3>', lambda event: find_previous())

# Run the application
root.mainloop()
