import csv
from variable_helper import date_file, cls_file
from variable_helper import storage_file, storage_columns, bought_file, bought_columns, sold_file, sold_columns, product_range_file, product_range_columns
from variable_helper import backup_bought_file, backup_sold_file, backup_storage_file, backup_product_range_file
import date_handlers
from rich.prompt import Confirm

# read and return data from csv file
def read_csv(filename):
    try:
        file_handling = open(filename, "r", encoding="utf8")
        if filename == date_file or filename == cls_file:
            csv_reader = csv.reader(file_handling)
            for item in csv_reader:
                if len(item) == 0:
                    file_handling.close()
                    return False
                else:
                    new_item = item[0]
                    file_handling.close()
                    return new_item
        else:
            csv_dicts = csv.DictReader(file_handling)
            csv_content = []
            for dict in csv_dicts:
                csv_content.append(dict)
            file_handling.close()
            return csv_content
    except:
        return print(f"Something went wrong, please check csv filenames")


# existing data in csv file will be replaced
def rewrite_csv(filename, line: str):
    try:
        file_handling = open(filename, "w", newline="", encoding="utf8")
        writer = csv.writer(file_handling)
        writer.writerow(line)
        file_handling.close()
    except:
        return print(f"Something went wrong, please check csv filenames")



def write_to_csv(filename, lines: tuple):
    try:
        file_handling = open(filename, "a", newline="", encoding="utf8")
        writer = csv.writer(file_handling)
        writer.writerow(lines)
        file_handling.close()
    except:
        return print(f"Something went wrong, please check csv filenames")


# updates and returns data from storage csv file
def get_updated_list_of_dicts_storage(product_name, quantity, nearest_exp_date, list_of_dicts, is_bought):
    new_list_of_dicts = list_of_dicts
    new_quantity = 0
    try:
        for item in new_list_of_dicts:
            if item["product_name"] == product_name:
                new_quantity = (
                    int(item["stock"]) + int(quantity)
                    if is_bought
                    else int(item["stock"]) - int(quantity)
                )
                item["stock"] = new_quantity
                item["nearest_exp_date"] = nearest_exp_date
        return new_list_of_dicts
    except:
        return print(f"Something went wrong, please check csv filenames")     


# updates and returns data from bought csv file
def get_updated_list_of_dicts_bought(quantity, list_of_dicts, bought_id):
    new_list_of_dicts = list_of_dicts
    new_quantity = 0
    try:
        for item in new_list_of_dicts:
            if int(item["bought_id"]) == int(bought_id):
                new_quantity = int(item["left_quantity"]) - int(quantity)
                item["left_quantity"] = new_quantity
        return new_list_of_dicts
    except:
        return print(f"Something went wrong, please check csv filenames")


# returns data from csv file as a list of dictionaries
def get_csv_as_list_of_dicts(filename):
    try:
        file_handler = open(filename, "r", encoding="utf-8")
        csv_dicts = csv.DictReader(file_handler)
        list_of_dicts = []
        for dict in csv_dicts:
            list_of_dicts.append(dict)
        file_handler.close()
        return list_of_dicts
    except:
        return print(f"Something went wrong, please check csv filenames")
    

# function for updating storage csv file
def update_storage(product_name, quantity, is_bought, bought_id):
    storage_list_of_dicts = get_csv_as_list_of_dicts(storage_file)
    new_exp_date = date_handlers.get_nearest_exp_date(product_name)
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
        bought_updated_list_of_dicts = get_updated_list_of_dicts_bought(quantity, bought_list_of_dicts, bought_id)
        with open(bought_file, "w", newline="", encoding="utf8") as file_handler:
            headers = [column["column_name"] for column in bought_columns]
            csv_writer = csv.DictWriter(file_handler, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerows(bought_updated_list_of_dicts)
            file_handler.close()


# function to write headers to csv files when first product is bought
def write_headers(backup: bool = False):
    storage_headers = tuple([item['column_name'] for item in storage_columns])
    bought_headers = tuple([item['column_name'] for item in bought_columns])
    sold_headers = tuple([item['column_name'] for item in sold_columns])
    product_range_headers = tuple([item['column_name'] for item in product_range_columns])

    if backup:
        print("writing headers to backup files...")
        rewrite_csv(backup_storage_file, storage_headers)
        rewrite_csv(backup_bought_file, bought_headers)
        rewrite_csv(backup_sold_file, sold_headers)
        rewrite_csv(backup_product_range_file, product_range_headers)
    else:
        write_to_csv(storage_file, storage_headers)
        write_to_csv(bought_file, bought_headers)
        write_to_csv(sold_file, sold_headers)
        write_to_csv(product_range_file, product_range_headers)
    

# function to write data to backup files
def backup_data():
    # ask user for confirmation
    confirm_text = f"""\n
    Are you sure you want to backup your data?
    All previous data in backup files will be overwritten!\n
    """
    are_you_sure = Confirm.ask(confirm_text)
    if not are_you_sure:
        return

    # first write headers
    write_headers(backup=True)

    # get data from csv files
    bought_data = read_csv(bought_file)
    sold_data = read_csv(sold_file)
    storage_data = read_csv(storage_file)
    product_range_data = read_csv(product_range_file)
    
    # put data as dicts in backup list
    backup_list = []
    backup_list.append({"bought":bought_data})
    backup_list.append({"sold":sold_data})
    backup_list.append({"storage":storage_data})
    backup_list.append({"product_range":product_range_data})
    
    # iterate through list and add data to backup files
    for data_dict in backup_list:
        dict_key = [key for key, _ in data_dict.items()][0]
        datalist = [value for _, value in data_dict.items()][0]
        for line_dict in datalist:
            line_list = []
            for value in line_dict.values():
                line_list.append(value)
            line_tuple = tuple(line_list)
            if dict_key == "bought":
                print(f"Writing data to {backup_bought_file}")
                write_to_csv(backup_bought_file,line_tuple)
            if dict_key == "sold":
                print(f"Writing data to {backup_sold_file}")
                write_to_csv(backup_sold_file,line_tuple)
            if dict_key == "storage":
                print(f"Writing data to {backup_storage_file}")
                write_to_csv(backup_storage_file,line_tuple)
            if dict_key == "product_range":
                print(f"Writing data to {backup_product_range_file}")
                write_to_csv(backup_product_range_file,line_tuple)
