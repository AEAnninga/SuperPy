import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import numpy as np
from csv_helper import get_csv_as_list_of_dicts, read_csv
from variable_helper import filenames


# function for plotting a graph with matplotlib > graph shows cost revenue and profit
def plot_graph_profit():
    # get data from csv files
    product_range_items =  read_csv(filenames["product_range"]["name"])
    bought_products = read_csv(filenames["bought"]["name"])
    sold_products = read_csv(filenames["sold"]["name"])

    # check if there are products
    if not product_range_items or len(product_range_items) < 3:
        return print(f"\n Not enough data available to display graph! \n")
    if not bought_products:
        return print(f"\n Not enough data available to display graph! \n")
    if not sold_products:
        return print(f"\n Not enough data available to display graph! \n")

    # create empty list
    data = []

    # create dictionary and add to list data > 
    for item in product_range_items:
        item_cost = sum([float(bought_item['cost']) for bought_item in bought_products if bought_item['product_name'] == item['product_name']])
        item_revenue = sum([float(sold_item['revenue']) for sold_item in sold_products if sold_item['product_name'] == item['product_name']])
        item_profit = item_revenue - item_cost
        new_dict = {
            "product_name": item["product_name"],
            "cost"      : item_cost,
            "revenue"   : item_revenue,
            "profit"    : item_profit,
        }
        data.append(new_dict)
    
    # data for graph
    y = np.arange(len(data))
    width = 0.2
    multiplier = 0
    
    fig, ax = plt.subplots()
    fig.set_size_inches(w=14, h=7)
    fig.set_facecolor("dimgrey")

    # data for labels yticks
    product_names = [item['product_name'] for item in data]

    # data for x axis (horizontal bars)
    finances = {
        "revenue": tuple([float(item["revenue"]) for item in data]),
        "cost": tuple([float(item["cost"]) for item in data]),
        "profit": tuple([float(item["profit"]) for item in data])
    }

    # define max and min x
    max_list = [max(finances["cost"]),max(finances["revenue"]),max(finances["profit"])]
    max_x = max(max_list)
    min_x = min(finances["profit"])

    bar_colors = {
        'revenue':'#6699cc',
        'cost': 'orange',
        'profit': '#15b01a'
    }

    # some data for little text box that shows total profit
    profit_box_facecolor = "red" if sum(finances['profit']) < 0 else "green"
    profit_box_x = 1.01 # * max_x
    profit_box_y = 0.85 # * len(product_names)
    
    # create 3 horizontal bars: revenue, cost, profit > each attribute has amounts of all products > so 7 products means 21 bars grouped per 3
    for attribute, amounts in finances.items():
        offset = width * multiplier
        bars = ax.barh(y + offset, amounts, width, label=attribute, color=bar_colors[attribute])
        ax.bar_label(bars, padding=2, label_type='edge', fontsize=7)
        multiplier += 1

    # set properties (legend, titles, spans, etc.)
    label_pad = max([len(item) for item in product_names]) * -1 # adjust labelpad according to longest product_name
    ax.set_ylabel('Product'.upper(), color="whitesmoke",loc="top",rotation="horizontal", labelpad=label_pad)
    ax.set_xlabel("Euro".upper(), color="whitesmoke",loc='right')
    ax.set_title('Cost, revenue & profit'.upper(), color="whitesmoke",loc="center",fontdict={'fontsize':18,'fontweight':10})
    ax.set_yticks(y + width, product_names)
    ax.set_xlim(min_x*1.25, max_x*1.25)
    ax.axvspan(min_x*1.25,0,0,len(product_names), color="#fec4c478", zorder=-2)
    ax.axvspan(0,max_x*1.25,0,len(product_names), color="#dbfcc791", zorder=-2)
    ax.legend(loc='upper right', bbox_to_anchor=(1.0065, 1.075), fancybox=True, shadow=True, ncol=5)
    # text box with total profit
    total_profit = round(sum(finances['profit']), 2)
    ax.text(profit_box_x, profit_box_y, f"Total profit: {total_profit} ", style='italic', color='whitesmoke', fontsize=8, transform=ax.transAxes,
        bbox={'facecolor': profit_box_facecolor, 'alpha': 0.5, 'pad': 10, 'edgecolor': 'whitesmoke'}
    )
    ax.tick_params(color="whitesmoke")
    plt.setp(ax.spines.values(), color="whitesmoke")
    plt.xticks(color="whitesmoke", fontsize=8)
    plt.yticks(color="whitesmoke", fontsize=8)
   
    plt.show()


