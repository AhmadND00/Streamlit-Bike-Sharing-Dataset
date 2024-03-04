import datetime
import matplotlib.pyplot as plt
import mplcyberpunk
import pandas as pd
import streamlit as st
import seaborn as sns


plt.style.use("cyberpunk")

st.title("Bike Sharing Dataset Visualization")

st.write("Created By: Ahmad Nurcahyo Dharmajati")

df_day = pd.read_csv("./dashboard/processed_df_day.csv")
df_hour = pd.read_csv("./dashboard/processed_df_hour.csv")

df_day['date'] = pd.to_datetime(df_day['date'])
earliest = df_day['date'].min()
latest = df_day['date'].max()

with st.sidebar:
    st.image("src/dataset-cover.jpg")

    filter = st.radio(
        "Check ",
        ["Daily Data", "Hourly Data"],
        index=None,
    )

    st.write("You selected:", filter)

if filter == None:
    st.write('Bike Sharing Dataset: ', df_hour)
    st.markdown('**Note**: Select one of the option at the sidebar to show visualization of the dataset')
elif filter == 'Daily Data':
    st.subheader("Seasonal Data")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(5,5))
        ax.plot(df_day['date'], df_day['cnt'])
        ax.set_title('Bike Rentals by Date')
        ax.set_xlabel('Date')
        plt.xticks(rotation=45)
        ax.set_ylabel('Number of Rentals')

        st.pyplot(fig)
    with col2:
        grouped_season = df_day.groupby('season').agg({
            'cnt': 'sum'
        })

        fig, ax = plt.subplots()
        ax.pie(
            x=grouped_season['cnt'],
            labels=grouped_season.index,
            autopct='%1.1f%%',
            wedgeprops={'width': 0.2}
        )
        ax.set_title('Bike Rentals by Season')
        st.pyplot(fig)

    option = st.selectbox(
       "Filter by Season",
       ("Spring 2011", "Summer 2011", "Fall 2011", 'Winter 2011', "Spring 2012", "Summer 2012", "Fall 2012", 'Winter 2012'),
       index=None,
       placeholder="Filter by season...",
    )

    if option == "Spring 2011":
        st.write("Data Between 1 January 2011 - 20 March 2011 (Incomplete)")
        df_range = df_day[(df_day['date'] >= '2011-01-01') & (df_day['date'] <= '2011-03-20')]
    elif option == "Summer 2011":
        st.write("Data Between 21 March 2011 - 20 June 2011")
        df_range = df_day[(df_day['date'] >= '2011-03-21') & (df_day['date'] <= '2011-06-20')]
    elif option == "Fall 2011":
        st.write("Data Between 21 June 2011 - 22 September 2011")
        df_range = df_day[(df_day['date'] >= '2011-06-21') & (df_day['date'] <= '2011-09-22')]
    elif option == "Winter 2011":
        st.write("Data Between 23 September 2011 - 20 December 2011")
        df_range = df_day[(df_day['date'] >= '2011-09-23') & (df_day['date'] <= '2011-12-20')]
    elif option == "Spring 2012":
        st.write("Data Between 1 January 2012 - 20 March 2012")
        df_range = df_day[(df_day['date'] >= '2011-12-21') & (df_day['date'] <= '2012-03-20')]
    elif option == "Summer 2012":
        st.write("Data Between 21 March 2012 - 20 June 2012")
        df_range = df_day[(df_day['date'] >= '2012-03-21') & (df_day['date'] <= '2012-06-20')]
    elif option == "Fall 2012":
        st.write("Data Between 21 June 2012 - 22 September 2012")
        df_range = df_day[(df_day['date'] >= '2012-06-21') & (df_day['date'] <= '2012-09-22')]
    elif option == "Winter 2012":
        st.write("Data Between 23 September 2012 - 20 December 2012")
        df_range = df_day[(df_day['date'] >= '2012-09-23') & (df_day['date'] <= '2012-12-20')]
    elif option == "Spring 2013":
        st.write("Data Between 21 December 2012 - 31 December 2012 (Incomplete)")
        df_range = df_day[(df_day['date'] >= '2012-12-21') & (df_day['date'] <= '2012-12-31')]

    if option:
        fig, ax = plt.subplots()
        ax.plot(df_range['date'], df_range['cnt'])
        ax.set_title(f'Bike Rentals in {option}')
        ax.set_ylabel('Number of Rentals')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.write('Total Rental: ', df_range['cnt'].sum())
        st.write('- Casual Rental: ', df_range['casual'].sum())
        st.write('- Registered Rental: ', df_range['registered'].sum())
        st.write(f"Number of Holiday : {(df_range['holiday'] == 1).sum()}")
        st.write(f"Number of Working Day : {(df_range['workingday'] == 1).sum()}")

        st.markdown("<h5 style='text-align: center; color: grey;'>Weather (Normalized Value)</h5>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric('Average Temperature', value=round(df_range['temp'].mean(), 2))
            fig1, ax1 = plt.subplots()
            ax1.scatter(df_range['temp'], df_range['cnt'])
            ax1.set_xlabel('Temperature (Celsius)')
            ax1.set_ylabel('Number of Rentals')
            ax1.set_title('Rental by Temperature')
            st.pyplot(fig1)

        with col2:
            st.metric('Average Humidity', value=round(df_range['hum'].mean(), 2))
            fig2, ax2 = plt.subplots()
            ax2.scatter(df_range['hum'], df_range['cnt'])
            ax2.set_xlabel('Humidity (%)')
            ax2.set_ylabel('Number of Rentals')
            ax2.set_title('Rental by Humidity')
            st.pyplot(fig2)

        with col3:
            st.metric('Average Wind Speed', value=round(df_range['windspeed'].mean(), 2))
            fig3, ax3 = plt.subplots()
            ax3.scatter(df_range['windspeed'], df_range['cnt'])
            ax3.set_xlabel('Wind Speed (m/s)')
            ax3.set_ylabel('Number of Rentals')
            ax3.set_title('Rental by Wind Speed')
            st.pyplot(fig3)

elif filter == 'Hourly Data':
    st.subheader("Average Bike Rental at Each Hour")
    fig, ax = plt.subplots()
    ax.bar(x=df_hour['hour'], height=df_hour['cnt'])
    plt.xlabel('Hour')
    plt.ylabel('Count')

    st.pyplot(fig)

    selected_date = st.date_input("Select Date:", value=None, min_value=pd.to_datetime('2011-01-01'),
                                  max_value=pd.to_datetime('2012-12-31'))

    if selected_date:
        df_hour['date'] = pd.to_datetime(df_hour['date'])
        df_hour['date'] = df_hour['date'].dt.date

        df_selected_day = df_hour[df_hour['date'] == (selected_date)]

        fig, ax = plt.subplots()
        sns.lineplot(data=df_selected_day, x='hour', y='casual', label='Casual', ax=ax)
        sns.lineplot(data=df_selected_day, x='hour', y='registered', label='Registered', ax=ax)

        plt.title('Number of Casual and Registered Bike Rentals Per Hour')
        plt.xlabel('Hour')
        plt.ylabel('Number of Bikes Rented')

        plt.legend()

        st.pyplot(fig)

        st.write('Total Rental: ', df_selected_day['cnt'].sum())
        st.write('- Casual Rental: ', df_selected_day['casual'].sum())
        st.write('- Registered Rental: ', df_selected_day['registered'].sum())

        if df_selected_day['holiday'].iloc[0] == 1:
            st.text("Today is a holiday!")

        st.markdown("<h5 style='text-align: center; color: grey;'>Weather (Normalized Value)</h5>",
                    unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric('Average Temperature', value=round(df_selected_day['temp'].mean(), 2))
            fig1, ax1 = plt.subplots()
            ax1.plot(df_selected_day['hour'], df_selected_day['temp'])
            ax1.set_xlabel('Hour')
            ax1.set_ylabel('Temperature (Celsius)')
            ax1.set_title('Hourly Temperature')
            st.pyplot(fig1)

        with col2:
            st.metric('Average Humidity', value=round(df_selected_day['hum'].mean(), 2))
            fig2, ax2 = plt.subplots()
            ax2.plot(df_selected_day['hour'], df_selected_day['hum'])
            ax2.set_xlabel('Hour')
            ax2.set_ylabel('Humidity')
            ax2.set_title('Hourly Humidity')
            st.pyplot(fig2)

        with col3:
            st.metric('Average Wind Speed', value=round(df_selected_day['windspeed'].mean(), 2))
            fig3, ax3 = plt.subplots()
            ax3.plot(df_selected_day['hour'], df_selected_day['windspeed'])
            ax3.set_xlabel('Hour')
            ax3.set_ylabel('Wind Speed')
            ax3.set_title('Hourly Wind Speed')
            st.pyplot(fig3)
