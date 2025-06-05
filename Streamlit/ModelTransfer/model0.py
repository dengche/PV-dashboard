"""
Python model 'model0.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import sum, not_implemented_function, if_then_else
from pysd.py_backend.statefuls import Integ, NonNegativeInteg
from pysd import Component

__pysd_version__ = "3.12.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


_subscript_dict = {
    "PVDev": [
        "Y2023",
        "Y2024",
        "Y2025",
        "Y2026",
        "Y2027",
        "Y2028",
        "Y2029",
        "Y2030",
        "Y2031",
        "Y2032",
        "Y2033",
        "Y2034",
        "Y2035",
        "Y2036",
        "Y2037",
        "Y2038",
        "Y2039",
        "Y2040",
        "Y2041",
        "Y2042",
        "Y2043",
        "Y2044",
        "Y2045",
        "Y2046",
        "Y2047",
        "Y2048",
        "Y2049",
        "Y2050",
    ],
    "StudyPeriod": [
        "Y2023",
        "Y2024",
        "Y2025",
        "Y2026",
        "Y2027",
        "Y2028",
        "Y2029",
        "Y2030",
        "Y2031",
        "Y2032",
        "Y2033",
        "Y2034",
        "Y2035",
        "Y2036",
        "Y2037",
        "Y2038",
        "Y2039",
        "Y2040",
        "Y2041",
        "Y2042",
        "Y2043",
        "Y2044",
        "Y2045",
        "Y2046",
        "Y2047",
        "Y2048",
        "Y2049",
        "Y2050",
    ],
}

component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 2023,
    "final_time": lambda: 2050,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="INITIAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="FINAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="TIME STEP", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


@component.add(
    name="SAVEPER",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The save time step for the simulation.
    """
    return __data["time"].saveper()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Annual Material Demand",
    units="Metric Tons/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"yearly_pv_industry_demand": 1, "annual_non_pv_demand": 1},
)
def annual_material_demand():
    return yearly_pv_industry_demand() + annual_non_pv_demand()


@component.add(
    name="PV Technology Production Capacity",
    units="GWp",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_pv_deployment": 1, "pv_technology_market_share": 1},
)
def pv_technology_production_capacity():
    return annual_pv_deployment() * pv_technology_market_share() / 100


@component.add(
    name="Recycling Efficiency", units="%", comp_type="Constant", comp_subtype="Normal"
)
def recycling_efficiency():
    return 90


@component.add(
    name="Percentage Panels Recycled",
    units="%",
    comp_type="Constant",
    comp_subtype="Normal",
)
def percentage_panels_recycled():
    return 100


@component.add(
    name="Collection efficiency", units="%", comp_type="Constant", comp_subtype="Normal"
)
def collection_efficiency():
    return 90


@component.add(
    name="Change in Material Price",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"material_cost_per_watt": 1, "op": 1},
)
def change_in_material_price():
    return material_cost_per_watt() - op()


@component.add(
    name="Material Price",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "supplygap_price_eq_degree": 2,
        "a_price": 3,
        "initial_material_price": 3,
        "annual_material_surplus": 6,
        "b_price": 3,
        "suppy_gap_delay": 3,
        "c_price": 2,
        "d_price": 1,
    },
)
def material_price():
    return if_then_else(
        supplygap_price_eq_degree() == 1,
        lambda: not_implemented_function(
            "delay",
            a_price() * annual_material_surplus() + b_price(),
            suppy_gap_delay(),
            initial_material_price(),
        ),
        lambda: if_then_else(
            supplygap_price_eq_degree() == 2,
            lambda: not_implemented_function(
                "delay",
                a_price() * annual_material_surplus() ** 2
                + b_price() * annual_material_surplus()
                + c_price(),
                suppy_gap_delay(),
                initial_material_price(),
            ),
            lambda: not_implemented_function(
                "delay",
                a_price() * annual_material_surplus() ** 3
                + b_price() * annual_material_surplus() ** 2
                + c_price() * annual_material_surplus()
                + d_price(),
                suppy_gap_delay(),
                initial_material_price(),
            ),
        ),
    )


@component.add(name="Price Threshold", comp_type="Constant", comp_subtype="Normal")
def price_threshold():
    return 0.33


@component.add(
    name="Condition",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "updated_pv_technology_asp": 1,
        "price_threshold": 1,
        "actual_pv_technology_production": 1,
        "pv_technology_production_capacity": 1,
    },
)
def condition():
    return if_then_else(
        updated_pv_technology_asp() > price_threshold(),
        lambda: 1,
        lambda: if_then_else(
            actual_pv_technology_production() < pv_technology_production_capacity(),
            lambda: 1,
            lambda: 0,
        ),
    )


@component.add(
    name="Weibull PDF Regular Loss",
    subscripts=["PVDev"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def weibull_pdf_regular_loss():
    value = xr.DataArray(np.nan, {"PVDev": _subscript_dict["PVDev"]}, ["PVDev"])
    value.loc[["Y2023"]] = 0
    value.loc[["Y2024"]] = 1.14589e-08
    value.loc[["Y2025"]] = 4.6437e-07
    value.loc[["Y2026"]] = 3.7324e-06
    value.loc[["Y2027"]] = 1.55503e-05
    value.loc[["Y2028"]] = 4.58141e-05
    value.loc[["Y2029"]] = 0.000109
    value.loc[["Y2030"]] = 0.000225416
    value.loc[["Y2031"]] = 0.000419991
    value.loc[["Y2032"]] = 0.000724122
    value.loc[["Y2033"]] = 0.001175012
    value.loc[["Y2034"]] = 0.001815758
    value.loc[["Y2035"]] = 0.002694991
    value.loc[["Y2036"]] = 0.0038661
    value.loc[["Y2037"]] = 0.005385871
    value.loc[["Y2038"]] = 0.007312366
    value.loc[["Y2039"]] = 0.00970182
    value.loc[["Y2040"]] = 0.012604341
    value.loc[["Y2041"]] = 0.016058261
    value.loc[["Y2042"]] = 0.020083043
    value.loc[["Y2043"]] = 0.024670873
    value.loc[["Y2044"]] = 0.029777319
    value.loc[["Y2045"]] = 0.035311818
    value.loc[["Y2046"]] = 0.041129281
    value.loc[["Y2047"]] = 0.047024564
    value.loc[["Y2048"]] = 0.052732091
    value.loc[["Y2049"]] = 0.057933068
    value.loc[["Y2050"]] = 0.062272547
    return value


@component.add(
    name="Annual Dismantled PV",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "new_pv_recycling_estimation_method": 1,
        "dismantled_pv_per_production_phase": 2,
        "average_pv_lifetime": 1,
    },
)
def annual_dismantled_pv():
    return if_then_else(
        new_pv_recycling_estimation_method() == 1,
        lambda: not_implemented_function(
            "delay",
            float(dismantled_pv_per_production_phase().loc["Y2023"]),
            average_pv_lifetime() - 1,
            0,
        ),
        lambda: sum(dismantled_pv_per_production_phase(), dim=[]),
    )


@component.add(
    name="Annual Material Surplus",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"material_production_annual": 1, "annual_material_demand": 1},
)
def annual_material_surplus():
    return material_production_annual() - annual_material_demand()


@component.add(
    name="Effect on Material byproduction Yield",
    units="untiless",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "price_yield_eq_degree": 2,
        "material_price": 6,
        "b_yield": 3,
        "a_yield": 3,
        "c_yield": 2,
        "d_yield": 1,
    },
)
def effect_on_material_byproduction_yield():
    return if_then_else(
        price_yield_eq_degree() == 1,
        lambda: a_yield() * material_price() + b_yield(),
        lambda: if_then_else(
            price_yield_eq_degree() == 2,
            lambda: a_yield() * material_price() ** 2
            + b_yield() * material_price()
            + c_yield(),
            lambda: a_yield() * material_price() ** 3
            + b_yield() * material_price() ** 2
            + c_yield() * material_price()
            + d_yield(),
        ),
    )


@component.add(
    name="Delayed yield Effect",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effect_on_material_byproduction_yield": 1, "price_yield_delay": 1},
)
def delayed_yield_effect():
    return not_implemented_function(
        "delay", effect_on_material_byproduction_yield(), price_yield_delay(), 1
    )


