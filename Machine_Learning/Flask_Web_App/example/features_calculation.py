import numpy as np
import pandas as pd
from datetime import date
from sklearn.linear_model import LinearRegression

def doTheCalculation(data):

	data['dayofyear']=(data['dteday']-

    	data['dteday'].apply(lambda x: date(x.year,1,1))

    	.astype('datetime64[ns]')).apply(lambda x: x.days)

	X = np.array(data[['instant','season','yr','holiday','weekday','workingday',

                  	'weathersit','temp','atemp','hum','windspeed','dayofyear']])

	return X


def returnSomething():

	return 200


def get_prediction(df, ls):
	# This is a linear regression object
	linreg = LinearRegression()

	# This is our predictors dataframe
	x = df.drop('SalePrice', axis=1)

	# We fit the model using the predictors
	linreg.fit(x, df['SalePrice'])

	# This is our observation we would like to predict. Initially we use the means of all observations
	# and we overwrite the fields which are provided by the user. i.e. the default of a field
	# is the mean for that field
	pred_x = x.mean().values.reshape(1, -1)

	# Loop through the user provided list of fields and update the list for our observation
	# whenever a field is supplied
	for i in range(len(ls)):
		if ls[i] != '':
			pred_x[0][i] = float(ls[i])

	# Return the predicted Sale Price
	return list(linreg.predict(pred_x))[0]
