import inquirer
from rich.prompt import Confirm
from csv_helper import read_csv, write_to_csv, update_storage
from variable_helper import no_products_text, no_products_to_sell_text, bought_file, sold_file, storage_file
from date_handlers import convert_date, get_working_date
from utils import is_valid_sell_price, is_valid_sell_quantity, create_id



def sell_product(args):
    bought_products = read_csv(bought_file)
    storage_products = read_csv(storage_file)
    working_date = convert_date(get_working_date())
    try:
        product_choices = [
            {
                item['product_name'] : [
                    {
                    "bought_id": int(subitem["bought_id"]),
                    "product_name": subitem["product_name"],
                    "left_quantity": subitem["left_quantity"],
                    "buy_price": subitem["buy_price"]
                    }
                    for subitem in bought_products
                    if int(subitem['left_quantity']) != 0
                    and subitem['product_name'] == item['product_name']
                ]
            }
            for item in storage_products
            if item['stock'] != 0
        ]
    except:
        return print(no_products_text)
    
    if len(product_choices) < 1:
        return print(no_products_to_sell_text)
    
    # get user input > product and sell_price
    product_choice = [
        inquirer.List('product',
            message="Choose product, use up and down arrows to select",
            choices=[list(item.keys())[0] for item in product_choices],
            carousel=True
        ),
    ]
    chosen_product = inquirer.prompt(product_choice)['product']
    chosen_product_with_bought_ids = []
    for item in product_choices:
        if list(item.keys())[0] == chosen_product:
            chosen_product_with_bought_ids = item[chosen_product]

    nested_product_choice = [
        inquirer.List('nested_product',
            message="Choose batch, use up and down arrows to select",
            choices=chosen_product_with_bought_ids,
            carousel=True
        ),
    ]
    nested_product = inquirer.prompt(nested_product_choice)['nested_product']
    bought_id = nested_product['bought_id']
    if not bought_id:
        return

    # get product_to_sell with bought_id  
    product_to_sell = [item for item in bought_products if int(item["bought_id"]) == int(bought_id)][0]
    
    # separate question for sell_price > display bought_price to user (via nested_product or product_to_sell)
    bought_price = nested_product["buy_price"]
    sell_price_question = {inquirer.Text('sell_price', message=f"Sell price ( bought for {bought_price} )", validate=lambda _, price:  is_valid_sell_price(price))}
    input_sell_price = inquirer.prompt(sell_price_question)
    sell_price = input_sell_price['sell_price']

    # separate question for quantity > display left_quantity as max when prompting user 
    max_sell_quantity = nested_product["left_quantity"]
    quantity_question = {inquirer.Text("sell_quantity", message=f"Sell quantity (max is {max_sell_quantity})", validate=lambda _, sell_quantity:  is_valid_sell_quantity(sell_quantity,max_sell_quantity))}
    chosen_quantity = inquirer.prompt(quantity_question)
    sell_quantity = chosen_quantity['sell_quantity']

    # create data for updating storage and sold files
    sell_date = args.used_date
    today = args.today
    new_id = create_id(sold_file, "sell_id")
    new_date = (working_date if today else convert_date(sell_date))  # datetime.fromisoformat(sell_date).date()
    revenue = round((float(sell_quantity) * float(sell_price)), 2)
    sold_tuple = (
        new_id,
        bought_id,
        product_to_sell["product_name"],
        new_date,
        sell_price,
        sell_quantity,
        revenue,
    )
    # confirm question text
    confirm_text = f"""
    Are you sure you want to sell:\n
    Product name:     {nested_product['product_name']}
    Bought id:        {bought_id}
    Sell price:       {sell_price}
    Sell quantity:    {sell_quantity}
    Revenue:          {revenue}\n
    """
    # prompt user to confirm
    are_you_sure = Confirm.ask(confirm_text)
    if not are_you_sure:
        return
    # update storage > storage.csv and bought.csv
    update_storage(nested_product["product_name"], sell_quantity, False, bought_id)
    # write sold item to sold.csv
    write_to_csv(sold_file, sold_tuple)

