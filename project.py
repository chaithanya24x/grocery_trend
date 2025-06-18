import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from PIL import Image, ImageTk

root = Tk()
root.title("Grocery Price Trend Analyzer")
root.geometry("800x700")
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "background.jpg")
bg_img = Image.open(image_path)
bg_img = bg_img.resize((800, 700), Image.Resampling.LANCZOS) 
bg_img = ImageTk.PhotoImage(bg_img)
bg_label = Label(root, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

frame1 = Frame(root)
frame1.pack(pady=10)
frame2 = Frame(root)
frame2.pack(pady=10)

for widget in root.winfo_children():
    widget.lift()

def show_graphs(df):
    df.fillna(method='ffill', inplace=True)
    fig1 = plt.figure(figsize=(6, 4))
    for item in df.columns[1:]:
        plt.plot(df["Date"], df[item], label=item)
    plt.title("Grocery Price Trends (2025)")
    plt.xlabel("Date")
    plt.ylabel("Price (₹)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
    canvas1.draw()
    canvas1.get_tk_widget().pack()

    correlation = df[df.columns[1:]].corr()
    fig2 = plt.figure(figsize=(6, 3))
    correlation["Rice_Price"].drop("Rice_Price").plot(kind='bar', title="Correlation with Rice Price", ylabel="Correlation Coefficient", color='skyblue')
    plt.tight_layout()

    canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
    canvas2.draw()
    canvas2.get_tk_widget().pack()

def show_duplicate_popup(missing_info, df):
    popup = tk.Toplevel()
    popup.title("Data Warnings & Options")
    popup.geometry("800x700")

    heading = ttk.Label(popup, text="Duplicates Values in Data", font=("Segoe UI", 17, "bold"), foreground="red")
    heading.pack(pady=(10, 5))

    content = tk.Text(popup, font=("Consolas", 14), height=20, width=90, wrap="word")
    content.insert(tk.END, missing_info)
    content.config(state='disabled')
    content.pack(pady=5, padx=10)

    def show_pricechanged_popup():
        price_changes = []
        for col in df.columns[1:]:
            start = df[col].iloc[0]
            end = df[col].iloc[-1]
            if pd.notnull(start) and pd.notnull(end):
                change = end - start
                percent = (change / start) * 100 if start != 0 else 0
                price_changes.append(f"{col}: ₹{change:.2f} ({percent:.2f}%)")

        pct_popup = tk.Toplevel()
        pct_popup.title("Price Change Summary")
        pct_popup.geometry("800x700")

        lbl = Label(pct_popup, text="Price Changed from Start to End", font=("Arial", 17, "bold"))
        lbl.pack(pady=10)

        txt = Text(pct_popup, font=("Consolas", 14), height=20, width=90)
        txt.insert(END, "\n".join(price_changes))
        txt.config(state='disabled')
        txt.pack(pady=5)

        graph_btn = ttk.Button(pct_popup, text="Show Graphs", command=lambda: [show_graphs(df), pct_popup.destroy(), popup.destroy()])
        graph_btn.pack(pady=10)

        close_btn = ttk.Button(pct_popup, text="Close", command=pct_popup.destroy)
        close_btn.pack()

    btn_pct = ttk.Button(popup, text="Show Price % Change", command=show_pricechanged_popup)
    btn_pct.pack(pady=(10, 5))

    close_btn = ttk.Button(popup, text="Close", command=popup.destroy)
    close_btn.pack(pady=(0, 10))

def load_and_analyze():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    try:
        df = pd.read_csv(file_path)
        df["Date"] = pd.to_datetime(df["Date"])

        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        missing_info = df.isnull().sum()
        show_duplicate_popup(str(missing_info), df)

    except Exception as e:
        messagebox.showerror("Error", str(e))

btn = Button(root, text="Load Grocery Details", command=load_and_analyze, font=("Arial", 14), bg="lightblue")
btn.pack(pady=170)

root.mainloop()