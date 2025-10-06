# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":Cup_with_straw: Customize Your Smoothie! :cupt with straw:")
#st.title(f"Customize The Smoothie: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie,** Fruits available: Apple,
  Mango
  Banana
  Pomegranate
  """
)
# Fruit_options= st.selectbox(
#     "Choose Your Custom Fruits?",
#     ("Apple", "Mango", "Banana","Pomegranate"),
# )
#st.write("You selected:", Fruit_options)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be:", name_on_order)

# Get the current credentials
cnx=st.connection("snowflake");
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

#st.dataframe(data=my_dataframe, use_container_width=True)



ingredients_list = st.multiselect ('Choose upto 10 ingridients:',my_dataframe,max_selections=7)

ingredients_string = ''

if ingredients_list:
    ingredients_string = ' '
    
    for fruit_choosen in ingredients_list:
        ingredients_string +=fruit_choosen+' '

#st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

st.write(my_insert_stmt)
#st.stop()

time_to_insert = st.button('Submit Your Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success("Your Smoothie " + name_on_order + " is ordered!", icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
