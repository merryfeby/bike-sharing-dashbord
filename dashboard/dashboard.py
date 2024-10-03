import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

##Assessing Data
day_data = pd.read_csv('dashboard/main_data.csv')

day_data_dtypes = day_data.dtypes

# Statistik deskriptif untuk setiap kolom
day_data_describe = day_data.describe(include='all')

# Jumlah nilai null untuk setiap kolom
day_data_missing_values = day_data.isnull().sum()

# Jumlah baris duplikat dalam dataset
day_duplicates = day_data.duplicated().sum()


##Cleaning Data
# Mengubah tipe data kolom 'dteday' menjadi datetime
day_data['dteday'] = pd.to_datetime(day_data['dteday'])

relevant_columns = ['weathersit', 'workingday']
day_data_clean = day_data[relevant_columns]

# Mapping kondisi cuaca 'weathersit' menjadi string
weather_map = {
    1: 'Sunny',
    2: 'Cloudy',
    3: 'Rain',
    4: 'Heavy Rain'
}
day_data['weathersit_label'] = day_data['weathersit'].map(weather_map).astype(str)

# Mapping hari kerja 'workingday' menjadi string
day_data['workingday_label'] = day_data['workingday'].map({
    0: 'Non-Working Day',
    1: 'Working Day'
}).astype(str)
#

# Judul dashboard
st.title("Dashboard Analisis Bike Sharing")

# Menambahkan gambar latar belakang
st.markdown(
    '<style>body{background-image: url("https://your-background-image-url.jpg"); background-size: cover;}</style>', 
    unsafe_allow_html=True
)

# Menampilkan Data Hari
st.subheader("📅 Data Hari")
st.dataframe(day_data)

# Grafik Pengaruh Hari Kerja terhadap Jumlah Sewa Sepeda
st.subheader("📊 Pengaruh Hari Kerja terhadap Jumlah Sewa Sepeda")
plt.figure(figsize=(8, 5))
sns.barplot(x='workingday_label', y='cnt', data=day_data, palette='viridis')
plt.title('Pengaruh Hari Kerja terhadap Jumlah Sewa Sepeda')
plt.xlabel('Jenis Hari')
plt.ylabel('Jumlah Sewa Sepeda')
st.pyplot(plt)  

# Statistik Sewa Sepeda berdasarkan Kondisi Cuaca
weather_stats = day_data.groupby('weathersit_label')['cnt'].agg(['mean', 'median', 'std'])
st.subheader("📊 Statistik Sewa Sepeda berdasarkan Kondisi Cuaca:")
st.dataframe(weather_stats.style.background_gradient(cmap='coolwarm'))

# Distribusi jumlah sewa sepeda
st.subheader('📈 Distribusi Jumlah Sewa Sepeda')
plt.figure(figsize=(10, 5))
sns.histplot(day_data['cnt'], kde=True, color='cyan', edgecolor='black')
plt.title('Distribusi Jumlah Sewa Sepeda')
plt.xlabel('Jumlah Sewa Sepeda')
plt.ylabel('Frekuensi')
st.pyplot(plt)

# Statistik deskriptif
st.subheader("📚 Statistik Deskriptif Jumlah Sewa Sepeda:")
desc_df = day_data['cnt'].describe().to_frame().reset_index()
desc_df.columns = ['Statistik', 'Nilai']  # Mengubah nama kolom
st.dataframe(desc_df.style.background_gradient(cmap='coolwarm'))

# Menampilkan statistik dan plot
st.sidebar.header("🌦️ Pilih Kondisi Cuaca")
weathersit_options = day_data['weathersit_label'].unique().tolist()
selected_weathersit = st.sidebar.selectbox("Pilih Kondisi Cuaca:", weathersit_options)

# Filter data berdasarkan kondisi cuaca yang dipilih
filtered_data = day_data[day_data['weathersit_label'] == selected_weathersit]

# Menampilkan bar chart untuk jumlah sewa sepeda berdasarkan kondisi cuaca yang dipilih
st.write(f"🚴 Jumlah Sewa Sepeda untuk Kondisi Cuaca: **{selected_weathersit}**")
st.bar_chart(filtered_data['cnt'])


# Menambahkan informasi duplikat dan nilai null
st.sidebar.subheader("Informasi Data")
st.sidebar.write(f"Jumlah Baris Duplikat: {day_data.duplicated().sum()}")
st.sidebar.write(f"Jumlah Nilai Null:\n{day_data.isnull().sum()}")

st.markdown("---")
st.markdown("### Thankyou! 🚀")
