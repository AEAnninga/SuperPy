from datetime import date, datetime, timedelta
from csv_helper import read_csv, rewrite_csv
from variable_helper import *
from rich import print as RichPrint
from rich.text import Text


# get nearest (earliest) date from expiration dates > used in reports
def get_nearest_exp_date(product_name):
    bought_products = read_csv(bought_file)
    product_exp_dates = [convert_date(item["expiration_date"], False) for item in bought_products if item["product_name"] == product_name]
    try:
        exp_date = min(product_exp_dates)
    except:
        return print(no_products_text)
    return convert_date(exp_date)

def get_working_date():
    working_date = read_csv(date_file)
    if working_date == False:
        change_working_date(date.today())
        working_date = read_csv(date_file)
    return working_date


def change_working_date(number_of_days: int = 0, given_date=None):
    if given_date:
        converted_date = convert_date(given_date)
        if converted_date != None:
            current_used_date = [converted_date]
            rewrite_csv(date_file, current_used_date)
    else:
        time_delta = timedelta(days=int(number_of_days))
        working_date = convert_date(get_working_date(), False) # False will give back a date object instead of a string
        converted_date = convert_date(working_date + time_delta)
        current_used_date = [converted_date]
        if converted_date != None:
            rewrite_csv(date_file, current_used_date)


# convert date to string or date object > can receive date as string or object
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
            return print(f"PLease use valid date in format <dd-MM-yyyy> or <yyyy-MM-dd>")
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
    

# date texts and warnings
def print_date_text(reset_text: bool=False, display_text: bool=False, change_text: bool=False):
    past_or_future = ("in the past" if convert_date(date.today(), False) >= convert_date(get_working_date(), False) else "in the future") 
    date_change_text = Text(f"\n Working date is {past_or_future}: {get_working_date()} \n".upper(),style="blink bold italic red r")
    date_today_text = Text(f"\n Working date is today: {get_working_date()} \n".upper(),style="bold italic white r")
    display_date_text = Text(f"\n Working date is: {get_working_date()} \n".upper(),style="bold italic white r")
    reset_date_text = Text(f"\n Resetting date to today: {get_working_date()} \n".upper(),style="bold italic white r")
    if reset_text:
        RichPrint(reset_date_text)
    if display_text:
        RichPrint(display_date_text)  
    if change_text:
        RichPrint(date_change_text) if convert_date(date.today()) != convert_date(get_working_date()) else RichPrint(date_today_text)

def print_date_warning(args):
    if (
        convert_date(date.today()) != convert_date(get_working_date())
        and args.reset_date == False
        and args.change_date == False
        and args.display_date == False
    ):
        today = convert_date(date.today())
        working_date = get_working_date()
        date_warning_text = Text(
            f"\n Please note you are currently working with date: {working_date} ".upper(
            ),
            style="blink bold italic red r",
        )
        date_warning_text.append(
            f"\n While today's date is {today} \n".upper(),
            style="blink bold italic yellow r",
        )

        date_action_text = Text(
            "\n To reset the working date to today, use: \n ".upper(),
            style="bold italic yellow r",
        )
        date_action_text.append(
            "\n python super.py -rd (or: --reset-date) \n",
            style="bold italic yellow r",
        )

        RichPrint(date_warning_text)
        RichPrint(date_action_text)