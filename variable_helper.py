from rich.console import Console
from rich.text import Text 

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

# backup files
backup_bought_file = "./backup_files/backup_bought.csv"
backup_sold_file = "./backup_files/backup_sold.csv"
backup_storage_file = "./backup_files/backup_storage.csv"
backup_product_range_file = "./backup_files/backup_product_range.csv"

# console variable for printing
console = Console()

# colors
blue = "#6699cc"
green = "#f25252"
red = "#35ae3d"
text_color = "#65e2fd"

# Anningast trademark text
table_caption = f"[#6699cc]A[/#6699cc][lightgrey]nningast[/lightgrey] [#6699cc]P[/#6699cc][lightgrey]roductions[/lightgrey] [#6699cc]\xa9[/#6699cc]"

# error handling text > when there are no products yet
no_products_text = f"\n No products available. Please buy products first! \n"
no_products_to_sell_text = f"\n No products available for selling. \n"

# dictionaries > keys as choices for arguments -report and -graph
REPORTS = {
    "bought": "Display table overview of bought products.",
    "sold": "Display table overview of sold products.",
    "storage": "Display table overview of current storage",
    "product_range": "Display table overview of product range",
    "all": "Display all table overviews",
}

GRAPHS = {
    "profit":"Shows horizontal barchart in a new window. Data: Cost, revenue and profit of bought/sold products",
    "bought":"Shows horizontal barchart in a new window. Data from bought.csv/sold.csv",
    "sold":"Shows horizontal barchart in a new window. Data from bought.csv/sold.csv",
    "storage":"Shows horizontal barchart in a new window. Data from storage.csv"
}

# HELP TEXT VARIABLES: text will be displayed as beneath, indentation and whitespaces are preserved

reports_help_text = f"""
-report bought | sold | storage | product_range | all

Displays report generated from csv-files:
bought          -->     {REPORTS["bought"]}
sold            -->     {REPORTS["sold"]}
storage         -->     {REPORTS["storage"]}
product_range   -->     {REPORTS["product_range"]}
all             -->     {REPORTS["all"]}
----------------------------------------------------------------------------------------------------\n    
"""

graphs_help_text = f"""
-graph profit | bought | sold | storage

Shows a graphic representation of data from csv-files:
profit          -->     {GRAPHS["profit"]}
bought          -->     {GRAPHS["bought"]}
sold            -->     {GRAPHS["sold"]}
storage         -->     {GRAPHS["storage"]}
----------------------------------------------------------------------------------------------------\n    
"""

buy_product_help_text = f"""
-bp | --buy-product [<product_name> <buy_price> <expiration_date> <quantity>]
required: --today | ( --use-date | -ud ) <dd-MM-yyyy> or <yyyy-MM--dd>

Buy new product and write its properties to csv files where needed: bought.csv storage.csv product_range.csv 
Fill in 4 product properties in correct order separated by spaces and use --today or --use-date 
For expiration_date and --use-date use format: <dd-MM-yyyy> or <yyyy-MM--dd>
If your product_name contains spaces, enclose name in single or double quotes: "product name"/'product name'
----------------------------------------------------------------------------------------------------\n    
"""

sell_product_help_text = f"""-sp | --sell-product
required: --today | ( --use-date | -ud ) <dd-MM-yyyy> or <yyyy-MM--dd>

Sells a bought product and updates csv files where needed: sold.csv bought.csv storage.csv
You will be prompted to:
1. choose a product name from product range
2. choose product batch (from bought products)
3. fill in sell_price
4. fill in sell_quantity
5. confirm sell
To abort early: ctrl c | ^c
----------------------------------------------------------------------------------------------------\n 
"""

use_date_help_text = f"""Use in combination with -bp | --buy-product | -sp | --sell-product 
Cannot be used simultaneously with --today.
----------------------------------------------------------------------------------------------------\n
"""

today_help_text = f"""Use instead of -ud | --use-date
Cannot be used simultaneously with -ud or --use-date.
----------------------------------------------------------------------------------------------------\n
"""

