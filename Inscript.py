import tkinter
#Création de la classe #
class DEMANDEUR:
    def __init__(self,N,P,S,D,L,SM,Pr):
        self.__Nom=N
        self.__Prenom=P
        self.__Sexe=S
        self.__date_de_naissance=D
        self.__Lieu_de_naissance=L
        self.__Situation_matrimoniale=SM
        self.__Profession=Pr
    #Définition des Getters #
    def get_Nom(self):
        return self.__Nom
    def get_Prenom(self):
        return self.__Prenom
    def get_Sexe(self):
        return self.__Sexe
    def get_dete_de_naissance(self):
        return self.__date_de_naissance
    def get_Lieu_de_naissance(self):
        return self.__Lieu_de_naissance
    def get_Situation_matrimoniale(self):
        return self.__Situation_matrimoniale
    def get_Profession(self):
        return self.__Profession
    #definition des setters#
    def set_Nom(self,NewNom):
        self.__Nom=NewNom
    def set_Prenom(self,NewPrenom):
        self.__Prenom=NewPrenom
    def set_Sexe(self,NewSexe):
        self.__Sexe=NewSexe
    def set_date_de_naissance(self,Newdate_de_naissance):
        self.__date_de_naissance=Newdate_de_naissance
    def set_Lieu_de_naissance(self,NewLieu_de_naissance):
        self.__Lieu_de_naissance=NewLieu_de_naissance
    def set_Situation_matrimoniale(self,NewSituation_matrimoniale):
        self.__Situation_matrimoniale=NewSituation_matrimoniale
    def set_Profession(self,NewProfession):
        self.__Profession=NewProfession
    def Infos_Demandeur(self):
        tkinter.Label(text="\t\tInformations du demandeur").pack()
        tkinter.Label(text="Nom")
        tkinter.Label(text=self.get_Nom().get())
        print("Prénoms: ",self.get_Prenom())
        print("Sexe : ",self.get_Sexe())
        print("Date de Naissance: ",self.get_dete_de_naissance())
        print("Lieu de naissance: ",self.get_Lieu_de_naissance())
        print("Situation matrimoniale: ",self.get_Situation_matrimonaile())
        print("Profession: ",self.get_Profession())
    def FICHE_INSCRIPTION(self):
        print("Types de logements disponibles: LT1,LT2,LT3,LT4")
        k=int(input("Votre âge: "))
        i=input("type de logement voulu: ")
        while "LT"+str(1)<=i<='LT'+str(4):
            print("Types de logements disponibles: LT1,LT2,LT3,LT4")
            i=input("type de logement voulu: ")
        if i !='LT1' or i !='LT2' or i !='LT3' or i !='LT4':
            print("Types de logements disponibles: LT1,LT2,LT3,LT4")
            i=input("type de logement voulu: ")
        j=int(input("En combien d'années finaliserez-vous le paiement?: "))
        print("\t\tInformations Personelles")
        print(self.Infos_Demandeur())
        print("Type de Logement choisi: ",i)
        if k<26 or k>66 or j>10:
            print("Rejetée")
        else:
            print("Acceptée")
def Inscription():
    import tkinter
    root=tkinter.Tk()
    root.title("Inscription")
    tkinter.Label(root,text="Votre Nom: ").pack()
    a=tkinter.Entry()
    a.pack()
    tkinter.Label(text="Votre prénoms: ").pack()
    b=tkinter.Entry()
    b.pack()
    tkinter.Label(text="Votre Sexe (M pour masculin,F pour féminin): ").pack()
    c=tkinter.Entry()
    c.pack()
    tkinter.Label(text="Date de naissance (JJ/MM/AAAA): ").pack()
    d=tkinter.Entry()
    d.pack()
    tkinter.Label(text="Lieu de Naissance: ").pack()
    e=tkinter.Entry()
    e.pack()
    tkinter.Label(text="Situation Matrimoniale: ").pack()
    f=tkinter.Entry()
    f.pack()
    tkinter.Label(text="Votre Profession: ").pack()
    g=tkinter.Entry()
    g.pack()
    tkinter.Label(text='Type de Logement voulu').pack()
    h=tkinter.Entry()
    h.pack()
    CLIENT=DEMANDEUR(a,b,c,d,e,f,g)
    def Ras():
         z=open(a.get()+"_"+b.get()+".txt",'a')
         z.write("Nom: "+a.get()+"\nPrénoms: "+b.get()+"\nSexe: "+c.get())
         z.write("\nDate de Naissance: "+d.get()+"\nLieu de Naissance: "+e.get())
         z.write("\nSituation Matrimoniale: "+f.get()+"\nProfession: "+g.get())
         z.close()
    def V�rification():
         root1=tkinter.Tk()
         root1.title("VERIFICATION")
         tkinter.Label(root1,text="Informations du demandeur").pack()
         tkinter.Label(root1,text="Nom: ").pack()
         tkinter.Label(root1,text=a.get()).pack()
         tkinter.Label(root1,text="Prénoms: ").pack()
         tkinter.Label(root1,text=b.get()).pack()
         tkinter.Label(root1,text="Sexe: ").pack()
         tkinter.Label(root1,text=c.get()).pack()
         tkinter.Label(root1,text="Date de Naissance: ").pack()
         tkinter.Label(root1,text=d.get()).pack()
         tkinter.Label(root1,text="Lieu de naissance: ").pack()
         tkinter.Label(root1,text=e.get()).pack()
         tkinter.Label(root1,text="Situation matrimoniale: ").pack()
         tkinter.Label(root1,text=f.get()).pack()
         tkinter.Label(root1,text="Profession: ").pack()
         tkinter.Label(root1,text=g.get()).pack()
         tkinter.Label(root1,text="Validez-vous ces infos?")
         button=tkinter.Button(root1,text="ENREGISTRER",command=Ras)
         button.pack()
    button_kira=tkinter.Button(root,text="Entrée")
    button_kira.config(command=Vérification)
    button_kira.pack()
    root.mainloop()
    return CLIENT
    