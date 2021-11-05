import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import altair as alt



#-------------------------------------------------DATA PRE-PROCESSING--------------------------------------------------------------------#
raw_data = pd.read_csv("updated_data.csv")
raw_data = raw_data.dropna()
column_names = [
    "Total Cases",
    "Total Deaths",
    "Total Recovered",
    "Active Cases",
    "Serious / Critical Condition",
    "Total Cases / 1M Population",
    "Deaths / 1M Population",
    "Total Tests",
    "Tests / 1M Population",
    "Population"]

for a in column_names:
    raw_data[a] = pd.to_numeric(raw_data[a])


#-------------------------------------------------STREAMLIT CODE--------------------------------------------------------------------#
st.title("COVID-19 Dashboard")


#SIDEBAR MENU
option = st.sidebar.selectbox(
    "Menu:",
    [
        "Homepage",
        "Download"
    ]
)


#------------------------------------------------- HOMEPAGE CODE --------------------------------------------------------------------#
if option == "Homepage":
    st.write("Coronavirus disease 2019 (COVID-19) is a contagious "
             "disease caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). "
             "The first known case was identified in Wuhan, China, in December 2019. "
             "The disease has since spread worldwide, leading to an ongoing pandemic.")

    st.write("This web app summarizes the dataset on Coronavirus Records for 2021. This dataset contains COVID-19 reports on:")
    st.write("1. Total cases")
    st.write("2. Total deaths")
    st.write("3. Total recovered")
    st.write("4. Active cases")
    st.write("5. Serious or Critical Condition")
    st.write("6. Total Cases per 1 Million Population")
    st.write("7. Deaths per 1 Million Population")
    st.write("8. Total Tests")
    st.write("9. Tests per 1 Million Population")
    st.write("10. Population")
    st.write("The original data has been pre-processed to include the langitude and longitude of the capital city of each country and the continent. "
             "This data only includes the countries that has records on the above indicators.")

    st.subheader("COVID-19 in the World")

    #DATA PRE-PROCESSING
    data_to_plot = raw_data[["Country, Other", "Total Cases", "Total Deaths", "CapitalLatitude", "CapitalLongitude"]]
    total_cases = raw_data["Total Cases"].sum()
    total_deaths = int(raw_data["Total Deaths"].sum())


    #SETUP METRIC
    col1, mid, col2 = st.columns([20,3,20])
    with col1:
        st.metric(label="Total cases", value="{:,}".format(total_cases))
    with col2:
        st.metric(label="Total deaths", value="{:,}".format(total_deaths))

    #SETUP FOLIUM
    st.write("Hover over the pin to see the country name and its total cases of COVID-19.")
    map = folium.Map(location=[raw_data.CapitalLatitude.mean(),raw_data.CapitalLongitude.mean()], zoom_start=1)

    for country in range(len(data_to_plot)):
        lat = data_to_plot.iloc[country, 3]
        long = data_to_plot.iloc[country, 4]

        country_name = data_to_plot.iloc[country, 0]
        total_cases = data_to_plot.iloc[country, 1]
        text = f"{country_name}, Total cases: {total_cases}"
        folium.Marker([lat, long], tooltip=text).add_to(map)

    folium_static(map)


    st.subheader("Distribution of Deaths by COVID-19")

    #SETUP ALTAIR
    chart1 = alt.Chart(data_to_plot).mark_rect().encode(
        alt.X("CapitalLatitude", bin=alt.Bin(maxbins=60)),
        alt.Y("CapitalLongitude", bin=alt.Bin(maxbins=40)),
        alt.Color("Total Deaths", scale=alt.Scale(scheme="yelloworangered")),
        tooltip=["Country, Other", "Total Cases", "Total Deaths"]
    ).properties(
        height=600,
        width=800
    )

    st.altair_chart(chart1)


#------------------------------------------------- ANALYSE BY CONTINENTS --------------------------------------------------------------------#
    st.subheader("Analysis of COVID-19 by Continent")

    continent_option = st.selectbox("Select continent",
        ["Africa",
        "Asia",
        "Australia",
        "Europe",
        "Central America",
        "North America",
        "South America"]
    )


    st.write("Data shown is normalized to 1M population.")

    #DATA PRE-PROCESSING
    country_list = []
    death_cases = []
    covid_cases = []

    for n in range(len(raw_data)):
        if raw_data.iloc[n, -1] == continent_option:
            country_list.append(raw_data.iloc[n, 1])
            covid_cases.append(raw_data.iloc[n, 7])
            death_cases.append(raw_data.iloc[n, 8])


    deaths = {"Country":country_list,
              "Total Deaths":death_cases}
    deaths = pd.DataFrame(deaths)
    cases = {"Country":country_list,
              "Total Cases":covid_cases}
    cases = pd.DataFrame(cases)


    #SETUP ALTAIR
    chart2 = alt.Chart(cases).mark_bar(
        color="lightgreen",
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3
    ).encode(
        x="Country:O",
        y="Total Cases:Q",
        tooltip=["Country", "Total Cases"]
    )

    st.altair_chart(chart2, use_container_width=True)


    chart3 = alt.Chart(deaths).mark_bar(
        color="tomato",
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3
    ).encode(
        x="Country:O",
        y="Total Deaths:Q",
        tooltip=["Country", "Total Deaths"]
    )

    st.altair_chart(chart3, use_container_width=True)



#------------------------------------------------- PAGE 2 DOWNLOAD --------------------------------------------------------------------#
else:
    st.header("Dowload")
    st.write("You can download the data used in this analysis.")

    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(raw_data)

    st.download_button(
        label="Download data as CSV",
        data = csv,
        file_name="world-covid-data.csv",
        mime='text/csv'
    )





st.caption("This is a web app demo using [streamlit](https://streamlit.io/) library. It is hosted on [heroku](https://www.heroku.com/).")
st.caption("For more info, please contact: [SarahMelina] (https://www.linkedin.com/in/sarahmelina/) on LinkedIn.")