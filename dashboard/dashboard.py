import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# KONFIGURASI DASHBOARD
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
sns.set_style("whitegrid")

# JUDUL
st.title("🚲 Bike Sharing Dashboard")
st.write(
    "Dashboard ini menyajikan analisis peminjaman sepeda berdasarkan "
    "kondisi cuaca, musim, dan tren waktu selama periode 2011–2012."
)
st.divider()

# LOAD DATA
df = pd.read_csv("data/day.csv")
df["dteday"] = pd.to_datetime(df["dteday"])
df.rename(columns={'cnt': 'total_rentals'}, inplace=True)

# Mapping musim & cuaca
season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df['season_name'] = df['season'].map(season_labels)

weather_labels = {1: 'Clear', 2: 'Mist', 3: 'Light Rain'}
df['weather_name'] = df['weathersit'].map(weather_labels)

# Tambah fitur waktu
df["month"] = df["dteday"].dt.to_period("M").astype(str)

# SIDEBAR INTERAKTIF
st.sidebar.title("📌 Filter Interaktif")

start_date = st.sidebar.date_input("Mulai Tanggal", df["dteday"].min())
end_date = st.sidebar.date_input("Sampai Tanggal", df["dteday"].max())

selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=df['season_name'].unique(),
    default=list(df['season_name'].unique())
)

selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=df['weather_name'].unique(),
    default=list(df['weather_name'].unique())
)

# Terapkan filter
filtered_df = df[
    (df["dteday"] >= pd.to_datetime(start_date)) &
    (df["dteday"] <= pd.to_datetime(end_date)) &
    (df["season_name"].isin(selected_season)) &
    (df["weather_name"].isin(selected_weather))
]

# GRAFIK 1: CUACA BULANAN
st.subheader("📊 Rata-rata Peminjaman Sepeda Bulanan Berdasarkan Kondisi Cuaca")

monthly_weather = filtered_df.groupby(
    ["month", "weather_name"]
)["total_rentals"].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(10,5))
sns.lineplot(
    data=monthly_weather,
    x="month",
    y="total_rentals",
    hue="weather_name",
    marker="o",
    ax=ax1
)

ax1.set_xlabel("Bulan")
ax1.set_ylabel("Rata-rata Peminjaman")
ax1.set_title("Tren Bulanan Peminjaman Berdasarkan Kondisi Cuaca")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.write(
    "**Insight:** Grafik menunjukkan bahwa peminjaman sepeda paling tinggi terjadi pada kondisi "
    "cuaca cerah hampir di seluruh bulan. Sementara itu, kondisi hujan ringan menghasilkan "
    "jumlah peminjaman terendah, yang menandakan pengaruh signifikan faktor cuaca terhadap "
    "perilaku pengguna."
)

st.divider()

# GRAFIK 2: MUSIM BULANAN
st.subheader("📊 Rata-rata Peminjaman Sepeda Bulanan Berdasarkan Musim")

monthly_season = filtered_df.groupby(
    ["month", "season_name"]
)["total_rentals"].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(10,5))
sns.lineplot(
    data=monthly_season,
    x="month",
    y="total_rentals",
    hue="season_name",
    marker="o",
    ax=ax2
)

ax2.set_xlabel("Bulan")
ax2.set_ylabel("Rata-rata Peminjaman")
ax2.set_title("Tren Bulanan Peminjaman Berdasarkan Musim")
plt.xticks(rotation=45)
st.pyplot(fig2)

st.write(
    "**Insight:** Peminjaman sepeda meningkat signifikan pada musim panas dan gugur, "
    "terutama pada pertengahan hingga akhir tahun. Sebaliknya, musim semi dan musim dingin "
    "menunjukkan tingkat peminjaman yang relatif lebih rendah."
)

st.divider()

# GRAFIK 3: TREND BULANAN KESELURUHAN
st.subheader("📊 Tren Peminjaman Sepeda Bulanan Keseluruhan")

monthly_trend = filtered_df.groupby("month")["total_rentals"].mean().reset_index()

fig3, ax3 = plt.subplots(figsize=(10,5))
sns.lineplot(
    data=monthly_trend,
    x="month",
    y="total_rentals",
    marker="o",
    ax=ax3
)

ax3.set_xlabel("Bulan")
ax3.set_ylabel("Rata-rata Peminjaman")
ax3.set_title("Tren Bulanan Peminjaman Sepeda")
plt.xticks(rotation=45)
st.pyplot(fig3)

st.write(
    "**Insight:** Terlihat adanya pola musiman yang kuat, di mana peminjaman meningkat "
    "secara bertahap hingga mencapai puncak di pertengahan tahun, kemudian menurun "
    "di akhir tahun."
)

st.divider()

# KESIMPULAN
st.subheader("📝 Kesimpulan")

st.write(
    "Dashboard ini membuktikan bahwa kondisi cuaca dan musim berpengaruh signifikan terhadap "
    "jumlah peminjaman sepeda. Cuaca cerah dan musim panas serta gugur menunjukkan tingkat "
    "peminjaman tertinggi, sedangkan hujan ringan dan musim semi menghasilkan peminjaman terendah. "
    "Fitur filter interaktif memungkinkan pengguna melakukan eksplorasi data secara fleksibel "
    "berdasarkan waktu, musim, dan kondisi cuaca."
)

st.caption("📌 Sumber Data: Bike Sharing Dataset (day.csv)")