@component.add(
    name="Planned Annual Incremental Capacity",
    units="GWp/year",
    subscripts=["PVDev"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def planned_annual_incremental_capacity():
    value = xr.DataArray(np.nan, {"PVDev": _subscript_dict["PVDev"]}, ["PVDev"])
    value.loc[["Y2023"]] = 3.33
    value.loc[["Y2024"]] = 4.22
    value.loc[["Y2025"]] = 4.33
    value.loc[["Y2026"]] = 4.55
    value.loc[["Y2027"]] = 5.33
    value.loc[["Y2028"]] = 6.39
    value.loc[["Y2029"]] = 7.55
    value.loc[["Y2030"]] = 7.69
    value.loc[["Y2031"]] = 8.04
    value.loc[["Y2032"]] = 9.26
    value.loc[["Y2033"]] = 10.97
    value.loc[["Y2034"]] = 10.48
    value.loc[["Y2035"]] = 10.69
    value.loc[["Y2036"]] = 11.97
    value.loc[["Y2037"]] = 12.1
    value.loc[["Y2038"]] = 12.57
    value.loc[["Y2039"]] = 14.35
    value.loc[["Y2040"]] = 16.1
    value.loc[["Y2041"]] = 18.73
    value.loc[["Y2042"]] = 18.85
    value.loc[["Y2043"]] = 22.66
    value.loc[["Y2044"]] = 23.63
    value.loc[["Y2045"]] = 22.98
    value.loc[["Y2046"]] = 28.93
    value.loc[["Y2047"]] = 32.67
    value.loc[["Y2048"]] = 32.84
    value.loc[["Y2049"]] = 0
    value.loc[["Y2050"]] = 0
    return value


@component.add(
    name="PV Deployment Initial Incremental",
    units="GWp/year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def pv_deployment_initial_incremental():
    return 3.84


@component.add(
    name="Material Cost per Watt",
    units="$/W",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pv_technology_material_intensity": 1, "material_price": 1},
)
def material_cost_per_watt():
    return pv_technology_material_intensity() * material_price()


@component.add(
    name="Recycling - Annual PV",
    subscripts=["PVDev"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"actual_annual_material_demand": 28},
)
def recycling_annual_pv():
    value = xr.DataArray(np.nan, {"PVDev": _subscript_dict["PVDev"]}, ["PVDev"])
    value.loc[["Y2023"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 0, 0
    )
    value.loc[["Y2024"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 1, 0
    )
    value.loc[["Y2025"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 2, 0
    )
    value.loc[["Y2026"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 3, 0
    )
    value.loc[["Y2027"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 4, 0
    )
    value.loc[["Y2028"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 5, 0
    )
    value.loc[["Y2029"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 6, 0
    )
    value.loc[["Y2030"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 7, 0
    )
    value.loc[["Y2031"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 8, 0
    )
    value.loc[["Y2032"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 9, 0
    )
    value.loc[["Y2033"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 10, 0
    )
    value.loc[["Y2034"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 11, 0
    )
    value.loc[["Y2035"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 12, 0
    )
    value.loc[["Y2036"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 13, 0
    )
    value.loc[["Y2037"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 14, 0
    )
    value.loc[["Y2038"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 15, 0
    )
    value.loc[["Y2039"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 16, 0
    )
    value.loc[["Y2040"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 17, 0
    )
    value.loc[["Y2041"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 18, 0
    )
    value.loc[["Y2042"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 19, 0
    )
    value.loc[["Y2043"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 20, 0
    )
    value.loc[["Y2044"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 21, 0
    )
    value.loc[["Y2045"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 22, 0
    )
    value.loc[["Y2046"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 23, 0
    )
    value.loc[["Y2047"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 24, 0
    )
    value.loc[["Y2048"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 25, 0
    )
    value.loc[["Y2049"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 26, 0
    )
    value.loc[["Y2050"]] = not_implemented_function(
        "delay", actual_annual_material_demand(), 27, 0
    )
    return value


@component.add(name="NPVGR", comp_type="Constant", comp_subtype="Normal")
def npvgr():
    return 3.96


@component.add(
    name="Direct Mining Estimation Method User Input",
    comp_type="Constant",
    comp_subtype="Normal",
)
def direct_mining_estimation_method_user_input():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return 1


@component.add(
    name="Total Annual Supply from Direct Mining",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "direct_mining_estimation_method_user_input": 1,
        "direct_mining_supply_manual": 1,
        "direct_mining_supply_rough_estimate": 1,
    },
)
def total_annual_supply_from_direct_mining():
    """
    1: Manual mines input
    2: Rough estimate
    """
    return if_then_else(
        direct_mining_estimation_method_user_input() == 1,
        lambda: direct_mining_supply_manual(),
        lambda: direct_mining_supply_rough_estimate(),
    )


@component.add(
    name="Direct Mining Supply Manual",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def direct_mining_supply_manual():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return np.interp(
        time(),
        [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    )


@component.add(
    name="Direct Mining Supply Rough Estimate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_production": 1,
        "direct_mining_current_production_user_input": 1,
    },
)
def direct_mining_supply_rough_estimate():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return not_implemented_function(
        "delay", annual_production(), 0, direct_mining_current_production_user_input()
    )


@component.add(
    name="Total Annual Supply from byproduction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "byproduction_estimation_method_user_input": 1,
        "byproduction_detailed_calculation_estimate": 1,
        "byproduction_supply_rough_estimate": 1,
    },
)
def total_annual_supply_from_byproduction():
    """
    1: Detailed Calculation
    2: Rough estimate
    """
    return if_then_else(
        byproduction_estimation_method_user_input() == 1,
        lambda: byproduction_detailed_calculation_estimate(),
        lambda: byproduction_supply_rough_estimate(),
    )


@component.add(
    name="Byproduction Detailed Calculation Estimate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "number_of_host_metals_user_input": 3,
        "hitchhiker_byproduction_host_metal": 3,
        "hitchhiker_byproduction_host_metal_3": 1,
        "hitchhiker_byproduction_host_metal_2": 2,
    },
)
def byproduction_detailed_calculation_estimate():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return if_then_else(
        number_of_host_metals_user_input() == 1,
        lambda: hitchhiker_byproduction_host_metal(),
        lambda: if_then_else(
            number_of_host_metals_user_input() == 2,
            lambda: hitchhiker_byproduction_host_metal()
            + hitchhiker_byproduction_host_metal_2(),
            lambda: if_then_else(
                number_of_host_metals_user_input() == 3,
                lambda: hitchhiker_byproduction_host_metal()
                + hitchhiker_byproduction_host_metal_2()
                + hitchhiker_byproduction_host_metal_3(),
                lambda: 0,
            ),
        ),
    )


@component.add(
    name="Byproduction Supply Rough Estimate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_byproduction": 1},
)
def byproduction_supply_rough_estimate():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return annual_byproduction()


@component.add(
    name="Byproduction Estimation Method User Input",
    comp_type="Constant",
    comp_subtype="Normal",
)
def byproduction_estimation_method_user_input():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return 1


@component.add(
    name="byproduction Growth Rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "byproduction_gr_affected": 1,
        "current_byproduction_growth_rate": 2,
        "new_byproduction_yield_avg_factor": 1,
    },
)
def byproduction_growth_rate():
    return if_then_else(
        byproduction_gr_affected() == 1,
        lambda: current_byproduction_growth_rate()
        * new_byproduction_yield_avg_factor(),
        lambda: current_byproduction_growth_rate(),
    )


@component.add(
    name="Host metal mining Growth Rate", comp_type="Constant", comp_subtype="Normal"
)
def host_metal_mining_growth_rate():
    return 2.5


@component.add(
    name="Hitchhiker content in Host Metal", comp_type="Constant", comp_subtype="Normal"
)
def hitchhiker_content_in_host_metal():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return 1


@component.add(
    name="Hitchhiker recovery efficiency from Host Metal 1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hitchhiker_1_affected": 1,
        "current_pv_material_byproduction_yield_1": 3,
        "new_byproduction_yield_factor": 1,
    },
)
def hitchhiker_recovery_efficiency_from_host_metal_1():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return if_then_else(
        hitchhiker_1_affected() == 1,
        lambda: not_implemented_function(
            "delay",
            new_byproduction_yield_factor()
            * current_pv_material_byproduction_yield_1(),
            0,
            current_pv_material_byproduction_yield_1(),
        ),
        lambda: current_pv_material_byproduction_yield_1(),
    )


@component.add(
    name="Hitchhiker ByProduction Host Metal",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "host_metal_annual_production": 1,
        "hitchhiker_content_in_host_metal": 1,
        "hitchhiker_recovery_efficiency_from_host_metal_1": 1,
    },
)
def hitchhiker_byproduction_host_metal():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return (
        host_metal_annual_production()
        * hitchhiker_content_in_host_metal()
        * hitchhiker_recovery_efficiency_from_host_metal_1()
    )


@component.add(
    name="Hitchhiker ByProduction Host Metal 2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "host_metal_2_annual_production": 1,
        "hitchhiker_content_in_host_metal_2": 1,
        "hitchhiker_recovery_efficiency_from_host_metal_2": 1,
    },
)
def hitchhiker_byproduction_host_metal_2():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return (
        host_metal_2_annual_production()
        * hitchhiker_content_in_host_metal_2()
        * hitchhiker_recovery_efficiency_from_host_metal_2()
    )


@component.add(
    name="Hitchhiker ByProduction Host Metal 3",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hitchhiker_recovery_efficiency_from_host_metal_3": 1,
        "hitchhiker_content_in_host_metal_3": 1,
        "host_metal_3_annual_production": 1,
    },
)
def hitchhiker_byproduction_host_metal_3():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return (
        hitchhiker_recovery_efficiency_from_host_metal_3()
        * hitchhiker_content_in_host_metal_3()
        * host_metal_3_annual_production()
    )


@component.add(
    name="Host metal 2 mining Growth Rate", comp_type="Constant", comp_subtype="Normal"
)
def host_metal_2_mining_growth_rate():
    return 2.5


@component.add(
    name="Hitchhiker content in Host Metal 2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hitchhiker_content_in_host_metal_2():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return 1


@component.add(
    name="Hitchhiker recovery efficiency from Host Metal 2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hitchhiker_2_affected": 1,
        "new_byproduction_yield_factor": 1,
        "current_pv_material_byproduction_yield_2": 3,
    },
)
def hitchhiker_recovery_efficiency_from_host_metal_2():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return if_then_else(
        hitchhiker_2_affected() == 1,
        lambda: not_implemented_function(
            "delay",
            new_byproduction_yield_factor()
            * current_pv_material_byproduction_yield_2(),
            0,
            current_pv_material_byproduction_yield_2(),
        ),
        lambda: current_pv_material_byproduction_yield_2(),
    )


@component.add(
    name="Host metal 3 mining Growth Rate", comp_type="Constant", comp_subtype="Normal"
)
def host_metal_3_mining_growth_rate():
    return 2.5


@component.add(
    name="Hitchhiker content in Host Metal 3",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hitchhiker_content_in_host_metal_3():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return 1


@component.add(
    name="Hitchhiker recovery efficiency from Host Metal 3",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hitchhiker_3_affected": 1,
        "new_byproduction_yield_factor": 1,
        "current_pv_material_byproduction_yield_3": 3,
    },
)
def hitchhiker_recovery_efficiency_from_host_metal_3():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return if_then_else(
        hitchhiker_3_affected() == 1,
        lambda: not_implemented_function(
            "delay",
            new_byproduction_yield_factor()
            * current_pv_material_byproduction_yield_3(),
            0,
            current_pv_material_byproduction_yield_3(),
        ),
        lambda: current_pv_material_byproduction_yield_3(),
    )


@component.add(
    name="Number of host metals user input", comp_type="Constant", comp_subtype="Normal"
)
def number_of_host_metals_user_input():
    """
    1: Manually input mines production
    2: Calculate based on current production and future growth
    """
    return 1


@component.add(
    name="Total Annual Recycling Supply from new PV",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_recycled_metalx": 1},
)
def total_annual_recycling_supply_from_new_pv():
    return annual_recycled_metalx()


@component.add(
    name="New PV Recycling Estimation Method",
    comp_type="Constant",
    comp_subtype="Normal",
)
def new_pv_recycling_estimation_method():
    """
    1: Fixed Lifetime
    2: Weibull Early Loss
    3: Weibull Regular Loss
    """
    return 1


@component.add(
    name="Weibull PDF Early Loss",
    subscripts=["PVDev"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def weibull_pdf_early_loss():
    value = xr.DataArray(np.nan, {"PVDev": _subscript_dict["PVDev"]}, ["PVDev"])
    value.loc[["Y2023"]] = 0
    value.loc[["Y2024"]] = 0.0002079
    value.loc[["Y2025"]] = 0.0009616
    value.loc[["Y2026"]] = 0.0020405
    value.loc[["Y2027"]] = 0.0033548
    value.loc[["Y2028"]] = 0.004857
    value.loc[["Y2029"]] = 0.0065125
    value.loc[["Y2030"]] = 0.0082919
    value.loc[["Y2031"]] = 0.0101678
    value.loc[["Y2032"]] = 0.0121142
    value.loc[["Y2033"]] = 0.0141052
    value.loc[["Y2034"]] = 0.016115
    value.loc[["Y2035"]] = 0.0181181
    value.loc[["Y2036"]] = 0.020089
    value.loc[["Y2037"]] = 0.0220029
    value.loc[["Y2038"]] = 0.0238356
    value.loc[["Y2039"]] = 0.025564
    value.loc[["Y2040"]] = 0.0271664
    value.loc[["Y2041"]] = 0.028623
    value.loc[["Y2042"]] = 0.0299159
    value.loc[["Y2043"]] = 0.0310297
    value.loc[["Y2044"]] = 0.0319518
    value.loc[["Y2045"]] = 0.0326725
    value.loc[["Y2046"]] = 0.033185
    value.loc[["Y2047"]] = 0.0334859
    value.loc[["Y2048"]] = 0.033575
    value.loc[["Y2049"]] = 0.0334553
    value.loc[["Y2050"]] = 0.033133
    return value


@component.add(
    name="Current Annual PV Deployment", comp_type="Constant", comp_subtype="Normal"
)
def current_annual_pv_deployment():
    return 13.56


@component.add(
    name="Planned PV Capacity",
    units="GWp",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def planned_pv_capacity():
    return np.interp(
        time(),
        [
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            13.56,
            17.4,
            20.73,
            24.95,
            29.28,
            33.83,
            39.16,
            45.56,
            53.11,
            60.79,
            68.83,
            78.09,
            89.06,
            99.54,
            110.23,
            122.2,
            134.3,
            146.87,
            161.23,
            177.33,
            196.06,
            214.9,
            237.56,
            261.19,
            284.16,
            313.09,
            345.76,
            378.6,
        ],
    )


@component.add(
    name="PV Technology Market Share",
    units="%",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def pv_technology_market_share():
    return np.interp(
        time(),
        [
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
            10.0,
        ],
    )


@component.add(
    name="PV Technology material intensity",
    units="kg/W",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def pv_technology_material_intensity():
    return np.interp(
        time(),
        [
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            0.7,
            2.1,
            4.6,
            6.8,
            6.8,
            6.8,
            6.8,
            5.3,
            3.0,
            3.0,
            3.0,
            3.0,
            4.65,
            5.0625,
            5.475,
            5.8875,
            6.3,
            6.7125,
            7.125,
            7.5375,
            7.95,
            8.3625,
            8.775,
            9.1875,
            9.6,
            0.0,
            0.0,
            0.0,
        ],
    )


@component.add(
    name="SupplyGap Price Eq degree",
    units="unitless",
    comp_type="Constant",
    comp_subtype="Normal",
)
def supplygap_price_eq_degree():
    return 1


@component.add(
    name="a price", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def a_price():
    return -1.336251


@component.add(
    name="b price", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def b_price():
    return 291.662152


@component.add(
    name="c price", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def c_price():
    return 1


@component.add(
    name="d price", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def d_price():
    return 1


@component.add(
    name="Initial Material Price",
    units="$/kg",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_material_price():
    return 70


@component.add(
    name="Suppy Gap Delay", units="Years", comp_type="Constant", comp_subtype="Normal"
)
def suppy_gap_delay():
    return 3


@component.add(
    name="PV Technology Current ASP", comp_type="Constant", comp_subtype="Normal"
)
def pv_technology_current_asp():
    return 0.32


@component.add(
    name="a yield", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def a_yield():
    return 0.0023


@component.add(
    name="b yield", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def b_yield():
    return 1


@component.add(
    name="c yield", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def c_yield():
    return 1


@component.add(
    name="d yield", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def d_yield():
    return 1


@component.add(
    name="price yield delay", units="Years", comp_type="Constant", comp_subtype="Normal"
)
def price_yield_delay():
    return 5


@component.add(
    name="Price Yield Eq degree",
    units="unitless",
    comp_type="Constant",
    comp_subtype="Normal",
)
def price_yield_eq_degree():
    return 1


@component.add(
    name="Current PV material byproduction yield 3",
    units="%",
    comp_type="Constant",
    comp_subtype="Normal",
)
def current_pv_material_byproduction_yield_3():
    return 0.5


@component.add(
    name="Current PV material byproduction yield 2",
    units="%",
    comp_type="Constant",
    comp_subtype="Normal",
)
def current_pv_material_byproduction_yield_2():
    return 0.5


@component.add(
    name="Current PV material byproduction yield 1",
    units="%",
    comp_type="Constant",
    comp_subtype="Normal",
)
def current_pv_material_byproduction_yield_1():
    return 0.5


@component.add(
    name="Hitchhiker 1 affected",
    units="unitless",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hitchhiker_1_affected():
    return 1


@component.add(
    name="Hitchhiker 2 affected",
    units="unitless",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hitchhiker_2_affected():
    return 1


@component.add(
    name="Hitchhiker 3 affected",
    units="unitless",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hitchhiker_3_affected():
    return 1


@component.add(
    name="Effect on Material direct mining GR",
    units="untiless",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "price_dmgr_eq_degree": 2,
        "b_gr": 3,
        "a_gr": 3,
        "material_price": 6,
        "c_gr": 2,
        "d_gr": 1,
    },
)
def effect_on_material_direct_mining_gr():
    return if_then_else(
        price_dmgr_eq_degree() == 1,
        lambda: a_gr() * material_price() + b_gr(),
        lambda: if_then_else(
            price_dmgr_eq_degree() == 2,
            lambda: a_gr() * material_price() ** 2 + b_gr() * material_price() + c_gr(),
            lambda: a_gr() * material_price() ** 3
            + b_gr() * material_price() ** 2
            + c_gr() * material_price()
            + d_gr(),
        ),
    )


@component.add(
    name="Delayed DMGR Effect",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effect_on_material_direct_mining_gr": 1, "price_dmgr_delay": 1},
)
def delayed_dmgr_effect():
    return not_implemented_function(
        "delay", effect_on_material_direct_mining_gr(), price_dmgr_delay(), 1
    )


@component.add(
    name="a GR", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def a_gr():
    return 0.0023


@component.add(
    name="b GR", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def b_gr():
    return 1


@component.add(
    name="c GR", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def c_gr():
    return 1


@component.add(
    name="d GR", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def d_gr():
    return 1


@component.add(
    name="price DMGR delay", units="Years", comp_type="Constant", comp_subtype="Normal"
)
def price_dmgr_delay():
    return 5


@component.add(
    name="Price DMGR Eq degree",
    units="unitless",
    comp_type="Constant",
    comp_subtype="Normal",
)
def price_dmgr_eq_degree():
    return 1


@component.add(
    name="Direct Mining Growth Rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"direct_mining_affected": 1, "current_dm_gr": 2, "new_dmgr_factor": 1},
)
def direct_mining_growth_rate():
    return if_then_else(
        direct_mining_affected() == 1,
        lambda: current_dm_gr() * new_dmgr_factor(),
        lambda: current_dm_gr(),
    )


@component.add(
    name="Direct Mining Affected",
    units="unitless",
    comp_type="Constant",
    comp_subtype="Normal",
)
def direct_mining_affected():
    return 0


@component.add(name="Current DM GR", comp_type="Constant", comp_subtype="Normal")
def current_dm_gr():
    return 2.5


@component.add(
    name="current byproduction Growth Rate", comp_type="Constant", comp_subtype="Normal"
)
def current_byproduction_growth_rate():
    return 2.5


@component.add(
    name="byproduction GR Affected",
    units="unitless",
    comp_type="Constant",
    comp_subtype="Normal",
)
def byproduction_gr_affected():
    return 0


@component.add(name="Average PV Lifetime", comp_type="Constant", comp_subtype="Normal")
def average_pv_lifetime():
    return 25


@component.add(
    name="PV Future Production User Input", comp_type="Constant", comp_subtype="Normal"
)
def pv_future_production_user_input():
    """
    1: Default
    2: User-specific
    """
    return 1


@component.add(
    name="Planned Annual Incremental Capacity User Input",
    units="GWp/year",
    subscripts=["PVDev"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def planned_annual_incremental_capacity_user_input():
    value = xr.DataArray(np.nan, {"PVDev": _subscript_dict["PVDev"]}, ["PVDev"])
    value.loc[["Y2023"]] = 3.33
    value.loc[["Y2024"]] = 4.22
    value.loc[["Y2025"]] = 4.33
    value.loc[["Y2026"]] = 4.55
    value.loc[["Y2027"]] = 5.33
    value.loc[["Y2028"]] = 6.39
    value.loc[["Y2029"]] = 7.55
    value.loc[["Y2030"]] = 7.69
    value.loc[["Y2031"]] = 8.04
    value.loc[["Y2032"]] = 9.26
    value.loc[["Y2033"]] = 10.97
    value.loc[["Y2034"]] = 10.48
    value.loc[["Y2035"]] = 10.69
    value.loc[["Y2036"]] = 11.97
    value.loc[["Y2037"]] = 12.1
    value.loc[["Y2038"]] = 12.57
    value.loc[["Y2039"]] = 14.35
    value.loc[["Y2040"]] = 16.1
    value.loc[["Y2041"]] = 18.73
    value.loc[["Y2042"]] = 18.85
    value.loc[["Y2043"]] = 22.66
    value.loc[["Y2044"]] = 23.63
    value.loc[["Y2045"]] = 22.98
    value.loc[["Y2046"]] = 28.93
    value.loc[["Y2047"]] = 32.67
    value.loc[["Y2048"]] = 32.84
    value.loc[["Y2049"]] = 0
    value.loc[["Y2050"]] = 0
    return value


@component.add(
    name="PV Deployment Initial Incremental User Input",
    units="GWp/year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def pv_deployment_initial_incremental_user_input():
    return 3.84


@component.add(
    name="Current Annual PV Deployment User Input",
    comp_type="Constant",
    comp_subtype="Normal",
)
def current_annual_pv_deployment_user_input():
    return 13.56


@component.add(
    name="Global Stocks User Input", comp_type="Constant", comp_subtype="Normal"
)
def global_stocks_user_input():
    return 7431.73


@component.add(
    name="Weibull PDF Regular Loss ExPV",
    subscripts=["PVDev"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def weibull_pdf_regular_loss_expv():
    value = xr.DataArray(np.nan, {"PVDev": _subscript_dict["PVDev"]}, ["PVDev"])
    value.loc[["Y2023"]] = 0
    value.loc[["Y2024"]] = 1.14589e-08
    value.loc[["Y2025"]] = 4.6437e-07
    value.loc[["Y2026"]] = 3.7324e-06
    value.loc[["Y2027"]] = 1.55503e-05
    value.loc[["Y2028"]] = 4.58141e-05
    value.loc[["Y2029"]] = 0.000109
    value.loc[["Y2030"]] = 0.000225416
    value.loc[["Y2031"]] = 0.000419991
    value.loc[["Y2032"]] = 0.000724122
    value.loc[["Y2033"]] = 0.001175012
    value.loc[["Y2034"]] = 0.001815758
    value.loc[["Y2035"]] = 0.002694991
    value.loc[["Y2036"]] = 0.0038661
    value.loc[["Y2037"]] = 0.005385871
    value.loc[["Y2038"]] = 0.007312366
    value.loc[["Y2039"]] = 0.00970182
    value.loc[["Y2040"]] = 0.012604341
    value.loc[["Y2041"]] = 0.016058261
    value.loc[["Y2042"]] = 0.020083043
    value.loc[["Y2043"]] = 0.024670873
    value.loc[["Y2044"]] = 0.029777319
    value.loc[["Y2045"]] = 0.035311818
    value.loc[["Y2046"]] = 0.041129281
    value.loc[["Y2047"]] = 0.047024564
    value.loc[["Y2048"]] = 0.052732091
    value.loc[["Y2049"]] = 0.057933068
    value.loc[["Y2050"]] = 0.062272547
    return value


@component.add(
    name="Annual Dismantled Existing PV",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "existing_pv_recycling_estimation_method": 1,
        "dismantled_expv": 2,
        "average_existing_pv_lifetime": 1,
    },
)
def annual_dismantled_existing_pv():
    return if_then_else(
        existing_pv_recycling_estimation_method() == 1,
        lambda: not_implemented_function(
            "delay",
            float(dismantled_expv().loc["Y2023"]),
            average_existing_pv_lifetime() - 1,
            0,
        ),
        lambda: sum(dismantled_expv(), dim=[]),
    )


@component.add(
    name="Recycling - Annual ExPV",
    subscripts=["StudyPeriod"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "material_intensity_input_method": 1,
        "expv_material_intensity_annual": 1,
        "expv_installed": 2,
        "expv_material_intensity_constant": 1,
    },
)
def recycling_annual_expv():
    return xr.DataArray(
        if_then_else(
            material_intensity_input_method() == 1,
            lambda: expv_installed() * expv_material_intensity_annual(),
            lambda: expv_installed() * expv_material_intensity_constant(),
        ),
        {"StudyPeriod": _subscript_dict["StudyPeriod"]},
        ["StudyPeriod"],
    )


@component.add(
    name="Existing PV Recycling Estimation Method",
    comp_type="Constant",
    comp_subtype="Normal",
)
def existing_pv_recycling_estimation_method():
    """
    1: Fixed Lifetime
    2: Weibull Early Loss
    3: Weibull Regular Loss
    """
    return 1


@component.add(
    name="Weibull PDF Early Loss ExPV",
    subscripts=["PVDev"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def weibull_pdf_early_loss_expv():
    value = xr.DataArray(np.nan, {"PVDev": _subscript_dict["PVDev"]}, ["PVDev"])
    value.loc[["Y2023"]] = 0
    value.loc[["Y2024"]] = 0.0002079
    value.loc[["Y2025"]] = 0.0009616
    value.loc[["Y2026"]] = 0.0020405
    value.loc[["Y2027"]] = 0.0033548
    value.loc[["Y2028"]] = 0.004857
    value.loc[["Y2029"]] = 0.0065125
    value.loc[["Y2030"]] = 0.0082919
    value.loc[["Y2031"]] = 0.0101678
    value.loc[["Y2032"]] = 0.0121142
    value.loc[["Y2033"]] = 0.0141052
    value.loc[["Y2034"]] = 0.016115
    value.loc[["Y2035"]] = 0.0181181
    value.loc[["Y2036"]] = 0.020089
    value.loc[["Y2037"]] = 0.0220029
    value.loc[["Y2038"]] = 0.0238356
    value.loc[["Y2039"]] = 0.025564
    value.loc[["Y2040"]] = 0.0271664
    value.loc[["Y2041"]] = 0.028623
    value.loc[["Y2042"]] = 0.0299159
    value.loc[["Y2043"]] = 0.0310297
    value.loc[["Y2044"]] = 0.0319518
    value.loc[["Y2045"]] = 0.0326725
    value.loc[["Y2046"]] = 0.033185
    value.loc[["Y2047"]] = 0.0334859
    value.loc[["Y2048"]] = 0.033575
    value.loc[["Y2049"]] = 0.0334553
    value.loc[["Y2050"]] = 0.033133
    return value


@component.add(
    name="Average Existing PV Lifetime", comp_type="Constant", comp_subtype="Normal"
)
def average_existing_pv_lifetime():
    return 25


@component.add(
    name="Recycling Efficiency ExPV",
    units="%",
    comp_type="Constant",
    comp_subtype="Normal",
)
def recycling_efficiency_expv():
    return 90


@component.add(
    name="Collection efficiency ExPV",
    units="%",
    comp_type="Constant",
    comp_subtype="Normal",
)
def collection_efficiency_expv():
    return 0.9


@component.add(
    name="Percentage Panels Recycled ExPV",
    units="%",
    comp_type="Constant",
    comp_subtype="Normal",
)
def percentage_panels_recycled_expv():
    return 100


@component.add(
    name="ExPV Material Intensity Annual",
    subscripts=["PVDev"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def expv_material_intensity_annual():
    value = xr.DataArray(np.nan, {"PVDev": _subscript_dict["PVDev"]}, ["PVDev"])
    value.loc[["Y2023"]] = 0
    value.loc[["Y2024"]] = 0
    value.loc[["Y2025"]] = 0
    value.loc[["Y2026"]] = 0
    value.loc[["Y2027"]] = 0
    value.loc[["Y2028"]] = 0
    value.loc[["Y2029"]] = 0
    value.loc[["Y2030"]] = 0
    value.loc[["Y2031"]] = 0
    value.loc[["Y2032"]] = 0
    value.loc[["Y2033"]] = 0
    value.loc[["Y2034"]] = 0
    value.loc[["Y2035"]] = 0
    value.loc[["Y2036"]] = 0
    value.loc[["Y2037"]] = 0
    value.loc[["Y2038"]] = 0
    value.loc[["Y2039"]] = 0
    value.loc[["Y2040"]] = 0
    value.loc[["Y2041"]] = 0
    value.loc[["Y2042"]] = 0
    value.loc[["Y2043"]] = 0
    value.loc[["Y2044"]] = 0
    value.loc[["Y2045"]] = 0
    value.loc[["Y2046"]] = 0
    value.loc[["Y2047"]] = 0
    value.loc[["Y2048"]] = 0
    value.loc[["Y2049"]] = 0
    value.loc[["Y2050"]] = 0
    return value


@component.add(
    name="ExPV Installed",
    subscripts=["PVDev"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def expv_installed():
    value = xr.DataArray(np.nan, {"PVDev": _subscript_dict["PVDev"]}, ["PVDev"])
    value.loc[["Y2023"]] = 0
    value.loc[["Y2024"]] = 0
    value.loc[["Y2025"]] = 0
    value.loc[["Y2026"]] = 0
    value.loc[["Y2027"]] = 0
    value.loc[["Y2028"]] = 0
    value.loc[["Y2029"]] = 0
    value.loc[["Y2030"]] = 0
    value.loc[["Y2031"]] = 0
    value.loc[["Y2032"]] = 0
    value.loc[["Y2033"]] = 0
    value.loc[["Y2034"]] = 0
    value.loc[["Y2035"]] = 0
    value.loc[["Y2036"]] = 0
    value.loc[["Y2037"]] = 0
    value.loc[["Y2038"]] = 0
    value.loc[["Y2039"]] = 0
    value.loc[["Y2040"]] = 0
    value.loc[["Y2041"]] = 0
    value.loc[["Y2042"]] = 0
    value.loc[["Y2043"]] = 0
    value.loc[["Y2044"]] = 0
    value.loc[["Y2045"]] = 0
    value.loc[["Y2046"]] = 0
    value.loc[["Y2047"]] = 0
    value.loc[["Y2048"]] = 0
    value.loc[["Y2049"]] = 0
    value.loc[["Y2050"]] = 0
    return value


@component.add(
    name="ExPV Material Intensity Constant", comp_type="Constant", comp_subtype="Normal"
)
def expv_material_intensity_constant():
    return 0


@component.add(
    name="Material Intensity Input Method", comp_type="Constant", comp_subtype="Normal"
)
def material_intensity_input_method():
    """
    1: Annual Input
    2: Constant value
    """
    return 1


@component.add(
    name="Recycled Material Flows User Input",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def recycled_material_flows_user_input():
    return np.interp(
        time(),
        [
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
    )


@component.add(
    name="Recycled Material Flows Estmation Method",
    comp_type="Constant",
    comp_subtype="Normal",
)
def recycled_material_flows_estmation_method():
    """
    1: Calculation using the dashboard
    2: Manual User Input (Calculated by the user outside the dashboard)
    """
    return 1


@component.add(name="Current nonPV demand", comp_type="Constant", comp_subtype="Normal")
def current_nonpv_demand():
    return 348


@component.add(
    name="d yield avg", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def d_yield_avg():
    return 1


@component.add(
    name="Effect on Material byproduction Yield avg",
    units="untiless",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "price_yield_eq_degree_avg": 2,
        "b_yield_avg": 3,
        "a_yield_avg": 3,
        "material_price": 6,
        "d_yield_avg": 1,
        "c_yield_avg": 2,
    },
)
def effect_on_material_byproduction_yield_avg():
    return if_then_else(
        price_yield_eq_degree_avg() == 1,
        lambda: a_yield_avg() * material_price() + b_yield_avg(),
        lambda: if_then_else(
            price_yield_eq_degree_avg() == 2,
            lambda: a_yield_avg() * material_price() ** 2
            + b_yield_avg() * material_price()
            + c_yield_avg(),
            lambda: a_yield_avg() * material_price() ** 3
            + b_yield_avg() * material_price() ** 2
            + c_yield_avg() * material_price()
            + d_yield_avg(),
        ),
    )


@component.add(
    name="price yield avg delay",
    units="Years",
    comp_type="Constant",
    comp_subtype="Normal",
)
def price_yield_avg_delay():
    return 5


@component.add(
    name="a yield avg", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def a_yield_avg():
    return 0.0023


@component.add(
    name="Price Yield Eq degree avg",
    units="unitless",
    comp_type="Constant",
    comp_subtype="Normal",
)
def price_yield_eq_degree_avg():
    return 1


@component.add(
    name="c yield avg", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def c_yield_avg():
    return 1


@component.add(
    name="b yield avg", units="unitless", comp_type="Constant", comp_subtype="Normal"
)
def b_yield_avg():
    return 1


@component.add(
    name="Delayed yield avg Effect",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_on_material_byproduction_yield_avg": 1,
        "price_yield_avg_delay": 1,
    },
)
def delayed_yield_avg_effect():
    return not_implemented_function(
        "delay", effect_on_material_byproduction_yield_avg(), price_yield_avg_delay(), 1
    )


@component.add(
    name="Annual Recycled metalX",
    units="Tons/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_dismantled_pv": 1,
        "collection_efficiency": 1,
        "percentage_panels_recycled": 1,
        "recycling_efficiency": 1,
    },
)
def annual_recycled_metalx():
    return np.maximum(
        annual_dismantled_pv()
        * collection_efficiency()
        * percentage_panels_recycled()
        * recycling_efficiency()
        / 1000000,
        0,
    )


@component.add(
    name="Yearly PV Industry Demand",
    units="Metric Tons/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pv_technology_production_capacity": 1,
        "pv_technology_material_intensity": 1,
    },
)
def yearly_pv_industry_demand():
    return np.maximum(
        (pv_technology_production_capacity() * 1000000000)
        * pv_technology_material_intensity()
        / 1000,
        0,
    )


@component.add(
    name="Yearly NonPV Industry Demand Annual Growth",
    units="Tons/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_non_pv_demand": 1, "npvgr": 1},
)
def yearly_nonpv_industry_demand_annual_growth():
    return np.maximum(annual_non_pv_demand() * (npvgr() / 100), 0)


@component.add(
    name="Material Production Annual",
    units="Metric Tons/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "recycled_material_flows_estmation_method": 1,
        "total_annual_supply_from_byproduction": 2,
        "total_annual_recycling_supply_from_existing_pv": 1,
        "total_annual_recycling_supply_from_new_pv": 2,
        "total_annual_supply_from_direct_mining": 2,
        "recycled_material_flows_user_input": 1,
    },
)
def material_production_annual():
    return np.maximum(
        if_then_else(
            recycled_material_flows_estmation_method() == 1,
            lambda: total_annual_supply_from_byproduction()
            + total_annual_recycling_supply_from_new_pv()
            + total_annual_recycling_supply_from_existing_pv()
            + total_annual_supply_from_direct_mining(),
            lambda: total_annual_supply_from_byproduction()
            + total_annual_recycling_supply_from_new_pv()
            + recycled_material_flows_user_input()
            + total_annual_supply_from_direct_mining(),
        ),
        0,
    )


@component.add(
    name="Material in the market (positive)",
    units="Metric Tons/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"material_production_annual": 2, "annual_material_demand": 2},
)
def material_in_the_market_positive():
    return np.maximum(
        if_then_else(
            material_production_annual() - annual_material_demand() < 0,
            lambda: 0,
            lambda: material_production_annual() - annual_material_demand(),
        ),
        0,
    )


@component.add(
    name="Material in the market (negative)",
    units="Metric Tons/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"material_production_annual": 2, "annual_material_demand": 2},
)
def material_in_the_market_negative():
    return np.maximum(
        if_then_else(
            material_production_annual() - annual_material_demand() > 0,
            lambda: 0,
            lambda: -material_production_annual() + annual_material_demand(),
        ),
        0,
    )


@component.add(name="OP", units="$/W/Year", comp_type="Constant", comp_subtype="Normal")
def op():
    return np.maximum(0, 0)


@component.add(
    name="Price in",
    units="$/W/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"material_cost_per_watt": 1},
)
def price_in():
    return np.maximum(material_cost_per_watt(), 0)


@component.add(
    name="Material Price pos",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"change_in_material_price": 2},
)
def material_price_pos():
    return np.maximum(
        if_then_else(
            change_in_material_price() > 0,
            lambda: change_in_material_price(),
            lambda: 0,
        ),
        0,
    )


@component.add(
    name="Material Price neg",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"change_in_material_price": 2},
)
def material_price_neg():
    return np.maximum(
        if_then_else(
            change_in_material_price() < 0,
            lambda: -change_in_material_price(),
            lambda: 0,
        ),
        0,
    )


@component.add(
    name="Annual Capacity Incremental",
    units="GWp/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pv_future_production_user_input": 1,
        "condition": 2,
        "pv_deployment_initial_incremental": 1,
        "counter_result": 54,
        "planned_annual_incremental_capacity": 28,
        "planned_annual_incremental_capacity_user_input": 28,
        "pv_deployment_initial_incremental_user_input": 1,
    },
)
def annual_capacity_incremental():
    return np.maximum(
        if_then_else(
            pv_future_production_user_input() == 1,
            lambda: not_implemented_function(
                "delay",
                if_then_else(
                    condition() == 0,
                    lambda: if_then_else(
                        counter_result() == 1,
                        lambda: float(
                            planned_annual_incremental_capacity().loc["Y2023"]
                        ),
                        lambda: if_then_else(
                            counter_result() == 2,
                            lambda: float(
                                planned_annual_incremental_capacity().loc["Y2024"]
                            ),
                            lambda: if_then_else(
                                counter_result() == 3,
                                lambda: float(
                                    planned_annual_incremental_capacity().loc["Y2025"]
                                ),
                                lambda: if_then_else(
                                    counter_result() == 4,
                                    lambda: float(
                                        planned_annual_incremental_capacity().loc[
                                            "Y2026"
                                        ]
                                    ),
                                    lambda: if_then_else(
                                        counter_result() == 5,
                                        lambda: float(
                                            planned_annual_incremental_capacity().loc[
                                                "Y2027"
                                            ]
                                        ),
                                        lambda: if_then_else(
                                            counter_result() == 6,
                                            lambda: float(
                                                planned_annual_incremental_capacity().loc[
                                                    "Y2028"
                                                ]
                                            ),
                                            lambda: if_then_else(
                                                counter_result() == 7,
                                                lambda: float(
                                                    planned_annual_incremental_capacity().loc[
                                                        "Y2029"
                                                    ]
                                                ),
                                                lambda: if_then_else(
                                                    counter_result() == 8,
                                                    lambda: float(
                                                        planned_annual_incremental_capacity().loc[
                                                            "Y2030"
                                                        ]
                                                    ),
                                                    lambda: if_then_else(
                                                        counter_result() == 9,
                                                        lambda: float(
                                                            planned_annual_incremental_capacity().loc[
                                                                "Y2031"
                                                            ]
                                                        ),
                                                        lambda: if_then_else(
                                                            counter_result() == 10,
                                                            lambda: float(
                                                                planned_annual_incremental_capacity().loc[
                                                                    "Y2032"
                                                                ]
                                                            ),
                                                            lambda: if_then_else(
                                                                counter_result() == 11,
                                                                lambda: float(
                                                                    planned_annual_incremental_capacity().loc[
                                                                        "Y2033"
                                                                    ]
                                                                ),
                                                                lambda: if_then_else(
                                                                    counter_result()
                                                                    == 12,
                                                                    lambda: float(
                                                                        planned_annual_incremental_capacity().loc[
                                                                            "Y2034"
                                                                        ]
                                                                    ),
                                                                    lambda: if_then_else(
                                                                        counter_result()
                                                                        == 13,
                                                                        lambda: float(
                                                                            planned_annual_incremental_capacity().loc[
                                                                                "Y2035"
                                                                            ]
                                                                        ),
                                                                        lambda: if_then_else(
                                                                            counter_result()
                                                                            == 14,
                                                                            lambda: float(
                                                                                planned_annual_incremental_capacity().loc[
                                                                                    "Y2036"
                                                                                ]
                                                                            ),
                                                                            lambda: if_then_else(
                                                                                counter_result()
                                                                                == 15,
                                                                                lambda: float(
                                                                                    planned_annual_incremental_capacity().loc[
                                                                                        "Y2037"
                                                                                    ]
                                                                                ),
                                                                                lambda: if_then_else(
                                                                                    counter_result()
                                                                                    == 16,
                                                                                    lambda: float(
                                                                                        planned_annual_incremental_capacity().loc[
                                                                                            "Y2038"
                                                                                        ]
                                                                                    ),
                                                                                    lambda: if_then_else(
                                                                                        counter_result()
                                                                                        == 17,
                                                                                        lambda: float(
                                                                                            planned_annual_incremental_capacity().loc[
                                                                                                "Y2039"
                                                                                            ]
                                                                                        ),
                                                                                        lambda: if_then_else(
                                                                                            counter_result()
                                                                                            == 18,
                                                                                            lambda: float(
                                                                                                planned_annual_incremental_capacity().loc[
                                                                                                    "Y2040"
                                                                                                ]
                                                                                            ),
                                                                                            lambda: if_then_else(
                                                                                                counter_result()
                                                                                                == 19,
                                                                                                lambda: float(
                                                                                                    planned_annual_incremental_capacity().loc[
                                                                                                        "Y2041"
                                                                                                    ]
                                                                                                ),
                                                                                                lambda: if_then_else(
                                                                                                    counter_result()
                                                                                                    == 20,
                                                                                                    lambda: float(
                                                                                                        planned_annual_incremental_capacity().loc[
                                                                                                            "Y2042"
                                                                                                        ]
                                                                                                    ),
                                                                                                    lambda: if_then_else(
                                                                                                        counter_result()
                                                                                                        == 21,
                                                                                                        lambda: float(
                                                                                                            planned_annual_incremental_capacity().loc[
                                                                                                                "Y2043"
                                                                                                            ]
                                                                                                        ),
                                                                                                        lambda: if_then_else(
                                                                                                            counter_result()
                                                                                                            == 22,
                                                                                                            lambda: float(
                                                                                                                planned_annual_incremental_capacity().loc[
                                                                                                                    "Y2044"
                                                                                                                ]
                                                                                                            ),
                                                                                                            lambda: if_then_else(
                                                                                                                counter_result()
                                                                                                                == 23,
                                                                                                                lambda: float(
                                                                                                                    planned_annual_incremental_capacity().loc[
                                                                                                                        "Y2045"
                                                                                                                    ]
                                                                                                                ),
                                                                                                                lambda: if_then_else(
                                                                                                                    counter_result()
                                                                                                                    == 24,
                                                                                                                    lambda: float(
                                                                                                                        planned_annual_incremental_capacity().loc[
                                                                                                                            "Y2046"
                                                                                                                        ]
                                                                                                                    ),
                                                                                                                    lambda: if_then_else(
                                                                                                                        counter_result()
                                                                                                                        == 25,
                                                                                                                        lambda: float(
                                                                                                                            planned_annual_incremental_capacity().loc[
                                                                                                                                "Y2047"
                                                                                                                            ]
                                                                                                                        ),
                                                                                                                        lambda: if_then_else(
                                                                                                                            counter_result()
                                                                                                                            == 26,
                                                                                                                            lambda: float(
                                                                                                                                planned_annual_incremental_capacity().loc[
                                                                                                                                    "Y2048"
                                                                                                                                ]
                                                                                                                            ),
                                                                                                                            lambda: if_then_else(
                                                                                                                                counter_result()
                                                                                                                                == 27,
                                                                                                                                lambda: float(
                                                                                                                                    planned_annual_incremental_capacity().loc[
                                                                                                                                        "Y2049"
                                                                                                                                    ]
                                                                                                                                ),
                                                                                                                                lambda: float(
                                                                                                                                    planned_annual_incremental_capacity().loc[
                                                                                                                                        "Y2050"
                                                                                                                                    ]
                                                                                                                                ),
                                                                                                                            ),
                                                                                                                        ),
                                                                                                                    ),
                                                                                                                ),
                                                                                                            ),
                                                                                                        ),
                                                                                                    ),
                                                                                                ),
                                                                                            ),
                                                                                        ),
                                                                                    ),
                                                                                ),
                                                                            ),
                                                                        ),
                                                                    ),
                                                                ),
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                    lambda: 0,
                ),
                0,
                pv_deployment_initial_incremental(),
            ),
            lambda: not_implemented_function(
                "delay",
                if_then_else(
                    condition() == 0,
                    lambda: if_then_else(
                        counter_result() == 1,
                        lambda: float(
                            planned_annual_incremental_capacity_user_input().loc[
                                "Y2023"
                            ]
                        ),
                        lambda: if_then_else(
                            counter_result() == 2,
                            lambda: float(
                                planned_annual_incremental_capacity_user_input().loc[
                                    "Y2024"
                                ]
                            ),
                            lambda: if_then_else(
                                counter_result() == 3,
                                lambda: float(
                                    planned_annual_incremental_capacity_user_input().loc[
                                        "Y2025"
                                    ]
                                ),
                                lambda: if_then_else(
                                    counter_result() == 4,
                                    lambda: float(
                                        planned_annual_incremental_capacity_user_input().loc[
                                            "Y2026"
                                        ]
                                    ),
                                    lambda: if_then_else(
                                        counter_result() == 5,
                                        lambda: float(
                                            planned_annual_incremental_capacity_user_input().loc[
                                                "Y2027"
                                            ]
                                        ),
                                        lambda: if_then_else(
                                            counter_result() == 6,
                                            lambda: float(
                                                planned_annual_incremental_capacity_user_input().loc[
                                                    "Y2028"
                                                ]
                                            ),
                                            lambda: if_then_else(
                                                counter_result() == 7,
                                                lambda: float(
                                                    planned_annual_incremental_capacity_user_input().loc[
                                                        "Y2029"
                                                    ]
                                                ),
                                                lambda: if_then_else(
                                                    counter_result() == 8,
                                                    lambda: float(
                                                        planned_annual_incremental_capacity_user_input().loc[
                                                            "Y2030"
                                                        ]
                                                    ),
                                                    lambda: if_then_else(
                                                        counter_result() == 9,
                                                        lambda: float(
                                                            planned_annual_incremental_capacity_user_input().loc[
                                                                "Y2031"
                                                            ]
                                                        ),
                                                        lambda: if_then_else(
                                                            counter_result() == 10,
                                                            lambda: float(
                                                                planned_annual_incremental_capacity_user_input().loc[
                                                                    "Y2032"
                                                                ]
                                                            ),
                                                            lambda: if_then_else(
                                                                counter_result() == 11,
                                                                lambda: float(
                                                                    planned_annual_incremental_capacity_user_input().loc[
                                                                        "Y2033"
                                                                    ]
                                                                ),
                                                                lambda: if_then_else(
                                                                    counter_result()
                                                                    == 12,
                                                                    lambda: float(
                                                                        planned_annual_incremental_capacity_user_input().loc[
                                                                            "Y2034"
                                                                        ]
                                                                    ),
                                                                    lambda: if_then_else(
                                                                        counter_result()
                                                                        == 13,
                                                                        lambda: float(
                                                                            planned_annual_incremental_capacity_user_input().loc[
                                                                                "Y2035"
                                                                            ]
                                                                        ),
                                                                        lambda: if_then_else(
                                                                            counter_result()
                                                                            == 14,
                                                                            lambda: float(
                                                                                planned_annual_incremental_capacity_user_input().loc[
                                                                                    "Y2036"
                                                                                ]
                                                                            ),
                                                                            lambda: if_then_else(
                                                                                counter_result()
                                                                                == 15,
                                                                                lambda: float(
                                                                                    planned_annual_incremental_capacity_user_input().loc[
                                                                                        "Y2037"
                                                                                    ]
                                                                                ),
                                                                                lambda: if_then_else(
                                                                                    counter_result()
                                                                                    == 16,
                                                                                    lambda: float(
                                                                                        planned_annual_incremental_capacity_user_input().loc[
                                                                                            "Y2038"
                                                                                        ]
                                                                                    ),
                                                                                    lambda: if_then_else(
                                                                                        counter_result()
                                                                                        == 17,
                                                                                        lambda: float(
                                                                                            planned_annual_incremental_capacity_user_input().loc[
                                                                                                "Y2039"
                                                                                            ]
                                                                                        ),
                                                                                        lambda: if_then_else(
                                                                                            counter_result()
                                                                                            == 18,
                                                                                            lambda: float(
                                                                                                planned_annual_incremental_capacity_user_input().loc[
                                                                                                    "Y2040"
                                                                                                ]
                                                                                            ),
                                                                                            lambda: if_then_else(
                                                                                                counter_result()
                                                                                                == 19,
                                                                                                lambda: float(
                                                                                                    planned_annual_incremental_capacity_user_input().loc[
                                                                                                        "Y2041"
                                                                                                    ]
                                                                                                ),
                                                                                                lambda: if_then_else(
                                                                                                    counter_result()
                                                                                                    == 20,
                                                                                                    lambda: float(
                                                                                                        planned_annual_incremental_capacity_user_input().loc[
                                                                                                            "Y2042"
                                                                                                        ]
                                                                                                    ),
                                                                                                    lambda: if_then_else(
                                                                                                        counter_result()
                                                                                                        == 21,
                                                                                                        lambda: float(
                                                                                                            planned_annual_incremental_capacity_user_input().loc[
                                                                                                                "Y2043"
                                                                                                            ]
                                                                                                        ),
                                                                                                        lambda: if_then_else(
                                                                                                            counter_result()
                                                                                                            == 22,
                                                                                                            lambda: float(
                                                                                                                planned_annual_incremental_capacity_user_input().loc[
                                                                                                                    "Y2044"
                                                                                                                ]
                                                                                                            ),
                                                                                                            lambda: if_then_else(
                                                                                                                counter_result()
                                                                                                                == 23,
                                                                                                                lambda: float(
                                                                                                                    planned_annual_incremental_capacity_user_input().loc[
                                                                                                                        "Y2045"
                                                                                                                    ]
                                                                                                                ),
                                                                                                                lambda: if_then_else(
                                                                                                                    counter_result()
                                                                                                                    == 24,
                                                                                                                    lambda: float(
                                                                                                                        planned_annual_incremental_capacity_user_input().loc[
                                                                                                                            "Y2046"
                                                                                                                        ]
                                                                                                                    ),
                                                                                                                    lambda: if_then_else(
                                                                                                                        counter_result()
                                                                                                                        == 25,
                                                                                                                        lambda: float(
                                                                                                                            planned_annual_incremental_capacity_user_input().loc[
                                                                                                                                "Y2047"
                                                                                                                            ]
                                                                                                                        ),
                                                                                                                        lambda: if_then_else(
                                                                                                                            counter_result()
                                                                                                                            == 26,
                                                                                                                            lambda: float(
                                                                                                                                planned_annual_incremental_capacity_user_input().loc[
                                                                                                                                    "Y2048"
                                                                                                                                ]
                                                                                                                            ),
                                                                                                                            lambda: if_then_else(
                                                                                                                                counter_result()
                                                                                                                                == 27,
                                                                                                                                lambda: float(
                                                                                                                                    planned_annual_incremental_capacity_user_input().loc[
                                                                                                                                        "Y2049"
                                                                                                                                    ]
                                                                                                                                ),
                                                                                                                                lambda: float(
                                                                                                                                    planned_annual_incremental_capacity_user_input().loc[
                                                                                                                                        "Y2050"
                                                                                                                                    ]
                                                                                                                                ),
                                                                                                                            ),
                                                                                                                        ),
                                                                                                                    ),
                                                                                                                ),
                                                                                                            ),
                                                                                                        ),
                                                                                                    ),
                                                                                                ),
                                                                                            ),
                                                                                        ),
                                                                                    ),
                                                                                ),
                                                                            ),
                                                                        ),
                                                                    ),
                                                                ),
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                    lambda: 0,
                ),
                0,
                pv_deployment_initial_incremental_user_input(),
            ),
        ),
        0,
    )


@component.add(
    name="Dismantled PV - per production phase",
    subscripts=["StudyPeriod"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "new_pv_recycling_estimation_method": 2,
        "weibull_pdf_early_loss": 1,
        "recycling_annual_pv": 3,
        "weibull_pdf_regular_loss": 1,
    },
)
def dismantled_pv_per_production_phase():
    return xr.DataArray(
        np.maximum(
            if_then_else(
                new_pv_recycling_estimation_method() == 2,
                lambda: recycling_annual_pv() * weibull_pdf_early_loss(),
                lambda: if_then_else(
                    new_pv_recycling_estimation_method() == 3,
                    lambda: recycling_annual_pv() * weibull_pdf_regular_loss(),
                    lambda: not_implemented_function(
                        "delay", recycling_annual_pv(), 25, 0
                    ),
                ),
            ),
            0,
        ),
        {"StudyPeriod": _subscript_dict["StudyPeriod"]},
        ["StudyPeriod"],
    )


@component.add(
    name="yield dummy in",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"delayed_yield_effect": 2, "new_byproduction_yield_factor": 2},
)
def yield_dummy_in():
    return np.maximum(
        if_then_else(
            delayed_yield_effect() < new_byproduction_yield_factor(),
            lambda: new_byproduction_yield_factor(),
            lambda: delayed_yield_effect(),
        ),
        0,
    )


@component.add(
    name="yield dummy out",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"yield_dummy_in": 1},
)
def yield_dummy_out():
    return np.maximum(not_implemented_function("delay", yield_dummy_in(), 1, 1), 0)


@component.add(
    name="Dummy Counter",
    units="Per Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"condition": 1},
)
def dummy_counter():
    return np.maximum(if_then_else(condition() == 0, lambda: 1, lambda: 0), 0)


@component.add(
    name="Actual PV Technology Production",
    units="GWp/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "material_in_the_market_cumulative": 1,
        "annual_material_demand": 1,
        "pv_technology_production_capacity": 3,
        "annual_non_pv_demand": 2,
        "pv_technology_material_intensity": 2,
        "material_production_annual": 2,
    },
)
def actual_pv_technology_production():
    return np.maximum(
        if_then_else(
            material_in_the_market_cumulative() > annual_material_demand(),
            lambda: pv_technology_production_capacity(),
            lambda: if_then_else(
                (material_production_annual() - annual_non_pv_demand())
                * 1000
                / pv_technology_material_intensity()
                > pv_technology_production_capacity(),
                lambda: pv_technology_production_capacity(),
                lambda: (material_production_annual() - annual_non_pv_demand())
                * 1000
                / (pv_technology_material_intensity() / 1000000000),
            ),
        ),
        0,
    )


@component.add(
    name="Actual Annual Material Demand",
    units="Metric Tons/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "actual_pv_technology_production": 1,
        "pv_technology_material_intensity": 1,
    },
)
def actual_annual_material_demand():
    return np.maximum(
        actual_pv_technology_production()
        * 1000000000
        * pv_technology_material_intensity()
        / 1000,
        0,
    )


@component.add(
    name="Annual Production",
    units="Tons/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "direct_mining_current_production_user_input": 1,
        "direct_mining_growth_rate": 1,
    },
)
def annual_production():
    return np.maximum(
        direct_mining_current_production_user_input()
        * direct_mining_growth_rate()
        / 100,
        0,
    )


@component.add(
    name="Annual byProduction",
    units="Tons/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"byproduction_supply_user_input": 1, "byproduction_growth_rate": 1},
)
def annual_byproduction():
    return np.maximum(
        byproduction_supply_user_input() * byproduction_growth_rate() / 100, 0
    )


@component.add(
    name="Host Metal Annual Production",
    units="Tons/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"host_metal_production_at_y0": 1, "host_metal_mining_growth_rate": 1},
)
def host_metal_annual_production():
    return np.maximum(
        host_metal_production_at_y0() * host_metal_mining_growth_rate() / 100, 0
    )


@component.add(
    name="Host Metal 2 Annual Production",
    units="Tons/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "host_metal_2_production_at_y0": 1,
        "host_metal_2_mining_growth_rate": 1,
    },
)
def host_metal_2_annual_production():
    return np.maximum(
        host_metal_2_production_at_y0() * host_metal_2_mining_growth_rate() / 100, 0
    )


@component.add(
    name="Host Metal 3 Annual Production",
    units="Tons/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "host_metal_3_production_at_y0": 1,
        "host_metal_3_mining_growth_rate": 1,
    },
)
def host_metal_3_annual_production():
    return np.maximum(
        host_metal_3_production_at_y0() * host_metal_3_mining_growth_rate() / 100, 0
    )


@component.add(
    name="DMGR dummy in",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"delayed_dmgr_effect": 2, "new_dmgr_factor": 2},
)
def dmgr_dummy_in():
    return np.maximum(
        if_then_else(
            delayed_dmgr_effect() < new_dmgr_factor(),
            lambda: new_dmgr_factor(),
            lambda: delayed_dmgr_effect(),
        ),
        0,
    )


@component.add(
    name="DMGR dummy out",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dmgr_dummy_in": 1},
)
def dmgr_dummy_out():
    return np.maximum(not_implemented_function("delay", dmgr_dummy_in(), 1, 1), 0)


@component.add(
    name="Dismantled ExPV",
    subscripts=["StudyPeriod"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "existing_pv_recycling_estimation_method": 2,
        "weibull_pdf_early_loss_expv": 1,
        "recycling_annual_expv": 3,
        "weibull_pdf_regular_loss_expv": 1,
    },
)
def dismantled_expv():
    return xr.DataArray(
        np.maximum(
            if_then_else(
                existing_pv_recycling_estimation_method() == 2,
                lambda: recycling_annual_expv() * weibull_pdf_early_loss_expv(),
                lambda: if_then_else(
                    existing_pv_recycling_estimation_method() == 3,
                    lambda: recycling_annual_expv() * weibull_pdf_regular_loss_expv(),
                    lambda: not_implemented_function(
                        "delay", recycling_annual_expv(), 25, 0
                    ),
                ),
            ),
            0,
        ),
        {"StudyPeriod": _subscript_dict["StudyPeriod"]},
        ["StudyPeriod"],
    )


@component.add(
    name="Total Annual Recycling Supply from existing PV",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_dismantled_existing_pv": 1,
        "collection_efficiency_expv": 1,
        "percentage_panels_recycled_expv": 1,
        "recycling_efficiency_expv": 1,
    },
)
def total_annual_recycling_supply_from_existing_pv():
    return np.maximum(
        annual_dismantled_existing_pv()
        * collection_efficiency_expv()
        * percentage_panels_recycled_expv()
        * recycling_efficiency_expv()
        / 10000,
        0,
    )


@component.add(
    name="yield avg dummy in",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"delayed_yield_avg_effect": 2, "new_byproduction_yield_avg_factor": 2},
)
def yield_avg_dummy_in():
    return np.maximum(
        if_then_else(
            delayed_yield_avg_effect() < new_byproduction_yield_avg_factor(),
            lambda: new_byproduction_yield_avg_factor(),
            lambda: delayed_yield_avg_effect(),
        ),
        0,
    )


@component.add(
    name="yield avg dummy out",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"yield_avg_dummy_in": 1},
)
def yield_avg_dummy_out():
    return np.maximum(not_implemented_function("delay", yield_avg_dummy_in(), 1, 1), 0)


@component.add(
    name="Cumulative Recycled metalX",
    units="Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_recycled_metalx": 1},
    other_deps={
        "_integ_cumulative_recycled_metalx": {
            "initial": {"annual_recycled_metalx": 1},
            "step": {"annual_recycled_metalx": 1},
        }
    },
)
def cumulative_recycled_metalx():
    return _integ_cumulative_recycled_metalx()


_integ_cumulative_recycled_metalx = NonNegativeInteg(
    lambda: annual_recycled_metalx(),
    lambda: annual_recycled_metalx(),
    "_integ_cumulative_recycled_metalx",
)


@component.add(
    name="Annual Non PV Demand",
    units="Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_annual_non_pv_demand": 1},
    other_deps={
        "_integ_annual_non_pv_demand": {
            "initial": {"current_nonpv_demand": 1},
            "step": {"yearly_nonpv_industry_demand_annual_growth": 1},
        }
    },
)
def annual_non_pv_demand():
    return _integ_annual_non_pv_demand()


_integ_annual_non_pv_demand = NonNegativeInteg(
    lambda: yearly_nonpv_industry_demand_annual_growth(),
    lambda: current_nonpv_demand(),
    "_integ_annual_non_pv_demand",
)


@component.add(
    name="Material Production - Cumulative",
    units="Metric Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_material_production_cumulative": 1},
    other_deps={
        "_integ_material_production_cumulative": {
            "initial": {},
            "step": {"material_production_annual": 1},
        }
    },
)
def material_production_cumulative():
    return _integ_material_production_cumulative()


_integ_material_production_cumulative = NonNegativeInteg(
    lambda: material_production_annual(),
    lambda: 0,
    "_integ_material_production_cumulative",
)


@component.add(
    name="Material in the market Cumulative",
    units="Metric Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_material_in_the_market_cumulative": 1},
    other_deps={
        "_integ_material_in_the_market_cumulative": {
            "initial": {"global_stocks_user_input": 1},
            "step": {
                "material_in_the_market_positive": 1,
                "material_in_the_market_negative": 1,
            },
        }
    },
)
def material_in_the_market_cumulative():
    return _integ_material_in_the_market_cumulative()


_integ_material_in_the_market_cumulative = NonNegativeInteg(
    lambda: material_in_the_market_positive() - material_in_the_market_negative(),
    lambda: global_stocks_user_input(),
    "_integ_material_in_the_market_cumulative",
)


@component.add(
    name="Material Price Old",
    units="$/W",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_material_price_old": 1},
    other_deps={
        "_integ_material_price_old": {
            "initial": {"price_in": 1},
            "step": {"price_in": 1, "op": 1},
        }
    },
)
def material_price_old():
    return _integ_material_price_old()


_integ_material_price_old = Integ(
    lambda: price_in() - op(), lambda: price_in(), "_integ_material_price_old"
)


@component.add(
    name="Updated PV Technology ASP",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_updated_pv_technology_asp": 1},
    other_deps={
        "_integ_updated_pv_technology_asp": {
            "initial": {"pv_technology_current_asp": 1},
            "step": {"material_price_pos": 1, "material_price_neg": 1},
        }
    },
)
def updated_pv_technology_asp():
    return _integ_updated_pv_technology_asp()


_integ_updated_pv_technology_asp = NonNegativeInteg(
    lambda: material_price_pos() - material_price_neg(),
    lambda: pv_technology_current_asp(),
    "_integ_updated_pv_technology_asp",
)


@component.add(
    name="Annual PV Deployment",
    units="GWp",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_annual_pv_deployment": 1},
    other_deps={
        "_integ_annual_pv_deployment": {
            "initial": {
                "pv_future_production_user_input": 1,
                "current_annual_pv_deployment": 1,
                "current_annual_pv_deployment_user_input": 1,
            },
            "step": {"annual_capacity_incremental": 1},
        }
    },
)
def annual_pv_deployment():
    return _integ_annual_pv_deployment()


_integ_annual_pv_deployment = Integ(
    lambda: annual_capacity_incremental(),
    lambda: if_then_else(
        pv_future_production_user_input() == 1,
        lambda: current_annual_pv_deployment(),
        lambda: current_annual_pv_deployment_user_input(),
    ),
    "_integ_annual_pv_deployment",
)


@component.add(
    name="Cumulative PV Technology Material Demand",
    units="Metric Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_pv_technology_material_demand": 1},
    other_deps={
        "_integ_cumulative_pv_technology_material_demand": {
            "initial": {},
            "step": {"yearly_pv_industry_demand": 1},
        }
    },
)
def cumulative_pv_technology_material_demand():
    return _integ_cumulative_pv_technology_material_demand()


_integ_cumulative_pv_technology_material_demand = Integ(
    lambda: yearly_pv_industry_demand(),
    lambda: 0,
    "_integ_cumulative_pv_technology_material_demand",
)


@component.add(
    name="New byproduction yield factor",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_new_byproduction_yield_factor": 1},
    other_deps={
        "_integ_new_byproduction_yield_factor": {
            "initial": {},
            "step": {"yield_dummy_in": 1, "yield_dummy_out": 1},
        }
    },
)
def new_byproduction_yield_factor():
    return _integ_new_byproduction_yield_factor()


_integ_new_byproduction_yield_factor = NonNegativeInteg(
    lambda: yield_dummy_in() - yield_dummy_out(),
    lambda: not_implemented_function("delay", 0, 0, 1),
    "_integ_new_byproduction_yield_factor",
)


@component.add(
    name="Counter Result",
    units="unitless",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_counter_result": 1},
    other_deps={"_integ_counter_result": {"initial": {}, "step": {"dummy_counter": 1}}},
)
def counter_result():
    return _integ_counter_result()


_integ_counter_result = NonNegativeInteg(
    lambda: dummy_counter(), lambda: 1, "_integ_counter_result"
)


@component.add(
    name="Cumulative PV Technology Produced",
    units="GWp",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_pv_technology_produced": 1},
    other_deps={
        "_integ_cumulative_pv_technology_produced": {
            "initial": {},
            "step": {"actual_pv_technology_production": 1},
        }
    },
)
def cumulative_pv_technology_produced():
    return _integ_cumulative_pv_technology_produced()


_integ_cumulative_pv_technology_produced = NonNegativeInteg(
    lambda: actual_pv_technology_production(),
    lambda: 0,
    "_integ_cumulative_pv_technology_produced",
)


@component.add(
    name="Cumulative Material Demand (Actual)",
    units="Metric Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_material_demand_actual": 1},
    other_deps={
        "_integ_cumulative_material_demand_actual": {
            "initial": {},
            "step": {"actual_annual_material_demand": 1},
        }
    },
)
def cumulative_material_demand_actual():
    return _integ_cumulative_material_demand_actual()


_integ_cumulative_material_demand_actual = NonNegativeInteg(
    lambda: actual_annual_material_demand(),
    lambda: 0,
    "_integ_cumulative_material_demand_actual",
)


@component.add(
    name="Direct mining current production User Input",
    units="Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_direct_mining_current_production_user_input": 1},
    other_deps={
        "_integ_direct_mining_current_production_user_input": {
            "initial": {},
            "step": {"annual_production": 1},
        }
    },
)
def direct_mining_current_production_user_input():
    return _integ_direct_mining_current_production_user_input()


_integ_direct_mining_current_production_user_input = NonNegativeInteg(
    lambda: annual_production(),
    lambda: 100,
    "_integ_direct_mining_current_production_user_input",
)


@component.add(
    name="Direct Mining Reserves User Input",
    units="Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_direct_mining_reserves_user_input": 1},
    other_deps={
        "_integ_direct_mining_reserves_user_input": {
            "initial": {},
            "step": {"annual_production": 1},
        }
    },
)
def direct_mining_reserves_user_input():
    return _integ_direct_mining_reserves_user_input()


_integ_direct_mining_reserves_user_input = NonNegativeInteg(
    lambda: -annual_production(),
    lambda: 1000000,
    "_integ_direct_mining_reserves_user_input",
)


@component.add(
    name="byproduction supply User Input",
    units="Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_byproduction_supply_user_input": 1},
    other_deps={
        "_integ_byproduction_supply_user_input": {
            "initial": {},
            "step": {"annual_byproduction": 1},
        }
    },
)
def byproduction_supply_user_input():
    return _integ_byproduction_supply_user_input()


_integ_byproduction_supply_user_input = NonNegativeInteg(
    lambda: annual_byproduction(), lambda: 100, "_integ_byproduction_supply_user_input"
)


@component.add(
    name="Hitchhiker metal Reserves User Input",
    units="Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_hitchhiker_metal_reserves_user_input": 1},
    other_deps={
        "_integ_hitchhiker_metal_reserves_user_input": {
            "initial": {},
            "step": {"annual_byproduction": 1},
        }
    },
)
def hitchhiker_metal_reserves_user_input():
    return _integ_hitchhiker_metal_reserves_user_input()


_integ_hitchhiker_metal_reserves_user_input = NonNegativeInteg(
    lambda: -annual_byproduction(),
    lambda: 1000000,
    "_integ_hitchhiker_metal_reserves_user_input",
)


@component.add(
    name="Host Metal Production at y0",
    units="Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_host_metal_production_at_y0": 1},
    other_deps={
        "_integ_host_metal_production_at_y0": {
            "initial": {},
            "step": {"host_metal_annual_production": 1},
        }
    },
)
def host_metal_production_at_y0():
    return _integ_host_metal_production_at_y0()


_integ_host_metal_production_at_y0 = NonNegativeInteg(
    lambda: host_metal_annual_production(),
    lambda: 100,
    "_integ_host_metal_production_at_y0",
)


@component.add(
    name="Host metal Reserves User Input",
    units="Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_host_metal_reserves_user_input": 1},
    other_deps={
        "_integ_host_metal_reserves_user_input": {
            "initial": {},
            "step": {"host_metal_annual_production": 1},
        }
    },
)
def host_metal_reserves_user_input():
    return _integ_host_metal_reserves_user_input()


_integ_host_metal_reserves_user_input = NonNegativeInteg(
    lambda: -host_metal_annual_production(),
    lambda: 1000000,
    "_integ_host_metal_reserves_user_input",
)


@component.add(
    name="Host Metal 2 Production at y0",
    units="Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_host_metal_2_production_at_y0": 1},
    other_deps={
        "_integ_host_metal_2_production_at_y0": {
            "initial": {},
            "step": {"host_metal_2_annual_production": 1},
        }
    },
)
def host_metal_2_production_at_y0():
    return _integ_host_metal_2_production_at_y0()


_integ_host_metal_2_production_at_y0 = NonNegativeInteg(
    lambda: host_metal_2_annual_production(),
    lambda: 100,
    "_integ_host_metal_2_production_at_y0",
)


@component.add(
    name="Host metal 2 Reserves User Input",
    units="Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_host_metal_2_reserves_user_input": 1},
    other_deps={
        "_integ_host_metal_2_reserves_user_input": {
            "initial": {},
            "step": {"host_metal_2_annual_production": 1},
        }
    },
)
def host_metal_2_reserves_user_input():
    return _integ_host_metal_2_reserves_user_input()


_integ_host_metal_2_reserves_user_input = NonNegativeInteg(
    lambda: -host_metal_2_annual_production(),
    lambda: 1000000,
    "_integ_host_metal_2_reserves_user_input",
)


@component.add(
    name="Host Metal 3 Production at y0",
    units="Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_host_metal_3_production_at_y0": 1},
    other_deps={
        "_integ_host_metal_3_production_at_y0": {
            "initial": {},
            "step": {"host_metal_3_annual_production": 1},
        }
    },
)
def host_metal_3_production_at_y0():
    return _integ_host_metal_3_production_at_y0()


_integ_host_metal_3_production_at_y0 = NonNegativeInteg(
    lambda: host_metal_3_annual_production(),
    lambda: 100,
    "_integ_host_metal_3_production_at_y0",
)


@component.add(
    name="Host metal 3 Reserves User Input",
    units="Tons",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_host_metal_3_reserves_user_input": 1},
    other_deps={
        "_integ_host_metal_3_reserves_user_input": {
            "initial": {},
            "step": {"host_metal_3_annual_production": 1},
        }
    },
)
def host_metal_3_reserves_user_input():
    return _integ_host_metal_3_reserves_user_input()


_integ_host_metal_3_reserves_user_input = NonNegativeInteg(
    lambda: -host_metal_3_annual_production(),
    lambda: 1000000,
    "_integ_host_metal_3_reserves_user_input",
)


@component.add(
    name="New DMGR factor",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_new_dmgr_factor": 1},
    other_deps={
        "_integ_new_dmgr_factor": {
            "initial": {},
            "step": {"dmgr_dummy_in": 1, "dmgr_dummy_out": 1},
        }
    },
)
def new_dmgr_factor():
    return _integ_new_dmgr_factor()


_integ_new_dmgr_factor = NonNegativeInteg(
    lambda: dmgr_dummy_in() - dmgr_dummy_out(),
    lambda: not_implemented_function("delay", 0, 0, 1),
    "_integ_new_dmgr_factor",
)


@component.add(
    name="Cumulative Recycled metalX ExPV",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_recycled_metalx_expv": 1},
    other_deps={
        "_integ_cumulative_recycled_metalx_expv": {
            "initial": {"total_annual_recycling_supply_from_existing_pv": 1},
            "step": {"total_annual_recycling_supply_from_existing_pv": 1},
        }
    },
)
def cumulative_recycled_metalx_expv():
    return _integ_cumulative_recycled_metalx_expv()


_integ_cumulative_recycled_metalx_expv = NonNegativeInteg(
    lambda: total_annual_recycling_supply_from_existing_pv(),
    lambda: total_annual_recycling_supply_from_existing_pv(),
    "_integ_cumulative_recycled_metalx_expv",
)


@component.add(
    name="New byproduction yield avg factor",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_new_byproduction_yield_avg_factor": 1},
    other_deps={
        "_integ_new_byproduction_yield_avg_factor": {
            "initial": {},
            "step": {"yield_avg_dummy_in": 1, "yield_avg_dummy_out": 1},
        }
    },
)
def new_byproduction_yield_avg_factor():
    return _integ_new_byproduction_yield_avg_factor()


_integ_new_byproduction_yield_avg_factor = NonNegativeInteg(
    lambda: yield_avg_dummy_in() - yield_avg_dummy_out(),
    lambda: not_implemented_function("delay", 0, 0, 1),
    "_integ_new_byproduction_yield_avg_factor",
)
