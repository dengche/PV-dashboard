import streamlit as st
import os
# import os
# import sys
# from streamlit_extras.app_logo import add_logo

class Dashboard:
    def __init__(self):
        self.data = {
            "project_title": "",
            "project_investigator": "",
            "project_institution": "",
            "project_PV_technology": "",
            "project_target_metal": "",
            "project_description": "",
            "project_start_year": 2023,
            "project_end_year": 2024,
            "num_mines": 0,
            "mine_data": [],
            "global_production": 0,
            "direct_mining_growth": 0,
            "host_metal_name": "",
            "host_metal_production": 0,
            "host_metal_production_growth": 0,
            "hitchhiker_content": 0,
            "hitchhiker_recovery_efficiency": 0,
            "panel_lifetime": 0,
            "recycling_efficiency": 0,
            "recycling_collection_efficiency": 0,
            "percentage_panels_recycled": 0,
            "custom_pv_production": [],
        }

# initialise the session state
if "input" not in st.session_state:
    st.session_state.input = {}

# Get the absolute path of the image file
#image_path = os.path.abspath('C:/Users/franc/OneDrive/Desktop/Materials Dashboard/msu.jpg')


# Add sidebar for navigation
#with st.sidebar:
    #st.image(image_path, width=200)


st.sidebar.title("Material Availability Assessment Dashboard")

page = st.sidebar.selectbox("Dashboard Navigation", ["Home","Project Description","Material Supply", "Material Demand", "Material Global Stocks", "Price Mechanism", "Modelling Inputs Review", "Calculate Results", "Plot Results"])

st.sidebar.subheader("Home")
st.sidebar.subheader("Project Description")
st.sidebar.subheader("Material Supply")
st.sidebar.subheader("Material Demand")
st.sidebar.subheader("Material Global Stocks")
st.sidebar.subheader("Price Mechanism")
st.sidebar.subheader("Modelling Inputs Review")
st.sidebar.subheader("Calculate Results")
st.sidebar.subheader("Plot Results")

# Page 0: Home
if page == "Home":
    st.header("Home", divider='grey')    

    st.subheader("Introduction")
    
    st.markdown("This dashboard is designed to help you assess the availability of materials for Photovoltaics")

    st.subheader("Dashboard Modules")

    st.markdown("The dashboard is divided into 8 modules, each of which is designed to help you with a specific task. The modules are as follows:")
    st.markdown("- Project Description")
    st.markdown("- Material Supply")
    st.markdown("- Material Demand")
    st.markdown("- Material Global Stocks")
    st.markdown("- Price Mechanism")
    st.markdown("- Modelling Inputs Review")
    st.markdown("- Calculate Results")
    st.markdown("- Plot Results")
    
    st.subheader("Features and Dashboard Output")

    st.markdown("The dashboard is designed to help you with the following tasks: blablabla etc.")

    st.subheader("Get Started")

    use_options = ["I want to create my own scenario", "I want to use an existing analysis"]
    selected_use_option = st.selectbox("What are you looking for?", use_options)

    if selected_use_option == "I want to use an existing analysis":
        baseline_options = ["Tellurium Availability for CdTe - High Demand Scenario", "Tellurium Availability for CdTe - Business-as-Usual Scenario","Tellurium Availability for CdTe - Low Demand Scenario"]
        selected_supply_option = st.selectbox("Select from the available analyses", baseline_options)


# Page 1: Project Description

if page == "Project Description":
    st.header("Project Description", divider='grey')
    project_title = st.text_input("Project title*")
    project_investigator = st.text_input("Enter your name*")
    project_institution = st.text_input("Institution*")
    project_PV_technology = st.text_input("PV Technology*")
    project_target_metal = st.text_input("Target metal*")
    project_starting_year= st.number_input("Project timeline - starting year*",min_value=2023, step=1, value=2023)
    project_final_year = st.number_input("Project timeline - final year*", min_value=2024, step=1, value=2024)
    project_description = st.text_area("Description*", height=200)

    # Display the image
    #st.image(image_path)

    if st.button("Save"):
        #store analysis metadata in session state
        st.session_state.input["project_title"] = project_title
        st.session_state.input["project_investigator"] = project_investigator
        st.session_state.input["project_institution"] = project_institution
        st.session_state.input["project_PV_technology"] = project_PV_technology
        st.session_state.input["project_target_metal"] = project_target_metal
        st.session_state.input["project_description"] = project_description
        st.session_state.input["project_starting_year"] = project_starting_year 
        st.session_state.input["project_final_year"] = project_final_year

    st.write("Note: The * indicates required fields")
