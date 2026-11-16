import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import pandas as pd
gk=pd.read_csv('puissance_éolienne.csv')
x=gk[['Vitesse','angle']].values
y=gk['puissance_générée']
x=np.array([[12.5,15.0],[14.0,12.0],[4.5,45.0],[15.5,10.0],[11.0,18.0],[3.8,50.0],[13.2,14.0],[5.2,40.0],[16.0,8.0],[10.5,20.0],[12.0,16.0],[6.0,35.0]])

y=np.array([450, 520, 50, 580, 390, 30, 480, 70, 610, 360, 420, 90])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)
model=LinearRegression()
model.fit(x_train, y_train)
b=cross_val_score(model, x_train, y_train, cv=3)
print('moyenne R au carré c-à-d score de précision = ',b.mean())
score=model.score(x_test, y_test)
mse=mean_squared_error(y_test, model.predict(x_test))
print('score selon test gen: ',score)
print('mse selon test gen: ',mse)

