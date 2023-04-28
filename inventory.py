from rich import box
from rich.console import Console
from rich.table import Table
from datetime import date, datetime
from rich.console import Console
import csv
from variable_helper import *
from date_handlers import *
from super import get_csv_as_list_of_dicts, working_date, convert_date
from csv_helper import get_csv_as_list_of_dicts


def create_bought_rows(dict, table):
    (
        bought_id,
        product_name,
        buy_date,
        expiration_date,
        buy_price,
        buy_quantity,
        left_quantity,
        cost,
    ) = dict.items()
    
    


    exp_date = convert_date(expiration_date[1], False)
    current_date = convert_date(get_working_date(), False)
    color = red if int(buy_quantity[1]) > 8 else green
    low_stock = "" if int(buy_quantity[1]) > 8 else f"  [yellow](Low stock!)[/yellow]"
    expired_text = f"Product expired!"
    discount_text = f"Discount on product!"
    normal_text = f"Normal pricing"
    days_till_expired = (exp_date - current_date).days
    date_color = (
        red
        if days_till_expired > 5
        else ("yellow" if 5 >= days_till_expired > 0 else green)
    )
    date_text = (
        normal_text
        if days_till_expired > 5
        else (discount_text if 5 >= days_till_expired > 0 else expired_text)
    )
    table.add_row(
        bought_id[1],
        f"[{text_color}]{product_name[1]}[/{text_color}]",
        buy_date[1],
        f"[{date_color}]{expiration_date[1]}    {date_text}[/{date_color}]",
        buy_price[1],
        f"{buy_quantity[1]}",
        f"{left_quantity[1]}",
        f"{cost[1]}",
    )


def create_sold_rows(dict, table):
    # print(dict)
    (
        sell_id,
        bought_id,
        product_name,
        sell_date,
        sell_price,
        sell_quantity,
        revenue,
    ) = dict.items()

    # exp_date = datetime.strptime(sell_date[1], f"%Y-%m-%d").date()
    # sold_date = datetime.fromisoformat(sell_date[1]).date()

    table.add_row(
        sell_id[1],
        bought_id[1],
        f"[{text_color}]{product_name[1]}[/{text_color}]",
        sell_date[1],
        sell_price[1],
        sell_quantity[1],
        revenue[1],
    )


def create_storage_rows(dict, table):
    product_name, quantity, nearest_exp_date = dict.items()

    # exp_date = datetime.fromisoformat(nearest_exp_date[1]).date()
    exp_date = convert_date(nearest_exp_date[1], False)
    current_date = convert_date(get_working_date(), False)
    color = red if int(quantity[1]) > 8 else green
    low_stock = (
        ""
        if int(quantity[1]) > 8
        else (
            f"  [red](Out of stock!)[/red]"
            if int(quantity[1]) <= 0
            else f"  [yellow](Low stock!)[/yellow]"
        )
    )
    expired_text = f"Can have expired items!"
    discount_text = f"Some items may need discount!!"
    normal_text = f"Normal pricing"
    date_color = (
        red
        if (exp_date - current_date).days > 5
        else ("yellow" if 5 >= (exp_date - current_date).days > 0 else green)
    )
    date_text = (
        normal_text
        if (exp_date - current_date).days > 5
        else (
            discount_text if 5 >= (exp_date - current_date).days > 0 else expired_text
        )
    )

    table.add_row(
        f"[{text_color}]{product_name[1]}[/{text_color}]",
        f"[{color}]{quantity[1]}[/{color}] {low_stock}",
        f"[{date_color}]{nearest_exp_date[1]}    {date_text}[/{date_color}]",
    )


def create_product_rows(dict, table):
    # print(dict)
    (product_id, product_name) = dict.items()

    table.add_row(product_id[1], f"[{text_color}]{product_name[1]}[/{text_color}]")


def report_inventory(filename):
    # print(filenames[filename])
    list_of_dicts = get_csv_as_list_of_dicts(filenames[filename]["name"])
    # print(list_of_dicts)
    columns = filenames[filename]["columns"]
    if filename == "product_range":
        filename = filename.replace("_", " ")
    # print(columns)
    table = Table(
        title=f"[{blue}]Report: [/{blue}] [{text_color}]{filename.upper()}[/{text_color}]",
        box=box.ROUNDED,
        show_header=True,
        header_style=blue,
        caption=f"[{blue}]Anningast Productions[/{blue}] [white]\xa9[/white]",
    )
    for column in columns:
        # column_width = column["column_width"]
        table.add_column(
            column["column_name"],
            no_wrap=True,
            justify="left",
            width=column["column_width"],
        )
    # table.add_column("bought_id", no_wrap=True, width=25)
    # table.add_column("Product Name", no_wrap=True, width=50)
    # table.add_column("Quantity", justify="left", no_wrap=True, width=50)
    # table.add_column("Buy Price", justify="center", no_wrap=True, width=50)
    # table.add_column("Expiration Date", justify="left", no_wrap=True, width=50)
    # # header_list = ["Product Name", "Quantity", "Buy Price", "Expiration Date"]
    # data = []
    if filename == "bought":
        # print(f"Filename: {filename}")
        for dict in list_of_dicts:
            create_bought_rows(dict, table)
    if filename == "sold":
        # print(f"Filename: {filename}")
        for dict in list_of_dicts:
            create_sold_rows(dict, table)
    if filename == "storage":
        # print(f"Filename: {filename}")
        for dict in list_of_dicts:
            create_storage_rows(dict, table)
    if filename == "product_range" or filename == "product range":
        # print(f"Filename: {filename}")
        for dict in list_of_dicts:
            create_product_rows(dict, table)

    console.print(table)
    console.print("\n\n")


def call_report_inventory():
    for key in REPORTS.keys():
        if key != "all":
            report_inventory(key)
