import csv
from variable_helper import date_file, cls_file


def read_csv(filename):
    file_handling = open(filename, "r", encoding="utf8")
    if filename == date_file or filename == cls_file:
        csv_reader = csv.reader(file_handling)
        # print(csv_reader.line_num)
        # csv_content = []
        for item in csv_reader:
            # print(len(item))
            if len(item) == 0:
                file_handling.close()
                return False
            else:
                # csv_content.append(item[0])
                new_item = item[0]
                file_handling.close()
                return new_item
        # return csv_content[0]
    else:
        csv_dicts = csv.DictReader(file_handling)
        csv_content = []
        for dict in csv_dicts:
            csv_content.append(dict)
        file_handling.close()
        return csv_content


def rewrite_csv(filename, line: str):
    file_handling = open(filename, "w", newline="", encoding="utf8")
    writer = csv.writer(file_handling)
    writer.writerow(line)
    file_handling.close()


def write_to_csv(filename, lines: tuple):
    file_handling = open(filename, "a", newline="", encoding="utf8")
    writer = csv.writer(file_handling)
    writer.writerow(lines)
    file_handling.close()


def get_updated_list_of_dicts_storage(
    product_name, quantity, nearest_exp_date, list_of_dicts, is_bought
):
    new_list_of_dicts = list_of_dicts
    new_quantity = 0
    for item in new_list_of_dicts:
        # print(item)
        if item["product_name"] == product_name:
            new_quantity = (
                int(item["stock"]) + int(quantity)
                if is_bought
                else int(item["stock"]) - int(quantity)
            )
            item["stock"] = new_quantity
            item["nearest_exp_date"] = nearest_exp_date
    return new_list_of_dicts


def get_updated_list_of_dicts_bought(quantity, list_of_dicts, bought_id):
    new_list_of_dicts = list_of_dicts
    new_quantity = 0
    for item in new_list_of_dicts:
        # print(item)
        if item["bought_id"] == bought_id:
            new_quantity = int(item["left_quantity"]) - int(quantity)
            item["left_quantity"] = new_quantity
    return new_list_of_dicts


def get_csv_as_list_of_dicts(filename):
    file_handler = open(filename, "r", encoding="utf-8")
    csv_dicts = csv.DictReader(file_handler)
    list_of_dicts = []
    for dict in csv_dicts:
        list_of_dicts.append(dict)
    file_handler.close()
    return list_of_dicts
