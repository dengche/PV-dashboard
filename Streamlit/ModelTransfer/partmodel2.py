"""
Python model 'partmodel2.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import if_then_else, not_implemented_function, sum
from pysd.py_backend.statefuls import NonNegativeInteg, Integ
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
    depends_on={"pv_technology_market_share": 2},
)
def pv_technology_production_capacity():
    return pv_technology_market_share() * pv_technology_market_share() / 100


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
        "average_pv_lifetime": 1,
        "dismantled_pv_per_production_phase": 2,
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


@component.add(name="Average PV Lifetime", comp_type="Constant", comp_subtype="Normal")
def average_pv_lifetime():
    return 25


@component.add(
    name="Global Stocks User Input", comp_type="Constant", comp_subtype="Normal"
)
def global_stocks_user_input():
    return 7431.73


@component.add(name="Current nonPV demand", comp_type="Constant", comp_subtype="Normal")
def current_nonpv_demand():
    return 348


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
    return np.maximum(
        annual_non_pv_demand() * not_implemented_function("cgrowth", npvgr()), 0
    )


@component.add(
    name="Material Production Annual",
    units="Metric Tons/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def material_production_annual():
    return np.maximum(0, 0)


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
    name="Actual PV Technology Production",
    units="GWp/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "material_in_the_market_cumulative": 1,
        "annual_material_demand": 1,
        "pv_technology_production_capacity": 3,
        "annual_non_pv_demand": 2,
        "material_production_annual": 2,
        "pv_technology_material_intensity": 2,
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
