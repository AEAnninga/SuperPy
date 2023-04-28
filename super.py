# Imports
import argparse
import csv
import sys
from argparse import RawTextHelpFormatter, MetavarTypeHelpFormatter
from rich_argparse import RawTextRichHelpFormatter, MetavarTypeRichHelpFormatter, RawDescriptionRichHelpFormatter
from os import system, name
from datetime import date, datetime
from tabulate import tabulate
from rich import box
from rich.text import Text
from rich.console import Console
from rich import print as RichPrint
from rich.table import Table
from inventory import *
from csv_helper import *
from variable_helper import *
from table_viewer import *
from date_handlers import *

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
# change_working_date()
# current_date = convert_date(get_working_date())
working_date = convert_date(get_working_date())


class MultipleFormatter(RawTextRichHelpFormatter, RawDescriptionRichHelpFormatter, MetavarTypeRichHelpFormatter):
    pass


def get_clear_screen():
    cls = read_csv(cls_file)
    # print(f"csv heeft inhoud: {cls}")
    return cls


def toggle_clear_screen():
    toggle = get_clear_screen()
    # print(toggle)
    if toggle != "ON" or toggle != "OFF":
        toggle_on = "ON"
        # print(f"csv wordt: {toggle_on}")
        rewrite_csv(cls_file, [toggle_on])
    if toggle == "OFF":
        toggle_on = "ON"
        # print(f"csv wordt: {toggle_on}")
        rewrite_csv(cls_file, [toggle_on])
    if toggle == "ON":
        toggle_off = "OFF"
        # print(f"csv wordt: {toggle_off}")
        rewrite_csv(cls_file, [toggle_off])


def clear_screen():
    clear_screen = get_clear_screen()
    if clear_screen == "ON":
        if name == "nt":
            system("cls")
        else:
            system("clear")


def create_id(filename, id_name):
    products = read_csv(filename)
    product_id_list = [int(item[id_name]) for item in products]
    if product_id_list:
        max_id = max(product_id_list)
        new_id = max_id + 1
    else:
        new_id = 1
    return new_id


def get_nearest_exp_date(product_name):
    bought_products = read_csv(bought_file)
    product_exp_dates = [
        convert_date(item["expiration_date"], False)
        for item in bought_products
        if item["product_name"] == product_name
    ]
    for date_object in product_exp_dates:
        print(type(date_object))
    exp_date = min(product_exp_dates)
    return convert_date(exp_date)


def get_cost_revenue(buy_date=None, product_name=None):
    bought_products = read_csv(bought_file)
    sold_products = read_csv(sold_file)
    if buy_date:
        product_cost = [
            round(float(item["cost"]), 2)
            for item in bought_products
            if item["buy_date"] == buy_date
        ]
        # print(product_cost)
        return product_cost
    elif product_name:
        product_cost = [
            {
                "bought_id": item["bought_id"],
                "name": item["product_name"],
                "cost": round(float(item["cost"]), 2),
                "revenue": sum(
                    [
                        round(float(sold_item["revenue"]), 2)
                        for sold_item in sold_products
                        if item["bought_id"] == sold_item["bought_id"]
                    ]
                ),
            }
            for item in bought_products
            if item["product_name"] == product_name
        ]
        if product_cost:
            create_table(
                product_cost, f"Product profit: {product_cost[0]['name']}")
            return product_cost
        else:
            print(f"No profit for this product: {product_name}")
    else:
        product_cost = [
            {
                "bought_id": item["bought_id"],
                "name": item["product_name"],
                "cost": round(float(item["cost"]), 2),
                "revenue": sum(
                    [
                        round(float(sold_item["revenue"]), 2)
                        for sold_item in sold_products
                        if item["bought_id"] == sold_item["bought_id"]
                    ]
                ),
            }
            for item in bought_products
        ]
        # print(product_cost)
        create_table(product_cost, "Overall profit")
        return product_cost


