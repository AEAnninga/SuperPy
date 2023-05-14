from csv_helper import rewrite_csv, read_csv
from variable_helper import cls_file, max_length_product_id
from os import system, name
from rich import print as RichPrint
from rich.text import Text


# get text from clear_screen.csv for use in function clear_screen()
def get_clear_screen():
    cls = read_csv(cls_file)
    return cls


# function to replace text in clear_screen.csv
def toggle_clear_screen():
    toggle = get_clear_screen()
    if toggle != "ON" or toggle != "OFF":
        toggle_on = "ON"
        rewrite_csv(cls_file, [toggle_on])
    if toggle == "OFF":
        toggle_on = "ON"
        rewrite_csv(cls_file, [toggle_on])
    if toggle == "ON":
        toggle_off = "OFF"
        rewrite_csv(cls_file, [toggle_off])
    RichPrint(Text(f"\n You toggled clear screen to {get_clear_screen()} \n",style="bold italic white r"))


# clear screen based on text from clear_screen.csv
def clear_screen():
    clear_screen = get_clear_screen()
    if clear_screen == "ON":
        if name == "nt":
            system("cls")
        else:
            system("clear")


# function for checking if input can be parsed to float
def is_float(answer) -> bool:
    # if you expect None to be passed:
    if answer is None: 
        return False
    try:
        float(answer)
        return True
    except ValueError:
        return False
    
  
# function for checking if input can be parsed to int
def is_int(answer) -> bool:
    # if you expect None to be passed:
    if answer is None: 
        return False
    try:
        int(answer)
        return True
    except ValueError:
        return False


# validation function for sell_price
def is_valid_sell_price(answer) -> bool:
    valid_float = is_float(answer)
    if valid_float:
        return (False if float(answer) <= 0 else True)


# validation function for sell_quantity
def is_valid_sell_quantity(answer,max_quantity) -> bool:
    valid_int = is_int(answer)
    if not valid_int:
        return False
    if int(answer) > int(max_quantity):
        print(f"\nQuantity exceeds maximum of {max_quantity}")
        return False
    elif int(answer) <= 0:
        print(f"\nQuantity cannot be 0 or negative!")
        return False
    else:
        return True


# functions for creating id 
def create_id(filename, id_name):
    products = read_csv(filename)
    product_id_list = [int(item[id_name]) for item in products]
    if product_id_list:
        max_id = max(product_id_list)
        new_id = max_id + 1
    else:
        new_id = 1
    return new_id


def create_product_id(productlist):
    first_id = "00001"
    if productlist:
        max_id = max([int(item["product_id"]) for item in productlist])
        preceeding_zeros_count = max_length_product_id - len(str(max_id + 1))
        new_id = (preceeding_zeros_count * "0") + str(max_id + 1)
        return new_id
    else:
        return first_id
