from time import time_ns

NILS_TO_MILS = 1e-6
MILS_TO_HOURS = 2.77778e-7
MILS_TO_MINS = 1.66667e-5
MILS_TO_SECS = 1e-3

def time_ms() -> float:
    """Return the current time in milliseconds since the Epoch"""
    return ns_to_ms(time_ns())

def ns_to_ms(ns: int) -> float:
    """Convert from nanoseconds to milliseconds"""
    return ns * NILS_TO_MILS

def ms_to_s(ms: int) -> float:
    """Convert from milliseconds to seconds"""
    return ms * MILS_TO_SECS

def ms_to_m(ms: int) -> float:
    """Convert from milliseconds to minutes"""
    return ms * MILS_TO_MINS

def ms_to_h(ms: int) -> float:
    """Convert from milliseconds to hours"""
    return ms * MILS_TO_HOURS
