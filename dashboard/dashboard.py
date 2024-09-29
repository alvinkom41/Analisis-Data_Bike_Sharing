import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


days_df = pd.read_csv("days.csv")
days_df.head()

days_df['weekday'] = pd.Categorical(days_df['weekday'], categories=
    ['Minggu','Senin','Selasa','Rabu','Kamis','Jumat','Sabtu'],ordered=True)

def create_use_df(df):
    daily_use_df = df.groupby(by='Date_Day').agg({
        'count': 'sum'
    }).reset_index()
    return daily_use_df

def create_register_df(df):
    daily_register_df = df.groupby(by='Date_Day').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_register_df

def create_casual_df(df):
    daily_casual_df = df.groupby(by='Date_Day').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_df

def create_season_df(df):
    daily_season_df = df.groupby(by='season').agg({
        'count': 'sum'
    }).reset_index()
    return daily_season_df

def create_weekday_df(df):
    daily_weekday_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_weekday_df



datetime_columns = ["Date_Day"]
days_df.sort_values(by="Date_Day", inplace=True)
days_df.reset_index(inplace=True)
 
for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])


min_date = days_df["Date_Day"].min()
max_date = days_df["Date_Day"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Periode Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = days_df[(days_df["Date_Day"] >= str(start_date)) & (days_df["Date_Day"] <= str(end_date))]

daily_use_df = create_use_df(main_df)
daily_season_df = create_season_df(main_df)
daily_weekday_df = create_weekday_df(main_df)
daily_register_df = create_register_df(main_df)
daily_casual_df = create_casual_df(main_df)



st.header('Statistik Penggunaan Speda :sparkles:')

st.subheader('Laporan Singkat')
 
col1, col2, col3 = st.columns(3)

with col1:
    total_speda = daily_use_df['count'].sum()
    st.metric("Total Speda Terpakai", value=total_speda)
with col2:
    total_register = daily_register_df['registered'].sum()  
    st.metric("Total Berlangganan", value=total_register)
with col3:
    total_casual = daily_casual_df['casual'].sum()
    st.metric("Total Tidak Berlangganan", value=total_casual)



st.subheader("Penggunaan Speda Berdasarkan Musim")
 
fig, ax = plt.subplots(figsize=(10, 5))
 
sns.barplot(
    y="count", 
    x="season",
    data=daily_season_df.sort_values(by="count", ascending=False),
    palette='coolwarm'
)
ax.set_title("Penggunaan Speda Berdasarkan Musim", loc="center", fontsize=15)
ax.set_ylabel('Jumlah Pengguna Speda')
ax.set_xlabel('Musim')
ax.tick_params(axis='x', labelsize=12)

for index, value in enumerate(daily_season_df['count']):
    ax.text(index, value, str(value), ha='center', va='bottom')

st.pyplot(fig)



st.subheader("Penggunaan Speda Berdasarkan Hari Weekday & Weekend")

fig, ax = plt.subplots()
sns.lineplot(
    data=daily_weekday_df ,
    x="weekday",
    y="count",
    color="darkred",
    marker="o",
    ax=ax
    )
 
ax.set_title("Penggunaan Sepeda Berdasarkan Hari", loc="center", fontsize=20)
plt.xlabel("Hari", fontsize=12)
ax.set_xlabel("Jumlah Penggunaan Sepeda", fontsize=12)
st.pyplot(fig)



st.subheader("Presentase Pengguna Sepeda yang Berlangganan dan Yang Tidak Berlangganan?")
total_registered = days_df['registered'].sum()
total_causal = days_df['casual'].sum()


label = ['Berlangganan', 'Tidak Berlangganan']
ukuran = [total_registered, total_causal]
colors = ['#93C572', '#E67F0D']  
explode = (0.1, 0)

fig, ax = plt.subplots()
ax.pie(
    x=ukuran,
    labels=label,
    autopct='%1.1f%%',
    colors=colors,
    explode=explode
)
ax.set_title("Distribusi Pengguna Berlangganan dan Tidak Berlangganan")
st.pyplot(fig)