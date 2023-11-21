import streamlit
import pandas

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




streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would like information about?', 'Kiwi')
streamlit.write('the user entered', fruit_choice)


import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output it the screen as table
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("the fruit list contains:")
streamlit.dataframe(my_data_rows)

# Streamlit App starten
add_my_fruit = streamlit.text_input('What fruit would you like to add?', "")

# Wenn der Benutzer eine Frucht eingibt und auf "Submit" klickt
if streamlit.button('Submit'):
    # Überprüfen, ob die Benutzereingabe nicht leer ist
    if add_my_fruit:
        # SQL-Anweisung zum Einfügen eines neuen Datensatzes in die Tabelle
        insert_query = "INSERT INTO fruit_load_list (column_name) VALUES (?)"
        
        # Tupel erstellen, das die Benutzereingabe enthält
        data_tuple = (add_my_fruit,)
        
        # Versuch, die Transaktion durchzuführen
        try:
            # Datensatz einfügen
            my_cur.execute(insert_query, data_tuple)
            
            # Änderungen in der Datenbank speichern
            my_cnx.commit()
            
            # Benutzer benachrichtigen
            streamlit.write('Thanks for adding', add_my_fruit, 'to the fruit list!')
        
        # Im Falle eines Fehlers die Transaktion rückgängig machen
        except Exception as e:
            my_cnx.rollback()
            streamlit.write('Error:', str(e))
          
streamlit.write('thanks for adding', add_my_fruit)