# Page 2: Material Supply
if page == "Material Supply":
    st.header("Material Supply Characterization", divider='grey')
    # Add content for Material Supply page
    st.subheader("Direct Mining")
    # Add content for Subsection 1
    supply_options = ["Manually input operating mines", "Calculate based on current production and future growth"]
    selected_supply_option = st.selectbox("Select Supply Option", supply_options)
    
    if selected_supply_option == "Manually input operating mines":
        num_mines = st.number_input("Enter the number of mines", min_value=0, step=1)
        mine_data = []

        for i in range(num_mines):
            st.subheader(f"Mine {i+1}")
            mine_name = st.text_input(f"Enter the name of Mine {i+1}")
            start_year = st.number_input(f"Enter the starting year for Mine {i+1}", min_value=0, step=1, key=f"start_year_{i}")
            #end_year = st.number_input(f"Enter the ending year for Mine {i+1}", min_value=start_year, step=1, key=f"end_year_{i}")
            annual_production = st.number_input(f"Enter the annual production for Mine {i+1}", min_value=0, step=1, key=f"annual_production_{i}")
            annual_production_growth = st.number_input(f"Enter the annual production growth for Mine {i+1}", min_value=0.0, step=0.01, key=f"annual_production_growth_{i}")
            operating_years = st.number_input(f"Enter the operating years for Mine {i+1}", min_value=0, step=1, key=f"operating_years_{i}")
            mine_data.append({
                "name": mine_name,
                "start_year": start_year,
                #"end_year": end_year,
                "annual_production": annual_production,
                "annual_production_growth": annual_production_growth,
                "operating_years": operating_years
            })
        #Store in session state
        st.session_state.input["mine_data"] = mine_data

        # Use mine_data for further processing
    
    if selected_supply_option == "Calculate based on current production and future growth":
        global_production = st.number_input("Enter the current annual global production", min_value=0)
        direct_mining_growth = st.number_input("Enter the annual growth rate", min_value = 0)
        #store inputs in session state
        st.session_state.input["global_production"] = global_production
        st.session_state.input["direct_mining_growth"] = direct_mining_growth

    st.divider()
    st.subheader("By-production")
    # Add content for Subsection 2
    host_metal_name = st.text_input("Enter the host metal name:")
    host_metal_production = st.number_input("Enter the host metal global annual production (in tonnes):")
    host_metal_production_growth = st.number_input("Enter the host metal annual production growth rate (%):")
    hitchhiker_content = st.number_input("Enter the hitchhiker metal content (ppm):")
    hitchhiker_recovery_efficiency = st.number_input("Enter the hitchhiker metal recovery efficiency (%):")

    st.session_state.input["host_metal_name"] = host_metal_name
    st.session_state.input["host_metal_name"] = host_metal_production
    st.session_state.input["host_metal_production_growth"] = host_metal_production_growth
    st.session_state.input["hitchhiker_content"] = hitchhiker_content
    st.session_state.input["hitchhiker_recovery_efficiency"] = hitchhiker_recovery_efficiency

    st.divider()
    st.subheader("Recycling")
    # Add content for Subsection 3
    panel_lifetime_options = ["Fixed Lifetime", "Weibull Model - Regular Loss Scenario", "Weibull Model - Early Loss Scenario"]
    selected_panel_lifetime_option = st.selectbox("Select the panel lifetime assumption", panel_lifetime_options)
    if selected_panel_lifetime_option == "Fixed Lifetime":
        panel_lifetime = st.number_input("Panel lifetime (in years)", min_value=0, step=1, value=25)
        #store in session state
        st.session_state.input["rec_panel_lifetime"] = panel_lifetime
    recycling_collection_efficiency = st.number_input("Enter the collection efficiency (%):", min_value=0, step=1, value=0)
    percentage_panels_recycled = st.number_input("Enter the percentage of panels recycled (%):", min_value=0, step=1, value=0)
    recycling_efficiency = st.number_input("Enter the recycling efficiency (%):", min_value=0, step=1, value=0)
    #store in session state
    st.session_state.input ["recycling_efficiency"] = recycling_efficiency
    st.session_state.input ["recycling_collection_efficiency"] = recycling_collection_efficiency
    st.session_state.input ["percentage_panels_recycled"] = percentage_panels_recycled

