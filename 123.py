import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pickle

data=pd.read_csv('assigment 2/iris.csv')
print(data)

# X = feature values, all the columns except the last column
X = data.iloc[:, :-1]
# y = target values, last column of the data frame
y = data.iloc[:, -1]
#Split the data into 80% training and 20% testing
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#Train the model
model = LogisticRegression()
model.fit(x_train, y_train) #Training the model
#Test the model
predictions = model.predict(x_test)
print( classification_report(y_test, predictions) )
print( accuracy_score(y_test, predictions))

pickle.dump(model,open('model.pkl','wb'))
p=model.predict([[5.1,3.5,1.4,0.2]])
print(p[0])
