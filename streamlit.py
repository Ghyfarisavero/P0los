import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import streamlit_option_menu
from streamlit_option_menu import option_menu

day_df = pd.read_csv("https://raw.githubusercontent.com/LittleBabyIcebear/Bike-Sharing-Project-/main/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/LittleBabyIcebear/Bike-Sharing-Project-/main/hour.csv")

day_df['dteday'] = pd.to_datetime(day_df["dteday"])
day_df['season'] = day_df['season'].astype('category')
day_df['season'] = day_df['season'].cat.rename_categories({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_df['weekday'] = day_df['weekday'].astype('category')
day_df['weekday'] = day_df['weekday'].cat.rename_categories({0: 'sunday', 1: 'monday', 2: 'tuesday', 3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday'})
day_df['holiday'] = day_df['holiday'].astype('category')
day_df['holiday'] = day_df['holiday'].cat.rename_categories({0: 'work', 1: 'holiday'})
day_df['weathersit'] = day_df['weathersit'].astype('category')
day_df['weathersit'] = day_df['weathersit'].cat.rename_categories({1: 'clear', 2: 'cloudy', 3: 'ltlrn', 4: 'hvyrn'})

hour_df['dteday'] = pd.to_datetime(hour_df["dteday"])
hour_df['season'] = hour_df['season'].astype('category')
hour_df['season'] = hour_df['season'].cat.rename_categories({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
hour_df['weekday'] = hour_df['weekday'].astype('category')
hour_df['weekday'] = hour_df['weekday'].cat.rename_categories({0: 'sunday', 1: 'monday', 2: 'tuesday', 3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday'})
hour_df['holiday'] = hour_df['holiday'].astype('category')
hour_df['holiday'] = hour_df['holiday'].cat.rename_categories({0: 'work', 1: 'holiday'})
hour_df['weathersit'] = hour_df['weathersit'].astype('category')
hour_df['weathersit'] = hour_df['weathersit'].cat.rename_categories({1: 'clear', 2: 'cloudy', 3: 'ltlrn', 4: 'hvyrn'})

st.title('Statistic Data Rental Bike')

with st.sidebar:
    selected = option_menu(
    menu_title = "Select statistic",
    options = ["Home","Pengaruh hari libur","Pengaruh beda hari","Pengaruh cuaca","Grafik sales"],
    default_index = 0,
    #orientation = "horizontal",
    )

if selected == 'Home':
    st.header ('tabel data')
    tab1, tab2 = st.tabs(['data harian', 'data per jam'])
    with tab1 :
        st.subheader('data harian')
        day_df

    with tab2 :
        st.subheader('data per jam')
        hour_df

if selected == 'Pengaruh hari libur':
    st.header ('Pengaruh Hari libur Terhadap Banyak Customer')
    x_day_df = day_df.groupby(['holiday'],as_index=False).cnt.sum()
    x_day_df

    fig , axs = plt.subplots(1, 2, figsize = (40,15))
    axs[0].bar(x= x_day_df['holiday'], height=x_day_df['cnt'])
    axs[0].tick_params(axis='y', labelsize=35)
    axs[0].tick_params(axis='x', labelsize=30)
    axs[0].set_ylabel('amount(million)', fontsize =45)

    axs[1].pie( x= x_day_df['cnt'], labels= x_day_df['holiday'], autopct='%1.1f%%', wedgeprops = {'width': 0.7}, explode= (0, 0.2), shadow=True, textprops={'fontsize': 35})

    st.pyplot(fig)
    with st.expander("Explanation"):
        st.write(
            """dapat dilihat bahwa hari libur mempengaruhi jumlah customer sebagaimana dapat dilihat pada grafik.
            pada hari kerja atau ketika tidak libur maka jumlah customer cenderung lebih banyak
            """
        )

if selected == 'Pengaruh beda hari' :
    st.header('pengaruh hari terhadap banyak customer')
    hari_day_mean = day_df.groupby(['weekday'], as_index=False).cnt.mean()
    hari_day= hari_day_mean['cnt'].map(int)
    hari_day_mean
    fig, axs =plt.subplots(1, 2, figsize=(40,15))
    
    axs[0].pie(x=hari_day, labels=hari_day_mean['weekday'], autopct='%1.1f%%', wedgeprops = {'width': 0.7}, textprops={'fontsize': 35})
    axs[0].tick_params(axis='y', labelsize=35)
    axs[0].tick_params(axis='x', labelsize=30)
    
    axs[1].barh(hari_day_mean['weekday'], hari_day_mean['cnt'])
    axs[1].set_xlabel('amount(milions)')

    st.pyplot(fig)
    with st.expander("Explanation"):
        st.write(
            """dapat dilihat bahwa perbedaan hari tidak seberapa berpengaruh terhadap jumlah customer.
            dari grafik dapat dilihat rata rata persentase jumlah customer di setiap harinya yakni 14%
            """
        )

if selected =='Pengaruh cuaca':
    st.header('Pengaruh Cuaca')
    
    season_df = day_df.groupby(["season", "weathersit"], as_index=False).agg({
    'temp' : "mean",
    'windspeed': 'mean' 
    })
    season_df
    st.subheader('pengaruh cuaca terhadap tempperatur dan kecepatan angin')

    fig, axs =plt.subplots(4, 1, figsize=(60,30))
    axs[1].scatter(season_df.at[0,'temp'], season_df.at[0,'windspeed'], label = 'clear')
    axs[1].scatter(season_df.at[1,'temp'], season_df.at[1,'windspeed'], label = 'cloudy')
    axs[1].scatter(season_df.at[2,'temp'], season_df.at[2,'windspeed'], label = 'little rain')
    axs[1].set_title("spring")

    axs[1].scatter(season_df.at[3,'temp'], season_df.at[3,'windspeed'], label = 'clear')
    axs[1].scatter(season_df.at[4,'temp'], season_df.at[4,'windspeed'], label = 'cloudy')
    axs[1].scatter(season_df.at[5,'temp'], season_df.at[5,'windspeed'], label = 'little rain')
    axs[1].set_title("summer")

    axs[2].scatter(season_df.at[6,'temp'], season_df.at[6,'windspeed'], label = 'clear')
    axs[2].scatter(season_df.at[7,'temp'], season_df.at[7,'windspeed'], label = 'cloudy')
    axs[2].scatter(season_df.at[8,'temp'], season_df.at[8,'windspeed'], label = 'little rain')
    axs[2].set_title("fall")

    axs[3].scatter(season_df.at[9,'temp'], season_df.at[9,'windspeed'], label = 'clear')
    axs[3].scatter(season_df.at[10,'temp'], season_df.at[10,'windspeed'], label = 'cloudy')
    axs[3].scatter(season_df.at[11,'temp'], season_df.at[11,'windspeed'], label = 'little rain')
    axs[3].set_title("winter")

    st.pyplot(fig)
    with st.expander('Explanation'):
        st.write(
            """ 
            - Pada grafik tersebut dapat dilihat pada musim gugur dan musim dingin kecepatan angin cenderung lebih pelan sedangkan pada musim semi dan musim panas kecepatan angin lebih kencang
            - Dari grafik tersebut dapat dilihat pada musim panas dan musim gugur temperatur akan jauh lebih hangat sedangkan pada musim semi dan musim dingin temperatur cenderung lebih tinggi
            - dari grafik tersebut pada saat cuaca sedikit hujan kecepatan angin berada di titik paling kencang sedangkan pada saat cuaca berawan kecepatan angin berada pada titik paling rendah
        """
        )

    st.subheader('pengaruh cuaca terhadap customer')
    season_day= day_df.groupby(['season'],as_index=False).cnt.sum()
    fig2, axs =plt.subplots(1, 2, figsize=(40, 15))

    plt.title('grafik pengaruh cuaca terhadap jumlah customer', fontsize = 30)
    axs[0].pie(x= season_day['cnt'], labels= season_day['season'], autopct='%1.1f%%', wedgeprops = {'width': 0.7},textprops={'fontsize': 35})
    axs[1].barh(season_day['season'], season_day['cnt'])
    axs[1].tick_params(axis='y', labelsize=35)
    axs[1].tick_params(axis='x', labelsize=30)
    axs[1].set_xlabel('amount(milions)', fontsize=30)

    st.pyplot(fig2)

    with st.expander('Explanation'):
        st.write(
            """ 
            Dari grafik tersebut dapat dilihat bahwa pada musim gugur jumlah customer penyewa sepeda berada di angka terbanyak,
            disusul dengan musim panas  kemudian musim dingin dan jumlah customer paling sedikit berada pada musim semi
        """
        )

if selected == 'Grafik sales':
    st.header('Grafik penjualan')
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    fig, ax = plt.subplots(figsize=(35, 15))
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=30)
    ax.plot(day_df['dteday'], day_df['cnt'])
    plt.xticks(rotation=45)
    
    st.pyplot(fig)
    with st.expander('Explanation'):
        st.write(
            """ 
            Dari grafik tersebut dapat kita lihat bahwa jumlah penjualan setiap hari dan bulannya selalu berfluktuatif tergantung dengan beberapa faktor yang telah di sebutkan sebelmunya
        """
        )