change_date_help_text = f"""-cd | --change-date [ --days <int> or <-int> | --date  <dd-MM-yyyy> or <yyyy-MM--dd> ]
required: --days or --date:

Change date the program is currently working with:
--days <int> | <-int>
    Advance or subtract number of days from today's date (not working date!).
    Advance:    use positive integer 
    Subtract:   use negative integer
    Use 0 (zero) to reset date to today.
--date <dd-MM-yyyy> | --date <yyyy-MM--dd> 
    Fill in date, use format: <dd-MM-yyyy> or <yyyy-MM--dd> 
----------------------------------------------------------------------------------------------------\n 
"""

display_date_help_text = f"""Displays date the program is currently working with.
----------------------------------------------------------------------------------------------------\n
"""

reset_date_help_text = f"""Resets the programs working date to todays date.
----------------------------------------------------------------------------------------------------\n
"""

days_help_text = f"""Use in combination with -cd or --change-date.  
Fill in number of days: use integer (positive or negative)
----------------------------------------------------------------------------------------------------\n
"""

date_help_text = f"""Use in combination with -cd or --change-date. 
Fill in date, use format: <dd-MM-yyyy> or <yyyy-MM--dd>
----------------------------------------------------------------------------------------------------\n
"""

profit_help_text = f"""Shows Cost, Revenue and profit. Filters: Overall profit, profit from date, profit from product.
----------------------------------------------------------------------------------------------------\n
"""

overall_profit_help_text = f"""Filter for profit, shows overall(total) profit.
----------------------------------------------------------------------------------------------------\n
"""

date_profit_help_text = f"""
-dp | --date-profit <date> <date>

Filter for profit, shows total profit made between two dates.
To show profit of single date, fill in same date twice. 
Fill in 2 dates, use format: <dd-MM-yyyy> or <yyyy-MM--dd>
----------------------------------------------------------------------------------------------------\n
"""

product_profit_help_text = f"""Filter for profit, shows cost and profit of single product. Fill in correct product_name
----------------------------------------------------------------------------------------------------\n
"""

toggle_cls_help_text = f"""Toggles clear screen on or off:
ON:  Console screen will be cleared with every command, except for -h (help) and -v (version). 
OFF: Console screen will not be cleared, scrolling up through history is possible.
----------------------------------------------------------------------------------------------------\n
"""

backup_help_text = f"""Writes data of bought, sold, storage and product_range files to backup files
\n\n
"""


# version text ascii art
version_text = f"""\n
  /$$$$$$                                          /$$$$$$$  /$$     /$$                                                                    
 /$$__  $$                                        | $$__  $$|  $$   /$$/                                                                    
| $$  \__/ /$$   /$$  /$$$$$$   /$$$$$$   /$$$$$$ | $$  \ $$ \  $$ /$$/                                                                     
|  $$$$$$ | $$  | $$ /$$__  $$ /$$__  $$ /$$__  $$| $$$$$$$/  \  $$$$/                                                                      
 \____  $$| $$  | $$| $$  \ $$| $$$$$$$$| $$  \__/| $$____/    \  $$/                                                                       
 /$$  \ $$| $$  | $$| $$  | $$| $$_____/| $$      | $$          | $$                                                                        
|  $$$$$$/|  $$$$$$/| $$$$$$$/|  $$$$$$$| $$      | $$          | $$                                                                        
 \______/  \______/ | $$____/  \_______/|__/      |__/          |__/                                                                        
                    | $$                                                                                                                    
                    | $$                                                                                                                    
                    |__/                                                                                                                    
                                                 /$$    /$$                              /$$                             /$$        /$$$$$$ 
                                                | $$   | $$                             |__/                           /$$$$       /$$$_  $$
                                                | $$   | $$ /$$$$$$   /$$$$$$   /$$$$$$$ /$$  /$$$$$$  /$$$$$$$       |_  $$      | $$$$\ $$
                                                |  $$ / $$//$$__  $$ /$$__  $$ /$$_____/| $$ /$$__  $$| $$__  $$        | $$      | $$ $$ $$
                                                 \  $$ $$/| $$$$$$$$| $$  \__/|  $$$$$$ | $$| $$  \ $$| $$  \ $$        | $$      | $$\ $$$$
                                                  \  $$$/ | $$_____/| $$       \____  $$| $$| $$  | $$| $$  | $$        | $$      | $$ \ $$$
                                                   \  $/  |  $$$$$$$| $$       /$$$$$$$/| $$|  $$$$$$/| $$  | $$       /$$$$$$ /$$|  $$$$$$/
                                                    \_/    \_______/|__/      |_______/ |__/ \______/ |__/  |__/      |______/|__/ \______/ 

\n
"""

