import tkinter as tk
from tkinter import filedialog, Text, simpledialog, messagebox
import re, os
import globals
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import docx  # python-docx
from spellchecker import SpellChecker
from tkinter import messagebox

# Functionality to open a file
def open_file():
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "r") as file:
            globals.text_area.delete(1.0, tk.END)
            globals.text_area.insert(tk.END, file.read())

# Functionality to save the current file
def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(globals.text_area.get(1.0, tk.END))

# Functionality to create a new file (clears the current text)
def new_file():
    globals.text_area.delete(1.0, tk.END)

# Functionality to find text in the text area
def find_text():
    global search_query, start_pos
    
    # Check if there's selected text
    selected_text = globals.text_area.selection_get() if globals.text_area.tag_ranges("sel") else ""
    
    # Prompt the user with the selected text pre-filled
    search_query = simpledialog.askstring("Find", "Enter text to find:", initialvalue=selected_text)

    start_pos = "1.0"  # Start at the beginning of the document
    if search_query:
        start_pos = globals.text_area.search(search_query, "1.0", stopindex=tk.END)
        if start_pos:
            end_pos = f"{start_pos}+{len(search_query)}c"
            globals.text_area.tag_remove("found", "1.0", tk.END)
            globals.text_area.tag_add("found", start_pos, end_pos)
            globals.text_area.tag_config("found", background="yellow", foreground="black")
            globals.text_area.mark_set(tk.INSERT, end_pos)
            globals.text_area.see(tk.INSERT)
            start_pos = end_pos  # Update start_pos to the end of the found text
        else:
            messagebox.showinfo("Find", "Text not found.")
            start_pos = None  # Reset start_pos after reaching the end

def find_next():
    global start_pos
    if search_query:
        # Start searching from just after the current match (or the current cursor position)
        if start_pos:
            start_pos = globals.text_area.index(f"{start_pos}+1c")  # Move one character forward
        else:
            start_pos = globals.text_area.index(tk.INSERT)  # Start from the current cursor position

        pos = globals.text_area.search(search_query, start_pos, stopindex=tk.END)
        if pos:
            end_pos = f"{pos}+{len(search_query)}c"
            globals.text_area.tag_remove("found", "1.0", tk.END)
            globals.text_area.tag_add("found", pos, end_pos)
            globals.text_area.tag_config("found", background="yellow", foreground="black")
            globals.text_area.mark_set(tk.INSERT, end_pos)
            globals.text_area.see(tk.INSERT)
            start_pos = end_pos  # Update start_pos to the end of the found text
        else:
            messagebox.showinfo("End of Document", "No more occurrences found.")
            start_pos = None  # Reset start_pos after reaching the end

def find_previous():
    global start_pos
    if search_query:
        # Start searching from just before the current match (or the current cursor position)
        if start_pos:
            start_pos = globals.text_area.index(f"{start_pos}-1c")  # Move one character backward
        else:
            start_pos = globals.text_area.index(tk.INSERT)  # Start from the current cursor position

        pos = globals.text_area.search(search_query, start_pos, stopindex="1.0", backwards=True)
        if pos:
            end_pos = f"{pos}+{len(search_query)}c"
            globals.text_area.tag_remove("found", "1.0", tk.END)
            globals.text_area.tag_add("found", pos, end_pos)
            globals.text_area.tag_config("found", background="yellow", foreground="black")
            globals.text_area.mark_set(tk.INSERT, pos)
            globals.text_area.see(tk.INSERT)
            start_pos = pos  # Update start_pos to the start of the found text
        else:
            messagebox.showinfo("Start of Document", "No more occurrences found.")
            start_pos = None  # Reset start_pos after reaching the start

def replace():
    find_text = simpledialog.askstring("Find", "Enter text to find:")
    replace_text = simpledialog.askstring("Replace", "Enter text to replace with:")
    if find_text and replace_text:
        content = globals.text_area.get("1.0", tk.END)
        new_content = content.replace(find_text, replace_text)
        globals.text_area.delete("1.0", tk.END)
        globals.text_area.insert(tk.END, new_content)

