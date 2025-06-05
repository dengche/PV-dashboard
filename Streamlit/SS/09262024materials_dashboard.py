import streamlit as st
import numpy as np
import pandas as pd
import os
import pysd
import xarray as xr
from io import BytesIO
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
            ### update 6/12/2024
            "user_input":0,
            "scenario":"",
            "mine_annual_production":"",
            "mine_annual_growth":"",
            "mine_operating_years":"",
            "supply_option": 2,
            "num_pv_years": 1,
            "pv_user_input": 1,
            ###
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
            'get_res': False,
            
        }

# initialise the session state
if "input" not in st.session_state:
    st.session_state.input = {}
if "num_mines" not in st.session_state:
    st.session_state.num_mines = 0

if "num_rec_years" not in st.session_state:
    st.session_state.num_rec_years = 0
if "num_bp_hosts" not in st.session_state.input:
    st.session_state.input["num_bp_hosts"] = 0
if "num_bp_hosts" not in st.session_state:
    st.session_state.num_bp_hosts = 0
# page 1 default input 09262024
if "project_title" not in st.session_state.input:
    st.session_state.input["project_title"] = ""
if "project_investigator" not in st.session_state.input:
    st.session_state.input["project_investigator"] = ""
if "project_institution" not in st.session_state.input:
    st.session_state.input["project_institution"] = ""
if "project_PV_technology" not in st.session_state.input:
    st.session_state.input["project_PV_technology"] = ""
if "project_target_metal" not in st.session_state.input:
    st.session_state.input["project_target_metal"] = ""
if "project_description" not in st.session_state.input:
    st.session_state.input["project_description"] = ""
if "project_starting_year" not in st.session_state.input:
    st.session_state.input["project_starting_year"] = 2023
if "project_final_year" not in st.session_state.input:
    st.session_state.input["project_final_year"] = 2024
if "user_input" not in st.session_state.input:
    st.session_state.input["user_input"] = 1
if "scenario" not in st.session_state.input:
    st.session_state.input["scenario"] = "Tellurium Availability for CdTe - High Demand Scenario"

# page 2 default input 09262024
if "supply_option" not in st.session_state.input:
    st.session_state.input["supply_option"] = 1
if "global_reserves" not in st.session_state.input:
    st.session_state.input["global_reserves"] = 0
if "global_production" not in st.session_state.input:
    st.session_state.input["global_production"] = 0
if "direct_mining_growth" not in st.session_state.input:
    st.session_state.input["direct_mining_growth"] = 0
if "bp_reserve_option" not in st.session_state.input:
    st.session_state.input["bp_reserve_option"] = 1
if "bp_current_supply" not in st.session_state.input:
    st.session_state.input["bp_current_supply"] = 0
if "bp_supply_growth" not in st.session_state.input:
    st.session_state.input["bp_supply_growth"] = 0
if "bp_supply_growth" not in st.session_state.input:
    st.session_state.input["num_bp_hosts"] = 0
if "bp_host_metal_name" not in st.session_state.input:
    st.session_state.input["bp_host_metal_name"] = ["","",""]
if "bp_annual_production" not in st.session_state.input:
    st.session_state.input["bp_annual_production"] = np.zeros(3)
if "bp_global_reserves" not in st.session_state.input:
    st.session_state.input["bp_global_reserves"] = np.zeros(3)
if "bp_annual_production_growth" not in st.session_state.input:
    st.session_state.input["bp_annual_production_growth"] = np.zeros(3)
if "bp_hitchhiker_content" not in st.session_state.input:
    st.session_state.input["bp_hitchhiker_content"] = np.zeros(3)
if "bp_hitchhiker_recovery_efficiency" not in st.session_state.input:
    st.session_state.input["bp_hitchhiker_recovery_efficiency"] = np.zeros(3)
if "newpv_lifetime_option" not in st.session_state.input:
    st.session_state.input["newpv_lifetime_option"] = 1
if "newpv_panel_lifetime" not in st.session_state.input:
    st.session_state.input["newpv_panel_lifetime"] = 25
if "newpv_recycling_efficiency" not in st.session_state.input:
    st.session_state.input["newpv_recycling_efficiency"] = 0
if "newpv_recycling_collection_efficiency" not in st.session_state.input:
    st.session_state.input["newpv_recycling_collection_efficiency"] = 0
if "newpv_percentage_panels_recycled" not in st.session_state.input:
    st.session_state.input["newpv_percentage_panels_recycled"] = 0
if "rec_cal_method" not in st.session_state.input:
    st.session_state.input["rec_cal_method"] = 1
if "num_pv_years" not in st.session_state.input:
    st.session_state.input["num_pv_years"] = 1
if "pv_capacity" not in st.session_state.input:
    st.session_state.input["pv_capacity"] = np.zeros(1)
if "pv_capacity1" not in st.session_state.input:
    st.session_state.input["pv_capacity1"] = np.zeros(1)
if "pv_recycling" not in st.session_state.input:
    st.session_state.input["pv_recycling"] = 100
if "pv_collection_efficiency" not in st.session_state.input:
    st.session_state.input["pv_collection_efficiency"] = 90
if "pv_recycling_efficiency" not in st.session_state.input:
    st.session_state.input["pv_recycling_efficiency"] = 90
if "pv_lifetime_option" not in st.session_state.input:
    st.session_state.input["pv_lifetime_option"] = 1
if "pv_annual_supply" not in st.session_state.input:
    st.session_state.input["pv_annual_supply"] = 0
if "pv_panel_lifetime" not in st.session_state.input:
    st.session_state.input["pv_panel_lifetime"] = 25
if "pv_mint" not in st.session_state.input:
    st.session_state.input["pv_mint"] = 1
if "pv_avg_mint" not in st.session_state.input:
    st.session_state.input["pv_avg_mint"] = 0
if "pv_annual_mint" not in st.session_state.input:
    st.session_state.input["pv_annual_mint"] = 0
if "pv_annual_mint1" not in st.session_state.input:
    st.session_state.input["pv_annual_mint1"] = 0


if "hitchhiker1_affected" not in st.session_state.input:
    st.session_state.input["hitchhiker1_affected"] = 0
if "hitchhiker2_affected" not in st.session_state.input:
    st.session_state.input["hitchhiker2_affected"] = 0
if "hitchhiker3_affected" not in st.session_state.input:
    st.session_state.input["hitchhiker3_affected"] = 0
if "pv_annual_mint" not in st.session_state.input:
    st.session_state.input["pv_annual_mint"] = 0
if "global_reserves" not in st.session_state.input:
    st.session_state.input["global_reserves"] = 0
if "global_production" not in st.session_state.input:
    st.session_state.input["global_production"] = 0
 
if "direct_mining_affected" not in st.session_state.input:
    st.session_state.input["direct_mining_affected"] = 0       
if "dmgr_delay" not in st.session_state.input:
    st.session_state.input["dmgr_delay"] = 0  
if "dmgr_eq_degree" not in st.session_state.input:
    st.session_state.input["dmgr_eq_degree"] = 0 
if "dmgr_eq_a" not in st.session_state.input:
    st.session_state.input["dmgr_eq_a"] = 0
if "dmgr_eq_b" not in st.session_state.input:
    st.session_state.input["dmgr_eq_b"] = 0 
if "dmgr_eq_c" not in st.session_state.input:
    st.session_state.input["dmgr_eq_c"] = 0 
if "dmgr_eq_d" not in st.session_state.input:
    st.session_state.input["dmgr_eq_d"] = 0 
if "bpgr_affected" not in st.session_state.input:
    st.session_state.input["bpgr_affected"] = 0 
if "bpgr_delay" not in st.session_state.input:
    st.session_state.input["bpgr_delay"] = 0 
if "bpgr_eq_degree" not in st.session_state.input:
    st.session_state.input["bpgr_eq_degree"] = 0 
if "bpgr_eq_a" not in st.session_state.input:
    st.session_state.input["bpgr_eq_a"] = 0
if "bpgr_eq_b" not in st.session_state.input:
    st.session_state.input["bpgr_eq_b"] = 0 
if "bpgr_eq_c" not in st.session_state.input:
    st.session_state.input["bpgr_eq_c"] = 0 
if "bpgr_eq_d" not in st.session_state.input:
    st.session_state.input["bpgr_eq_d"] = 0 
if "bpy_delay" not in st.session_state.input:
    st.session_state.input["bpy_delay"] = 0 
if "bpy_eq_degree" not in st.session_state.input:
    st.session_state.input["bpy_eq_degree"] = 0 
if "bpy_eq_a" not in st.session_state.input:
    st.session_state.input["bpy_eq_a"] = 0
if "bpy_eq_b" not in st.session_state.input:
    st.session_state.input["bpy_eq_b"] = 0 
if "bpy_eq_c" not in st.session_state.input:
    st.session_state.input["bpy_eq_c"] = 0 
if "bpy_eq_d" not in st.session_state.input:
    st.session_state.input["bpy_eq_d"] = 0 
    



# Get the absolute path of the image file
#image_path = os.path.abspath('C:/Users/franc/OneDrive/Desktop/Materials Dashboard/msu.jpg')


# Add sidebar for navigation


with st.sidebar:
    st.image("msu_logo.png")
st.sidebar.title("Material Availability Assessment Dashboard")
#"Home"
page = st.sidebar.selectbox("Dashboard Navigation", ["Project Description","Material Supply", "Material Demand", "Supply Gap and Price Effect", "Modelling Inputs Review", "Calculate Results", "Plot Results"])

#st.sidebar.subheader("Home")
st.sidebar.subheader("Project Description")
st.sidebar.subheader("Material Supply")
st.sidebar.subheader("Material Demand")
st.sidebar.subheader("Supply Gap and Price Effect")
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

   