# Page 3: Material Demand

if page == "Material Demand":
    st.header("Material Demand Characterization", divider='grey')
    # Add content for Material Demand page
    st.subheader("1- PV Demand")
    # Add content for Subsection 1
    st.markdown("<p style='font-family: Arial; font-size: 16pt; font-weight: bold;'> 1.1- Future PV Production (GWp)</p>", unsafe_allow_html=True)
    future_pv_options = ["Default values", "Custom User Input"]
    selected_supply_option = st.selectbox("Future PV Production (GWp)", future_pv_options)
    if selected_supply_option == "Custom User Input":
        custom_years = st.session_state.input["project_final_year"] - st.session_state.input["project_starting_year"] + 1
        custom_pv_production = []
        for i in range(custom_years):
            year = st.session_state.input["project_starting_year"] + i
            # st.subheader(f"Year {year}")
            pv_production = st.number_input(f"Enter the PV production (GWp) for Year {year}", min_value=0, step=1, key=f"pv_production_{i}")
            custom_pv_production.append({
                "pv_production": pv_production
            })
        st.session_state.input["custom_pv_production"] = custom_pv_production
    
    # Use custom_years for further processing
    
    market_share_options = ["Constant", "Variable"]
    selected_market_share= st.selectbox("How do you want to calculate the future market share of the PV techology being assessed?", market_share_options)
    if selected_market_share == "Constant":
        pv_tech_market_share = st.number_input("Input market share of the PV being assessed (%)", min_value=0, step=1, value=0)
        st.session_state.input ["pv_tech_market_share"] = pv_tech_market_share
    else:
        current_pv_tech_market_share = st.number_input("Enter market share of the PV technology being assessed (%):", min_value=0, step=1, value=0)
        pv_tech_market_share_growth = st.number_input("Enter the future change in the market share (%):", min_value=0, step=1, value=0)
        st.session_state.input ["current_pv_tech_market_share"] = current_pv_tech_market_share
        st.session_state.input ["pv_tech_market_share_growth"] = pv_tech_market_share_growth


    st.markdown("<p style='font-family: Arial; font-size: 16pt; font-weight: bold;'> 1.2- Material Intensity</p>", unsafe_allow_html=True) 

    material_intensity_options = ["Preset Material Intensity Value","Customized Material Intensity Calculation Process"]
    selected_material_intensity = st.selectbox ("How do you want to input the material intensity?", material_intensity_options)
    if selected_material_intensity == "Preset Material Intensity Value":
        material_intensity = st.number_input("Enter the material intensity (kg/GWp)", min_value = 0, step=1, value = 0)
        st.session_state.input ["material_intensity"] = material_intensity
    else:
        st.write ("This feature is not available, yet.")

    material_intensity_change_options = ["I want to use a constant annual change (%)", "I want to manually input the material intensity every year"]
    selected_mat_int_change = st.selectbox ("How do you want to forecast material intensity change?", material_intensity_change_options)
    if selected_mat_int_change == "I want to use a constant annual change (%)":
        delta_mat_int = st.number_input ("Enter the annual material intensity change (%):", min_value = 0, step=1, value = 0)
        st.session_state.input ["delta_mat_int"] = delta_mat_int
    else:
        custom_material_intensity = []
        custom_years = st.session_state.input["project_final_year"] - st.session_state.input["project_starting_year"] + 1
        for i in range(custom_years):
            year = st.session_state.input["project_starting_year"] + i
            mat_int_annual = st.number_input(f"Enter the material intensity (kg/GWp) for Year {year}", min_value=0, step=1, key=f"mat_int_annual_{i}")
            custom_material_intensity.append({
                "material_intensity": mat_int_annual
            })
            st.session_state.input ["custom_material_intensity"] = custom_material_intensity
    st.subheader("2- Non-PV Demand")
    # Add content for Subsection 2          

    sty = st.session_state.input["project_starting_year"]
    nonPV_demand = st.number_input (f"Enter the current non-PV demand for Year {sty} (tonnes)", min_value=0, step=1, value = 0)
    nonPV_demand_gr = st.number_input ("Enter the annual growth rate in non-PV demand (%)", min_value=0, step=1, value = 0)
    st.session_state.input ["nonPV_demand"] = nonPV_demand
    st.session_state.input ["nonPV_demand_gr"] = nonPV_demand_gr
    
    
    # Page 4: Material Global Stocks
