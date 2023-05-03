from rich import box
from rich.table import Table
from variable_helper import *
from date_handlers import get_working_date, convert_date
from csv_helper import get_csv_as_list_of_dicts


def create_bought_rows(dict, table):
    # extract dictionary items
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

    # data for creating rows
    exp_date = convert_date(expiration_date[1], False)
    current_date = convert_date(get_working_date(), False)
    expired_text = f"Product expired!"
    discount_text = f"Discount on product!"
    normal_text = f"Normal pricing"
    days_till_expired = (exp_date - current_date).days
    date_color = red if days_till_expired > 5 else ("yellow" if 5 >= days_till_expired > 0 else green)
    date_text = normal_text if days_till_expired > 5 else (discount_text if 5 >= days_till_expired > 0 else expired_text)
    
    # add rows to table 
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
    # extract dictionary items
    (
        sell_id,
        bought_id,
        product_name,
        sell_date,
        sell_price,
        sell_quantity,
        revenue,
    ) = dict.items()

    # add rows to table
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
    # extract dictionary items
    product_name, quantity, nearest_exp_date = dict.items()

    # data for creating rows
    exp_date = convert_date(nearest_exp_date[1], False)
    current_date = convert_date(get_working_date(), False)
    color = red if int(quantity[1]) > 8 else green
    low_stock = "" if int(quantity[1]) > 8 else (f"  [red](Out of stock!)[/red]" if int(quantity[1]) <= 0 else f"  [yellow](Low stock!)[/yellow]")
    expired_text = f"Can have expired items!"
    discount_text = f"Some items may need discount!!"
    normal_text = f"Normal pricing"
    date_color = red if (exp_date - current_date).days > 5 else ("yellow" if 5 >= (exp_date - current_date).days > 0 else green)
    date_text = normal_text if (exp_date - current_date).days > 5 else (discount_text if 5 >= (exp_date - current_date).days > 0 else expired_text)

    # add rows to table
    table.add_row(
        f"[{text_color}]{product_name[1]}[/{text_color}]",
        f"[{color}]{quantity[1]}[/{color}] {low_stock}",
        f"[{date_color}]{nearest_exp_date[1]}    {date_text}[/{date_color}]",
    )


def create_product_rows(dict, table):
    # extract dictionary items
    (product_id, product_name) = dict.items()

    # add row to table
    table.add_row(product_id[1], f"[{text_color}]{product_name[1]}[/{text_color}]")


# function to create and display inventory report
def create_inventory_report(filename):
    # get csv data as list of dictionaries
    list_of_dicts = get_csv_as_list_of_dicts(filenames[filename]["name"])

    # get the right columns from filenames dictionary (from variable_helper file)
    columns = filenames[filename]["columns"]

    # create table Title: remove underscore _ from filename (filename no longer needed for getting data) 
    if filename == "product_range":
        filename = filename.replace("_", " ")
    
    # create table instance
    table = Table(
        title=f"[{blue}]Report: [/{blue}] [{text_color}]{filename.upper()}[/{text_color}]",
        box=box.ROUNDED,
        show_header=True,
        header_style=blue,
        caption=f"[{blue}]Anningast Productions[/{blue}] [white]\xa9[/white]",
    )

    # add columns (headers)
    for column in columns:
        table.add_column(
            column["column_name"],
            no_wrap=True,
            justify="left",
            width=column["column_width"],
        )

    # use filename as condition to create rows 
    if filename == "bought":
        for dict in list_of_dicts:
            create_bought_rows(dict, table)
    if filename == "sold":
        for dict in list_of_dicts:
            create_sold_rows(dict, table)
    if filename == "storage":
        for dict in list_of_dicts:
            create_storage_rows(dict, table)
    if filename == "product_range" or filename == "product range":
        for dict in list_of_dicts:
            create_product_rows(dict, table)

    # display table and add some extra lines above and underneath table
    console.print("\n\n")
    console.print(table)
    console.print("\n\n")


# function to create and display all possible inventory reports
def create_all_inventory_reports():
    for key in REPORTS.keys():
        if key != "all":
            create_inventory_report(key)
