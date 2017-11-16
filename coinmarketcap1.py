from coinmarketcap import Market
import csv
import time
from datetime import datetime

def collect_data(currency_name, price_list):
    coinmarketcap = Market()
    data = coinmarketcap.ticker(currency_name, limit=3, convert='USD')
    data = data.pop(0)
    now_time = datetime.now()
    now_time = str(now_time.strftime('%Y/%m/%d %H:%M'))
    data_list = [now_time]
    for key, value in data.items():
        if key == 'price_usd':
            value = float(value)
            data_list.append(value)
            if value > price_list[-1]:
                # Här kan vi skapa flera fält för att se till olika lagg
                data_list.append(1)
            else:
                data_list.append(0)
            price_list.append(value)
        elif key == 'price_btc':
            data_list.append(value)
        elif key == '24h_volume_usd':
            data_list.append(value)
        elif key == 'percent_change_1h':
            data_list.append(value)
        elif key == 'percent_change_24h':
            data_list.append(value)
        elif key == 'percent_change_7d':
            data_list.append(value)
    return data_list

def write_data_row(filename,row_data):
    with open(filename, 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(row_data)
        print(row_data)
        f.close()


# Writing csv titles
def initiate(filename):
    titles = ['date', 'price_usd','increased' 'price_btc','24h_volume_usd','percent_change_1h','percent_change_24h','percent_change_7d']
    with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(titles)
            print(titles)
            f.close()

def run_catcher(filename,currency_name):
    initiate(filename)
    price_list = [0]
    for i in range(10000):
        row_data = collect_data(currency_name,price_list)
        write_data_row(filename,row_data)
        time.sleep(300)

#filename = str(date.today())

today = datetime.now()
filename = str(today.strftime('%Y%m%d'))
currency_name = 'bitcoin-cash'
filename+= currency_name
filename+= '.txt'


run_catcher(filename,currency_name)