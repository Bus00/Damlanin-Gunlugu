import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("BKB_WaterQualityData_2020084.csv")

df = df.rename(columns={
    "Salinity (ppt)": "Tuzluluk",
    "Dissolved Oxygen (mg/L)": "Oksijen",
    "pH (standard units)": "pH",
    "Water Temp (?C)": "Sicaklik"
})

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


df["pH_skor"] = df["pH"].apply(skor_ph)
df["Oksijen_skor"] = df["Oksijen"].apply(skor_oksijen)
df["Sicaklik_skor"] = df["Sicaklik"].apply(skor_sicaklik)
df["Tuzluluk_skor"] = df["Tuzluluk"].apply(skor_tuzluluk)

df["Su_Kalitesi_Skoru"] = (
    df[["pH_skor", "Oksijen_skor", "Sicaklik_skor", "Tuzluluk_skor"]]
    .mean(axis=1)
)

yearly_quality = df.groupby("Year")["Su_Kalitesi_Skoru"].mean()

plt.figure(figsize=(10,5))
plt.plot(yearly_quality.index, yearly_quality.values, marker="o", color="#00BFA5")
plt.title("🌿 Yıllara Göre Ortalama Su Kalitesi Skoru (0 = kötü, 1 = mükemmel)", fontsize=13, fontweight="bold")
plt.xlabel("Yıl")
plt.ylabel("Ortalama Skor")
plt.grid(True)
plt.show()
