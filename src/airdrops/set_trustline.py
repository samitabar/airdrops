import sys
import os
import time


from xrpy import Wallet, JsonRpcClient, set_trust_line

from constants import XRPL_FOUNDATION
from csv_func import WalletCSV
from utils import Report


XRP_MAIN_CLIENT = JsonRpcClient(XRPL_FOUNDATION)
report = Report()


def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        pass


def mass_trust_line(path_to_csv: str, currency: str, value: int, issuer: str, sleep_time: int = 0, debug: bool = False):
    print(f'{path_to_csv=} | {currency=} | {value=} | {issuer=} | {debug=}')

    wallet_csv = WalletCSV(path_to_csv)
    wallet_data = wallet_csv.get_all_csv_info()[1:]

    if debug:
        print(f'{len(wallet_data)} wallets imported')

    for data in wallet_data:
        if debug:
            print(f'{data}')

        wallet = Wallet(data[wallet_csv.seed_index], data[wallet_csv.sequence_index])

        try:
            _trust_line = set_trust_line(XRP_MAIN_CLIENT, wallet, currency, str(value), issuer)

            if _trust_line and (_trust_line.result.get("meta").get("TransactionResult")) == 'tesSUCCESS':
                report.add_success()

                if debug:
                    print(_trust_line.result.get("meta").get("TransactionResult"))

                time.sleep(sleep_time)
            else:
                report.add_failed()
                if debug:
                    print(f'Failed: [Unknown Error]')
                continue

        except Exception as e:
            report.add_failed()
            print(f'{e}')
            continue


def enter():
    path_to_csv = input('Enter path to csv file: ')

    currency = input('Enter currency: ')

    try:
        value = int(input('Enter value: '))
    except ValueError:
        sys.exit('Value must be an integer')

    issuer = input('Enter issuer: ')

    try:
        sleep_time = int(input('Enter sleep time: '))
    except ValueError:
        sys.exit('Sleep time must be an integer')

    if sleep_time < 0:
        sys.exit('Invalid sleep time')

    _debug = input('Debug? (y/n): ') or 'y'

    if _debug.lower() == 'y':
        debug = True
    elif _debug.lower() == 'n':
        debug = False
    else:
        sys.exit('Invalid debug')

    clear()

    mass_trust_line(path_to_csv, currency, value, issuer, sleep_time, debug)

    print('\n\n')
    print(report.get_report())


if __name__ == '__main__':
    enter()