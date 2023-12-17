from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/exchange-rate-history/usd-idr').text
soup = BeautifulSoup(url_get,"html.parser")

#find your right key here
table = soup.find_all('table', attrs={'class': 'history-rates-data'})

# Get the table rows
tr_lists = table[0].tbody.find_all('tr')

# Get the table columns
columns = []
for row in tr_lists:
    columns.append(row.find_all('td'))

# Build the columns
date = []
amount_in_rupiah = []
for i in columns:
    try:
        date_temp_1 = i[0].find('a', attrs={'class': 'n'}).text
        amount_temp_1 = i[1].find('span', attrs={'class': 'n'}).text
        date_temp_2 = date_temp_1.replace('-', '')
        amount_temp_2 = amount_temp_1.replace(',', '').replace('$1 = Rp', '')

        # Append to the list
        date.append(date_temp_2)
        amount_in_rupiah.append(amount_temp_2)
    except:
        continue

#insert data wrangling here
# crate the dataframe
dataframe = {'date': date, 
             'amount_in_rupiah': amount_in_rupiah}
df = pd.DataFrame(dataframe)

#Update Dtype
df['date'] = df['date'].astype('datetime64[ns]')
df['amount_in_rupiah']= df['amount_in_rupiah'].astype('float64')

#end of data wranggling 


# cara 1
# @app.route("/")
# def index(): 
	
# 	df['date'] = pd.to_datetime(df['date'])

# 	card_data = plt.plot(df['date'], df['amount_in_rupiah'], marker='o', linestyle='-', color='b')

# 	# generate plot
# 	plt.figure(figsize=(12, 6))
# 	plt.xlabel('Date')
# 	plt.ylabel('Amount in Rupiah')
# 	plt.xticks(rotation=45)
# 	plt.grid(True)
# 	plt.tight_layout()
# 	plt.show()

# 	# Rendering plot
# 	# Do not change this
# 	figfile = BytesIO()
# 	plt.savefig(figfile, format='png', transparent=True)
# 	figfile.seek(0)
# 	figdata_png = base64.b64encode(figfile.getvalue())
# 	plot_result = str(figdata_png)[2:-1]

# 	# render to html
# 	return render_template('index.html',
# 		card_data = card_data, 
# 		plot_result=plot_result
# 		)


# if __name__ == "__main__": 
#     app.run(debug=True)






# cara 2
@app.route("/")
def index(): 
	
	card_data = f'{df["amount_in_rupiah"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (12,6)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)

