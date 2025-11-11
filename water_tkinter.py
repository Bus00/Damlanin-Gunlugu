
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- ANA PENCERE ---
root = tk.Tk()
root.title("💧🐣 Su Kalitesi Analiz Paneli")
root.state("zoomed")  # tam ekran yapmak için
root.config(bg="#E1F5FE") 

df = None  # veri globali için

# --- DOSYA YÜKLEME ---
def dosya_yukle():
    global df
    filepath = filedialog.askopenfilename(
        title="CSV Dosyası Seç",
        filetypes=(("CSV dosyaları", "*.csv"), ("Tüm dosyalar", "*.*"))
    )
    if filepath:
        df = pd.read_csv(filepath)
        messagebox.showinfo("Başarılı ✅", f"Veri yüklendi: {len(df)} satır bulundu.")
        dosya_label.config(text=f"Yüklü Dosya: {filepath.split('/')[-1]}")

# --- PARAMETRELERİN TÜRKÇELEŞTİRİLMESİ --- (türkçesini anlayabilmek için)
def duzelt(df):
    df = df.rename(columns={
        "Salinity (ppt)": "Tuzluluk",
        "Dissolved Oxygen (mg/L)": "Oksijen",
        "pH (standard units)": "pH",
        "Water Temp (?C)": "Sıcaklık",
        "Year": "Yıl"
    })
    return df

# --- GRAFİK 1: Parametre Dağılımları ---
def grafik_parametreler():
    if df is None:
        messagebox.showwarning("Uyarı 🙅‍♀️⚠️", "Lütfen önce veri yükleyin.")
        return
    local_df = duzelt(df)
    local_df[["Tuzluluk", "Oksijen", "pH", "Sıcaklık"]].hist(
        bins=20, figsize=(10, 8), color="#4FC3F7", edgecolor="black"
    )
    plt.suptitle("💧 Su Kalitesi Parametrelerinin Dağılımı", fontsize=16, fontweight="bold")
    plt.show()

# --- GRAFİK 2: Yıllara Göre Ortalama Kalite ---
def grafik_yillar():
    if df is None:
        messagebox.showwarning("Uyarı 🙅‍♀️⚠️", "Lütfen önce veri yükleyin.")
        return
    local_df = duzelt(df)

    # Skor fonksiyonları
    def skor_ph(x):
        if pd.isna(x): return np.nan
        if 6.5 <= x <= 8.5: return 1
        elif 5 <= x < 6.5 or 8.5 < x <= 9.5: return 0.5
        else: return 0

    def skor_oksijen(x):
        if pd.isna(x): return np.nan
        if x >= 7: return 1
        elif 5 <= x < 7: return 0.7
        elif 3 <= x < 5: return 0.4
        else: return 0

    def skor_sicaklik(x):
        if pd.isna(x): return np.nan
        if 15 <= x <= 25: return 1
        elif 10 <= x < 15 or 25 < x <= 30: return 0.6
        else: return 0.3

    def skor_tuzluluk(x):
        if pd.isna(x): return np.nan
        if x < 5: return 1
        elif 5 <= x <= 30: return 0.7
        else: return 0.4

    local_df["pH_skor"] = local_df["pH"].apply(skor_ph)
    local_df["Oksijen_skor"] = local_df["Oksijen"].apply(skor_oksijen)
    local_df["Sıcaklık_skor"] = local_df["Sıcaklık"].apply(skor_sicaklik)
    local_df["Tuzluluk_skor"] = local_df["Tuzluluk"].apply(skor_tuzluluk)

    local_df["Su_Kalitesi_Skoru"] = local_df[["pH_skor", "Oksijen_skor", "Sıcaklık_skor", "Tuzluluk_skor"]].mean(axis=1)
    yearly = local_df.groupby("Yıl")["Su_Kalitesi_Skoru"].mean()

    # Grafik
    plt.figure(figsize=(10,5))
    plt.plot(yearly.index, yearly.values, marker="o", linewidth=2, color="#0277BD")
    plt.title("📅 Yıllara Göre Ortalama Su Kalitesi Skoru", fontsize=15, fontweight="bold")
    plt.xlabel("Yıl")
    plt.ylabel("Ortalama Kalite (0 = kötü, 1 = mükemmel)")
    plt.grid(True)
    plt.show()

    # Ortalama sonucu göster
    ort = yearly.mean()
    if ort > 0.7:
        renk = "#2E7D32"  
    elif ort > 0.4:
        renk = "#F9A825"  
    else:
        renk = "#C62828"  

    sonuc_label.config(text=f"🌊 Ortalama Su Kalitesi: {ort:.2f}", bg=renk, fg="white")

# --- ARAYÜZ ---
title_label = tk.Label(
    root, text="💦🌟💧🫧SU KALİTESİ ANALİZ PANELİ💦🌟💧🫧",
    font=("Arial", 22, "bold"), bg="#E1F5FE", fg="#0D47A1"
)
title_label.pack(pady=20)

frame = tk.Frame(root, bg="#E1F5FE")
frame.pack(pady=10)

btn_style = {"font": ("Arial", 14, "bold"), "width": 22, "height": 2}

tk.Button(frame, text="📂 Veri Yükle", command=dosya_yukle, bg="#81C784", fg="#1B5E20", **btn_style).grid(row=0, column=0, padx=15, pady=10)
tk.Button(frame, text="📊 Parametre Dağılımları", command=grafik_parametreler, bg="#4FC3F7", fg="#0D47A1", **btn_style).grid(row=0, column=1, padx=15, pady=10)
tk.Button(frame, text="📈 Yıllara Göre Kalite", command=grafik_yillar, bg="#FFB74D", fg="#E65100", **btn_style).grid(row=0, column=2, padx=15, pady=10)

dosya_label = tk.Label(root, text="Henüz dosya yüklenmedi", bg="#E1F5FE", fg="#01579B", font=("Arial", 13, "italic"))
dosya_label.pack(pady=10)

sonuc_label = tk.Label(root, text="🌊 Ortalama Su Kalitesi: --", font=("Arial", 18, "bold"), bg="#B3E5FC", fg="#0D47A1", padx=20, pady=10)
sonuc_label.pack(pady=30)

root.mainloop()


