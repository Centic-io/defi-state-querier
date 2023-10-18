from defi_services.constants.time_constant import TimeConstants


def apr_to_apy(apr, seconds_per_year=TimeConstants.A_YEAR):
    apy = ((1 + (apr / seconds_per_year)) ** seconds_per_year) - 1
    return apy


def apy_to_apr(apy, seconds_per_year=TimeConstants.A_YEAR):
    apr = ((1 + apy) ** (1 / seconds_per_year) - 1) * seconds_per_year
    return apr
