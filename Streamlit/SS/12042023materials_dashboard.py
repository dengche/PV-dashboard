import streamlit as st
#from streamlit_option_menu import option_menu
#from streamlit_extras.switch_page_button import switch_page

# Add sidebar for navigation
st.sidebar.title("Material Availability Assessment Dashboard")
page = ["Material Supply", "Material Demand", "Material Global Stocks", "Price Mechanism", "Modelling Inputs Review", "Calculate Results", "Plot Results"]
page = st.sidebar.selectbox("Select Step", ["Material Supply", "Material Demand", "Material Global Stocks", "Price Mechanism", "Modelling Inputs Review", "Calculate Results", "Plot Results"])

# Page 1: Material Supply
if page == "Material Supply":
    st.header("Material Supply Characterization", divider='grey')
    # Add content for Material Supply page
    st.subheader("Main Production")
    # Add content for Subsection 1
    supply_options = ["Manually input operating mines", "Calculate based on current production and future growth"]
    selected_supply_option = st.selectbox("Select Supply Option", supply_options)

    st.subheader("ByProduction")
    # Add content for Subsection 2
    host_metal_name = st.text_input("Enter the host metal name:")
    
    st.subheader("Recycling")
    # Add content for Subsection 3
    recycling_rate = st.text_input("Enter the recycling rate:")
    recycling_rate = st.text_input("Enter the collection efficiency:")

# Page 2: Material Demand
if page == "Material Demand":
    st.header("Material Demand Characterization", divider='grey')
    # Add content for Material Demand page
    st.subheader("PV Demand")
    # Add content for Subsection 1

    st.subheader("Non-PV Demand")
    # Add content for Subsection 2    

# Page 3: Material Global Stocks
if page == "Material Global Stocks":
    st.header("Material Global Stocks", divider = 'grey')
    # Add content for Material Global Stocks page
    st.subheader("Historical Supply")
    # Add content for Subsection 1

    st.subheader("Historical Demand")
    # Add content for Subsection 2

    st.subheader("Global Stocks Calculation")
    # Add content for Subsection 3


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