# Page 1: Project Description



if page == "Project Description":

    st.header("Project Description", divider='grey')
    project_title = st.text_input("Project title*", value=st.session_state.input["project_title"])
    project_investigator = st.text_input("Enter your name*", value=st.session_state.input["project_investigator"])
    project_institution = st.text_input("Institution*", value=st.session_state.input["project_institution"])
    use_options = ["I want to create my own scenario", "I want to use an existing analysis"]
    selected_use_option = st.selectbox("Scenario*", use_options,index=st.session_state.input["user_input"])

    if selected_use_option == "I want to use an existing analysis":
        user_input = 1
        baseline_options = ["Tellurium Availability for CdTe - High Demand Scenario", "Tellurium Availability for CdTe - Business-as-Usual Scenario","Tellurium Availability for CdTe - Low Demand Scenario"]
        ind = baseline_options.index(st.session_state.input["scenario"])
        selected_supply_option = st.selectbox("Select from the available analyses", baseline_options)
        project_pv_technology = st.text_input("PV Technology*",value="CdTe",disabled=True)
        project_target_metal = st.text_input("Target metal*",value="Tellurium",disabled=True)
    elif selected_use_option == "I want to create my own scenario":
        user_input = 0
        selected_supply_option = "none"
        project_pv_technology = st.text_input("PV Technology*", value=st.session_state.input["project_PV_technology"])
        project_target_metal = st.text_input("Target metal*", value=st.session_state.input["project_target_metal"])
    project_starting_year= st.number_input("Project timeline - starting year*",min_value=2023, step=1, value=st.session_state.input["project_starting_year"])
    project_final_year = st.number_input("Project timeline - final year*", min_value=2024, step=1, value=st.session_state.input["project_final_year"])
    
    project_description = st.text_area("Description*", height=200, value=st.session_state.input["project_description"])

    # Display the image
    #st.image(image_path)
    st.write("Note: The * indicates required fields")
    
    if st.button("Save"):
        #store analysis metadata in session state
        if project_starting_year <= project_final_year:
            st.session_state.input["project_title"] = project_title
            st.session_state.input["project_investigator"] = project_investigator
            st.session_state.input["project_institution"] = project_institution
            st.session_state.input["project_PV_technology"] = project_pv_technology
            st.session_state.input["project_target_metal"] = project_target_metal
            st.session_state.input["project_description"] = project_description
            st.session_state.input["project_starting_year"] = project_starting_year 
            st.session_state.input["project_final_year"] = project_final_year
            st.session_state.input["user_input"] = user_input
            st.session_state.input["scenario"] = selected_supply_option
            st.session_state.save1 = True
            st.write(f'<p style="color:red; font-size:18px;">Data saved</p>',unsafe_allow_html=True)
        else:
            st.markdown(f'<p style="color:red;font-weight:bold">Please enter the appropriate project timeline and try again</p>', unsafe_allow_html=True)
        

    

# Page 2: Material Supply
if page == "Material Supply":
    st.header("Material Supply Characterization", divider='grey')
    # Add content for Material Supply page

