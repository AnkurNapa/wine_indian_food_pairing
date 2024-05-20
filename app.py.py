# Streamlit Wine Pairing App

import streamlit as st
import pandas as pd

# Load the datasets
wine_data = pd.read_csv('vivno_dataset.csv', encoding='utf-16')
food_data = pd.read_csv('indian_food.csv')

# Add example food items to various categories for demonstration purposes
food_data.loc[food_data['name'] == 'Paneer Tikka', 'flavor_profile'] = 'less spicy'
food_data.loc[food_data['name'] == 'Butter Chicken', 'flavor_profile'] = 'less spicy'
food_data.loc[food_data['name'] == 'Malai Kofta', 'flavor_profile'] = 'less spicy'
food_data.loc[food_data['name'] == 'Korma', 'flavor_profile'] = 'less spicy'
food_data.loc[food_data['name'] == 'Chicken Tikka', 'flavor_profile'] = 'less spicy'

food_data.loc[food_data['name'] == 'Vindaloo', 'flavor_profile'] = 'spicy'
food_data.loc[food_data['name'] == 'Chili Chicken', 'flavor_profile'] = 'spicy'
food_data.loc[food_data['name'] == 'Chettinad Chicken', 'flavor_profile'] = 'spicy'
food_data.loc[food_data['name'] == 'Bhuna Gosht', 'flavor_profile'] = 'spicy'
food_data.loc[food_data['name'] == 'Spicy Paneer', 'flavor_profile'] = 'spicy'

food_data.loc[food_data['name'] == 'Gulab Jamun', 'flavor_profile'] = 'sweet'
food_data.loc[food_data['name'] == 'Jalebi', 'flavor_profile'] = 'sweet'
food_data.loc[food_data['name'] == 'Rasgulla', 'flavor_profile'] = 'sweet'
food_data.loc[food_data['name'] == 'Ladoo', 'flavor_profile'] = 'sweet'
food_data.loc[food_data['name'] == 'Peda', 'flavor_profile'] = 'sweet'

food_data.loc[food_data['name'] == 'Mushroom Masala', 'flavor_profile'] = 'umami'
food_data.loc[food_data['name'] == 'Kebabs', 'flavor_profile'] = 'umami'
food_data.loc[food_data['name'] == 'Palak Paneer', 'flavor_profile'] = 'umami'
food_data.loc[food_data['name'] == 'Baingan Bharta', 'flavor_profile'] = 'umami'
food_data.loc[food_data['name'] == 'Rajma', 'flavor_profile'] = 'umami'

food_data.loc[food_data['name'] == 'Bitter Gourd Fry', 'flavor_profile'] = 'bitter'
food_data.loc[food_data['name'] == 'Fenugreek Thepla', 'flavor_profile'] = 'bitter'
food_data.loc[food_data['name'] == 'Karela Sabzi', 'flavor_profile'] = 'bitter'
food_data.loc[food_data['name'] == 'Neem Leaf Chutney', 'flavor_profile'] = 'bitter'
food_data.loc[food_data['name'] == 'Methi Paratha', 'flavor_profile'] = 'bitter'

def suggest_wine_pairing(food_flavor, wine_data, num_wines=3):
    if food_flavor == 'spicy':
        suggested_wines = wine_data[wine_data['ABV %'] <= 12.0]
    elif food_flavor == 'sweet':
        suggested_wines = wine_data[(wine_data['ABV %'] > 12.0) & (wine_data['Names'].str.contains("Dessert", case=False))]
    elif food_flavor == 'sour':
        suggested_wines = wine_data[wine_data['Names'].str.contains("Riesling|Sauvignon Blanc|Chardonnay", case=False) | 
                                    wine_data['Countrys'].str.contains("Germany|France", case=False)]
    elif food_flavor == 'less spicy':
        suggested_wines = wine_data[wine_data['Names'].str.contains("Sparkling|Champagne", case=False) | 
                                    wine_data['Countrys'].str.contains("France|Italy", case=False)]
    elif food_flavor == 'umami':
        suggested_wines = wine_data[wine_data['Names'].str.contains("Pinot Noir|Merlot", case=False) | 
                                    wine_data['Countrys'].str.contains("Burgundy|Italy", case=False)]
    elif food_flavor == 'bitter':
        suggested_wines = wine_data[wine_data['Names'].str.contains("Cabernet|Syrah", case=False) | 
                                    wine_data['Countrys'].str.contains("Bordeaux|Australia", case=False)]
    else:
        suggested_wines = wine_data

    # Get the top 3 highest priced wines
    high_priced_wines = suggested_wines.sort_values(by='Prices', ascending=False).head(num_wines)

    # Get the top 3 lowest priced wines
    low_priced_wines = suggested_wines.sort_values(by='Prices', ascending=True).head(num_wines)

    return high_priced_wines, low_priced_wines

# Streamlit App
st.title("Wine Pairing with Indian Food by Ankur Napa")

st.write("""
### About this App
I just created this app to try out the concept. Feel free to reach out to me if you really want to build similar and more powerful tools for your wine and fine dining restaurants.

**Contact:** [Ankur Napa on LinkedIn](https://www.linkedin.com/in/ankur-napa/)
""")

# Select food category
food_category = st.selectbox("Choose a food category:", ['spicy', 'less spicy', 'sweet', 'umami', 'bitter'])

# Filter food items based on selected category
filtered_food_data = food_data[food_data['flavor_profile'] == food_category]

selected_food = st.selectbox("Choose a food item:", filtered_food_data['name'].unique())

if st.button("🍷Get Wine Pairings"):
    high_priced_wines, low_priced_wines = suggest_wine_pairing(food_category, wine_data)
    food_details = filtered_food_data[filtered_food_data['name'] == selected_food].iloc[0]
    
    st.write(f"### Selected Food Item: {selected_food}")
    st.write(f"**Ingredients:** {food_details['ingredients']}")
    st.write(f"**Diet:** {food_details['diet']}")
    st.write(f"**Prep Time:** {food_details['prep_time']} minutes")
    st.write(f"**Cook Time:** {food_details['cook_time']} minutes")
    st.write(f"**Course:** {food_details['course']}")
    st.write(f"**State:** {food_details['state']}")
    st.write(f"**Region:** {food_details['region']}")
    st.write(f"**ABV (Alcohol by Volume) Note:** The selected wines have varied ABV percentages.")

    st.write("### Suggested Wines")

    # Combine high and low priced wines without icons
    high_priced_wines['Price'] = high_priced_wines['Prices'].astype(str)
    low_priced_wines['Price'] = low_priced_wines['Prices'].astype(str)
    
    combined_wines = pd.concat([high_priced_wines, low_priced_wines])

    st.table(combined_wines[['Names', 'Countrys', 'Price']].rename(columns={
        'Names': 'Wine Name',
        'Countrys': 'Country',
        'Price': 'Price'
    }))
