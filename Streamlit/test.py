"""
Python model 'test.py'
Translated using PySD
"""

from pathlib import Path

from pysd.py_backend.statefuls import DelayFixed
from pysd import Component

__pysd_version__ = "3.13.2"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 1,
    "final_time": lambda: 13,
    "time_step": lambda: 1 / 4,
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
    name="INITIAL TIME", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="FINAL TIME", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="TIME STEP", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


@component.add(
    name="SAVEPER",
    units="Months",
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


@component.add(name="Converter 1", comp_type="Constant", comp_subtype="Normal")
def converter_1():
    return 1


@component.add(
    name="Converter 2",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_converter_2": 1},
    other_deps={"_delayfixed_converter_2": {"initial": {}, "step": {"converter_1": 1}}},
)
def converter_2():
    return _delayfixed_converter_2()


_delayfixed_converter_2 = DelayFixed(
    lambda: converter_1(), lambda: 2, lambda: 0, time_step, "_delayfixed_converter_2"
)