def update_storage(product_name, quantity, is_bought, bought_id):
    storage_list_of_dicts = get_csv_as_list_of_dicts(storage_file)
    new_exp_date = get_nearest_exp_date(product_name)
    # print(new_exp_date)
    storage_updated_list_of_dicts = get_updated_list_of_dicts_storage(
        product_name, quantity, new_exp_date, storage_list_of_dicts, is_bought
    )
    with open(storage_file, "w", newline="", encoding="utf8") as file_handler:
        headers = [column["column_name"] for column in storage_columns]
        csv_writer = csv.DictWriter(file_handler, fieldnames=headers)
        csv_writer.writeheader()
        csv_writer.writerows(storage_updated_list_of_dicts)
        file_handler.close()
    if not is_bought:
        bought_list_of_dicts = get_csv_as_list_of_dicts(bought_file)
        bought_updated_list_of_dicts = get_updated_list_of_dicts_bought(
            quantity, bought_list_of_dicts, bought_id
        )
        with open(bought_file, "w", newline="", encoding="utf8") as file_handler:
            headers = [column["column_name"] for column in bought_columns]
            csv_writer = csv.DictWriter(file_handler, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerows(bought_updated_list_of_dicts)
            file_handler.close()


def create_product_id(productlist):
    max_id = max([int(item["product_id"]) for item in productlist])
    preceeding_zeros_count = max_length_product_id - len(str(max_id))
    new_id = preceeding_zeros_count * "0" + str(max_id + 1)
    return new_id


def buy_product(args):
    product_name, buy_price, expiration_date, buy_quantity = args.bought
    valid_buy_price = True
    valid_buy_quantity = True
    valid_exp_date = convert_date(expiration_date)

    try:
        buy_price = float(buy_price)
    except ValueError as err:
        print(f"Argument given: {buy_price}")
        print(f"{err}")
        print(f"Please replace '{buy_price}' with float or integer\n")
        valid_buy_price = False

    try:
        buy_quantity = int(buy_quantity)
    except ValueError as err:
        print(f"Argument given: {buy_quantity}")
        print(f"{err}")
        print(f"Please replace '{buy_quantity}' with integer\n")
        valid_buy_quantity = False


    if not valid_buy_price or not valid_buy_quantity:
        return print(f"Your arguments: {args.bought}\n")
    
    if not valid_exp_date:
        return

    left_quantity = buy_quantity
    buy_date = args.buy_date
    today = args.today
    new_date = working_date if today else convert_date(
        buy_date)  # datetime.fromisoformat(buy_date).date()
    new_id = create_id(bought_file, "bought_id")
    cost = float(buy_price) * float(buy_quantity)
    # print(f"New bought id: {new_id}")
    bought_tuple = (
        new_id,
        product_name,
        new_date,
        valid_exp_date,
        buy_price,
        buy_quantity,
        left_quantity,
        cost,
    )
    write_to_csv(bought_file, bought_tuple)

    products_overview = read_csv(product_range_file)
    product_exist = [
        item for item in products_overview if item["product_name"] == product_name
    ]
    if not product_exist:
        product_id = create_product_id(products_overview)
        new_product_tuple = (product_id, product_name)
        write_to_csv(product_range_file, new_product_tuple)

    storage_products = read_csv(storage_file)
    product = [
        item for item in storage_products if item["product_name"] == product_name
    ]
    if product:
        # print(product)
        update_storage(product[0]["product_name"], buy_quantity, True, new_id)
    else:
        storage_tuple = (product_name, buy_quantity, valid_exp_date)
        write_to_csv(storage_file, storage_tuple)


def sell_product(args):
    storage_products = read_csv(storage_file)
    bought_products = read_csv(bought_file)
    bought_id, sell_price, sell_quantity = args.sold
    get_product = [
        item for item in bought_products if int(item["bought_id"]) == int(bought_id)
    ]
    if len(get_product) == 0:
        print(
            f"A product with bought_id {bought_id} does not exist. Did you make a typo?"
        )
        return
    product = get_product[0]
    max_sell_quantity = [
        sell_item["stock"]
        for sell_item in storage_products
        if sell_item["product_name"] == product["product_name"]
    ][0]

    if int(sell_quantity) > int(max_sell_quantity):
        print(
            f"Only {max_sell_quantity} left in storage, choose {max_sell_quantity} or lower for quantity"
        )
        return
    if int(sell_quantity) <= 0:
        print(f"Quantity cannot be 0 or negative!")
        return
    else:
        sell_date = args.sell_date
        today = args.today
        new_id = create_id(sold_file, "sell_id")
        new_date = (working_date if today else convert_date(sell_date))  # datetime.fromisoformat(sell_date).date()
        revenue = round((float(sell_quantity) * float(sell_price)), 2)
        # print(product)
        sold_tuple = (
            new_id,
            bought_id,
            product["product_name"],
            new_date,
            sell_price,
            sell_quantity,
            revenue,
        )
        # print(sold_tuple)
        # print(product["product_name"])
        update_storage(product["product_name"],
                       sell_quantity, False, bought_id)
        write_to_csv(sold_file, sold_tuple)



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


def main():
    parser = argparse.ArgumentParser(
        prog="SuperPy",
        description="Keep track of your supermarket inventory!",
        # formatter_class=RawTextHelpFormatter,
        formatter_class=MultipleFormatter,
        add_help=False,
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help=help_text,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s 1.0",
        help=version_text,
    )
    parser.add_argument(
        "-report",
        nargs=1,
        dest="report",
        # required="i" in sys.argv,
        choices=REPORTS.keys(),
        help=reports_help_text,
        type=str,
    )
    parser.add_argument(
        "-bp",
        "--buy-product",
        nargs=4,
        dest="bought",
        # required="b" in sys.argv,
        help=buy_product_help_text,
        type=str,
    )
    parser.add_argument(
        "-sp",
        "--sell-product",
        nargs=3,
        dest="sold",
        type=str,
        # required="s" in sys.argv,
        help=sell_product_help_text,
    )
    parser.add_argument(
        "-bd",
        "--buy-date",
        required="-bp" in sys.argv
        and "--today" not in sys.argv
        or "--buy-product" in sys.argv
        and "--today" not in sys.argv,
        dest="buy_date",
        help=buy_date_help_text,
        type=str,
    )
    parser.add_argument(
        "-sd",
        "--sell-date",
        required=("-sp" or "--sell-product") in sys.argv
        and ("--today") not in sys.argv,
        dest="sell_date",
        help=sell_date_help_text,
        type=str,
    )
    parser.add_argument(
        "--today",
        action="store_true",
        required=("-sp" or "--sell-product" or "-bp" or "--buy-product") in sys.argv
        and ("-sd" or "--sell-date" or "-bd" or "--buy-date") not in sys.argv,
        dest="today",
        help=today_help_text,
    )
    parser.add_argument(
        "-cd",
        "--change-date",
        action="store_true",
        required="--date" in sys.argv or "--days" in sys.argv,
        dest="change_date",
        help=change_date_help_text,
    )
    parser.add_argument(
        "--days",
        required="-cd" in sys.argv
        and "--date" not in sys.argv
        or "--change-date" in sys.argv
        and "--date" not in sys.argv,
        dest="number_of_days",
        help=days_help_text,
        type=int,
    )
    parser.add_argument(
        "--date",
        required="-cd" in sys.argv
        and "--days" not in sys.argv
        or "--change-date" in sys.argv
        and "--days" not in sys.argv,
        dest="wanted_date",
        help=date_help_text,
        type=str,
    )
    parser.add_argument(
        "-dd",
        "--display-date",
        action="store_true",
        dest="display_date",
        help=display_date_help_text,
    )
    parser.add_argument(
        "-rd",
        "--reset-date",
        action="store_true",
        dest="reset_date",
        help=reset_date_help_text,
    )
    parser.add_argument(
        "-p",
        "--profit",
        dest="profit",
        action="store_true",
        # choices=["o","d"],
        # required="b" in sys.argv,
        help=profit_help_text,
    )
    parser.add_argument(
        "-op",
        "--overall-profit",
        required=("-p" or "--profit") in sys.argv
        and ("-dp" or "--date-profit") not in sys.argv
        and ("-pp" or "--product-profit") not in sys.argv,
        action="store_true",
        dest="overall_profit",
        help=overall_profit_help_text,
    )
    parser.add_argument(
        "-dp",
        "--date-profit",
        required=("-p" or "--profit") in sys.argv
        and ("-op" or "--overall-profit") not in sys.argv
        and ("-pp" or "--product-profit") not in sys.argv,
        dest="date_profit",
        help=date_profit_help_text,
        type=str,
    )
    parser.add_argument(
        "-pp",
        "--product-profit",
        required=("-p" or "--profit") in sys.argv
        and ("-dp" or "--date-profit") not in sys.argv
        and ("-op" or "--overall-profit") not in sys.argv,
        dest="product_profit",
        help=product_profit_help_text,
        type=str,
    )
    parser.add_argument(
        "--toggle-cls",
        action="store_true",
        dest="toggle_cls",
        help=toggle_cls_help_text,
    )
    parsed_args = parser.parse_args()

    execute_action(parsed_args)


def execute_action(args):
    clear_screen()

    raise_error = len(sys.argv) <= 1
    print(args)
    # today_date_type = type(convert_date(date.today()))
    # working_date_type = type(convert_date(get_working_date()))
    # print(f"today_date_type: {today_date_type}")
    # print(f"working_date_type: {working_date_type}")

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
    if not raise_error:
        if args.report:
            # print(f"Superpy regel 376, argument: {args.report[0]}")
            if args.report[0] != "all":
                report_inventory(args.report[0])
            else:
                call_report_inventory()
        if args.bought:
            # print(args)
            buy_product(args)
        if args.sold:
            # print(args)
            sell_product(args)
        if args.change_date:
            change_working_date(args.number_of_days, args.wanted_date)
            print_date_text(change_text=True)
        if args.display_date:
            print_date_text(display_text=True)
        if args.reset_date:
            change_working_date()
            print_date_text(reset_text=True)
        if args.profit:
            # print(args)
            cost = get_cost_revenue(
                buy_date=args.date_profit, product_name=args.product_profit
            )
            # print(cost)
        if args.toggle_cls:
            toggle_clear_screen()
            print(f"You toggled clear screen to {get_clear_screen()}")
    else:
        print("Please fill in arguments")
        print("For help type: python main.py -h")


if __name__ == "__main__":
    main()
