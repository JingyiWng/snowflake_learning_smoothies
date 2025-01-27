# Import python packages
import streamlit as st
import requests
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("Your favorite fruit is:", option)

# session = get_active_session() # Use this for SiS (Streamlit in Snowflake)
# With SniS, users will be able to connect to your app more easily. You can set up your SniS app in a way that doesn't require them to log in or have a USER in your Snowflake account. In fact, Streamlit will host your app for free if you make it open to the public. 
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# Convert the Snowpark df to a pandas df, so we can use the loc function                                                                       
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)                                                                

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5) 



if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}', icon="✅")
