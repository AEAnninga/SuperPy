from csv_helper import read_csv
from variable_helper import bought_file, sold_file, product_range_file, no_products_text
from date_handlers import convert_date
from table_viewer import create_table
import inquirer


def calculate_date_profit(buy_dates, bought_products, sold_products) -> str:
    first_date, second_date = buy_dates
    # create date objects for date comparison     
    first_date_object = convert_date(first_date, False)
    second_date_object = convert_date(second_date, False)
    # try clause if date conversion failed > error message generated by convert_date(), but return will be None
    try:
        if first_date_object > second_date_object:
            latest_date = first_date
            earliest_date = second_date
        if first_date_object < second_date_object:
            latest_date = second_date
            earliest_date = first_date
    except:
        return
    # same date > calculate profit from 1 day/date
    if first_date_object == second_date_object:
        try:
            product_cost = sum([
                round(float(item["cost"]), 2) 
                for item in bought_products 
                if item['buy_date'] == convert_date(first_date)
            ])
            product_revenue = sum([
                round(float(sold_item["revenue"]), 2)
                for sold_item in sold_products
                if sold_item["sell_date"] == convert_date(first_date)
            ])
            return f"\nThe profit on {convert_date(first_date)} is:\n\n{product_revenue - product_cost}\n"
        except:
            return print(no_products_text)
    
    # different date > calculate total profit between the the dates 
    if first_date_object != second_date_object:
        try:
            product_cost = sum([
                round(float(item["cost"]), 2) 
                for item in bought_products 
                if convert_date(item['buy_date'], False) <= convert_date(latest_date, False)
                and convert_date(item['buy_date'], False) >= convert_date(earliest_date, False)
            ])
            product_revenue = sum([
                round(float(sold_item["revenue"]), 2)
                for sold_item in sold_products
                if convert_date(sold_item["sell_date"], False) <= convert_date(latest_date, False)
                and convert_date(sold_item["sell_date"], False) >= convert_date(earliest_date, False) 
            ])
            return f"\nThe profit between {convert_date(earliest_date)} and {convert_date(latest_date)} is:\n\n{product_revenue - product_cost}\n"
        except:
            return print(no_products_text)
        

def calculate_product_profit(bought_products, sold_products, product_range):
        # product choices needed > selection list for user to choose from
        try:
            product_choices = [
                {
                    "product_id": int(item["product_id"]),
                    "product_name": item["product_name"]
                }
                for item in product_range
            ]
        except:
            return print(no_products_text)
        
        questions = [
            inquirer.List('product_name',
                message="Choose product, use up and down arrows to select and press enter",
                choices=[item['product_name'] for item in product_choices],
            ),
        ]
        chosen_product = inquirer.prompt(questions)['product_name']
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
            if item["product_name"] == chosen_product
        ]

        return product_cost



# function for showing/displaying profit 
def show_profit(buy_dates=[], product_profit=False):
    bought_products = read_csv(bought_file)
    sold_products = read_csv(sold_file)
    if len(bought_products) == 0 or len(sold_products) == 0:
        return print(f"\nNo products available, or not enough products (sold) to calculate profit\n") 
    # buy_dates length default is 0 when no dates are given > otherwise exactly 2 dates are required 
    if len(buy_dates) != 0:    
        try:
            profit_message = calculate_date_profit(buy_dates, bought_products, sold_products)
        except:
            return
        
        if len(profit_message) > 0:
            print(profit_message)
        else:
            return
        
    # calculate product profit > table is displayed
    elif product_profit:
        product_range = read_csv(product_range_file)
        product_cost = calculate_product_profit(bought_products, sold_products, product_range)
        if product_cost:
            create_table(product_cost, f"Product profit: {product_cost[0]['name']}")
            return
        else:
            print(f"No profit for this product: {product_cost['name']}")
    # remaining argument from parsed arguments is -op | --overall-profit        
    else:
        try:
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
        except:
            return print(no_products_text)
        create_table(product_cost, "Overall profit")
        # return
