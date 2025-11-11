"""
import pandas as pd
import matplotlib.pyplot as plt

# 1️⃣ Veri setini oku (dosya adını seninkine göre yaz)
data = pd.read_csv("BKB_WaterQualityData_2020084.csv")
print("Veri hakkında genel bilgiler:")
print(data.info())

# 3️⃣ Eksik veri kontrolü
print("\nEksik veri sayısı:")
print(data.isnull().sum())

# 4️⃣ pH dağılımı grafiği
plt.hist(data["pH (standard units)"].dropna(), bins=20, edgecolor='black')
plt.title("pH Dağılımı")
plt.xlabel("pH Değeri")
plt.ylabel("Frekans")
plt.show()
"""

import pandas as pd
import matplotlib.pyplot as plt

# Veriyi oku
df = pd.read_csv("BKB_WaterQualityData_2020084.csv")

# Sütun adlarını kısaltalım ve anlaşılır hale getirelim
df = df.rename(columns={
    "Salinity (ppt)": "Tuzluluk",
    "Dissolved Oxygen (mg/L)": "Oksijen",
    "pH (standard units)": "pH",
    "Secchi Depth (m)": "Berraklık",
    "Water Temp (?C)": "Su Sicakligi",
    "AirTemp (C)": "Hava Sicakligi"
})

# Eksik değerleri at (sadece sayısal olanlar)
df_numeric = df[["Tuzluluk", "Oksijen", "pH", "Berraklık", "Su Sicakligi"]].dropna()

# --- GRAFİK 1: Genel dağılımlar (hepsi tek grafikte) ---
df_numeric.hist(bins=20, figsize=(10,8), color="#8EC5FC")
plt.suptitle("💧 Su Kalitesi Parametrelerinin Dağılımı", fontsize=14, fontweight="bold")
plt.show()

# --- GRAFİK 2: Yıla göre ortalama pH, sıcaklık ve oksijen ---
yearly_avg = df.groupby("Year")[["pH", "Oksijen", "Su Sicakligi"]].mean()

yearly_avg.plot(kind="line", marker="o", figsize=(10,6))
plt.title("📅 Yıllara Göre Ortalama pH, Oksijen ve Su Sıcaklığı", fontsize=14, fontweight="bold")
plt.xlabel("Yıl")
plt.ylabel("Ortalama Değer")
plt.grid(True)
plt.show()

# --- GRAFİK 3: Su kalitesi genel özeti ---
# Basit bir skor oluşturalım (örnek formül)
df["Kalite_Skoru"] = (
    (df["Oksijen"].fillna(0) / 10) * 0.4 +
    (7 - abs(df["pH"].fillna(7) - 7)) * 0.3 +
    ((30 - df["Su Sicakligi"].fillna(20)) / 30) * 0.3
)


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Veriyi oku
df = pd.read_csv("BKB_WaterQualityData_2020084.csv")

# İsimleri sadeleştir
df = df.rename(columns={
    "Salinity (ppt)": "Tuzluluk",
    "Dissolved Oxygen (mg/L)": "Oksijen",
    "pH (standard units)": "pH",
    "Water Temp (?C)": "Sicaklik"
})

# --- Skor hesaplama fonksiyonları ---
def skor_ph(x):
    if pd.isna(x):
        return np.nan
    if 6.5 <= x <= 8.5:
        return 1
    elif 5 <= x < 6.5 or 8.5 < x <= 9.5:
        return 0.5
    else:
        return 0

def skor_oksijen(x):
    if pd.isna(x):
        return np.nan
    if x >= 7:
        return 1
    elif 5 <= x < 7:
        return 0.7
    elif 3 <= x < 5:
        return 0.4
    else:
        return 0

def skor_sicaklik(x):
    if pd.isna(x):
        return np.nan
    if 15 <= x <= 25:
        return 1
    elif 10 <= x < 15 or 25 < x <= 30:
        return 0.6
    else:
        return 0.3

def skor_tuzluluk(x):
    if pd.isna(x):
        return np.nan
    if x < 5:
        return 1
    elif 5 <= x <= 30:
        return 0.7
    else:
        return 0.4

# --- Her parametre için skor sütunları ---
df["pH_skor"] = df["pH"].apply(skor_ph)
df["Oksijen_skor"] = df["Oksijen"].apply(skor_oksijen)
df["Sicaklik_skor"] = df["Sicaklik"].apply(skor_sicaklik)
df["Tuzluluk_skor"] = df["Tuzluluk"].apply(skor_tuzluluk)

# --- Toplam su kalitesi skoru (ağırlıklı ortalama) ---
df["Su_Kalitesi_Skoru"] = (
    df[["pH_skor", "Oksijen_skor", "Sicaklik_skor", "Tuzluluk_skor"]]
    .mean(axis=1)
)

# --- Yıllık ortalama skor ---
yearly_quality = df.groupby("Year")["Su_Kalitesi_Skoru"].mean()

# --- Grafik ---
plt.figure(figsize=(10,5))
plt.plot(yearly_quality.index, yearly_quality.values, marker="o", color="#00BFA5")
plt.title("🌿 Yıllara Göre Ortalama Su Kalitesi Skoru (0 = kötü, 1 = mükemmel)", fontsize=13, fontweight="bold")
plt.xlabel("Yıl")
plt.ylabel("Ortalama Skor")
plt.grid(True)
plt.show()
