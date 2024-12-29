import requests
import pandas as pd


r = requests.get('https://www.freetogame.com/api/games')
data = r.json()
df = pd.DataFrame(data)



save_csv = df.to_csv('games.csv',index=False)

print(df)