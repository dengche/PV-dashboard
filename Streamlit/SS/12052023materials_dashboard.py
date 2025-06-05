import streamlit as st


#List of variables
project_final_year = 2024  # Define the variable before using it
project_starting_year = 2023  # Define the variable before using it

# Add sidebar for navigation
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
    project_title = st.text_input("Project title")
    project_investigator = st.text_input("Enter your name")
    project_institution = st.text_input("Institution")
    project_PV_technology = st.text_input("PV Technology")
    project_target_metal = st.text_input("Target metal")
    project_starting_year= st.number_input("Project timeline - starting year",min_value=2023, step=1, value=2023)
    project_final_year = st.number_input("Project timeline - final year", min_value=2024, step=1, value=2024)
    project_description = st.text_area("Description", height=200)

# Create or get the session state
state = st.session_state.get("project_starting_year", project_starting_year)
state = st.session_state.get("project_final_year", project_final_year)


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

        # Use mine_data for further processing
    
    if selected_supply_option == "Calculate based on current production and future growth":
        global_production = st.number_input("Enter the current annual global production", min_value=0)
        direct_mining_growth = st.number_input("Enter the annual growth rate", min_value = 0)

    st.divider()
    st.subheader("By-production")
    # Add content for Subsection 2
    host_metal_name = st.text_input("Enter the host metal name:")
    host_metal_production = st.number_input("Enter the host metal global annual production (in tonnes):")
    host_metal_production_growth = st.number_input("Enter the host metal annual production growth rate (%):")
    hitchhiker_content = st.number_input("Enter the hitchhiker metal content (ppm):")
    hitchhiker_recovery_efficiency = st.number_input("Enter the hitchhiker metal recovery efficiency (%):")

    st.divider()
    st.subheader("Recycling")
    # Add content for Subsection 3
    panel_lifetime_options = ["Fixed Lifetime", "Weibull Model - Regular Loss Sceario", "Weibull Model - Early Loss Sceario"]
    selected_panel_lifetime_option = st.selectbox("Select the panel lifetime assumption", panel_lifetime_options)
    if selected_panel_lifetime_option == "Fixed Lifetime":
        panel_lifetime = st.number_input("Panel lifetime (in years)", min_value=0, step=1, value=25)
    recycling_efficiency = st.text_input("Enter the recycling efficiency (%):")
    recycling_collection_efficiency = st.text_input("Enter the collection efficiency (%):")
    percentage_panels_recycled = st.number_input("Enter the percentage of panels recycled (%):")

# Page 3: Material Demand

if page == "Material Demand":
    st.header("Material Demand Characterization", divider='grey')
    # Add content for Material Demand page
    st.subheader("1- PV Demand")
    # Add content for Subsection 1
    st.markdown("<p style='font-family: Arial; font-size: 16pt; font-weight: bold;'> 1.1- Future PV Production (GWp)</p>", unsafe_allow_html=True)
    future_pv_options = ["Default values", "Custom User Input"]
    selected_supply_option = st.selectbox("Future PV Production", future_pv_options)
    if selected_supply_option == "Custom User Input":
        custom_years = project_final_year - project_starting_year + 1
        custom_pv_production = []
        for i in range(custom_years):
            st.subheader(f"Year {project_starting_year +i}")
            pv_production = st.number_input(f"Enter the PV production (GWp)", min_value=0, step=1, key=f"pv_production_{i}")
            custom_pv_production.append({
                "pv_production": pv_production
            })

    # Use custom_years for further processing

    st.subheader("2- Non-PV Demand")
    # Add content for Subsection 2    

# Page 4: Material Global Stocks
if page == "Material Global Stocks":
    st.header("Material Global Stocks", divider = 'grey')
    # Add content for Material Global Stocks page
    st.subheader("Historical Supply")
    # Add content for Subsection 1

    st.subheader("Historical Demand")
    # Add content for Subsection 2

    st.subheader("Global Stocks Calculation")
    # Add content for Subsection 3


# Page 5: Price Mechanism
if page == "Price Mechanism":
    st.header("Price Mechanism Setup", divider = 'grey')
    # Add content for Price Mechanism page


    st.subheader("2- Non-PV Demand")
    # Add content for Subsection 2    


# Page 6: Modelling Inputs Review
if page == "Modelling Inputs Review":
    st.header("Modelling Inputs Review", divider = 'grey')
    # Add content for Modelling Inputs Review page

# Page 7: Calculate Results
if page == "Calculate Results":
    st.header("Calculate Results", divider = 'grey')
    # Add content for Calculate Results page

# Page 8: Plot Results
if page == "Plot Results":
    st.header("Plot Results", divider = 'grey')
    # Add content for Plot Results page


