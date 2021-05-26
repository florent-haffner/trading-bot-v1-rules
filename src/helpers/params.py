from src.helpers.environmentEnum import __ENVIRONMENTS


""" APP PARAMETERS """
__DEBUG: bool = True  # Handle exception and send it via email or break state
__OFFLINE: bool = False  # Manage the mock path
__ENVIRONMENT = __ENVIRONMENTS.PROD.value  # Get the value of the Env enum, change .DEV or .PROD


"""
    COMPUTATION
"""
MAXIMUM_PERCENTAGE_EUR: float = .99
MAXIMUM_FEES: float = .05
