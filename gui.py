import tkinter as tk
from tkinter import StringVar, ttk, messagebox
import pandas as pd
import requests
from tkinter import filedialog
import os

category_options = [
    "Véhicules", "Immobilier", "ImmoNeuf", "Entreprises", "Pour la Maison et Jardin"
]

BASE_URL = "http://localhost:8000/tayara"  

def scrape_data():
    query = entry_search.get()
    category = category_var.get()

    if not query and not category:
        messagebox.showwarning("Input Error", "Please provide at least one (search or category).")
        return

    try:
        response = requests.post(f"{BASE_URL}/description", json={"query": query, "category": category})
        if response.status_code == 200:
            data = response.json().get("descriptions", [])
            show_preview(data)
        else:
            messagebox.showerror("Error", f"Failed to fetch data: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Request Error", str(e))

def export_pdf():
    query = entry_search.get()
    category = category_var.get()

    if not query and not category:
        messagebox.showwarning("Input Error", "Please provide at least one (search or category).")
        return

    try:
        response = requests.post(f"{BASE_URL}/export", json={"query": query, "category": category}, stream=True)
        if response.status_code == 200:
            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                df = pd.read_excel(save_path)
                show_preview(df.to_dict("records"))
                messagebox.showinfo("Success", f"Excel exported and saved to:\n{save_path}")
        else:
            messagebox.showerror("Export Failed", f"Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_preview(data):
    preview_table.delete(*preview_table.get_children())

    if not data:
        messagebox.showinfo("No Data", "No results found.")
        return

    columns = list(data[0].keys())
    preview_table["columns"] = columns
    preview_table["show"] = "headings"

    for col in columns:
        preview_table.heading(col, text=col)
        preview_table.column(col, width=150, anchor="w")

    for item in data:
        preview_table.insert("", "end", values=[item.get(col, "") for col in columns])

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("TuniHUNT")
root.geometry("1000x600")
root.resizable(False, False)

sidebar = tk.Frame(root, bg="#f0f0f0", width=150)
sidebar.pack(side="left", fill="y")

tk.Label(sidebar, text="Networks", font=("Arial", 10, "bold")).pack(pady=(20, 5))
tk.Button(sidebar, text="Tayara", bg="white", relief="solid").pack(fill="x", padx=10)

topbar = tk.Frame(root, height=40, bg="#f9f9f9")
topbar.pack(side="top", fill="x")

tk.Label(topbar, text="TuniHUNT", font=("Arial", 12, "bold")).pack(side="left", padx=20)

main_frame = tk.Frame(root)
main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

input_frame = tk.Frame(main_frame)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Search").grid(row=0, column=0, padx=10)
entry_search = tk.Entry(input_frame, width=30)
entry_search.grid(row=1, column=0, padx=10)

tk.Label(input_frame, text="List Category").grid(row=0, column=1, padx=10)
category_var = StringVar()
combo_category = ttk.Combobox(input_frame, textvariable=category_var, values=category_options, width=28)
combo_category.grid(row=1, column=1, padx=10)
combo_category.set(category_options[0])

btn_frame = tk.Frame(main_frame)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Scrape", command=scrape_data, width=12).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Export Excel", command=export_pdf, width=12).grid(row=0, column=1, padx=10)

table_label = tk.Label(main_frame, text="Preview Excel", font=("Arial", 10, "bold"))
table_label.pack(pady=5)

preview_table = ttk.Treeview(main_frame)
preview_table.pack(expand=True, fill="both", padx=20)

root.mainloop()
