from sklearn.linear_model import LogisticRegression
import numpy as np
x=np.array([[45,1.2],[50,1.5],[85,4.8],[42,1.1],[90,5.2],[78,3.9]])
y=np.array([0,0,1,0,1,1])
model=LogisticRegression()
model.fit(x,y)
s=float(input("Enter température :"))
d=float(input("Enter pression moteur : "))
test=np.array([[s,d]])
if model.predict(test)==1:
    print(" Le moteur est en surcharge !")
elif model.predict(test)==0:
    print(" Le moteur est hors de danger, fontionnement normal !")
