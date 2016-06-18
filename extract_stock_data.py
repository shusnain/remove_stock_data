from yahoo_finance import Share
from csv import writer

s_p = Share('^GSPC')
s_p_historical = s_p.get_historical('1950-01-01', '2016-06-11')
volume = [stock_data['Volume'] for stock_data in s_p_historical]
symbol = [stock_data['Symbol'] for stock_data in s_p_historical]
adj_close = [stock_data['Adj_Close'] for stock_data in s_p_historical]
high = [stock_data['High'] for stock_data in s_p_historical]
low = [stock_data['Low'] for stock_data in s_p_historical]
date = [stock_data['Date'] for stock_data in s_p_historical]
day_close = [stock_data['Close'] for stock_data in s_p_historical]
day_open = [stock_data['Open'] for stock_data in s_p_historical]

out = open('s_p_data.csv', 'w', newline='')

rows = zip(volume, symbol, adj_close, high, low, date, day_close, day_open)

csv = writer(out)
csv.writerow(['Volume', 'Symbol', 'Adj_Close', 'High', 'Low', 'Date', 'Close', 'Open'])
for row in rows:
	csv.writerow(row)
out.close()

