import tkinter as tk
from qr_code_reader_module import QRCodeReaderApp

# Create the main window
root = tk.Tk()
root.title("Main Window")

# Create an instance of the QRCodeReaderApp and attach it to the main window
qr_app = QRCodeReaderApp(root)

# Run the Tkinter event loop
root.mainloop()
