import argparse, csv, sys, pandas
from datetime import date, datetime
from time import sleep
from tabulate import tabulate
from rich import box
from rich.console import Console
from rich.table import Table
from inventory import *
from csv_helper import *
from variable_helper import *


def create_table(dict_list, title):

    table = Table(
        title=f"[{blue}]{title}[/{blue}]",
        box=box.ROUNDED,
        show_header=True,
        header_style=blue,
        caption=f"[blue]Anningast Productions[/blue] [white]\xa9[/white]",
        show_footer=True
    )
    total_profit = sum([(item['revenue'] - item['cost']) for item in dict_list])
    print(total_profit)
    for key in dict_list[0].keys():
        column_width = 25 if key != "name" else 50
        justify_column = "left" if key == "name" else "center"
        footer_text = "Total profit" if key == "revenue" else ""
        table.add_column(key, justify=justify_column, no_wrap=True, width=column_width, footer=footer_text)
    profit_footer_text = str(total_profit)
    table.add_column("profit", justify="center", no_wrap=True, width=50, footer=profit_footer_text)

    for dict in dict_list:
        bought_id, name, cost, revenue = dict.values()
        profit = revenue - cost
        # total_profit.append(profit)
        table.add_row(
            bought_id,
            f"[{text_color}]{name}[/{text_color}]",
            str(cost),
            str(revenue),
            str(profit),
        )
    # table.footer_style(
    #     "",
    #     "",
    #     "",
    #     "Total profit:",
    #     str(sum(total_profit))
    # )

    console.print(table)
