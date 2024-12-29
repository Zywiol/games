from datetime import datetime
import pandas as pd

df = pd.read_csv('games.csv')

df['release_date'] = pd.to_datetime(df['release_date'],errors='coerce',format='%Y-%m-%d')
df['release_month'] = df['release_date'].dt.month
df['release_year'] = df['release_date'].dt.year

print(df.columns)

dict_platform = {
    'PC (Windows)':'PC',
    'Web Browser':'Web Browser',
    'PC (Windows), Web Browser':'Both'
}

df['platform'] = df['platform'].map(dict_platform)


def data():
    return df

