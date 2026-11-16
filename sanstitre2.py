# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 19:51:01 2024

@author: Moubine Mamadou
"""
N=int(input("bonjour de quel nombre voulez-vous la table ? "))
n=int(input("par quel nombre finir? "))
for i in range(N,n,1):
    print(N,"*",i,"=",N*i)