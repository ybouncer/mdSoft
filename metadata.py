import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def get_pdf_metadata(pdf_path):
    pdf_document = fitz.open(pdf_path)
    metadata = pdf_document.metadata
    pdf_document.close()
    return metadata

def reset_pdf_metadata(input_pdf_path, output_pdf_path=None):
    pdf_document = fitz.open(input_pdf_path)
    pdf_document.set_metadata({})
    if output_pdf_path:
        pdf_document.save(output_pdf_path)
    else:
        temp_output_path = input_pdf_path + ".temp"
        pdf_document.save(temp_output_path)
        pdf_document.close()
        os.replace(temp_output_path, input_pdf_path)
        return
    pdf_document.close()

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        input_path.set(file_path)
        metadata_before = get_pdf_metadata(file_path)
        metadata_text_before.set(f"Metadata before resetting:\n{metadata_before}")

def save_file():
    if save_to_original.get():
        reset_pdf_metadata(input_path.get())
        metadata_after = get_pdf_metadata(input_path.get())
        metadata_text_after.set(f"Metadata after resetting:\n{metadata_after}")
        messagebox.showinfo("Success", "Metadata has been reset and file saved.")
    else:
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            output_path.set(file_path)
            reset_pdf_metadata(input_path.get(), file_path)
            metadata_after = get_pdf_metadata(file_path)
            metadata_text_after.set(f"Metadata after resetting:\n{metadata_after}")
            messagebox.showinfo("Success", "Metadata has been reset and file saved.")

app = tk.Tk()
app.title("PDF Metadata Remover")
app.geometry("500x400")  # Set fixed window size

input_path = tk.StringVar()
output_path = tk.StringVar()
metadata_text_before = tk.StringVar()
metadata_text_after = tk.StringVar()
save_to_original = tk.BooleanVar()

tk.Label(app, text="Upload PDF:").pack(pady=5)
tk.Entry(app, textvariable=input_path, width=50).pack(pady=5)
tk.Button(app, text="Browse", command=upload_file).pack(pady=5)

tk.Label(app, textvariable=metadata_text_before, wraplength=450).pack(pady=5)

tk.Checkbutton(app, text="Save to original file", variable=save_to_original).pack(pady=5)

tk.Label(app, text="Save PDF:").pack(pady=5)
tk.Entry(app, textvariable=output_path, width=50).pack(pady=5)
tk.Button(app, text="Save As", command=save_file).pack(pady=5)

tk.Label(app, textvariable=metadata_text_after, wraplength=450).pack(pady=5)

app.mainloop()