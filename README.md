# Notorius - A Tkinter-based Text Editor

Notorius is a lightweight text editor built using Python's Tkinter library. It provides essential text editing features along with additional functionalities such as spell checking, recent files management, and basic text formatting.

## Features

- **Basic Text Editing**: Create, open, save, and edit text files with ease.
- **Recent Files**: Automatically keeps track of the last 10 recently opened files, allowing quick access to them via a "Recent Files" menu.
- **Spell Check**: Integrated spell-checking functionality using `pyspellchecker` to help you write without errors.
- **Find and Replace**: Easily search for specific words or phrases and replace them in the text.
- **Tabbed Table Formatting**: Quickly format selected text into a simple tabbed table structure.
- **Context Menu**: A right-click context menu that offers basic text operations like cut, copy, and paste.
- **Line Numbering**: Displays line numbers alongside the text for easier navigation.

## Installation

1. **Clone the repository**:

   ```
   bash
   git clone https://github.com/yourusername/notorius.git
   cd notorius

   ```

2. **Create and activate a virtual environment:**

   ```
   python -m venv venv
   source venv/bin/activate # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```
   pip install -r requirements.txt
   ```

The dependencies include:

-   textblob (for spell checking)
-   pyspellchecker (alternative spell checker)
-   nltk (for natural language processing, used with textblob)
-   tkinter (standard Python GUI library)

4.  **Download NLTK corpora (if using TextBlob spell checker)**:

    You may need to download additional corpora for spell checking with TextBlob:

    ```
    import nltk
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    

    from textblob import download_corpora
    download_corpora.download_all()
    ```

## Usage

1.  **Run the app:**

    After setting up the environment, launch the app with:

    ```
    python notorius.py
    ```


2.  **Opening Files:**

-   Use the "File" menu to open existing text files.
-   Recently opened files will be automatically saved in a list (up to 10) under the "Recent Files" submenu for quick access.

3.  **Spell Checking:**

    - Use the built-in spell check feature to highlight misspelled words.
    - The spell checking feature is powered by pyspellchecker.

1.  **Find and Replace:**

    - Access the "Find/Replace" functionality to quickly locate specific words or phrases and replace them in the text.

5.  **Context Menu:**

    - Right-click within the text area to access basic text operations (Cut, Copy, Paste).

6.  **Tabbed Table Formatting:**

    - Select text and use the "Format" menu to create simple tabbed tables.
  

# Project Structure

    ```
    Notorius/
    │
    ├── notorius.py # Main application script
    ├── utils.py # Utility functions (spell check, recent files handling, etc.)
    ├── requirements.txt # List of dependencies
    ├── README.md # This file
    └── recent_files.json # Stores the list of recent files (auto-generated)
    ```

# Contributing

1. **Fork the repository.**
2. **Create a new branch** for your feature/bugfix.
3. **Submit a pull request.**

We welcome contributions to improve Notorius!


# License

This project is licensed under the MIT License - see the LICENSE file for details.
