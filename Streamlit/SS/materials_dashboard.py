import streamlit as st
#from streamlit_option_menu import option_menu
#from streamlit_extras.switch_page_button import switch_page

# Add sidebar for navigation
st.sidebar.title("Material Availability Assessment Dashboard")
page = ["Material Supply", "Material Demand", "Material Global Stocks", "Price Mechanism", "Modelling Inputs Review", "Calculate Results", "Plot Results"]
page = st.sidebar.selectbox("Select Step", ["Material Supply", "Material Demand", "Material Global Stocks", "Price Mechanism", "Modelling Inputs Review", "Calculate Results", "Plot Results"])

# def navigation_bar():
#     with st.container():
#         selected = option_menu(
#             menu_title=None,
#             options=["Home", "Upload", "Analytics", 'Settings', 'Contact'],
#             icons=['house', 'cloud-upload', "graph-up-arrow", 'gear', 'phone'],
#             menu_icon="cast",
#             orientation="horizontal",
#             styles={
#                 "nav-link": {
#                     "text-align": "left",
#                     "--hover-color": "#eee",
#                 }
#             }
#         )

# Page 1: Material Supply
if page == "Material Supply":
    st.header("Material Supply Characterization", divider='grey')
    # Add content for Material Supply page

# Page 2: Material Demand
if page == "Material Demand":
    st.header("Material Demand Characterization", divider='grey')
    # Add content for Material Demand page

# Page 3: Material Global Stocks
if page == "Material Global Stocks":
    st.header("Material Global Stocks", divider = 'grey')
    # Add content for Material Global Stocks page

# Page 4: Price Mechanism
if page == "Price Mechanism":
    st.header("Price Mechanism Setup", divider = 'grey')
    # Add content for Price Mechanism page

# Page 5: Modelling Inputs Review
if page == "Modelling Inputs Review":
    st.header("Nodelling Inputs Review", divider = 'grey')
    # Add content for Modelling Inputs Review page

# Page 6: Calculate Results
if page == "Calculate Results":
    st.header("Calculate Results", divider = 'grey')
    # Add content for Calculate Results page

# Page 7: Plot Results
if page == "Plot Results":
    st.header("Plot Results", divider = 'grey')
    # Add content for Plot Results page

