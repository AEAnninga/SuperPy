from datetime import date, datetime, timedelta
from csv_helper import *
from variable_helper import *


def get_working_date():
    working_date = read_csv(date_file)
    #    print(working_date)
    return working_date


def change_working_date(number_of_days: int = 0, wanted_date=None):
    if wanted_date:
        converted_date = convert_date(wanted_date)
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


def convert_date(date_object, return_string: bool = True):
    date_type = type(date_object)
    # print(f"Wat voor date-type gaat erin: {date_type}")
    if date_type == str:
        # #     date_obj = date(date_object)
        start_length = len(date_object.split("-")[0])
        if start_length <= 2:
            try:
                new_date = (
                    datetime.strptime(date_object, f"%d-%m-%Y").date()
                    # .__format__(f"%d-%m-%Y")
                )
                # print(f"Returned datetype from string: {type(new_date)}")
            except ValueError as err:
                print(f"{date_object} is not a valid date")
                return print(err)
        if start_length == 4:
            try:
                # print("starts with year")
                reversed_date = (
                    datetime.strptime(date_object, f"%Y-%m-%d")
                    .date()
                    .__format__(f"%d-%m-%Y")
                )
                # print(reversed_date)
                new_date = (
                    datetime.strptime(reversed_date, f"%d-%m-%Y").date()
                    # .__format__(f"%d-%m-%Y")
                )
                # new_date = reversed_date.__format__(f"%d-%m-%Y")
                # print(f"Returned datetype from string: {type(new_date)}")
            except ValueError as err:
                print(f"{date_object} is not a valid date")
                return print(err)
        # print(f"Wat voor date-type gaat eruit: {type(new_date)}")
        if return_string:
            new_date = new_date.__format__(f"%d-%m-%Y")
        return new_date
    else:
        new_date = date_object.__format__(f"%d-%m-%Y")
        try:
            test_date = datetime.strptime(new_date, f"%d-%m-%Y").date()
        except ValueError as err:
            print(f"{date_object} is not a valid date")
            return print(err)
        if return_string:
            test_date = test_date.__format__(f"%d-%m-%Y")
        # print(f"Wat voor date-type gaat eruit: {type(test_date)}")
        return test_date
