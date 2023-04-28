from datetime import date, datetime, timedelta
from csv_helper import *
from variable_helper import *


def get_working_date():
    working_date = read_csv(date_file)
    #    print(working_date)
    return working_date


def change_working_date(number_of_days: int = 0, given_date=None):
    if given_date:
        converted_date = convert_date(given_date)
        current_used_date = [converted_date]
        # print(f"Date to go in csv: {current_used_date[0]}")
        if converted_date != None:
            rewrite_csv(date_file, current_used_date)
        # return current_used_date
    else:
        time_delta = timedelta(days=int(number_of_days))
        converted_date = convert_date(date.today() + time_delta)
        current_used_date = [converted_date]
        if converted_date != None:
            rewrite_csv(date_file, current_used_date)
        # return current_used_date



def convert_date(given_date, return_string: bool = True):
    date_type = type(given_date)
    if date_type == str:
        start_length = len(given_date.split("-")[0])
        date_format = (f"%d-%m-%Y" if start_length <= 2 else f"%Y-%m-%d")
        try:
            # convert to date object for when return_string is False (date objects do not keep the desired format)
            date_as_object = datetime.strptime(given_date, date_format).date()
        except ValueError as err:
            print(f"{given_date} is not a valid date")
            return print(f"PLease use valid date")
            # print(f"Wat voor date-type gaat eruit: {type(new_date)}")
        if return_string:
            date_as_string = date_as_object.__format__(f"%d-%m-%Y")
            return date_as_string
        return date_as_object    
    else:
        # convert date object to string in desired format
        try:
            date_as_string = given_date.__format__(f"%d-%m-%Y")
        except ValueError as err:
            print(f"something went wrong trying to convert {given_date} to a string")
            return print(err)
        if return_string:
            return date_as_string
        return given_date

# test date conversion

# def convert_date_long(date_object, return_string: bool = True):
#     date_type = type(date_object)
#     # print(f"Wat voor date-type gaat erin: {date_type}")
#     if date_type == str:
#         # #     date_obj = date(date_object)
#         start_length = len(date_object.split("-")[0])
#         if start_length <= 2:
#             try:
#                 new_date = (
#                     datetime.strptime(date_object, f"%d-%m-%Y").date()
#                     # .__format__(f"%d-%m-%Y")
#                 )
#                 # print(f"Returned datetype from string: {type(new_date)}")
#             except ValueError as err:
#                 print(f"{date_object} is not a valid date")
#                 print(err)
#                 return print(f"please use valid date")
#         if start_length == 4:
#             try:
#                 # print("starts with year")
#                 reversed_date = (
#                     datetime.strptime(date_object, f"%Y-%m-%d")
#                     .date()
#                     .__format__(f"%d-%m-%Y")
#                 )
#                 new_date = (
#                     datetime.strptime(reversed_date, f"%d-%m-%Y").date()
#                     # .__format__(f"%d-%m-%Y")
#                 )
#                 # new_date = reversed_date.__format__(f"%d-%m-%Y")
#                 # print(f"Returned datetype from string: {type(new_date)}")
#             except ValueError as err:
#                 print(f"{date_object} is not a valid date")
#                 print(err)
#                 return print(f"PLease use valid date")
#         # print(f"Wat voor date-type gaat eruit: {type(new_date)}")
#         if return_string:
#             new_date = new_date.__format__(f"%d-%m-%Y")
#         return new_date
#     else:
#         new_date = date_object.__format__(f"%d-%m-%Y")
#         try:
#             test_date = datetime.strptime(new_date, f"%d-%m-%Y").date()
#         except ValueError as err:
#             print(f"{date_object} is not a valid date")
#             return print(err)
#         if return_string:
#             test_date = test_date.__format__(f"%d-%m-%Y")
#         # print(f"Wat voor date-type gaat eruit: {type(test_date)}")
#         return test_date

# test = "21-12-2023"
# test_american = "2023-12-21"

# reversed_date_str = (
#     datetime.strptime(test_american, f"%Y-%m-%d")
#     .date()
#     .__format__(f"%d-%m-%Y")
# )
# reversed_date_obj = datetime.strptime(reversed_date_str, f"%d-%m-%Y")

# print(f"{type(reversed_date_str)} : {reversed_date_str}")
# print(f"{type(reversed_date_obj)} : {reversed_date_obj}")

# testdate2 = date(2023,12,21)
# print(f"{test} wordt: {convert_date_long(test, False)}")
# print(f"{test_american} wordt: {convert_date_long(test_american, False)}")
# print(f"{testdate2} wordt: {convert_date_long(testdate2, False)}")