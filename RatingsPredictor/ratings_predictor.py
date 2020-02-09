import pandas as pd
from random import randint
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import numpy as np

ratings = pd.read_csv('ratings_w_box_off.csv', encoding = 'ISO-8859-1')

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(ratings.head())

ratings['Genres'] = ratings['Genres'].astype('category')
ratings['Genres_cat'] = ratings['Genres'].cat.codes

genre_columns = ['Animation', 'Action', 'Comedy', 'Family', 'Sci-Fi', 'Drama', 
			'Romance', 'Crime', 'Thriller', 'Adventure', 'War', 'Mystery', 
			'Biography', 'Sport', 'History', 'Musical', 'Fantasy', 'Music', 
			'Western', 'Horror', 'Documentary', 'Film-Noir', 'Short']

ratings.rename(columns={'Box Office Gross USA':'box_office_gross_usa',
				'Inflation Adjusted Box Office Gross USA':
				'infl_adjusted_box_office_gross_usa'}, inplace=True)

# Fill the 0s in the Box Office columns with the avg box office
box_mean = ratings.box_office_gross_usa.mean()
adj_box_mean = ratings.infl_adjusted_box_office_gross_usa.mean()
for i in range(len(ratings.box_office_gross_usa)):
	if (ratings.box_office_gross_usa.iat[i] == 0):
		ratings.box_office_gross_usa.iat[i] = box_mean
		ratings.infl_adjusted_box_office_gross_usa.iat[i] = adj_box_mean

# Create a new column in ratings for each genre
for i in range(len(genre_columns)):
	ratings[genre_columns[i]] = 0

# Fill each genre column with 1 if the movie is of that genre and
# 0 if the movie is not
for i in range(len(ratings.Genres)):
	for k in range(len(genre_columns)):
		genre1 = genre_columns[k]
		genre2 = ratings.Genres.iat[i]
		if (genre1 in genre2):
			ratings.iloc[i, ratings.columns.get_loc(genre1)] = 1
		else:
			ratings.iloc[i, ratings.columns.get_loc(genre1)] = 0


features = ['IMDb Rating', 'Year', # 'Num Votes', 
			'box_office_gross_usa'] # + genre_columns
X = ratings[features]
y = ratings['Your Rating']

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0)

# Decision tree regressor
# model = DecisionTreeRegressor(random_state=0, max_leaf_nodes=12)
# model.fit(train_X, train_y)
# pred = model.predict(val_X)

# Linear regressor
reg = LinearRegression().fit(train_X, train_y)
pred = reg.predict(val_X)

# print(pred)

rand_ints = []
for i in range(len(pred)):
	rand_ints.append(randint(5, 10))


index = 0
for i in val_y:
	print(i, " ", pred[index], "  ", rand_ints[i])
	index = index + 1


print("pred mae: ", mean_absolute_error(val_y, pred))
print("rand mae: ", mean_absolute_error(val_y, rand_ints))
print(ratings.describe())

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# 	print(ratings.head())


