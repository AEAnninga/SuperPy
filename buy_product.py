from utils import is_float, is_int, create_id, create_product_id
from date_handlers import convert_date, get_working_date
from variable_helper import bought_file, product_range_file, storage_file, no_products_text
from rich.prompt import Confirm
from csv_helper import read_csv, write_to_csv, update_storage, write_headers


def buy_product(args):
    product_name, buy_price, expiration_date, buy_quantity = args.bought
    working_date = convert_date(get_working_date())
    # check price and quantity validity, if so > parse to float and int 
    if is_float(buy_price) and is_int(buy_quantity):
        buy_price = float(buy_price)
        buy_quantity = int(buy_quantity)
    else:
        print(f"Arguments given: {buy_price} and {buy_quantity}")
        return print(f"{buy_price} (buy_price) must be float or int \n{buy_quantity} (buy_quantity) must be integer\n")

    # validation feedback on date is given through convert_date()
    valid_exp_date = convert_date(expiration_date)
    if not valid_exp_date:
        return

    # create data for updating bought and storage files
    left_quantity = buy_quantity
    buy_date = args.used_date
    
    new_date = working_date if buy_date == None else convert_date(buy_date)
    new_id = create_id(bought_file, "bought_id")
    cost = round(float(buy_price) * float(buy_quantity), 2)

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

    # confirm question text
    confirm_text = f"""
    Are you sure you want to buy:\n
    Product name:       {product_name}
    Buy price:          {buy_price}
    Expiration date:    {valid_exp_date}
    Buy quantity:       {buy_quantity}
    Cost:               {cost}\n
    """
    # prompt user to confirm
    are_you_sure = Confirm.ask(confirm_text)
    if not are_you_sure:
        return

    # check for products > if no product is bought yet > write headers to csv files
    products_overview = read_csv(product_range_file)
    if not products_overview:
        print("First product, writing headers to csv file...")
        print("Adding product...")
        write_headers()
    
    # update bought file
    write_to_csv(bought_file, bought_tuple)
    try:
        product_exist = [
            item for item in products_overview if item["product_name"] == product_name
        ]
    except:
        print(no_products_text)
    # if product_exist is empty list > not product_exist equates to True > new product     
    if not product_exist:
        product_id = create_product_id(products_overview)
        new_product_tuple = (product_id, product_name)
        write_to_csv(product_range_file, new_product_tuple)

    storage_products = read_csv(storage_file)
    try:
        product = [item for item in storage_products if item["product_name"] == product_name]
    except:
        print(no_products_text)

    # if list not empty > product found > update product in storage > otherwise add to storage
    if product:
        update_storage(product[0]["product_name"], buy_quantity, True, new_id)
    else:
        storage_tuple = (product_name, buy_quantity, valid_exp_date)
        write_to_csv(storage_file, storage_tuple)
