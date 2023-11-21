import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner 1')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

###########################################################################################################################
#create the repeatable code block (called function)
def get_fruityvice_data(this_fruit_choice):
          fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
          fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
          return fruityvice_normalized

#New Section to display fruitvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
          fruit_choice = streamlit.text_input('What fruit would like information about?')
          if not fruit_choice:
                    streamlit.error("please select a fruit to get information.")
          else:
                    back_from_function = get_fruityvice_data(fruit_choice)
                    streamlit.dataframe(back_from_function)          

###############################################################################################################################          
streamlit.header("the fruit list contains:")
#Snowflake-related functions
def get_fruit_load_list():
          with my_cnx.cursor() as my_cur:
               my_cur.execute("SELECT * from fruit_load_list")
               return my_cur.fetchall()

#add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
          my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
          my_data_rows = get_fruit_load_list()
          streamlit.dataframe(my_data_rows)
################################################################################################################################

def insert_row_snowflake(new_fruit):
          with my_cnx.cursor() as my_cur:
                    my_cur.execute("INSERT INTO fruit_load_list VALUES ('from streamlit')")
                    return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
          my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
          back_from_function = insert_row_snowflake(new_fruit)
          streamlit.text(back_from_function)

