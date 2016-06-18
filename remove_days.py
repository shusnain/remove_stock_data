import pandas as pd
import numpy as np
import vincent
import math
import sys
from scipy.stats import gmean

args = sys.argv

def adjusted_returns(start, pct_df):
	prices = [start]
	prev = start
	for p in pct_df[1:]:
		new = prev*(1+p)
		prices.append(new)
		prev = new
	return prices

def remove_n_values(df, n, best_worst):
	if best_worst == 'best' or best_worst == 'both':
		df = df.sort_values('pct_change').head(len(df) - n)
	if best_worst == 'worst' or best_worst == 'both':
		df = df.sort_values('pct_change').tail(len(df) - n)
	df = df.sort_values('Date', ascending=True)
	return df

df = pd.read_csv(args[1])
df.Date = pd.DatetimeIndex(df.Date)
df = df.sort_values('Date', ascending=True)
start_price = df.Open.iloc[0]
pct_change = df.Open.pct_change()
df['pct_change'] = pct_change
df = df.fillna(0)
# drops_both = PrettyTable(['Index', 'Value'])
# drops_best = PrettyTable(['Index', 'Value'])
# drops_worst = PrettyTable(['Index', 'Value'])
drops_both = []
drops_best = []
drops_worst = []
for i in range(0,100):
	best_worst =['best', 'worst', 'both']
	for j in best_worst:
		temp_df = df
		df_removed_values = remove_n_values(df, i, j)
		prices = adjusted_returns(start_price, df_removed_values['pct_change'])
		prices_df = pd.DataFrame({'Open': prices, 'Date': df_removed_values['Date']})
		grouped_prices_df = prices_df.groupby(prices_df['Date'].map(lambda x: x.year))
		first_day_prices = grouped_prices_df.first()
		first_day_prices_per_diff = first_day_prices.Open.pct_change().dropna()
		first_day_prices['pct_change'] = first_day_prices_per_diff
		first_day_prices = first_day_prices.dropna()
		returns = first_day_prices['pct_change'].values.tolist()
		returns_1 = [x + 1 for x in returns]
		average = gmean(returns_1) - 1
		if j == 'best':
			drops_best.append(average)
		if j == 'worst':
			drops_worst.append(average)
		if j == 'both':
			drops_both.append(average)

drops = {'best': drops_best, 'worst': drops_worst, 'both': drops_both}
df_data = pd.DataFrame(drops)

ax = df_data.plot()
fig = ax.get_figure()
fig.savefig('figure.pdf')

chart = vincent.Line(df_data)
chart.axis_titles(x='Number of Days Dropped', y='Annual Return')
chart.legend(title='Legend')
chart.axes['y'].title_offset = 50
chart.scales['color'].range = 'category10'
chart.to_json('./chart.json')