#---------------------------------------------------------------------------
    st.subheader("Direct Mining")
    # Add content for Subsection 1
    supply_options = ["Manually input annual production", "Calculate based on current production and future growth"]
    selected_supply_option = st.selectbox("Select Supply Calculation Method", supply_options,index=st.session_state.input["supply_option"]-1)
    if selected_supply_option == "Manually input annual production":
        supply_option = 1
        year_s = st.session_state.input["project_starting_year"]
        year_f = st.session_state.input["project_final_year"]
        if "mine_prod" not in st.session_state:
            st.session_state.mine_prod = np.zeros(year_f-year_s+1)
        years_list = [f"{i}" for i in range(year_s, year_f+1)]
        year = st.selectbox("Select the year for input",years_list)
        i = years_list.index(year)
        mine_prod = st.number_input(f"Enter the annual production for {year}", min_value=0, step=1, key=f"mine_annual_prod{i}")
        if st.button("Add",key="mine_prod1"):
            st.session_state.mine_prod[i] = mine_prod

        mine_data = pd.DataFrame({
            "Year":years_list,
            #"start_year": start_year,
            #"end_year": end_year,
            "Annual production": st.session_state.mine_prod
        })
        st.write(mine_data.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
        
        ###
        # Use mine_data for further processing
    
    if selected_supply_option == "Calculate based on current production and future growth":
        supply_option = 2
        global_reserves = st.number_input("Enter the global reserves (tonnes)",min_value = 0, value=st.session_state.input["global_reserves"])
        global_production = st.number_input("Enter the current annual global production (tonnes)", min_value=0, value=st.session_state.input["global_production"])
        direct_mining_growth = st.number_input("Enter the annual growth rate (%)", min_value = 0, value=st.session_state.input["direct_mining_growth"])
       
#---------------------------------------------------------------------------
    st.divider()
    st.subheader("By-production")
    # Add content for Subsection 2
    bp_option = ["Manually input", "Use current production and average growth"]
    bp_global_reserves_option = st.selectbox("Select Calculation method", bp_option, key="bp_global_reserves_option1",index=st.session_state.input["bp_reserve_option"]-1)
    if bp_global_reserves_option == "Use current production and average growth":
        bp_reserve_option = 2
        bp_current_supply = st.number_input("Enter the current supply from by-production", min_value=0, step=1, key="bp_current_supply1", value=st.session_state.input["bp_current_supply"])
        bp_supply_growth = st.number_input("Enter the supply growth rate from by-production (%)", min_value=0, step=1, key="bp_supply_growth1", value=st.session_state.input["bp_supply_growth"])

    elif bp_global_reserves_option == "Manually input":
        bp_reserve_option = 1
        num_bp_hosts = st.selectbox("Select the number of host metals (maximum 3)", [0,1,2,3],key="num_bp_hosts1", index=st.session_state.input["num_bp_hosts"])
        if num_bp_hosts > 0 and num_bp_hosts !=  st.session_state.num_bp_hosts:
            st.session_state.num_bp_hosts = num_bp_hosts
        if num_bp_hosts > 0:
            bp_host_metal_name = [0]*3
            bp_annual_production = np.zeros(3)
            bp_global_reserves = np.zeros(3)
            bp_annual_production_growth = np.zeros(3)
            bp_hitchhiker_content = np.zeros(3)
            bp_hitchhiker_recovery_efficiency = np.zeros(3)
            for i in range(num_bp_hosts):
                st.write(f"#### host metal {i+1}") 
                bp_host_metal_name[i] = st.text_input(f"Enter the host metal {i+1} name",key=f"bp_host_metal_name{i}",value=st.session_state.input["bp_host_metal_name"][i])
                bp_annual_production[i] = st.number_input(f"Enter the host metal {i+1} annual production (tonnes)",value=st.session_state.input["bp_annual_production"][i])
                bp_global_reserves[i] = st.number_input(f"Enter the host metal {i+1} gloabl reserves (tonnes)", value=st.session_state.input["bp_global_reserves"][i])
                bp_annual_production_growth[i] = st.number_input(f"Enter the host metal {i+1} annual production growth rate (%)", value=st.session_state.input["bp_annual_production_growth"][i])
                bp_hitchhiker_content[i] = st.number_input(f"Enter the host metal {i+1} hitchhiker content (ppm)", value=st.session_state.input["bp_hitchhiker_content"][i])
                bp_hitchhiker_recovery_efficiency[i] = st.number_input(f"Enter the host metal {i+1} hitchhiker recovery efficiency (%)", value=st.session_state.input["bp_hitchhiker_recovery_efficiency"][i])
        else:
            bp_host_metal_name = [0]*num_bp_hosts
            bp_annual_production = np.zeros(3)
            bp_global_reserves = np.zeros(3)
            bp_annual_production_growth = np.zeros(3)
            bp_hitchhiker_content = np.zeros(3)
            bp_hitchhiker_recovery_efficiency = np.zeros(3)

   
#---------------------------------------------------------------------------
    st.divider()
    ### update 06/14/2024
    st.subheader("Recycling of new solar panels")
    # Add content for Subsection 3
    panel_lifetime_options = ["Fixed Lifetime", "Weibull Model - Regular Loss Scenario", "Weibull Model - Early Loss Scenario"]
    newpv_selected_panel_lifetime_option = st.selectbox("Select the panel lifetime assumption", panel_lifetime_options, key = "newpv_lifetime_option1", index=st.session_state.input["newpv_lifetime_option"]-1)
    if newpv_selected_panel_lifetime_option == "Fixed Lifetime":
        newpv_lifetime_option = 1
        newpv_panel_lifetime = st.number_input("Panel lifetime (years)", min_value=0, step=1, value=st.session_state.input["newpv_panel_lifetime"],key = "newpv_lifetime_input1")
    elif newpv_selected_panel_lifetime_option == "Weibull Model - Early Loss Scenario":
        newpv_lifetime_option = 2
    elif newpv_selected_panel_lifetime_option == "Weibull Model - Regular Loss Scenario":
        newpv_lifetime_option = 3
        
    newpv_recycling_efficiency = st.number_input("Enter the recycling efficiency (%):", min_value=0, step=1, value=st.session_state.input["newpv_recycling_efficiency"], key = "newpv_efficiency1")    
    newpv_recycling_collection_efficiency = st.number_input("Enter the collection efficiency (%):", min_value=0, step=1, value=st.session_state.input["newpv_recycling_collection_efficiency"], key = "newpv_collection1")
    newpv_percentage_panels_recycled = st.number_input("Enter the percentage of panels recycled (%):", min_value=0, step=1, value=st.session_state.input["newpv_percentage_panels_recycled"], key = "newpv_percentage1")

#---------------------------------------------------------------------------    
    st.divider()
    st.subheader("Recycling of existing PV")
    # Add content for Subsection 4
    cal_methods = ["Calculation using the dashboard", "Manual User Input (Calculated by the user outside the dashboard)"]
    rec_calculation_method = st.selectbox("Select the recycled materials calculation method",cal_methods,key = "pv calculation method1", index=st.session_state.input["rec_cal_method"]-1)
    if rec_calculation_method == cal_methods[0]:
        rec_cal_method = 1
        num_pv_years = st.number_input("Enter the number of years", min_value=1, step=1,value=st.session_state.input["num_pv_years"])
        if num_pv_years != st.session_state.input["num_pv_years"]:
            st.session_state.input["pv_capacity1"] = np.zeros(num_pv_years)
            st.session_state.input["num_pv_years"] = num_pv_years
            st.session_state.input["pv_annual_mint1"] = np.zeros(num_pv_years)
        years_list = [f"Year {i}" for i in range(1, num_pv_years + 1)]
        
        material_intensity = ["Constant Material Intensity", "Variable Material Intensity"]
        pv_material_intensity = st.selectbox("Material intensity of existing solar panels", material_intensity, key="pv_material_intensity1", index=st.session_state.input["pv_mint"]-1)
        if pv_material_intensity == "Constant Material Intensity":
            pv_mint = 1
            pv_avg_mint = st.number_input("Please enter the average material intensity of existing solar panels", min_value=0, value=st.session_state.input["pv_avg_mint"], step=1, key="pv_avg_mint1")
            year = st.selectbox("Select the year for input",years_list,key="pv_mint_year1")            
            y = years_list.index(year)
            pv_capacity = st.number_input(f"Enter the annual installed PV capacity (Specific technology considered) for Year {y+1}", min_value=0, step=1, key=f"pv_capacity1_{y}")
            if st.button("Add",key="cap1"):
                st.session_state.input["pv_capacity1"][y] = pv_capacity
            pv_mint_data = pd.DataFrame({
                "Year":range(1,num_pv_years+1),
                "PV production":st.session_state.input["pv_capacity1"],
                #"start_year": start_year,
                #"end_year": end_year,
                "Annual Material Intensity": [pv_avg_mint]*num_pv_years,
            })
            st.write(pv_mint_data.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
            
        elif pv_material_intensity == "Variable Material Intensity":
            pv_mint = 2
            
            year = st.selectbox("Select the year for input",years_list,key="pv_mint_year2")            
            y = years_list.index(year)
            pv_capacity = st.number_input(f"Enter the annual installed PV capacity (Specific technology considered) for Year {y+1}", min_value=0, step=1, key=f"pv_capacity2_{y}")
            mint = st.number_input(f"Enter the annual material intensity for Year {i+1}", min_value=0, step=1, key=f"annual_mint{y}")
            if st.button("Add",key="mint1"):
                st.session_state.input["pv_capacity1"][y] = pv_capacity
                st.session_state.input["pv_annual_mint1"][y] = mint
        
            pv_mint_data = pd.DataFrame({
                "Year":range(1,num_pv_years+1),
                "PV production":st.session_state.input["pv_capacity1"],
                #"start_year": start_year,
                #"end_year": end_year,
                "Annual Material Intensity": st.session_state.input["pv_annual_mint1"],
            })
            st.write(pv_mint_data.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
        pv_recycling = st.number_input("Enter the percentage of panels recycled (%)",min_value=0, step=1, value=st.session_state.input["pv_recycling"], key = "pv_recycling1")
        pv_collection_efficiency = st.number_input("Enter the collection efficiency (%)",min_value=0, step=1, value=st.session_state.input["pv_collection_efficiency"], key = "pv_collection_efficiency1")
        pv_recycling_efficiency = st.number_input("Enter the recycling efficiency (%)",min_value=0, step=1, value=st.session_state.input["pv_recycling_efficiency"], key = "pv_recycling_efficiency1")
        
        panel_lifetime_options = ["Fixed Lifetime", "Weibull Model - Regular Loss Scenario", "Weibull Model - Early Loss Scenario"]
        pv_panel_lifetime_option =  st.selectbox("Select the panel lifetime assumption", panel_lifetime_options, index=st.session_state.input["newpv_lifetime_option"]-1, key = "pv_lifetime_option1")
        if pv_panel_lifetime_option == panel_lifetime_options[0]:
            pv_lifetime_option = 1
            pv_panel_lifetime = st.number_input("Panel Lifetime (years)", min_value=0, step=1, value=st.session_state.input["pv_panel_lifetime"],key = "pv_lifetime_input1")

        elif pv_panel_lifetime_option == panel_lifetime_options[1]:
            pv_lifetime_option = 2

        elif pv_panel_lifetime_option == panel_lifetime_options[1]:
            pv_lifetime_option = 3

        

        
        

    if rec_calculation_method == cal_methods[1]:
        rec_cal_method = 2
        year_s = st.session_state.input["project_starting_year"]
        year_f = st.session_state.input["project_final_year"]
        years_list2 = [f"{i}" for i in range(year_s, year_f+1)]
        if "pv_material_supply" not in st.session_state:
            st.session_state.pv_material_supply = np.zeros(year_f-year_s+1)
        year2 = st.selectbox("Select the year for input",years_list2,key="y_list2")            
        y = years_list2.index(year2)
        m_supply = st.number_input(f"Enter the annual material supply for {year2}", min_value=0, step=1, key=f"annual_supply{y}")
        if st.button("Add",key="material supply1"):
            st.session_state.pv_material_supply[y] = m_supply
        
        pv_annual_supply_data = pd.DataFrame({
            "Year":years_list,
            #"start_year": start_year,
            #"end_year": end_year,
            "Annual Supply": st.session_state.pv_material_supply,
        })
        st.write(pv_annual_supply_data.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)

#---------------------------------------------------------------------------    
    st.divider()
    if st.button("Save"):       
        #store inputs in session state
        st.session_state.input["supply_option"] = supply_option
        if supply_option == 1:
            st.session_state.input["mine_data"] = mine_data
        elif supply_option == 2:
            st.session_state.input["global_reserves"] = global_reserves
            st.session_state.input["global_production"] = global_production
            st.session_state.input["direct_mining_growth"] = direct_mining_growth
        st.session_state.input["bp_reserve_option"] = bp_reserve_option
        if bp_reserve_option == 2:
            st.session_state.input["bp_current_supply"] = bp_current_supply
            st.session_state.input["bp_supply_growth"] = bp_supply_growth
        elif bp_reserve_option == 1:
            st.session_state.input["num_bp_hosts"] = num_bp_hosts
            st.session_state.input["bp_host_metal_name"] = bp_host_metal_name
            st.session_state.input["bp_annual_production"] = bp_annual_production
            st.session_state.input["bp_global_reserves"] = bp_global_reserves
            st.session_state.input["bp_annual_production_growth"] = bp_annual_production_growth
            st.session_state.input["bp_hitchhiker_content"] = bp_hitchhiker_content
            st.session_state.input["bp_hitchhiker_recovery_efficiency"] = bp_hitchhiker_recovery_efficiency

        st.session_state.input["newpv_lifetime_option"] = newpv_lifetime_option
        if newpv_lifetime_option == 1:
            st.session_state.input["newpv_panel_lifetime"] = newpv_panel_lifetime
        st.session_state.input["newpv_recycling_efficiency"] = newpv_recycling_efficiency
        st.session_state.input["newpv_recycling_collection_efficiency"] = newpv_recycling_collection_efficiency
        st.session_state.input["newpv_percentage_panels_recycled"] = newpv_percentage_panels_recycled

        st.session_state.input["rec_cal_method"] = rec_cal_method
        if rec_cal_method == 1:
            st.session_state.input["num_pv_years"] = num_pv_years
            st.session_state.input["pv_capacity"] = st.session_state.input["pv_capacity1"]
            st.session_state.input["pv_recycling"] = pv_recycling
            st.session_state.input["pv_collection_efficiency"] = pv_collection_efficiency
            st.session_state.input["pv_recycling_efficiency"] = pv_recycling_efficiency
            st.session_state.input["pv_lifetime_option"] = pv_lifetime_option
            st.session_state.input["pv_annual_supply"] = 0
            if pv_lifetime_option == 1:
                st.session_state.input["pv_panel_lifetime"] = pv_panel_lifetime
            st.session_state.input["pv_mint"] = pv_mint
            if pv_mint == 1:
                st.session_state.input["pv_avg_mint"] = pv_avg_mint
            elif pv_mint == 2:
                st.session_state.input["pv_mint_data"] = pv_mint_data
                st.session_state.input["pv_annual_mint"] = st.session_state.input["pv_annual_mint1"]
        elif rec_cal_method == 2:
            st.session_state.input["pv_annual_supply_data"] = pv_annual_supply_data
            st.session_state.input["pv_annual_supply"] = st.session_state.pv_material_supply
            
        st.session_state.save2 = True
        st.write(f'<p style="color:red; font-size:18px;">Data saved</p>',unsafe_allow_html=True)
            

#---------------------------------------------------------------------------
# Page 3: Material Demand

if page == "Material Demand":
    st.header("Material Demand Characterization", divider='grey')
    # Add content for Material Demand page
    st.subheader("1- PV Demand")
    # Add content for Subsection 1
    st.markdown("<p style='font-family: Arial; font-size: 16pt; font-weight: bold;'> 1.1- Future PV Production (GWp)</p>", unsafe_allow_html=True)
    future_pv_options = ["Default values", "Custom User Input"]
    start_year = st.session_state.input["project_starting_year"]
    final_year = st.session_state.input["project_final_year"]
    pv_years = final_year + 1 - start_year
    years_list = range(start_year, final_year+1)
    if "pv_market_share" not in st.session_state:
        st.session_state.pv_market_share = np.zeros(pv_years)
    if "pv_material_intensity" not in st.session_state:
        st.session_state.pv_material_intensity = np.zeros(pv_years)

    selected_supply_option = st.selectbox("Future PV Production (GWp)", future_pv_options)
    if selected_supply_option == "Default values":
        pv_user_input = 1
        # to be determined 
        annual_incremental_capacity1 = 0
        pv_initial_incremental1 = 0
        pv_annual_deployment1 = 0
        pv_year = st.selectbox("Select the year for input",years_list, key="pv_production_year1")
        ind = years_list.index(pv_year)
        if "pv_production" not in st.session_state:
            st.session_state.pv_production = np.zeros(pv_years)
        pv_market_share = st.number_input(f"Enter the market share of the PV technology of interest (%) for {years_list[ind]}", min_value=0, step=1, value=0,key=f"annual_pv_share1{years_list[ind]}")
        pv_material_intensity = st.number_input(f"Enter the material intensity (kg/GWp) for {years_list[ind]}", min_value = 0, step=1, value = 0,key=f"annual_pv_intensity1{years_list[ind]}")
        if st.button("Add",key="pv_production1"):
            st.session_state.pv_market_share[ind] =  pv_market_share
            st.session_state.pv_material_intensity[ind] =  pv_material_intensity
        pv_production = pd.DataFrame({
            "year": range(start_year, final_year+1),
            "PV production (GWp)": st.session_state.pv_production,
            "market share (%)": st.session_state.pv_market_share,
            "material intensity (kg/GWp)": st.session_state.pv_material_intensity
        })
        st.write(pv_production.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
    if selected_supply_option == "Custom User Input":
        pv_user_input = 2
        pv_year = st.selectbox("Select the year for input",years_list, key="pv_production_year2") 
        pv_production = np.zeros(pv_years)
        if "pv_production" not in st.session_state:
            st.session_state.pv_production = np.zeros(pv_years)
        
        ind = years_list.index(pv_year)
        pv_annual_production = st.number_input(f"Enter the PV annual production (GWp) for {years_list[ind]}", min_value=0.0, key=f"annual_pv{years_list[ind]}")
        pv_market_share = st.number_input(f"Enter the market share of the PV technology of interest (%) for {years_list[ind]}", min_value=0, step=1, value=0,key=f"annual_pv_share2{years_list[ind]}")
        pv_material_intensity = st.number_input(f"Enter the material intensity (kg/GWp) for {years_list[ind]}", min_value = 0, step=1, value = 0,key=f"annual_pv_intensity2{years_list[ind]}")
        if st.button("Add",key="pv_production2"):
            st.session_state.pv_production[ind] = pv_annual_production
            st.session_state.pv_market_share[ind] =  pv_market_share
            st.session_state.pv_material_intensity[ind] =  pv_material_intensity
        pv_production = pd.DataFrame({
            "year": range(start_year, final_year+1),
            "PV production (GWp)": st.session_state.pv_production,
            "market share (%)": st.session_state.pv_market_share,
            "material intensity (kg/GWp)": st.session_state.pv_material_intensity
        })
        st.write(pv_production.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
        
        if pv_years>=2:
            pv_initial_incremental2 =st.session_state.pv_production[1]-st.session_state.pv_production[0]
            annual_incremental_capacity2 = st.session_state.pv_production[1:]-st.session_state.pv_production[:-1]
        else:
            pv_initial_incremental2 = 0
            annual_incremental_capacity2 = [0]
        pv_annual_deployment2 = st.session_state.pv_production[0]



        
    # previous code
    if False:
        market_share_options = ["Constant", "Variable"]
        selected_market_share= st.selectbox("How do you want to calculate the future market share of the PV techology being assessed?", market_share_options)
        if selected_market_share == "Constant":
            pv_tech_market_share = st.number_input("Enter the market share of the PV technology of interest (%)", min_value=0, step=1, value=0)
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
        pass
        
    st.subheader("2- Non-PV Demand")
    # Add content for Subsection 2          

    # sty = st.session_state.input["project_starting_year"]
    nonpv_demand = st.number_input (f"Enter the current non-PV demand for first Year (tonnes)", min_value=0, step=1, value = 0)
    nonpv_demand_gr = st.number_input ("Enter the annual growth rate in non-PV demand (%)", min_value=0, step=1, value = 0)
    
    
    if st.button("Save",key="pv_demand1"):
        st.session_state.input["pv_user_input"] = pv_user_input
        if pv_user_input == 1:
            st.session_state.input["annual_incremental_capacity"] = annual_incremental_capacity1
            st.session_state.input["pv_initial_incremental"] = pv_initial_incremental1
            st.session_state.input["pv_annual_deployment"] = pv_annual_deployment1
        elif pv_user_input == 2:
            st.session_state.input["pv_production"] = pv_production
            st.session_state.input["annual_incremental_capacity"] = annual_incremental_capacity2
            st.session_state.input["pv_initial_incremental"] = pv_initial_incremental2
            st.session_state.input["pv_annual_deployment"] = pv_annual_deployment2
        st.session_state.input["pv_market_share"] = st.session_state.pv_market_share
        st.session_state.input["pv_material_intensity"] = st.session_state.pv_material_intensity
        st.session_state.input ["nonpv_demand"] = nonpv_demand
        st.session_state.input ["nonpv_demand_gr"] = nonpv_demand_gr
        st.session_state.save3 = True
        st.write(f'<p style="color:red; font-size:18px;">Data saved</p>',unsafe_allow_html=True)
#--------------------------------------------------        
    # Page 4: Supply Gap and Price Effect
if page == "Supply Gap and Price Effect":
    # Add content for Price Mechanism - Effect of Surplus on Material Price
    st.header("Price Mechanism - Effect of Surplus on Material Price", divider = 'grey')
    target_metal_price = st.number_input("Enter the current price of the target metal ($/tonne)", min_value=0.00, step=0.01,key="target_metal_price1")
    supply_gap_delay = st.number_input("Enter the delay time of surplus or gap (years)", min_value=0, step=1,key="supply_gap_delay1")
    col1,col2 = st.columns([12,2])
    supply_gap_eq_degree = col1.selectbox("Please select the degree of supply gap price equation",[1,2,3],key="supply_gap_eq_degree1")
    col2.write("")
    col2.write("")
    if col2.button("Equation"):
        if supply_gap_eq_degree == 1:
            st.latex(r'\text{Material Price} = a \times \text{(Gap or Surplus)} + b')
        elif supply_gap_eq_degree == 2:
            st.latex(r'\text{Material Price} = a \times \text{(Gap or Surplus)}^2 + b\times \text{(Gap or Surplus)}+c')
        elif supply_gap_eq_degree == 3:
            st.latex(r'\text{Material Price} = a \times \text{(Gap or Surplus)}^3 + b\times \text{(Gap or Surplus)}^2\\+c\times \text{(Gap or Surplus)}+d')
    with st.expander("**Please enter the parameters**"):
        if supply_gap_eq_degree == 1:
            col3,col4 = st.columns(2)
            supply_gap_eq_a = col3.number_input("**a**")
            supply_gap_eq_b = col4.number_input("**b**")
            supply_gap_eq_c = 0
            supply_gap_eq_d = 0
        elif supply_gap_eq_degree == 2:
            col3,col4 = st.columns(2)
            supply_gap_eq_a = col3.number_input("**a**")
            supply_gap_eq_b = col4.number_input("**b**")
            supply_gap_eq_c = col3.number_input("**c**")
            supply_gap_eq_d = 0
        elif supply_gap_eq_degree == 3:
            col3,col4 = st.columns(2)
            supply_gap_eq_a = col3.number_input("**a**")
            supply_gap_eq_b = col4.number_input("**b**")
            supply_gap_eq_c = col3.number_input("**c**")
            supply_gap_eq_d = col4.number_input("**d**")
    # Add contend for Price Mechanism - Effect on Direct Mining 
    if st.session_state.input["supply_option"] == 2:
        st.divider()
        st.subheader("Price Mechanism - Effect on Direct Mining") 
        affect_choice = ["Direct mining growth rate affected by price", "Direct mining growth rate not affected by price"]
        affected = st.selectbox("Does the price affect the growth of direct mining?",affect_choice,index=1)
        if affected == affect_choice[1]:
            direct_mining_affected = 2
        elif affected == affect_choice[0]:
            direct_mining_affected = 1
            dmgr_delay = st.number_input("Enter the delay time of growth rate of direct mining (years)", min_value=0, step=1,key="dmgr_delay1")
            col21,col22 = st.columns([12,2])
            dmgr_eq_degree = col21.selectbox("Please select the degree of growth rate of direct mining equation",[1,2,3],key="dmgr_eq_degree1")
            col22.write("")
            col22.write("")
            if col22.button("Equation",key="dmgr_eq"):
                if dmgr_eq_degree == 1:
                    st.latex(r'\text{Direct Mining Growth Rate} = a \times \text{(Material Price)} + b')
                elif dmgr_eq_degree == 2:
                    st.latex(r'\text{Direct Mining Growth Rate} = a \times \text{(Material Price)}^2 + b\times \text{(Material Price)}+c')
                elif dmgr_eq_degree == 3:
                    st.latex(r'\text{Direct Mining Growth Rate} = a \times \text{(Material Price)}^3 + b\times \text{(Material Price)}^2\\+c\times \text{(Material Price)}+d')
            with st.expander("**Please enter the parameters**"):
                if dmgr_eq_degree == 1:
                    col23,col24 = st.columns(2)
                    dmgr_eq_a = col23.number_input("**a**",key="dmgr_a")
                    dmgr_eq_b = col24.number_input("**b**",key="dmgr_b")
                    dmgr_eq_c = 0
                    dmgr_eq_d = 0
                elif dmgr_eq_degree == 2:
                    col23,col24 = st.columns(2)
                    dmgr_eq_a = col23.number_input("**a**",key="dmgr_a")
                    dmgr_eq_b = col24.number_input("**b**",key="dmgr_b")
                    dmgr_eq_c = col23.number_input("**c**",key="dmgr_c")
                    dmgr_eq_d = 0
                elif dmgr_eq_degree == 3:
                    col23,col24 = st.columns(2)
                    dmgr_eq_a = col23.number_input("**a**",key="dmgr_a")
                    dmgr_eq_b = col24.number_input("**b**",key="dmgr_b")
                    dmgr_eq_c = col23.number_input("**c**",key="dmgr_c")
                    dmgr_eq_d = col24.number_input("**d**",key="dmgr_d")

    # Add contend for Price Mechanism - Effect on Byproduction (avg estimation)
    bp_reserve_option = st.session_state.input["bp_reserve_option"]
    if bp_reserve_option==2:
        st.divider()
        st.subheader("Price Mechanism - Effect on byproduction") 
        affect_choice2 = ["Byproduction growth rate affected by price", "Byproduction growth rate not affected by price"]
        affected2 = st.selectbox("Does the price affect the byproduction growth rate?",affect_choice2,index=1)
        if affected2 == affect_choice2[1]:
            bpgr_affected = 2
        elif affected2 == affect_choice2[0]:
            bpgr_affected = 1
            bpgr_delay = st.number_input("Enter the delay time of growth rate of byproduction (years)", min_value=0, step=1,key="bpgr_delay1")
            col31,col32 = st.columns([12,2])
            bpgr_eq_degree = col31.selectbox("Please select the degree of growth rate of byproduction equation",[1,2,3],key="bpgr_eq_degree1")
            col32.write("")
            col32.write("")
            if col32.button("Equation",key="bpgr_eq"):
                if bpgr_eq_degree == 1:
                    st.latex(r'\text{Byproduction Growth Rate} = a \times \text{(Material Price)} + b')
                elif bpgr_eq_degree == 2:
                    st.latex(r'\text{Byproduction Growth Rate} = a \times \text{(Material Price)}^2 + b\times \text{(Material Price)}+c')
                elif bpgr_eq_degree == 3:
                    st.latex(r'\text{Byproduction Growth Rate} = a \times \text{(Material Price)}^3 + b\times \text{(Material Price)}^2\\+c\times \text{(Material Price)}+d')
            with st.expander("**Please enter the parameters**"):
                if bpgr_eq_degree == 1:
                    col33,col34 = st.columns(2)
                    bpgr_eq_a = col33.number_input("**a**",key="bpgr_a")
                    bpgr_eq_b = col34.number_input("**b**",key="bpgr_b")
                    bpgr_eq_c = 0
                    bpgr_eq_d = 0
                elif bpgr_eq_degree == 2:
                    col33,col34 = st.columns(2)
                    bpgr_eq_a = col33.number_input("**a**",key="bpgr_a")
                    bpgr_eq_b = col34.number_input("**b**",key="bpgr_b")
                    bpgr_eq_c = col33.number_input("**c**",key="bpgr_c")
                    bpgr_eq_d = 0
                elif bpgr_eq_degree == 3:
                    col33,col34 = st.columns(2)
                    bpgr_eq_a = col33.number_input("**a**",key="bpgr_a")
                    bpgr_eq_b = col34.number_input("**b**",key="bpgr_b")
                    bpgr_eq_c = col33.number_input("**c**",key="bpgr_c")
                    bpgr_eq_d = col34.number_input("**d**",key="bpgr_d")
    # Add contend for Price Mechanism - Effect on Byproduction (detailed estimation)
    elif st.session_state.input["bp_reserve_option"] == 1:
        if st.session_state.input["num_bp_hosts"] != 0: 
            st.divider()
            st.subheader("Price Mechanism - Effect on byproduction") 
            metals = st.session_state.input["bp_host_metal_name"]
            affect_choice3 = ["Byproduction yield affected by price", "Byproduction yield not affected by price"]
                
            if st.session_state.input["num_bp_hosts"] == 1:
                affected3 = st.selectbox(f"Does the metals' price affect the yield of metal 1 {metals[0]}?",affect_choice3,index=1)
                hitchhiker1_affected = 1 if affected3 == affect_choice3[0] else 2
                hitchhiker2_affected = 0
                hitchhiker3_affected = 0
            elif st.session_state.input["num_bp_hosts"] == 2:
                affected3 = st.selectbox(f"Does the metals' price affect the yield of metal 1 {metals[0]}?",affect_choice3,index=1)
                affected4 = st.selectbox(f"Does the metals' price affect the yield of metal 2 {metals[1]}?",affect_choice3,index=1)
                hitchhiker1_affected = 1 if affected3 == affect_choice3[0] else 2
                hitchhiker2_affected = 1 if affected4 == affect_choice3[0] else 2
                hitchhiker3_affected = 0
            elif st.session_state.input["num_bp_hosts"] == 3:
                affected3 = st.selectbox(f"Does the metals' price affect the yield of metal 1 {metals[0]}?",affect_choice3,index=1)
                affected4 = st.selectbox(f"Does the metals' price affect the yield of metal 2 {metals[1]}?",affect_choice3,index=1)
                affected5 = st.selectbox(f"Does the metals' price affect the yield of metal 3 {metals[2]}?",affect_choice3,index=1)
                hitchhiker1_affected = 1 if affected3 == affect_choice3[0] else 2
                hitchhiker2_affected = 1 if affected4 == affect_choice3[0] else 2
                hitchhiker3_affected = 1 if affected5 == affect_choice3[0] else 2
        
            if hitchhiker1_affected == 1 or hitchhiker2_affected == 1 or hitchhiker3_affected == 1:
                bpy_delay = st.number_input("Enter the delay time of yield of byproduction (years)", min_value=0, step=1,key="bpy_delay1")
                col31,col32 = st.columns([12,2])
                bpy_eq_degree = col31.selectbox("Please select the degree of yield of byprodction equation",[1,2,3],key="bpy_eq_degree1")
                col32.write("")
                col32.write("")
                if col32.button("Equation",key="bpy_eq"):
                    if bpy_eq_degree == 1:
                        st.latex(r'\text{Byproduction Yield} = a \times \text{(Material Price)} + b')
                    elif bpy_eq_degree == 2:
                        st.latex(r'\text{Byproduction Yield} = a \times \text{(Material Price)}^2 + b\times \text{(Material Price)}+c')
                    elif bpy_eq_degree == 3:
                        st.latex(r'\text{Byproduction Yield} = a \times \text{(Material Price)}^3 + b\times \text{(Material Price)}^2\\+c\times \text{(Material Price)}+d')
                with st.expander("**Please enter the parameters**"):
                    if bpy_eq_degree == 1:
                        col33,col34 = st.columns(2)
                        bpy_eq_a = col33.number_input("**a**",key="bpy_a")
                        bpy_eq_b = col34.number_input("**b**",key="bpy_b")
                        bpy_eq_c = 0
                        bpy_eq_d = 0
                    elif bpy_eq_degree == 2:
                        col33,col34 = st.columns(2)
                        bpy_eq_a = col33.number_input("**a**",key="bpy_a")
                        bpy_eq_b = col34.number_input("**b**",key="bpy_b")
                        bpy_eq_c = col33.number_input("**c**",key="bpy_c")
                        bpy_eq_d = 0
                    elif bpy_eq_degree == 3:
                        col33,col34 = st.columns(2)
                        bpy_eq_a = col33.number_input("**a**",key="bpy_a")
                        bpy_eq_b = col34.number_input("**b**",key="bpy_b")
                        bpy_eq_c = col33.number_input("**c**",key="bpy_c")
                        bpy_eq_d = col34.number_input("**d**",key="bpy_d")    
        else:
            hitchhiker1_affected = 0
            hitchhiker2_affected = 0
            hitchhiker3_affected = 0

    # Add contend for Price Mechanism - Effect on PV Demand
    st.divider()
    st.subheader("Price Mechanism - Effect on PV Demand")
    pv_price_threshold = st.number_input("Please enter the price of the competitive technologies($/Wp)", min_value=0.00, step=0.01, value=0.00)
    pv_tech_price = st.number_input("Please enter the current selling price of the PV technology ($/Wp)", min_value=0.00, step=0.01, value=0.00)

    # Add content for Material Global Stocks
    st.divider()
    st.subheader("Global Stocks")
    global_stocks = st.number_input("Please enter the global stocks", min_value=0.00, step=0.01, value=0.00)

    # save the data
    st.divider()
    if st.button("Save"):
        st.session_state.input["target_metal_price"] = target_metal_price
        st.session_state.input["supply_gap_delay"] = supply_gap_delay
        st.session_state.input["supply_gap_eq_degree"] = supply_gap_eq_degree
        st.session_state.input["supply_gap_eq_a"] = supply_gap_eq_a
        st.session_state.input["supply_gap_eq_b"] = supply_gap_eq_b
        st.session_state.input["supply_gap_eq_c"] = supply_gap_eq_c
        st.session_state.input["supply_gap_eq_d"] = supply_gap_eq_d
        if st.session_state.input["supply_option"] == 2:
            st.session_state.input["direct_mining_affected"] = direct_mining_affected
            if direct_mining_affected == 1:
                st.session_state.input["dmgr_delay"] = dmgr_delay
                st.session_state.input["dmgr_eq_degree"] = dmgr_eq_degree
                st.session_state.input["dmgr_eq_a"] = dmgr_eq_a
                st.session_state.input["dmgr_eq_b"] = dmgr_eq_b
                st.session_state.input["dmgr_eq_c"] = dmgr_eq_c
                st.session_state.input["dmgr_eq_d"] = dmgr_eq_d
        if st.session_state.input["bp_reserve_option"] == 2:
            st.session_state.input["bpgr_affected"] = bpgr_affected
            if bpgr_affected == 1:
                st.session_state.input["bpgr_delay"] = bpgr_delay
                st.session_state.input["bpgr_eq_degree"] = bpgr_eq_degree
                st.session_state.input["bpgr_eq_a"] = bpgr_eq_a
                st.session_state.input["bpgr_eq_b"] = bpgr_eq_b
                st.session_state.input["bpgr_eq_c"] = bpgr_eq_c
                st.session_state.input["bpgr_eq_d"] = bpgr_eq_d
        elif st.session_state.input["bp_reserve_option"] == 1:
            st.session_state.input["hitchhiker1_affected"] = hitchhiker1_affected
            st.session_state.input["hitchhiker2_affected"] = hitchhiker2_affected
            st.session_state.input["hitchhiker3_affected"] = hitchhiker3_affected
            if hitchhiker1_affected == 1 or hitchhiker2_affected == 1 or hitchhiker3_affected == 1:
                st.session_state.input["bpy_delay"] = bpy_delay
                st.session_state.input["bpy_eq_degree"] = bpy_eq_degree
                st.session_state.input["bpy_eq_a"] = bpy_eq_a
                st.session_state.input["bpy_eq_b"] = bpy_eq_b
                st.session_state.input["bpy_eq_c"] = bpy_eq_c
                st.session_state.input["bpy_eq_d"] = bpy_eq_d
        st.session_state.input["pv_price_threshold"] = pv_price_threshold
        st.session_state.input["pv_tech_price"] = pv_tech_price
        st.session_state.input["global_stocks"] = global_stocks
        st.session_state.save4 = True
        st.write(f'<p style="color:red; font-size:18px;">Data saved</p>',unsafe_allow_html=True)


# Page 5: Modelling Inputs Review
if page == "Modelling Inputs Review":
    st.header("Modelling Inputs Review", divider = 'grey')
    inputs_name = ["","Project Description","Material Supply", "Material Demand","Supply Gap and Price Effect"]
    selected_inputs = st.selectbox("Select inputs", inputs_name, index=0)
    if selected_inputs == "Project Description":
        if "save1" not in st.session_state:
            st.write(f'<p style="color:red; font-size:18px;">Inputs are not saved</p>',unsafe_allow_html=True)
        else:
            project_values = ["project_title","project_investigator","project_institution","project_PV_technology","project_target_metal","project_description","project_starting_year","project_final_year"]
            inputs = st.session_state.input
            st.markdown("<h3 class='small-header'>Project Description</h3>", unsafe_allow_html=True)
            project_df = pd.DataFrame({
                "Inputs": ["Title", "Investigator", "Institution", "PV technology","Taget metal","Description","Starting year","Final year"],
                "Values": [inputs[project_values[i]] for i in range(len(project_values))]
            })
            st.write(project_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
    if selected_inputs == "Material Supply":
        if "save2" not in st.session_state:
            st.write(f'<p style="color:red; font-size:18px;">Inputs are not saved</p>',unsafe_allow_html=True)
        else:
            inputs = st.session_state.input
            st.markdown("<h3 class='small-header'>Direct Mining</h3>", unsafe_allow_html=True)
            dm_values1 = "mine_data"
            dm_values2 = ["global_reserves","global_production","direct_mining_growth"]
            if st.session_state.input["supply_option"] == 1:
                if st.session_state.num_mines > 0:
                    dm_df = st.session_state.input[dm_values1]
                    st.write(dm_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
                else:
                    st.markdown("There is no direct mining data")
            elif st.session_state.input["supply_option"] == 2:
                dm_df = pd.DataFrame({
                "Inputs": ["Global reserves (tonnes)", "Current annual production (tonnes)", "Annual grwoth rate (%)"],
                "Values": [inputs[dm_values2[i]] for i in range(len(dm_values2))]
                })
                st.write(dm_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
                
            st.divider()
            st.markdown("<h3 class='small-header'>By-production</h3>", unsafe_allow_html=True)
            if st.session_state.input["bp_reserve_option"] == 1:
                if st.session_state.input["num_bp_hosts"] > 0:
                    num_bp = st.session_state.input["num_bp_hosts"]
                    bp_df = pd.DataFrame({
                        "Host metal":range(1,num_bp+1),
                        "Name": inputs["bp_host_metal_name"][:num_bp],
                        "Annual production (tonnes)": inputs["bp_annual_production"][:num_bp],
                        "Gloabl reserves (tonnes)": inputs["bp_annual_production"][:num_bp],
                        "Annual production growth rate (%)": inputs["bp_annual_production_growth"][:num_bp],
                        "Hitchhiker content (ppm)": inputs["bp_hitchhiker_content"][:num_bp],
                        "Hitchhiker recovery efficiency (%)": inputs["bp_hitchhiker_recovery_efficiency"][:num_bp],
                    })
                    
                    st.write(bp_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
                else:
                    st.markdown("There is no by-production data")
            elif st.session_state.input["bp_reserve_option"] == 2:
                bp_values2 = ["bp_current_supply","bp_supply_growth"]
                bp_df = pd.DataFrame({
                "Inputs": ["Current supply from by-production (tonnes)", "Supply growth rate from by-production (%)"],
                "Values": [inputs[bp_values2[i]] for i in range(len(bp_values2))]
                })
                st.write(bp_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)

            st.divider()
            st.markdown("<h3 class='small-header'>Recycling of new solar panels</h3>", unsafe_allow_html=True)
            if st.session_state.input["newpv_lifetime_option"] == 1:
                newpv_values1 = ["newpv_panel_lifetime","newpv_recycling_efficiency","newpv_recycling_collection_efficiency","newpv_percentage_panels_recycled"]
                newpv_df = pd.DataFrame({
                    "Inputs":["Lifetime assumption","Panel lifetime (years)","Recycling efficiency","Collection efficiency","Percentage of panels recycled (%)"],
                    "Values":["Fixed lifetime"]+[inputs[newpv_values1[i]] for i in range(len(newpv_values1))]
                })           
            elif st.session_state.input["newpv_lifetime_option"] == 2 or 3:
                newpv_values2 = ["newpv_recycling_efficiency","newpv_recycling_collection_efficiency","newpv_percentage_panels_recycled"]
                ind = st.session_state.input["newpv_lifetime_option"]-2
                assumption = ["Weibull Model - Regular Loss Scenario","Weibull Model - Early Loss Scenario"][ind]
                newpv_df = pd.DataFrame({
                    "Inputs":["Lifetime assumption","Recycling efficiency","Collection efficiency","Percentage of panels recycled (%)"],
                    "Values":[assumption]+[inputs[newpv_values2[i]] for i in range(len(newpv_values2))]
                })
            st.write(newpv_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
            
            st.divider()
            st.markdown("<h3 class='small-header'>Recycling of existing PV</h3>", unsafe_allow_html=True)
            if st.session_state.input["rec_cal_method"] == 1:
                pv_lists = ["pv_capacity","pv_recycling","pv_collection_efficiency","pv_recycling_efficiency"]
                pv_values = [inputs[pv_lists[i]] for i in range(len(pv_lists))]
                pv_inputs = ["PV capacity","Percentage of panels recycled (%)","Collection efficiency (%)","Recycling efficiency (%)","Panel life time assumption"]
                if st.session_state.input["pv_lifetime_option"] == 1:
                    pv_values.append("Fixed Lifetime")
                    pv_values.append(inputs["pv_panel_lifetime"])
                    pv_inputs.append("Panel lifetime (years)")
                elif st.session_state.input["pv_lifetime_option"] == 2:
                    pv_values.append("Weibull Model - Regular Loss Scenario")
                else:
                    pv_values.append("Weibull Model - Early Loss Scenario") 
                if st.session_state.input["pv_mint"] == 2:
                    pv_values.append("Variable")
                    pv_inputs.append("Material intensity assumption")
                else:
                    pv_values.append("Constant")
                    pv_inputs.append("Material intensity assumption")
                    
                pv_df = pd.DataFrame({
                    "Inputs":pv_inputs,
                    "Values":pv_values
                })
                st.markdown("**Calculation method**: Using the dashboard")
                st.write(pv_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
                if st.session_state.input["pv_mint"] == 2:
                    pv_df2 = st.session_state.input["pv_mint_data"]
                else:
                    pv_df2 = pd.DataFrame({
                        "Inputs":["Average material intensity"],
                        "Values":[st.session_state.input["pv_avg_mint"]]
                    })
                st.write(pv_df2.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
            elif st.session_state.input["rec_cal_method"] == 2:
                pv_df = st.session_state.input["pv_annual_supply_data"]
                st.markdown("**Calculation method**: Manual input")
                st.write(pv_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
    if selected_inputs == "Material Demand":
        if "save3" not in st.session_state:
            st.write(f'<p style="color:red; font-size:18px;">Inputs are not saved</p>',unsafe_allow_html=True)
        else:
            inputs = st.session_state.input
            st.markdown("<h3 class='small-header'>PV Demand</h3>", unsafe_allow_html=True)
            if st.session_state.input["pv_user_input"] == 1:
                st.markdown("**PV production input**: Default values")
                pv_demand_lists = ["annual_incremental_capacity","pv_initial_incremental","pv_annual_deployment","pv_market_share","pv_material_intensity"]
                pv_demand_values = [inputs[pv_demand_lists[i]] for i in range(len(pv_demand_lists))]
                pv_demand_inputs = ["Planned annual incremental capacity","PV deployment initial incremental","Current annual PV deployment","PV technology market share","PV technology material intensity"]
                pv_demand_df = pd.DataFrame({
                    "Inputs":pv_demand_inputs,
                    "Values":pv_demand_values
                })
                st.write(pv_demand_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
            elif st.session_state.input["pv_user_input"] == 2:
                st.markdown("**PV production input**: User specific")
                pv_demand_lists = ["pv_market_share","pv_material_intensity"]
                pv_demand_values = [inputs[pv_demand_lists[i]] for i in range(len(pv_demand_lists))]
                pv_demand_df1 = st.session_state.input["pv_production"]
                st.write(pv_demand_df1.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
                
            st.divider()
            st.markdown("<h3 class='small-header'>Non PV Demand</h3>", unsafe_allow_html=True)
            nonpv_demand_df = pd.DataFrame({
                    "Inputs":["Current non-PV demand (tonnes)","Annual growth rate in non-PV demand (%)"],
                    "Values":[inputs["nonpv_demand"],inputs["nonpv_demand_gr"]],
                })
            st.write(nonpv_demand_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
    if selected_inputs == "Supply Gap and Price Effect":
        if "save4" not in st.session_state:
            st.write(f'<p style="color:red; font-size:18px;">Inputs are not saved</p>',unsafe_allow_html=True)
        else:
            inputs = st.session_state.input
            st.markdown("<h3 class='small-header'>Effect of Surplus on Material Price</h3>", unsafe_allow_html=True)
            supply_gap_ef_lists = ["target_metal_price","supply_gap_delay","supply_gap_eq_degree","supply_gap_eq_a","supply_gap_eq_b"]
            supply_gap_ef_inputs = ["Initial Material Price","Supply Gap Delay","Equation degree","Equation parameter <b>a</b>","Equation parameter <b>b</b>"]
            if st.session_state.input["supply_gap_eq_degree"] >= 2:
                supply_gap_ef_lists.append("supply_gap_eq_c")
                supply_gap_ef_inputs.append("Equation parameter <b>c</b>")
            if st.session_state.input["supply_gap_eq_degree"] >= 3:
                supply_gap_ef_lists.append("supply_gap_eq_d")
                supply_gap_ef_inputs.append("Equation parameter <b>d</b>")
            supply_gap_ef_values = [inputs[supply_gap_ef_lists[i]] for i in range(len(supply_gap_ef_lists))]
            sp_ef_df = pd.DataFrame({
                "Inputs":supply_gap_ef_inputs,
                "Values":supply_gap_ef_values
                })
            st.write(sp_ef_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
            if st.session_state.input["supply_gap_eq_degree"] == 1:
                a = supply_gap_ef_values[3]
                b = supply_gap_ef_values[4]
                st.latex(rf'\text{{Material Price}} = {a} \times \text{{(Gap or Surplus)}} + {b}')
            elif st.session_state.input["supply_gap_eq_degree"] == 2:
                a = supply_gap_ef_values[3]
                b = supply_gap_ef_values[4]
                c = supply_gap_ef_values[5]
                st.latex(rf'\text{{Material Price}} = {a} \times \text{{(Gap or Surplus)}}^2 + {b}\times \text{{(Gap or Surplus)}} + {c}')
            elif st.session_state.input["supply_gap_eq_degree"] == 3:
                a = supply_gap_ef_values[3]
                b = supply_gap_ef_values[4]
                c = supply_gap_ef_values[5]
                d = supply_gap_ef_values[6]
                st.latex(rf'\text{{Material Price}} = {a} \times \text{{(Gap or Surplus)}}^3 + {b}\times \text{{(Gap or Surplus)}}^2 + {c}\times \text{{(Gap or Surplus)}}+{d}')

            st.divider()
            st.markdown("<h3 class='small-header'>Effect of Direct Mining</h3>", unsafe_allow_html=True)
            if st.session_state.input["supply_option"] == 1 or st.session_state.input["direct_mining_affected"] == 2:
                st.markdown("There is no price effect on direct mining")
            else:
                dmgr_lists = ["dmgr_delay","dmgr_eq_degree","dmgr_eq_a","dmgr_eq_b"]
                dmgr_inputs = ["Direct mining growth rate delay","Equation degree","Equation parameter <b>a</b>","Equation parameter <b>b</b>"]
                if st.session_state.input["dmgr_eq_degree"] >= 2:
                    dmgr_lists.append("dmgr_eq_c")
                    dmgr_inputs.append("Equation parameter <b>c</b>")
                if st.session_state.input["dmgr_eq_degree"] >= 3:
                    dmgr_lists.append("dmgr_eq_d")
                    dmgr_inputs.append("Equation parameter <b>d</b>")
                dmgr_values = [inputs[dmgr_lists[i]] for i in range(len(dmgr_lists))]
                dmgr_df = pd.DataFrame({
                    "Inputs":dmgr_inputs,
                    "Values":dmgr_values
                    })
                st.write(dmgr_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
                if st.session_state.input["dmgr_eq_degree"] == 1:
                    a2 = dmgr_values[2]
                    b2 = dmgr_values[3]
                    st.latex(rf'\text{{Direct Mining Growth Rate}} = {a2} \times \text{{(Material Price)}} + {b2}')
                elif st.session_state.input["dmgr_eq_degree"] == 2:
                    a2 = dmgr_values[2]
                    b2 = dmgr_values[3]
                    c2 = dmgr_values[4]
                    st.latex(rf'\text{{Direct Mining Growth Rate}} = {a2} \times \text{{(Material Price)}}^2 + {b2}\times \text{{(Material Prices)}} + {c2}')
                elif st.session_state.input["dmgr_eq_degree"] == 3:
                    a2 = dmgr_values[2]
                    b2 = dmgr_values[3]
                    c2 = dmgr_values[4]
                    d2 = dmgr_values[5]
                    st.latex(rf'\text{{Direct Mining Growth Rate}} = {a2} \times \text{{(Material Price)}}^3 + {b2}\times \text{{(Material Price)}}^2 + {c2}\times \text{{(Material Price)}}+{d2}')

            st.divider()
            st.markdown("<h3 class='small-header'>Effect of Byproduction </h3>", unsafe_allow_html=True)
            if st.session_state.input["bp_reserve_option"] == 2:
                if st.session_state.input["bpgr_affected"] == 2:
                    st.markdown("There is no price effect on byproduction")
                elif st.session_state.input["bpgr_affected"] == 1:
                    bpgr_lists = ["bpgr_delay","bpgr_eq_degree","bpgr_eq_a","bpgr_eq_b"]
                    bpgr_inputs = ["Byproduction growth rate delay","Equation degree","Equation parameter <b>a</b>","Equation parameter <b>b</b>"]
                    if st.session_state.input["bpgr_eq_degree"] >= 2:
                        bpgr_lists.append("bpgr_eq_c")
                        bpgr_inputs.append("Equation parameter <b>c</b>")
                    if st.session_state.input["bpgr_eq_degree"] >= 3:
                        bpgr_lists.append("bpgr_eq_d")
                        bpgr_inputs.append("Equation parameter <b>d</b>")
                    bpgr_values = [inputs[bpgr_lists[i]] for i in range(len(bpgr_lists))]
                    bpgr_df = pd.DataFrame({
                        "Inputs":bpgr_inputs,
                        "Values":bpgr_values
                        })
                    st.write(bpgr_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
                    if st.session_state.input["bpgr_eq_degree"] == 1:
                        a3 = bpgr_values[2]
                        b3 = bpgr_values[3]
                        st.latex(rf'\text{{Byproduction Growth Rate}} = {a3} \times \text{{(Material Price)}} + {b3}')
                    elif st.session_state.input["bpgr_eq_degree"] == 2:
                        a3 = bpgr_values[2]
                        b3 = bpgr_values[3]
                        c3 = bpgr_values[4]
                        st.latex(rf'\text{{Byproduction Growth Rate}} = {a3} \times \text{{(Material Price)}}^2 + {b3}\times \text{{(Material Prices)}} + {c3}')
                    elif st.session_state.input["bpgr_eq_degree"] == 3:
                        a3 = bpgr_values[2]
                        b3 = bpgr_values[3]
                        c3 = bpgr_values[4]
                        d3 = bpgr_values[5]
                        st.latex(rf'\text{{Byproduction Growth Rate}} = {a3} \times \text{{(Material Price)}}^3 + {b3}\times \text{{(Material Price)}}^2 + {c3}\times \text{{(Material Price)}}+{d3}')
            elif st.session_state.input["bp_reserve_option"] == 1:
                if st.session_state.input["num_bp_hosts"] == 0:
                    st.markdown("There is no price effect on byproduction")
                else:
                    num_bp = st.session_state.input["num_bp_hosts"]
                    bpy_affect_lists = ["hitchhiker1_affected","hitchhiker2_affected","hitchhiker3_affected"]
                    bpy_affect_values = [inputs[i] for i in bpy_affect_lists]
                    bpy_affect_df = pd.DataFrame({
                        "Host metal":range(1,num_bp+1),
                        "Name": inputs["bp_host_metal_name"][:num_bp],
                        "Yield affected by metal price":["Yes" if i==1 else "No" for i in bpy_affect_values][:num_bp]
                        })
                    st.write(bpy_affect_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
                    if 1 in bpy_affect_values:
                        bpy_lists = ["bpy_delay","bpy_eq_degree","bpy_eq_a","bpy_eq_b"]
                        bpy_inputs = ["Byproduction growth rate delay","Equation degree","Equation parameter <b>a</b>","Equation parameter <b>b</b>"]
                        if st.session_state.input["bpy_eq_degree"] >= 2:
                            bpy_lists.append("bpy_eq_c")
                            bpy_inputs.append("Equation parameter <b>c</b>")
                        if st.session_state.input["bpy_eq_degree"] >= 3:
                            bpy_lists.append("bpy_eq_d")
                            bpy_inputs.append("Equation parameter <b>d</b>")
                        bpy_values = [inputs[bpy_lists[i]] for i in range(len(bpy_lists))]
                        bpy_df = pd.DataFrame({
                            "Inputs":bpy_inputs,
                            "Values":bpy_values
                            })
                        st.write(bpy_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
                        if st.session_state.input["bpy_eq_degree"] == 1:
                            a3 = bpy_values[2]
                            b3 = bpy_values[3]
                            st.latex(rf'\text{{Byproduction Yield}} = {a3} \times \text{{(Material Price)}} + {b3}')
                        elif st.session_state.input["bpy_eq_degree"] == 2:
                            a3 = bpy_values[2]
                            b3 = bpy_values[3]
                            c3 = bpy_values[4]
                            st.latex(rf'\text{{Byproduction Yield}} = {a3} \times \text{{(Material Price)}}^2 + {b3}\times \text{{(Material Prices)}} + {c3}')
                        elif st.session_state.input["bpy_eq_degree"] == 3:
                            a3 = bpy_values[2]
                            b3 = bpy_values[3]
                            c3 = bpy_values[4]
                            d3 = bpy_values[5]
                            st.latex(rf'\text{{Byproduction Yield}} = {a3} \times \text{{(Material Price)}}^3 + {b3}\times \text{{(Material Price)}}^2 + {c3}\times \text{{(Material Price)}}+{d3}')
                    else:
                        st.markdown("There is no price effect on byproduction")
                    
            st.divider()
            st.markdown("<h3 class='small-header'>Effect of PV Demand </h3>", unsafe_allow_html=True)
            pv_price_df = pd.DataFrame({
                        "Inputs":["Price thershold ($/Wp)","PV technology selling price ($/Wp)"],
                        "Values": [inputs["pv_price_threshold"],inputs["pv_tech_price"]],
                        })
            st.write(pv_price_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)

            st.divider()
            st.markdown("<h3 class='small-header'>Global Stocks </h3>", unsafe_allow_html=True)
            gs_df = pd.DataFrame({
                        "Inputs":["Global stocks"],
                        "Values": [inputs["global_stocks"]],
                        })
            st.write(gs_df.to_html(index=False,justify='left', escape=False), unsafe_allow_html=True)
    # This is previous code
    if False:
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
        pass 

# Page 7: Calculate Results
if page == "Calculate Results":
    st.header("Calculate Results", divider='grey')

    st.write("Results")
    button = st.button("Calculate", use_container_width=True)

    if button and "input" in st.session_state:
        # load the pysd file
        model = pysd.load('09032024_PVMat.py')
        data = st.session_state["input"]
    # Add content for Calculate Results page
        start_year = data["project_starting_year"]
        end_year = data["project_final_year"]
        for year in range(start_year, end_year + 1):
            ind = year-start_year
            st.write(data["pv_capacity"])
            output = model.run(params={"Time":year,
                                       "PV Future Production User Input":data["pv_user_input"],
                                       "Planned Annual Incremental Capacity":data["annual_incremental_capacity"],
                                       "PV Deployment Initial Incremental": data["pv_initial_incremental"],
                                       "Current Annual PV Deployment": data["pv_annual_deployment"],
                                       "Planned Annual Incremental Capacity User Input":data["annual_incremental_capacity"],
                                       "PV Deployment Initial Incremental User Input":data["pv_initial_incremental"],
                                       "Current Annual PV Deployment User Input":data["pv_annual_deployment"],
                                       "PV Technology Market Share":data["pv_market_share"][ind],
                                       "PV Technology Material Intensity":data["pv_material_intensity"][ind],
                                       "Current nonPV demand":data["nonpv_demand"],
                                       "NPVGR":data["nonpv_demand_gr"],
                                       "New PV Recycling Estimation Method": data["newpv_lifetime_option"],
                                       "Average PV Lifetime":data["newpv_panel_lifetime"],
                                       "Recycling efficiency":data["newpv_recycling_efficiency"],
                                       "Collection efficiency":data["newpv_recycling_collection_efficiency"],
                                       "Percentage Panels Recycled":data["newpv_percentage_panels_recycled"],
                                       "Recycled Material Flows Estimation Method":data["rec_cal_method"],
                                       "Recycled Material Flows User Input":data["pv_annual_supply"],
                                       "ExPV Installed":data["pv_capacity"],
                                       "Percentage Panels Recycled ExPV":data["pv_recycling"],
                                       "Collection efficiency ExPV":data["pv_collection_efficiency"],
                                       "Recycling Efficiency ExPV":data["pv_recycling_efficiency"],
                                       "Existing PV Recycling Estimation Method":data["pv_lifetime_option"],
                                       "Average Existing PV Lifetime":data["pv_panel_lifetime"],
                                       "Material Intensity Input Method":data["pv_mint"],
                                       "ExPV Material Intensity Annual":data["pv_annual_mint"],
                                       "ExPV Material Intensity Constant":data["pv_avg_mint"],
                                       "Direct Mining Estimation Method User Input":data["supply_option"],
                                       ### may have some errors
                                       "Direct Mining Supply Manual":data["mine_data"]["Annual production"],
                                       ###
                                       "Direct Mining Reserves User Input":data["global_reserves"],
                                       "Current DM GR":data["global_production"],
                                       "Direct mining current production User Input":data["direct_mining_growth"],
                                       "Byproduction Estimation Method User Input":data["bp_reserve_option"],
                                       "byproduction supply User Input":data["bp_current_supply"],
                                       "current byproduction Growth Rate":data["bp_supply_growth"],
                                       "Number of host metals user input":data["num_bp_hosts"],
                                       "Host Metal Production at y0":data["bp_annual_production"][0],
                                       "Host metal Reserves User Input":data["bp_global_reserves"][0],
                                       "Host metal mining Growth Rate":data["bp_annual_production_growth"][0],
                                       "Hitchhiker content in Host Metal":data["bp_hitchhiker_content"][0],
                                       "Current PV material byproduction yield 1":data["bp_hitchhiker_recovery_efficiency"][0],
                                       "Host Metal 2 Production at y0":data["bp_annual_production"][1],
                                       "Host metal 2 Reserves User Input":data["bp_global_reserves"][1],
                                       "Host metal 2 mining Growth Rate":data["bp_annual_production_growth"][1],
                                       "Hitchhiker content in Host Metal 2":data["bp_hitchhiker_content"][1],
                                       "Current PV material byproduction yield 2":data["bp_hitchhiker_recovery_efficiency"][1],
                                       "Host Metal 3 Production at y0":data["bp_annual_production"][2],
                                       "Host metal 3 Reserves User Input":data["bp_global_reserves"][2],
                                       "Host metal 3 mining Growth Rate":data["bp_annual_production_growth"][2],
                                       "Hitchhiker content in Host Metal 3":data["bp_hitchhiker_content"][2],
                                       "Current PV material byproduction yield 3":data["bp_hitchhiker_recovery_efficiency"][2],
                                       "Initial Material Price":data["target_metal_price"],
                                       "Suppy Gap Delay":data["supply_gap_delay"],
                                       "SupplyGap Price Eq degree":data["supply_gap_eq_degree"],
                                       "a price":data["supply_gap_eq_a"],
                                       "b price":data["supply_gap_eq_b"],
                                       "c price":data["supply_gap_eq_c"],
                                       "d price":data["supply_gap_eq_d"],
                                       "Direct Mining Affected":data["direct_mining_affected"],
                                       "Price DMGR delay":data["dmgr_delay"],
                                       "Price DMGR Eq degree":data["dmgr_eq_degree"],
                                       "a GR":data["dmgr_eq_a"],
                                       "b GR":data["dmgr_eq_b"],
                                       "c GR":data["dmgr_eq_c"],
                                       "d GR":data["dmgr_eq_d"],
                                       "byproduction GR Affected":data["bpgr_affected"],
                                       "price yield avg delay":data["bpgr_delay"],
                                       "Price Yield Eq degree avg":data["bpgr_eq_degree"],
                                       "a yield avg":data["bpgr_eq_a"],
                                       "b yield avg":data["bpgr_eq_b"],
                                       "c yield avg":data["bpgr_eq_c"],
                                       "d yield avg":data["bpgr_eq_d"],
                                       "Hitchhiker 1 affected":data["hitchhiker1_affected"],
                                       "Hitchhiker 2 affected":data["hitchhiker2_affected"],
                                       "Hitchhiker 3 affected":data["hitchhiker3_affected"],
                                       "price yield delay":data["bpy_delay"],
                                       "Price Yield Eq degree":data["bpy_eq_degree"],
                                       "a yield":data["bpy_eq_a"],
                                       "b yield":data["bpy_eq_b"],
                                       "c yield":data["bpy_eq_c"],
                                       "d yield":data["bpy_eq_d"],
                                       "Price Threshold":data["pv_price_threshold"],
                                       "PV Technology Current ASP":data["pv_tech_price"],
                                       "Global Stocks User Input":data["global_stocks"],
                                      })
        st.write(output)
        #output1 = BytesIO()
        #with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Write each DataFrame to a different sheet
            #output.to_excel(writer, index=True)
        #excel_data = output1.getvalue()
        #st.download_button(
            #label=f"Click to Download output",
            #data=excel_data,
            #key=f"download127",
            #file_name=f"output.csv",
            #mime="text/csv",
        #)                  
                                        

# Page 8: Plot Results
if page == "Plot Results":
    st.header("Plot Results", divider='grey')
    # Add content for Plot Results page

dashboard = Dashboard()
