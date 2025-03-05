#menyiapkan semua library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# Membuat fungsi yang mereturn data
def season_avg_data(df):
    season_avg = df.groupby("season")["cnt"].mean()
    season_names = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    season_avg = season_avg.rename(season_names)
    return season_avg

def user_percentage_data(df):
    total_registered = df.registered.sum()
    total_casual = df.casual.sum()

    percent_registered = (total_registered / (total_registered + total_casual)) * 100
    percent_casual = 100 - percent_registered
    return percent_registered, percent_casual

def weather_data(df):
    df_weather = df.groupby("weathersit")["cnt"].sum()
    df_weather = df_weather.sort_values(ascending=False)
    return df_weather

def bike_sharing(df): 
    bike_sharing.groupby(by="season_hourly").agg({
    "workingday_hourly": "count", #menjumlahkan penyewa pada hari kerja berdasarkan musim
    "windspeed_hourly": ["max", "min", "mean", lambda x: x.max() - x.min()]  # Membuat fungsi kustom untuk range
}).sort_values(by=("workingday_hourly", "count"), ascending=False)

hour_dt = pd.read_csv("datset_hour.csv")
bike_sharing = pd.read_csv("datset_bike_sharing.csv")
season_avg_df = season_avg_data(hour_dt)
percent_registered, percent_casual = user_percentage_data(hour_dt)
weather_df = weather_data(hour_dt)

st.title("Bike Sharing Dataset Data Analysis")

# Dashboard
selected_content = st.sidebar.selectbox(
    "Select Chart to Display",
    options=["Average Hourly Bike Sharing by Season",
             "Distribution of Registered and Casual Users",
             "Total Bike Sharing by Weather",
             "Pattern of Daily Bicycle Rental Number by Month",
             "Pattern of Number of Daily Bicycle Rentals Based on Hours",
             "The Effect of Weathersit on the Number of Daily Bicycle Rentals",
             "Is there a difference between working days/weekdays and holidays (holidays/weekends) in the number of daily bicycle rentals?"]
)

if selected_content == "Average Hourly Bike Sharing by Season":
    # Chart 1
    st.title("1. Average Hourly Bike Sharing by Season")
    fig = plt.figure(figsize=(6,4))
    season_avg_df.plot(kind="bar", color="pink")
    plt.xlabel("Season")
    plt.ylabel("Average Hourly Sharing")
    plt.title("Average Hourly Bike Sharing by Season")
    plt.xticks(rotation=0)
    st.pyplot(fig)
    st.write("Berdasarkan visualisasi diatas dapat diketahui bahwa :")
    st.markdown("*   pada saat musim semi/fall rata-rata peminjam sepeda mencapai angka tertinggi mencapai 230 lebih pengguna.")
    st.markdown("*   pada saat musim dingin jumlah peminjam sepeda turun menjadi 198 pengguna, hal ini wajar terjadi kerena penurunan suhu yang cukup drastis di musim dingin")
    st.markdown("*   dan terakhir ada musim semi yang memiliki angka rata-rata peminjam sepeda yang paling rendah yaitu berjumlah 111 pengguna")
    
elif selected_content == "Distribution of Registered and Casual Users":
    # Chart 2
    st.title("2. Distribution of Registered and Casual Users")
    fig, ax = plt.subplots(figsize=(6,5))
    labels = ["Registered Users", "Casual Users"]
    sizes = [percent_registered, percent_casual]
    colors = ['orange', 'red']
    explode = (0.1, 0)
    ax.pie(sizes, explode=explode, labels=labels, autopct="%1.1f%%", startangle=140, colors=colors)
    ax.set_title("Distribution of Registered and Casual Users")
    ax.axis('equal')  
    st.pyplot(fig)
    st.markdown("*   Berdasarkan visualisasi data diatas, terlihat bahwa pengguna yang terdaftar lebih banyak meminjam sepeda daripada pengguna kasual. Persentase peminjaman pengguna terdaftar yaitu mencapai 81.2%,sedangkan pengguna kasual hanya 18%")
    st.markdown("*   Statistik ini menunjukkan kalau peminjaman yang dilakukan oleh pengguna terdaftar hampir 4,5 kali lipat dibandingkan pengguna kasual")

