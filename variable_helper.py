from datetime import date, datetime
from rich.console import Console
from argparse import HelpFormatter


# columns
bought_columns = [
    {"column_name": "bought_id", "column_width": 25},
    {"column_name": "product_name", "column_width": 40},
    {"column_name": "buy_date", "column_width": 40},
    {"column_name": "expiration_date", "column_width": 40},
    {"column_name": "buy_price", "column_width": 25},
    {"column_name": "buy_quantity", "column_width": 25},
    {"column_name": "left_quantity", "column_width": 25},
    {"column_name": "cost", "column_width": 25},
]

sold_columns = [
    {"column_name": "sell_id", "column_width": 25},
    {"column_name": "bought_id", "column_width": 25},
    {"column_name": "product_name", "column_width": 40},
    {"column_name": "sell_date", "column_width": 40},
    {"column_name": "sell_price", "column_width": 25},
    {"column_name": "sell_quantity", "column_width": 25},
    {"column_name": "revenue", "column_width": 25},
]

storage_columns = [
    {"column_name": "product_name", "column_width": 55},
    {"column_name": "stock", "column_width": 55},
    {"column_name": "nearest_exp_date", "column_width": 55},
]

product_range_columns = [
    {"column_name": "product_id", "column_width": 25},
    {"column_name": "product_name", "column_width": 55},
]

# files
cls_file = "clear_screen.csv"
date_file = "working_date.csv"
bought_file = "bought.csv"
sold_file = "sold.csv"
storage_file = "storage.csv"
product_range_file = "product_range.csv"
max_length_product_id = 5

filenames = {
    "bought": {"name": bought_file, "columns": bought_columns},
    "sold": {"name": sold_file, "columns": sold_columns},
    "storage": {"name": storage_file, "columns": storage_columns},
    "product_range": {"name": product_range_file, "columns": product_range_columns},
}

console = Console()

# colors
blue = "#6699cc"
green = "#f25252"
red = "#35ae3d"
text_color = "#65e2fd"


# actions
ACTION = {
    "i": "Shows Inventory(bought, sold, storage)",
    "b": "Add your bought products to inventory (csv)",
    "s": "Add Sold products to Sold overview and removes them from inventory",
    "e": "Remove expired products from inventory",
}

action_help_text = f"""
    Choose your action:
    i = {ACTION["i"]}
    b = {ACTION["b"]}
    s = {ACTION["s"]}
    e = {ACTION["e"]}
"""

REPORTS = {
    "bought": "Display table overview of bought products.",
    "sold": "Display table overview of sold products.",
    "storage": "Display table overview of current storage",
    "product_range": "Display table overview of product range",
    "all": "Display all table overviews",
}

# help text variables, text will be displayed as eneath, indentation and whitespaces will be preserved

help_text = f"""Show this help message and exit.\n
"""

version_text = f"""Show version number of SuperPy and exit.\n 
"""

reports_help_text = f"""
Choose your report:
----------------------------------------------------------------------------------------------------
bought          -->     {REPORTS["bought"]}
sold            -->     {REPORTS["sold"]}
storage         -->     {REPORTS["storage"]}
product_range   -->     {REPORTS["product_range"]}
all             -->     {REPORTS["all"]}
----------------------------------------------------------------------------------------------------\n    
"""

buy_product_help_text = f"""
Add 4 product properties in correct order separated by space:
----------------------------------------------------------------------------------------------------
[<product_name> <buy_price> <expiration_date> <quantity>]
For expiration_date use format: <dd-MM-yyyy> or <yyyy-MM--dd>
If your product_name contains spaces, enclose name in single or double quotes: "product name"/'product name'
----------------------------------------------------------------------------------------------------\n    
"""

sell_product_help_text = f""" 
Add 3 bought product properties after in correct order separated by spaces:
----------------------------------------------------------------------------------------------------
[<bought_id> <sell_price> <quantity>]
----------------------------------------------------------------------------------------------------\n 
"""

buy_date_help_text = f"""Use in combination with -bp or --buy-product. When --today is also added, this date will be ignored.\n
"""

sell_date_help_text = f"""Use in combination with -sp or --sell-product. When --today is also added, this date will be ignored.\n
"""

today_help_text = f"""Flag which disregards the given sell or buy date and uses working_date.\n
"""

change_date_help_text = f"""
Change date the program is currently working with:
----------------------------------------------------------------------------------------------------
Advance or subtract number of days from today's date (not working date!).
Use positive integer: Advance
Use negative integer: Subtract
Or fill in date, use format: <dd-MM-yyyy> or <yyyy-MM--dd> 
Use 0 (zero) or leave empty to reset date to today.
----------------------------------------------------------------------------------------------------\n 
"""

display_date_help_text = f"""Displays date the program is currently working with.\n
"""

reset_date_help_text = f"""Resets the programs working date to todays date.\n
"""

days_help_text = f"""Use in combination with -cd or --change-date.  
Fill in number of days: number\[integer]
--date will be ignored when using --days\n
"""

date_help_text = f"""Use in combination with -cd or --change-date. 
Fill in date, use format: <dd-MM-yyyy> or <yyyy-MM--dd>
When --days is also used, --date will be ignored\n
"""

profit_help_text = f"""
Shows Cost, Revenue and profit. Filters: Overall profit, profit from date, profit from product.\n
"""

overall_profit_help_text = f"""Filter for profit, shows overall(total) profit.\n
"""

date_profit_help_text = f"""Filter for profit, shows profit of single date/day. 
Fill in date, use format: <dd-MM-yyyy> or <yyyy-MM--dd>\n
"""

product_profit_help_text = f"""Filter for profit, shows cost and profit of single product . Fill in correct product_name\n
"""

toggle_cls_help_text = f"""
Toggles clear screen on or off:
----------------------------------------------------------------------------------------------------
ON:  Display will be refreshed with every command, except for -h (help) and -v (version). 
OFF: Everything stays visible, scrolling through history enabled.
----------------------------------------------------------------------------------------------------\n
"""
