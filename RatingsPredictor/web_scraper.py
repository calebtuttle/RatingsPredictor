import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import ssl

urls = pd.read_csv('ratings1.csv', encoding = 'ISO-8859-1')
urls = urls['URL']


def add_num_awards(csv_in, csv_out):
	ratings = pd.read_csv(csv_in, encoding = 'ISO-8859-1')
	ratings['Num Award Wins'] = 0
	ratings['Num Award Wins'].fillna(value=0, inplace=True)
	ratings['Num Award Noms'] = 0
	ratings['Num Award Noms'].fillna(value=0, inplace=True)

	context = ssl._create_unverified_context()

	for i in range(len(urls)):
		url = urls[i] + "awards"

		# Open connection, read html, close connection
		uClient = uReq(url, context=context)
		page_html = uClient.read()
		uClient.close()

		# html parser
		page_soup = soup(page_html, 'html.parser')

		# print(page_soup.body.span)

		title = page_soup.title.get_text()
		print(title)

		# Get the text saying how many wins and nominations the
		# movie received
		header = page_soup.find('div', {'class':'article listo'})
		no_awards_str = "looks like we don't have any Awards"
		if (no_awards_str not in header.get_text()):
			header = header.find('div', {'class':'header'})
			header = header.find('div', {'class':'nav'})
			header = header.find('div', {'class':'desc'})
			header = header.get_text()

			wins_noms = [int(s) for s in header.split() if s.isdigit()]
			num_wins = wins_noms[0]
			num_noms = wins_noms[1]
		else:
			num_wins = 0
			num_noms = 0

		wins_loc = ratings.columns.get_loc('Num Award Wins')
		ratings.iat[i, wins_loc] = num_wins

		noms_loc = ratings.columns.get_loc('Num Award Noms')
		ratings.iat[i, noms_loc] = num_noms

		print("Num wins: ", num_wins)
		print("Num noms: ", num_noms)
		print()
		print('----------------------------------')
		print()

	ratings.to_csv(csv_out)



def add_box_office(csv_in, csv_out):
	ratings = pd.read_csv(csv_in, encoding = 'ISO-8859-1')
	ratings['Box Office Gross USA'] = 0
	ratings['Box Office Gross USA'].fillna(value=0, inplace=True)
	infl_string = 'Inflation Adjusted Box Office Gross USA'
	ratings[infl_string] = 0
	ratings[infl_string].fillna(value=0, inplace=True)

	context = ssl._create_unverified_context()

	for i in range(len(urls)):
		url = urls[i]

		# Open connection, read html, close connection
		uClient = uReq(url, context=context)
		page_html = uClient.read()
		uClient.close()

		# html parser
		page_soup = soup(page_html, 'html.parser')

		# print(page_soup.body.span)

		title = page_soup.title.get_text()
		print(title)
		movie_year = '2020'
		if (not 'TV Series' in title and not 'TV Mini-Series' in title):
			open_paren = title.find('(')
			close_paren = title.find(')')
			movie_year = title[open_paren+1:close_paren]
			print('Year: ', movie_year)

		box_office_gross = page_soup.find('div', {'id':'main_bottom'})
		box_office_gross = box_office_gross.find('div', {'id':'titleDetails'})
		box_office_gross = box_office_gross.findAll('div', {'class':'txt-block'})
		print('num divs: ', len(box_office_gross))
		j = 0
		has_gross_usa = False
		for j in range(4, len(box_office_gross)):
			if ('Gross USA' in box_office_gross[j].get_text()):
				has_gross_usa = True
				break
		if (has_gross_usa):
			box_office_gross = box_office_gross[j].get_text()
			dollar_index = box_office_gross.find('$')
			box_office_gross = box_office_gross[dollar_index + 1:]
			box_office_gross = box_office_gross.replace(',', '')
		else:
			box_office_gross = 0

		t = datetime.now().year - int(movie_year)
		# Inflation adjusted box office gross
		infl_adj_gross = float(box_office_gross) * (pow((1 + 1.84545 / 100), t)) 

		box_off_loc = ratings.columns.get_loc('Box Office Gross USA')
		ratings.iat[i, box_off_loc] = float(box_office_gross)
		ratings.iat[i, box_off_loc + 1] = float(infl_adj_gross)


		# Format numbers to $xxx,xxx,xxx.xx
		infl_adj_gross = '${:,.2f}'.format(infl_adj_gross)
		box_office_gross = '${:,.2f}'.format(float(box_office_gross))

		print("Box office gross: ", box_office_gross)
		print("Box office gross (inflation adjusted): ", infl_adj_gross)
		print()
		print('----------------------------------')
		print()

	ratings.to_csv(csv_out)





add_num_awards('ratings2.csv', 'ratings3.csv')



