import pandas as pd

def get_oil_weekly_prices() -> pd.DataFrame:
	df = pd.read_csv('../Datasets/Oil.csv')
	# converting the date dtype and setting it as index
	df['date'] = pd.to_datetime(df['period_start_date'])
	df = df.set_index('date').sort_index()
	# N/A for public holidays, therefore we forward fill
	df['DCOILWTICO'] = df['DCOILWTICO'].ffill(limit=2)
	weekly = df.resample('W-FRI').last()
	weekly['closing'] = weekly['DCOILWTICO']
	weekly.drop(['DCOILWTICO', 'period_start_date'], axis='columns', inplace=True)
	return weekly

def get_power_consumption() -> pd.DataFrame:
	df = pd.read_parquet("../Datasets/basel-energy-demand.parquet")
	df = df.loc[:, ('timestamp_interval_start', 'stromverbrauch_kwh')]
	df.rename(columns={'stromverbrauch_kwh': 'consumptions(kWh)', 'timestamp_interval_start': 'time'}, inplace=True)
	df['time'] = pd.to_datetime(df['time'])
	df = df.set_index('time')
	return df