def plot_graph(filename):
    # condition for creating or plotting profit graph
    if filename == "profit":
        plot_graph_profit()
        return
    
    list_of_dicts = get_csv_as_list_of_dicts(filenames[filename]["name"])
    if len(list_of_dicts) == 0:
        return print(f"Not enough data available to display graph!")
    
    # conditions for changing quantity_key > quantities needed have different keys depending on which filename is given
    if filename == "storage":
        quantity_key = "stock"
    if filename == "sold":
        quantity_key = "sell_quantity"
    if filename == "bought":
        quantity_key = "buy_quantity"

    # get data from csv file 
    data=[]
    # will be coordinates for x axis
    left_coordinates = []

    # length is number of items >
    for i in range(len(list_of_dicts)):
        coord = i + 1
        left_coordinates.append(coord*10)

    # create dictionary > add to data >            
    for dict in list_of_dicts:
        new_dict = {
            "product_name": dict['product_name'],
            "sell_date" : dict["sell_date"] if filename == "sold" else "",
            "buy_date"  : dict["buy_date"] if filename == "bought" else "",
            "quantity"  : int(dict[quantity_key])
        }
        data.append(new_dict)

    # quantities for horizontal bars
    product_quantities = [item["quantity"] for item in data]

   # set properties, legends, titles etc.
    fig, ax = plt.subplots()
    fig.set_size_inches(w=14, h=7)
    fig.set_facecolor("dimgrey")
    prod = ax.barh(left_coordinates,product_quantities, align='center', height=5, color="#6699cc")
    y_labels = [label["product_name"] for label in data]
    ax.set_yticks(left_coordinates, labels=y_labels)
    ax.invert_yaxis()  
    ax.set_xlabel("Quantity".upper(), loc="right", color="whitesmoke")
    label_pad = max([len(item) for item in y_labels]) * -1 # adjust labelpad according to longest product_name
    ax.set_ylabel("Product".upper(), labelpad=label_pad, loc="top", color="whitesmoke", rotation="horizontal")
    custom_title = f"Products in {filename}".upper() if filename == "storage" else f"{filename} products".upper() 
    ax.set_title(custom_title, color="whitesmoke")
    ax.set_xlim(left=0,right=max(product_quantities)*1.25)
    custom_labels = [
        f" {item['quantity']} ({filename} on {item['sell_date']} {item['buy_date']})" if filename != 'storage' 
        else  f" {item['quantity']}" 
        for item in data
    ]
    ax.bar_label(prod, labels=custom_labels, label_type='edge', fontsize=8)
    # add vertical lines and spans if data comes from storage
    if filename == "storage":
        y_max = len(list_of_dicts)
        ax.axvline(5,0,y_max, dashes=[4,2], color="red",zorder=-1)
        ax.axvspan(0,5,0,y_max, color="#ff929278", zorder=-2, label="Approaching Out of stock")
        ax.axvline(10,0,y_max, dashes=[4,2], color="green", zorder=-1)
        ax.axvspan(5,10,0,y_max, color="#ffd388a3", zorder=-2, label="Time to order product")
        ax.legend()

    ax.tick_params(color="whitesmoke")
    ax.xaxis.set_major_locator(tck.MultipleLocator(5))
    plt.setp(ax.spines.values(), color="whitesmoke")
    plt.xticks(fontsize=8, color="whitesmoke")
    plt.yticks(fontsize=8, color="whitesmoke")

    plt.show()
