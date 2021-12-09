"""
Name: Allison Curcio
CS230: Section 5
Data: Skyscraper
URL:
Description: This program is intended for a engineer developer interested in looking at previous skyscraper projects.
The user can come into the application, select multiple cities, the maximum number in a range of floors in a skyscraper,
the minimum number in a range of years, and the type of material the skyscraper is made of. From there, the
user can see a table of the skyscraper rank, name, city, completion year, height (m), floors, and function. The user
can see a map of all the skyscrapers with their name, completion year, and function. There is a pie chart that shows
the percentage of skyscrapers in each selected city based on the filters, and a bar graph that shows the total number
of skyscrapers in each city based on the filters.
"""
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
from PIL import Image
import folium


def read_data():
    return pd.read_csv("Skyscrapers2021.csv").set_index("RANK")


# filter the data
def filter_data(sel_city, min_completion, max_floor, material):
    df = read_data()
    df = df.loc[df['CITY'].isin(sel_city)]
    df = df.loc[df['FLOORS'] < max_floor]
    df = df.loc[df['MATERIAL'] == material]
    df = df.loc[df['COMPLETION'] > min_completion]
    st.dataframe(df.iloc[:, [0, 1, 5, 7, 9, 11]])
    return df


def count_cities(cities, df):
    return [df.loc[df['CITY'].isin([CITY])].shape[0] for CITY in cities]


def all_cities():
    df = read_data()
    df = df.sort_values(['CITY'], ascending=True)
    lst = []
    for ind, row in df.iterrows():
        if row['CITY'] not in lst:
            lst.append(row['CITY'])
    return lst


def materials():
    df = read_data()
    lst_material = []
    for ind, row in df.iterrows():
        if row["MATERIAL"] not in lst_material:
            lst_material.append(row['MATERIAL'])
    return lst_material


# Pie Chart
def generate_pie_chart(counts, sel_city):
    plt.figure()
    st.write(f"Cities Chosen that Show: {','.join(sel_city)}")
    explodes = [0 for i in range(len(counts))]
    maximum = counts.index(np.max(counts))
    explodes[maximum] = 0.25
    plt.pie(counts, labels=sel_city, explode=explodes, autopct="%.2f")
    plt.title(f"Share of Skyscrapers")
    return plt


# x in bar chart: city
def skyscraper_city(df):
    count = [row['NAME'] for ind, row in df.iterrows()]
    cities = [row['CITY'] for ind, row in df.iterrows()]
    dict = {}
    for city in cities:
        dict[city] = []
    for i in range(len(count)):
        dict[cities[i]].append(count[i])
    return dict


# y in bar chart: number of skyscrapers
def skyscraper_counts(dict_count):
    dict = {}
    for key in dict_count.keys():
        dict[key] = len(dict_count[key])
    return dict


# Bar Chart
def generate_bar_chart(dict_count):
    plt.figure()
    x = dict_count.keys()
    y = dict_count.values()
    st.write(f"Cities Chosen that Show: {','.join(dict_count.keys())}")
    plt.bar(x, y, color='y')
    plt.xticks(rotation=45)
    plt.ylabel("Number of Skyscrapers")
    plt.xlabel("City")
    plt.title(f"Number of Skyscrapers per City")
    return plt


# Map- thought was cool using folium!
def showonmap(df):
    df = df.filter(['NAME', 'CITY', 'COMPLETION', 'FUNCTION', 'Latitude', 'Longitude'])
    center = [42.36165764, -71.08567345]
    map = folium.Map(location=center,
                     zoom_start=2, control_scale=True)
    for index, location_info in df.iterrows():
        folium.Marker(location=[location_info["Latitude"], location_info['Longitude']],
                      tooltip=location_info["NAME"],
                      popup='Created in ' + str(location_info["COMPLETION"]) +
                            ' in ' + location_info["CITY"] + '. Used for ' + location_info["FUNCTION"]).add_to(map)
    folium_static(map)


def main():
    # I thought my title was cool/complex! I am not familiar with HTML, taught myself for this!
    # Adding the picture is something I thought was cool!
    new_title = '<p style="font-family:sans-serif; color:Purple; font-size: 42px;">Skyscrapers</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    image = Image.open('Skyscrapers.jpg')
    st.image(image)
    st.subheader("Open the sidebar to begin.")
    st.write("You have chosen the following data:")
    st.sidebar.write("Please choose your options to display data.")
    city = st.sidebar.multiselect("Select a City: ", all_cities())
    max_floor = st.sidebar.slider("Maximum Number of Floors: ", 0, 200)  # everything less than selected floor
    min_completion = st.sidebar.slider("Created after Selected Year: ", 1900,
                                       2020)  # everything greater than selected year
    material = st.sidebar.radio("Select a Building Material", materials())
    data = filter_data(city, min_completion, max_floor, material)
    series = count_cities(city, data)

    if len(city) > 0 and min_completion > 0 and max_floor > 0 and len(material) > 0:
        new_title = '<p style="font-family:sans-serif; color:Purple; font-size: 35px;">Map of Selected Cities</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        showonmap(data)

        new_title = '<p style="font-family:sans-serif; color:Purple; font-size: 35px;">Skyscraper Pie Chart</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.write(f"For years after: {(str(min_completion))}")
        st.write(f"Skyscrapers up to {max_floor} floors")
        st.pyplot(generate_pie_chart(series, city))

        new_title = '<p style="font-family:sans-serif; color:Purple; font-size: 35px;">Skyscraper Bar Chart</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.write(f"For years after: {(str(min_completion))}")
        st.write(f"Skyscrapers up to {max_floor} floors")
        st.pyplot(generate_bar_chart(skyscraper_counts(skyscraper_city(data))))


main()
