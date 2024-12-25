from datetime import datetime, timedelta
from lib.configs.base_variables_config import min_age, min_days

def date_checker(user_date: str) -> bool:
    """
    The manipulation function used to tell if the user is the minimum age to be a member of the server
    
    Args:
        user_date (str): gotten from the user's response to the prompt sent by the bot -- this message will be formatted and sent using main.py
    
    Return boolean meaning:
        true -> user is of age and can be given the members role (role id will be given in the main.py)
        false -> user is too young to be a member of the server and will be banned

    ValueError will be raised if the date is not in the correct format

    This command will be used by both the command where the user verifies themselves to become a member of the server and the command where the moderators request verification
    """

    try:
        user_dob = datetime.strptime(user_date, "%Y-%m-%d")
        today = datetime.now()
        min_date = today - timedelta(days=(min_age * 365 + min_days)) #minimum DOB to JUST be turning the age to be in the server
        return user_dob <= min_date
    
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

