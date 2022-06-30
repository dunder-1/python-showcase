import webbrowser
import streamlit as st
from src import *

st.set_page_config(page_title="The MealDB", page_icon="🥗")

st.title("🥗 Recipes of The MealDB")

searchbar = st.text_input(
    "Search for recipes:", 
    placeholder="Try something like 'Pizza' 🍕 or 'Curry' 🍛"
)

#if rnd_recipe:
#    url_recipe = "https://www.themealdb.com/api/json/v1/1/random.php"

if searchbar:
    url_recipe = f"https://www.themealdb.com/api/json/v1/1/search.php?s={searchbar}"
    st.session_state.data = get_json(url_recipe, save_in_db=True)

    if st.session_state.data:
        st.caption(f"I found {len(st.session_state.data['meals'])} recipe(s) for you:")

        for i, meal in enumerate(st.session_state.data["meals"], start=1):

            meal = Meal.from_json(meal)

            with st.expander(meal.name):

                st.subheader(meal.name)

                col1, col2 = st.columns(2)

                with col1:
                    st.image(meal.thumbnail_url, use_column_width=True)
                    if st.button("Video", key=i):
                        webbrowser.open_new_tab(meal.youtube_url)
                    #st.write(f"[Video]({meal.youtube_url})", "", f"[Source]({meal.source_url})")
                    st.write("##### Ingredients")
                    lang = st.radio("Unit format:", ["en", "de"], key=i)#, horizontal=True) # streamlit >= 1.10.0
                    for ing, meas in meal.ingredients_translated(country_code=lang):
                        st.write(f"- {ing} ({meas})") 

                with col2:
                    st.write("##### Steps")
                    st.write(meal.instructions_as_md())

                #st.write("---")

    else:
        st.warning("Sorry, i didn't find anything :(")

