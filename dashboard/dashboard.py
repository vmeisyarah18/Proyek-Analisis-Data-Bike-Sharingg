import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# KONFIGURASI DASHBOARD
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)
sns.set_style("whitegrid")
# JUDUL
st.title("🚲 Bike Sharing Dashboard")
st.write(
    "Dashboard ini menyajikan analisis peminjaman sepeda berdasarkan "
    "kondisi cuaca dan musim."
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

# SIDEBAR INTERAKTIF
st.sidebar.title("📌 Filter Interaktif")

# Filter tanggal
start_date = st.sidebar.date_input("Mulai Tanggal", df["dteday"].min())
end_date = st.sidebar.date_input("Sampai Tanggal", df["dteday"].max())

# Filter musim
selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=df['season_name'].unique(),
    default=list(df['season_name'].unique())
)

# Filter cuaca
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

# GRAFIK 1: PENGARUH CUACA
st.subheader("📊 Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman")

weather_avg = filtered_df.groupby("weather_name")["total_rentals"].mean().reset_index()

fig1, ax1 = plt.subplots()
sns.barplot(data=weather_avg, x="weather_name", y="total_rentals", ax=ax1, palette="Blues_d")
ax1.set_xlabel("Kondisi Cuaca")
ax1.set_ylabel("Rata-rata Peminjaman")
ax1.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Cuaca")
st.pyplot(fig1)

st.write(
    "**Insight:** Rata-rata peminjaman sepeda paling tinggi terjadi pada kondisi cuaca cerah, "
    "diikuti oleh cuaca berkabut atau mendung ringan. Sementara itu, kondisi hujan ringan "
    "menunjukkan penurunan jumlah peminjaman yang cukup signifikan, menandakan bahwa "
    "faktor cuaca sangat memengaruhi minat pengguna."
)

st.divider()

# GRAFIK 2: PENGARUH MUSIM
st.subheader("📊 Pola Peminjaman Sepeda Berdasarkan Musim")

season_avg = filtered_df.groupby("season_name")["total_rentals"].mean().reset_index()

fig2, ax2 = plt.subplots()
sns.barplot(data=season_avg, x="season_name", y="total_rentals", ax=ax2, palette="Blues_d")
ax2.set_xlabel("Musim")
ax2.set_ylabel("Rata-rata Peminjaman")
ax2.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Musim")
st.pyplot(fig2)

st.write(
    "**Insight:** Peminjaman sepeda cenderung meningkat pada musim panas dan gugur, "
    "sementara musim semi memiliki rata-rata peminjaman paling rendah. Hal ini menunjukkan "
    "bahwa kondisi cuaca yang lebih hangat dan stabil mendorong aktivitas bersepeda."
)
st.divider()

# KESIMPULAN
st.subheader("📝 Kesimpulan")
st.write(
    "Dashboard interaktif ini menunjukkan bahwa kondisi cuaca dan musim "
    "memiliki pengaruh signifikan terhadap jumlah peminjaman sepeda. "
    "Pengguna dapat memfilter data berdasarkan tanggal, musim, dan kondisi cuaca "
    "untuk melakukan eksplorasi data secara dinamis."
)
st.caption("📌 Sumber Data: Bike Sharing Dataset (day.csv)")