if page == "Material Global Stocks":
    st.header("Material Global Stocks", divider = 'grey')

    global_stocks_options = ["Yes, I can proceed with a quick input", "No, I need to calculate it"]
    selected_global_stocks_option = st.selectbox ("Do you know the current metal global stocks?", global_stocks_options)
    sty = st.session_state.input["project_starting_year"]
    metal = st.session_state.input["project_target_metal"]
    
    if selected_global_stocks_option == "Yes, I can proceed with a quick input":
        global_stocks = st.number_input (f"Enter the global stocks of {metal} for Year {sty}",min_value=0, step=1, value = 0)
        st.session_state.input ["global_stocks"] = global_stocks
    
    else:
        historical_starting_date = st.number_input("How historical is your historical data?", min_value = 1800, step = 5, value=2000)
        historical_ending_date = st.number_input("When does your historical analysis end?", min_value = 1800, step = 5, value = 2020)
        #store in session state
        st.session_state.input ["historical_starting_date"]=historical_starting_date
        st.session_state.input ["historical_ending_date"]=historical_ending_date



        # Add content for Material Global Stocks page
        st.subheader("Historical Supply")
        # Add content for Subsection 1
        metal = st.session_state.input["project_target_metal"] 
        historical_supply_user_data = []
        custom_years = st.session_state.input["historical_ending_date"] - st.session_state.input["historical_starting_date"] + 1
        for i in range(custom_years):
            year = st.session_state.input["historical_starting_date"] + i
            annual_hist_supply = st.number_input(f"Enter the {metal} supply for Year {year} (tonnes)", min_value=0, step=1, key=f"annual_hist_supply_{i}")
            historical_supply_user_data.append({
            "hist_supply": annual_hist_supply
            })
        st.session_state.input ["historical_supply_user_data"] = historical_supply_user_data

        st.subheader("Historical Demand")
        # Add content for Subsection 2
        metal = st.session_state.input["project_target_metal"] 
        historical_demand_user_data = []
        custom_years = st.session_state.input["historical_ending_date"] - st.session_state.input["historical_starting_date"] + 1
        for i in range(custom_years):
            year = st.session_state.input["historical_starting_date"] + i
            annual_hist_demand = st.number_input(f"Enter the {metal} demand for Year {year} (tonnes)", min_value=0, step=1, key=f"annual_hist_demand_{i}")
            historical_demand_user_data.append({
            "hist_supply": annual_hist_demand
            })
        st.session_state.input ["historical_demand_user_data"] = historical_demand_user_data

        #st.subheader("Global Stocks Calculation")
        # Add content for Subsection 3

# Page 5: Price Mechanism
if page == "Price Mechanism":
    st.header("Price Mechanism Setup", divider = 'grey')
    # Add content for Price Mechanism page

    metal = st.session_state.input["project_target_metal"]  

    st.subheader(f"1- Effect of Supply & Demand on the Price of {metal}")
    # Add content for Subsection 1    

    st.subheader("2- Effect of Price on PV demand")
    # Add content for Subsection 1
  
    st.subheader(f"3- Effect of Price on {metal} Yield")
    # Add content for Subsection 1

# Page 6: Modelling Inputs Review
if page == "Modelling Inputs Review":
    st.header("Modelling Inputs Review", divider = 'grey')
    # Add content for Modelling Inputs Review page

    proj_title = st.session_state.input["project_title"]
    proj_investigator = st.session_state.input["project_investigator"]
    proj_institution = st.session_state.input["project_institution"] 
    proj_PV_tech = st.session_state.input["project_PV_technology"] 
    proj_metal = st.session_state.input["project_target_metal"]
    Proj_Dscrpt = st.session_state.input["project_description"]
    
    st.subheader(f"{proj_title} - Project Information")
    st.write("User: " + proj_investigator)
    st.write("Institution: " + proj_institution)
    st.write("PV Technology: " + proj_PV_tech)
    st.write("Metal: " + proj_metal)
    st.write("Project Description: " + Proj_Dscrpt)

# Page 7: Calculate Results
if page == "Calculate Results":
    st.header("Calculate Results", divider='grey')
    # Add content for Calculate Results page

# Page 8: Plot Results
if page == "Plot Results":
    st.header("Plot Results", divider='grey')
    # Add content for Plot Results page

dashboard = Dashboard()
