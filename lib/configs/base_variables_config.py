#global variables 

min_age = 18 #default
min_days = 0 #default

def set_min(age):
    global min_age
    min_age = age

    return(f"The minimum age has been set to {age} years old.")

def get_min_age():
    return min_age