elif selected_content == "Total Bike Sharing by Weather":
    # Chart 3
    st.title("3. Total Bike Sharing by Weather")
    fig = plt.figure(figsize=(10, 6))
    plt.barh(weather_df.index, weather_df, color='skyblue')
    plt.xlabel("Total Count")
    plt.ylabel("Weather")
    plt.title("Total Bike Sharing by Weather (Descending)")

    for i, v in enumerate(weather_df):
        plt.text(v + 50, i, f"{v}", va='center')

    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.xticks(rotation=0)
    plt.tight_layout()

    st.pyplot(fig)
    st.write("Berdasarkan visualisasi diatas, terlihat bahwa pada saat cuaca yang cerah(1) memiliki total peminjaman tertinggi. Kemudian cuaca mendung(2) dan hujan(3) memiliki total peminjaman yang rendah dibandingkan cuaca cerah. Terakhir yaitu cuaca salju(4) yang memiliki total peminjaman paling rendah")
   
elif selected_content == "Pattern of Daily Bicycle Rental Number by Month":
    # Chart 4
    st.title("4. Pattern of Daily Bicycle Rental Number by Month")
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(12, 6))
    sns.lineplot(x="mnth_daily", y="cnt_daily", data=bike_sharing, ci=None)
    plt.title("Pola Jumlah Sewa Sepeda Harian Berdasarkan Bulan")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Sewa Sepeda Harian")
    plt.show()
    st.pyplot(fig)
    st.markdown("*   Berdasarkan bulan jumlah sewa sepeda meningkat pada bulan 9 (September) dan bulan 6 (Juni) dengan total yang sama yaitu jumlah penyewa 5750 pengguna")
    st.markdown("*   Jika berdasarkan dilihat dari kategori variable jam jumlah sewa sepeda meningkat sekitar jam 8 pagi dengan total penyewa 350 lebih pengguna dan sekitar jam 5 atau 6 sore dengan total penyewa 450 pengguna")
    
elif selected_content == "Pattern of Number of Daily Bicycle Rentals Based on Hours":
    # Chart 5
    st.title("5. Pattern of Number of Daily Bicycle Rentals Based on Hours")
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(12, 6))
    sns.lineplot(x="hr", y="cnt_hourly", data=bike_sharing, ci=None)
    plt.title("Pola Jumlah Sewa Sepeda Harian Berdasarkan Jam")
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Sewa Sepeda Harian")
    plt.show()
    st.pyplot(fig)
    st.markdown("*   Jumlah sewa sepeda mengingkat ketika cuaca Cerah, Sedikit awan, Berawan sebagian, Berawan sebagian.")
    st.markdown("*   Yaitu pada ketika musim gugur rata rata peminjam sepeda mencapai angka tertinggi dengan total 236,016237 (236) pengguna yang mana detail")
    
elif selected_content == "The Effect of Weathersit on the Number of Daily Bicycle Rentals":
    # Chart 6
    st.title("6. The Effect of Weathersit on the Number of Daily Bicycle Rentals")
    fig = plt.figure(figsize=(12, 6))
    sns.boxplot(x="weathersit_daily", y="cnt_daily", data=bike_sharing)
    plt.title("Pengaruh Weathersit Terhadap Jumlah Sewa Sepeda Harian")
    plt.xlabel("Weathersit")
    plt.ylabel("Jumlah Sewa Sepeda Harian")
    plt.show()
    st.pyplot(fig)
    st.markdown("*   Berdasarkan visualisasi data diatas, terlihat bahwa pengguna yang terdaftar lebih banyak meminjam sepeda daripada pengguna kasual. Persentase peminjaman pengguna terdaftar yaitu mencapai 81.2%,sedangkan pengguna kasual hanya 18%")
    st.markdown("*   Statistik ini menunjukkan kalau peminjaman yang dilakukan oleh pengguna terdaftar hampir 4,5 kali lipat dibandingkan pengguna kasual")
elif selected_content == "Is there a difference between working days/weekdays and holidays (holidays/weekends) in the number of daily bicycle rentals?":
    # Chart 7
    st.title("7. Is there a difference between working days/weekdays and holidays (holidays/weekends) in the number of daily bicycle rentals?")
    fig = plt.figure(figsize=(10, 5))
    sns.boxplot(x="workingday_daily", y="cnt_daily", data=bike_sharing)
    plt.title("Perbedaan Antara Hari Kerja dan Hari Libur dalam Jumlah Sewa Sepeda Harian")
    plt.xlabel("Workingday")
    plt.ylabel("Jumlah Sewa Sepeda Harian")
    plt.show()
    st.pyplot(fig)
    st.markdown("*   Berdasarkan hasil analisis data tersebut jumlah penyewa lebih banyak dihasilkan ketika hari kerja dari pada hari libur dengan total penyewa pmencapai 6000 pengguna") 