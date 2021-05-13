import enum


class __ENVIRONMENTS(enum.Enum):
    DEV = 'dev'
    PROD = 'prod'


""" APP PARAMETERS """
__DEBUG: bool = True  # Handle exception and send it via email or break state
__OFFLINE: bool = False  # Manage the data path
__ENVIRONMENT = __ENVIRONMENTS.DEV


"""
    COMPUTATION
"""
MAXIMUM_PERCENTAGE_EUR: float = .99
MAXIMUM_FEES: float = .05
