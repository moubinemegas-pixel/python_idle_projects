from sklearn.linear_model import LogisticRegression
import numpy as np
x=np.array([[12,2.5],[15,3.0],[45,9.5],[10,2],[50,10.8],[38,8.2]])
y=np.array([0,0,1,0,1,1])
model=LogisticRegression()
model.fit(x,y)
a=float(input("Entrer un ampérage : "))
b=float(input("Entrer la puissance correspondante en kW : "))
new=np.array([[a,b]])
if model.predict(new)==0:
    print("tout est sous contrôle")
elif model.predict(new)==1:
    print("Gonna be bad bro")