version_text_rich = f"""\n\n
[#6699cc]  /$$$$$$                                         [/#6699cc][medium_purple2] /$$$$$$$  /$$     /$$[/medium_purple2]                                                                    
[#6699cc] /$$__  $$                                        [/#6699cc][medium_purple2]| $$__  $$|  $$   /$$/[/medium_purple2]                                                                    
[#6699cc]| $$  \__/ /$$   /$$  /$$$$$$   /$$$$$$   /$$$$$$ [/#6699cc][medium_purple2]| $$  \ $$ \  $$ /$$/ [/medium_purple2]                                                                    
[#6699cc]|  $$$$$$ | $$  | $$ /$$__  $$ /$$__  $$ /$$__  $$[/#6699cc][medium_purple2]| $$$$$$$/  \  $$$$/  [/medium_purple2]                                                                    
[#6699cc] \____  $$| $$  | $$| $$  \ $$| $$$$$$$$| $$  \__/[/#6699cc][medium_purple2]| $$____/    \  $$/   [/medium_purple2]                                                                    
[#6699cc] /$$  \ $$| $$  | $$| $$  | $$| $$_____/| $$      [/#6699cc][medium_purple2]| $$          | $$    [/medium_purple2]                                                                    
[#6699cc]|  $$$$$$/|  $$$$$$/| $$$$$$$/|  $$$$$$$| $$      [/#6699cc][medium_purple2]| $$          | $$    [/medium_purple2]                                                                    
[#6699cc] \______/  \______/ | $$____/  \_______/|__/      [/#6699cc][medium_purple2]|__/          |__/    [/medium_purple2]                                                                    
                    [#6699cc]| $$ [/#6699cc]                                                                                                                   
                    [#6699cc]| $$ [/#6699cc]                                                                                                                   
                    [#6699cc]|__/ [/#6699cc]                                                                                                                  
                                [grey70] /$$    /$$                              /$$                           /$$        /$$$$$$  [/grey70]
                                [grey70]| $$   | $$                             |__/                         /$$$$       /$$$_  $$ [/grey70]
                                [grey70]| $$   | $$ /$$$$$$   /$$$$$$   /$$$$$$$ /$$  /$$$$$$  /$$$$$$$     |_  $$      | $$$$\ $$ [/grey70]
                                [grey70]|  $$ / $$//$$__  $$ /$$__  $$ /$$_____/| $$ /$$__  $$| $$__  $$      | $$      | $$ $$ $$ [/grey70]
                                [grey70] \  $$ $$/| $$$$$$$$| $$  \__/|  $$$$$$ | $$| $$  \ $$| $$  \ $$      | $$      | $$\ $$$$ [/grey70]
                                [grey70]  \  $$$/ | $$_____/| $$       \____  $$| $$| $$  | $$| $$  | $$      | $$      | $$ \ $$$ [/grey70]
                                [grey70]   \  $/  |  $$$$$$$| $$       /$$$$$$$/| $$|  $$$$$$/| $$  | $$     /$$$$$$ /$$|  $$$$$$/ [/grey70]
                                [grey70]    \_/    \_______/|__/      |_______/ |__/ \______/ |__/  |__/    |______/|__/ \______/  [/grey70]
\n\n                                
"""
