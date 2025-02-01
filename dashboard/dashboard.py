import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# load data
days_df = pd.read_csv('./data/days_data.csv')
hours_df = pd.read_csv('./data/hours_data.csv')

min_date = days_df["dteday"].min()
max_date = days_df["dteday"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# define data berdasarkan rentang waktu
main_df = days_df[(days_df["dteday"] >= str(start_date)) & 
                (days_df["dteday"] <= str(end_date))]

main_df_hours = hours_df[(hours_df["dteday"] >= str(start_date)) &
                        (hours_df["dteday"] <= str(end_date))]

# exploratory data analysis
weather_df = main_df.groupby('weathersit')['cnt'].sum().sort_values(ascending=False).reset_index()
weather_df.columns = ['weather', 'cnt']
season_df = main_df.groupby('season')['cnt'].sum().sort_values(ascending=False) .reset_index()
season_df.columns = ['season', 'cnt']
trend_df = days_df.groupby(by=['yr', 'mnth']).agg({'cnt': 'sum'}).reset_index()
hour_use_df = main_df_hours.groupby(by='hr').agg({'cnt': 'sum'}).reset_index()

trend_df['yr'] = trend_df['yr'] + 2011
trend_df['date'] = pd.to_datetime(trend_df['yr'].astype(str) + '-' + trend_df['mnth'].astype(str))

st.header("Data Penyewaan Sepeda Tahun 2011-2012")

# Data trend penyewaan sepeda per bulan dalam 2 tahun
st.subheader("Data trend penyewaan sepeda per bulan dalam 2 tahun")
st.write("*static data")
fig, ax = plt.subplots(figsize=(24, 10))
ax.plot(
    trend_df["date"],
    trend_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# Penyewaan sepeda berdasarkan cuaca dan musim
st.subheader("Penyewaan sepeda berdasarkan cuaca dan musim")
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    sns.barplot(
        y="cnt", 
        x="weather",
        data=weather_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Penyewaan sepeda berdasarkan cuaca", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="cnt", 
        x="season",
        data=season_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Penyewaan sepeda berdasarkan musim", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)


# Penyewaan sepeda berdasarkan jam / Jam paling sibuk
st.subheader("Penyewaan sepeda berdasarkan jam")
col1, col2 = st.columns(2)
 
with col1:
    most_active_hour = hour_use_df.loc[hour_use_df['cnt'].idxmax()]['hr']
    st.metric("Jam paling aktif", value=most_active_hour)
 
with col2:
    less_active_hour = hour_use_df.loc[hour_use_df['cnt'].idxmin()]['hr']
    st.metric("Jam paling tidak aktif", value=less_active_hour)

fig, ax = plt.subplots(figsize=(20, 10))
ax.bar(hour_use_df['hr'], hour_use_df['cnt'], color='#90CAF9')
ax.set_title('Penyewaan sepeda berdasarkan jam', fontsize=30)
ax.set_xlabel('Jam', fontsize=20)
ax.set_ylabel('Total Penyewaan', fontsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)