def go_to_line():
    line_number = simpledialog.askinteger("Go to Line", "Enter line number:")
    if line_number is not None:
        globals.text_area.mark_set(tk.INSERT, f"{line_number}.0")
        globals.text_area.see(tk.INSERT)

def select_all():
    globals.text_area.tag_add("sel", "1.0", "end")

def cut():
    globals.text_area.event_generate("<<Cut>>")

def copy():
    globals.text_area.event_generate("<<Copy>>")

def paste():
    globals.text_area.event_generate("<<Paste>>")

def show_context_menu(event):
    try:
        globals.context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        globals.context_menu.grab_release()

def calculate_from_text():
    # Check if there's selected text
    selected_text = globals.text_area.selection_get() if globals.text_area.tag_ranges("sel") else ""

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
        start_pos = globals.text_area.index(tk.SEL_FIRST)
        end_pos = globals.text_area.index(tk.SEL_LAST)
        
        # Delete the selected text
        globals.text_area.delete(start_pos, end_pos)
        
        # Insert the new text at the position of the original selection
        globals.text_area.insert(start_pos, new_text)
        
        # Optionally, re-select the new text
        globals.text_area.tag_add("sel", start_pos, f"{start_pos}+{len(new_text)}c")
    
    except tk.TclError:
        # If there's no selection, show a message
        messagebox.showinfo("Replace", "No text selected.")

def update_status_bar(event=None):
    line, column = globals.text_area.index(tk.INSERT).split('.')
    content = globals.text_area.get("1.0", tk.END)
    
    # Calculate the number of characters (excluding the last newline)
    num_chars = len(content) - 1
    
    # Calculate the number of words
    num_words = len(content.split())
    
    globals.status_text.set(f"Line: {line} | Column: {int(column) + 1} | Characters: {num_chars} | Words: {num_words}")     

def on_text_change(event=None):
    update_status_bar()    

def import_text():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
        globals.text_area.insert(tk.END, content)

def import_pdf():
    # Step 1: Open a dialog to select a PDF file
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

    if file_path:
        try:
            # Step 2: Extract text from the PDF file
            pdf_document = fitz.open(file_path)
            pdf_text = ""
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                pdf_text += page.get_text()

            # Close the PDF document
            pdf_document.close()

            # Step 3: Append the text to text_area
            globals.text_area.insert(tk.END, pdf_text)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to read the PDF file: {e}")

def import_msword():
    # Step 1: Open a dialog to select a Microsoft Word file
    file_path = filedialog.askopenfilename(filetypes=[("Word files", "*.docx")])

    if file_path:
        try:
            # Step 2: Extract text from the Word file
            doc = docx.Document(file_path)
            doc_text = ""
            for paragraph in doc.paragraphs:
                doc_text += paragraph.text + "\n"

            # Step 3: Append the text to text_area
            globals.text_area.insert(tk.END, doc_text)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to read the Word file: {e}") 

def clean_text(text):
    # Step 1: Remove leading and trailing whitespace
    text = text.strip()
    
    # Step 2: Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Step 3: Normalize newlines to single newlines
    # text = re.sub(r'(\n\s*)+', '\n', text)
    
    return text    

def import_from_link():
    # Step 1: Open a dialog to ask for the web link
    url = simpledialog.askstring("Import From Link", "Enter the URL:")

    if url:
        try:
            # Step 2: Fetch the page content
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes

            # Step 3: Parse the page content and extract text
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text()            

            # Step 4: Clean the extracted text
            cleaned_text = clean_text(page_text)
            print(cleaned_text)

            # Step 5: Append the cleaned text to text_area
            globals.text_area.insert(tk.END, cleaned_text)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve the webpage: {e}")

