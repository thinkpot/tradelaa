from dashboard.models import TickerName
import pandas as pd


def run():
    csv_file = pd.read_csv('EQUITY_L.csv')
    df = pd.DataFrame(csv_file, columns=['SYMBOL', 'NAME OF COMPANY'])
    for index, rows in df.iterrows():
        ticker_name = TickerName.objects.create(symbol=rows['SYMBOL'], name=rows['NAME OF COMPANY'])
        ticker_name.save()
    print("Saved Successfully")