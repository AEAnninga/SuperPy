from rich import box
from rich.table import Table
from variable_helper import *


def create_table(dict_list, title):

    table = Table(
        title=f"[{blue}]{title}[/{blue}]",
        box=box.ROUNDED,
        show_header=True,
        header_style=blue,
        caption=table_caption,
        show_footer=True
    )

    # dict_list already has floats for revenue and cost
    total_profit = round(sum([(item['revenue'] - item['cost']) for item in dict_list]), 2)
    
    # create table headers (columns) from dict keys
    for key in dict_list[0].keys():
        column_width = 25 if key != "name" else 50
        justify_column = "left" if key == "name" else "center"
        footer_text = "Total profit" if key == "revenue" else ""
        table.add_column(key, justify=justify_column, no_wrap=True, width=column_width, footer=footer_text)

    profit_footer_text = str(total_profit)
    table.add_column("profit", justify="center", no_wrap=True, width=50, footer=profit_footer_text)

    # create rows
    for dict in dict_list:
        bought_id, name, cost, revenue = dict.values()
        profit = round((revenue - cost), 2)
        table.add_row(
            bought_id,
            f"[{text_color}]{name}[/{text_color}]",
            str(cost),
            str(revenue),
            str(profit),
        )

    console.print(table)