def reformat_to_list():
    try:
        # Get the selected text
        selected_text = globals.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        
        # Split the selected text into lines
        lines = selected_text.splitlines()
        
        # Reformat each line into a numbered list
        numbered_lines = [f"{i + 1}. {line}" for i, line in enumerate(lines)]
        
        # Join the numbered lines back into a single string
        formatted_text = "\n".join(numbered_lines)
        
        # Replace the selected text with the formatted text
        globals.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        globals.text_area.insert(tk.INSERT, formatted_text)
    
    except tk.TclError:
        messagebox.showwarning("No Selection", "Please select some text to reformat.")

def save_selected_text():
    try:
        # Step 1: Get the selected text from the text_area
        selected_text = globals.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        
        # Step 2: Display a dialog to enter a file name
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                 filetypes=[("Text files", "*.txt")],
                                                 title="Save or Append to File")

        if file_path:
            try:
                # Step 3: Check if file exists and determine mode (write or append)
                mode = 'a' if os.path.exists(file_path) else 'w'
                
                # Step 4: Save or append the selected text to the file
                with open(file_path, mode) as file:
                    if mode == 'a':
                        file.write("\n")  # Ensure there is a new line before appending
                    file.write(selected_text)
                
                messagebox.showinfo("Success", "Text saved successfully.")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save text: {e}")
    
    except tk.TclError:
        messagebox.showwarning("No Selection", "Please select some text to save.")

def format_to_table():
    # Get the selected text
    selected_text = globals.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
    
    # Split the selected text into lines and then into words
    lines = [line.split() for line in selected_text.splitlines()]
    
    # Find the maximum length for each column
    max_lengths = [max(len(word) for word in column) for column in zip(*lines)]
    
    # Format each line to align columns
    formatted_lines = []
    for line in lines:
        formatted_line = "\t".join(f"{word.ljust(max_lengths[i])}" for i, word in enumerate(line))
        formatted_lines.append(formatted_line)
    
    # Join the formatted lines back into a single string
    formatted_text = "\n".join(formatted_lines)
    
    # Replace the selected text with the formatted text
    globals.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
    globals.text_area.insert(tk.INSERT, formatted_text)        

def spell_check():
    # Create a SpellChecker object
    spell = SpellChecker()

    # Get the content from the text area
    text_content = globals.text_area.get("1.0", "end-1c")
    words = text_content.split()

    # Find the misspelled words
    misspelled = spell.unknown(words)

    # Highlight misspelled words
    globals.text_area.tag_remove('misspelled', '1.0', 'end')
    for word in misspelled:
        start_index = '1.0'
        while True:
            start_index = globals.text_area.search(word, start_index, nocase=True, stopindex='end')
            if not start_index:
                break
            end_index = f"{start_index}+{len(word)}c"
            globals.text_area.tag_add('misspelled', start_index, end_index)
            globals.text_area.tag_config('misspelled', foreground='#FA8072', underline=True)
            start_index = end_index

    if misspelled:
        # messagebox.showinfo("Spell Check", f"Found misspelled words: {', '.join(misspelled)}")
        pass
    else:
        messagebox.showinfo("Spell Check", "No misspelled words found.")     

def clear_spell_check():
    # Create a SpellChecker object
    spell = SpellChecker()

    # Get the content from the text area
    text_content = globals.text_area.get("1.0", "end-1c")
    words = text_content.split()

    # Find the misspelled words
    misspelled = spell.unknown(words)

    # Highlight misspelled words
    globals.text_area.tag_remove('misspelled', '1.0', 'end')
    for word in misspelled:
        start_index = '1.0'
        while True:
            start_index = globals.text_area.search(word, start_index, nocase=True, stopindex='end')
            if not start_index:
                break
            end_index = f"{start_index}+{len(word)}c"
            globals.text_area.tag_add('misspelled', start_index, end_index)
            globals.text_area.tag_config('misspelled', foreground='#1e1e1e', underline=False)
            start_index = end_index

    if misspelled:
        # messagebox.showinfo("Spell Check", f"Found misspelled words: {', '.join(misspelled)}")
        pass
    else:
        messagebox.showinfo("Spell Check", "No misspelled words found.")           