# Imports
import argparse, sys
from rich_argparse import RawTextRichHelpFormatter, MetavarTypeRichHelpFormatter, RawDescriptionRichHelpFormatter
from rich.text import Text
from rich import print as RichPrint
from inventory import create_inventory_report, create_all_inventory_reports
from variable_helper import *
from date_handlers import convert_date, get_working_date, print_date_warning, print_date_text, change_working_date
from graph_plotter import plot_graph
from buy_product import buy_product
from sell_product import sell_product
from cost_revenue import show_profit
from utils import toggle_clear_screen, clear_screen

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
# Have working date available, every time the script runs, working date is refreshed
working_date = convert_date(get_working_date())

# create class which combines 3 formatter classes from rich_argparse
class MultipleFormatter(RawTextRichHelpFormatter, RawDescriptionRichHelpFormatter, MetavarTypeRichHelpFormatter):
    pass

# main function for parsing arguments
def main():
    # create ArgumentParser
    parser = argparse.ArgumentParser(
        prog="SuperPy",
        description="Keep track of your supermarket inventory!",
        formatter_class=MultipleFormatter,
        add_help=False,
    )

    # add arguments
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help=help_text,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s 1.0",
        help=version_text,
    )
    parser.add_argument(
        "-report",
        nargs=1,
        dest="report",
        choices=REPORTS.keys(),
        help=reports_help_text,
        type=str,
    )
    parser.add_argument(
        "-graph",
        nargs=1,
        dest="graph",
        choices=GRAPHS.keys(),
        help=graphs_help_text,
        type=str,
    )
    parser.add_argument(
        "-bp",
        "--buy-product",
        nargs=4,
        dest="bought",
        help=buy_product_help_text,
        type=str,
    )
    parser.add_argument(
        "-sp",
        "--sell-product",
        action="store_true",
        dest="sold",
        help=sell_product_help_text,
    )

    # create mutually exclusive group for -ud | --use-date and --today > set required condition first
    buy_sell_group_is_required = "-bp" in sys.argv or "-sp" in sys.argv or "--buy-product" in sys.argv or "--sell-product" in sys.argv
    buy_sell_group = parser.add_mutually_exclusive_group(required=buy_sell_group_is_required)

    # add mutually exclusive arguments to buy_sell_group
    buy_sell_group.add_argument(
        "-ud",
        "--use-date",
        dest="used_date",
        help=use_date_help_text,
        type=str,
    )
    buy_sell_group.add_argument(
        "--today",
        action="store_true",
        dest="today",
        help=today_help_text,
    )

    # arguments
    parser.add_argument(
        "-cd",
        "--change-date",
        action="store_true",
        required="--date" in sys.argv or "--days" in sys.argv,
        dest="change_date",
        help=change_date_help_text,
    )

    # create mutually exclusive group for --days and -date > set required condition first
    change_date_is_required = "-cd" in sys.argv or "--change-date" in sys.argv
    change_date_group = parser.add_mutually_exclusive_group(required=change_date_is_required)

    # add mutually exclusive arguments to change_date_group
    change_date_group.add_argument(
        "--days",
        dest="number_of_days",
        help=days_help_text,
        type=int,
    )
    change_date_group.add_argument(
        "--date",
        dest="wanted_date",
        help=date_help_text,
        type=str,
    )

    # arguments
    parser.add_argument(
        "-dd",
        "--display-date",
        action="store_true",
        dest="display_date",
        help=display_date_help_text,
    )
    parser.add_argument(
        "-rd",
        "--reset-date",
        action="store_true",
        dest="reset_date",
        help=reset_date_help_text,
    )
    parser.add_argument(
        "-profit",
        dest="profit",
        action="store_true",
        help=profit_help_text,
    )

    # create mutually exclusive group for profit filters > set required condition first
    profit_group_is_required = "-profit" in sys.argv
    profit_group = parser.add_mutually_exclusive_group(required=profit_group_is_required)

    # add mutually exclusive arguments to profit_group
    profit_group.add_argument(
        "-op",
        "--overall-profit",
        action="store_true",
        dest="overall_profit",
        help=overall_profit_help_text,
    )
    profit_group.add_argument(
        "-dp",
        "--date-profit",
        nargs=2,
        dest="date_profit",
        help=date_profit_help_text,
        type=str,
    )
    profit_group.add_argument(
        "-pp",
        "--product-profit",
        action="store_true",
        dest="product_profit",
        help=product_profit_help_text,
    )

    # arguments
    parser.add_argument(
        "--toggle-cls",
        action="store_true",
        dest="toggle_cls",
        help=toggle_cls_help_text,
    )
    
    # parse arguments from user
    parsed_args = parser.parse_args()

    # call execute_action with parsed args > execute actions based on arguments
    execute_action(parsed_args)


# function with logic for executing the right actions depending on the arguments
def execute_action(args):
    # function to check if screen must be cleared after each command from th user
    clear_screen()

    # function to print date warning if date is not today
    print_date_warning(args)

    # raise error if no arguments are given > length will be 1 if no arguments are given
    raise_error = len(sys.argv) <= 1

    if not raise_error:
        # actions based on present arguments:
        if args.report:
            if args.report[0] != "all":
                create_inventory_report(args.report[0])
            else:
                create_all_inventory_reports()
        if args.graph:
            plot_graph(args.graph[0])
        if args.bought:
            buy_product(args)
        if args.sold:
            sell_product(args)
        if args.change_date:
            change_working_date(args.number_of_days, args.wanted_date)
            print_date_text(change_text=True)
        if args.display_date:
            print_date_text(display_text=True)
        if args.reset_date:
            change_working_date()
            print_date_text(reset_text=True)
        if args.profit:
            given_buy_dates = args.date_profit
            if not args.date_profit:
                given_buy_dates = []
            show_profit(buy_dates=given_buy_dates, product_profit=args.product_profit)
        if args.toggle_cls:
            toggle_clear_screen()
    else:
        no_args_text = Text(f"\n Please fill in arguments \n For help type: python super.py -h \n",style="bold italic white r")
        RichPrint(no_args_text)


if __name__ == "__main__":
    main()
