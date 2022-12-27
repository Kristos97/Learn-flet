# import matplotlib
# import matplotlib.pyplot as plt
import random as rd
import flet
from flet import (
    Page, Text, UserControl,
    Row, TextField, ElevatedButton,
    Column, Container
    )

class NodesCH(UserControl):
    def __init__(self, nb_nodes):
        super().__init__()
        self.nb_nodes = int(nb_nodes) # le nombre total des noeuds
        self.CHs = [] # l'ensemble des Cluster-Head apres un round
        self.nodes = [] # l'ensemble des noeuds signés entre [0..1]
        self.CH_T = [] # l'ensemble des Cluster-Head apres tous les round
        self.viewCH = [] #controls for View
        self.G = [] # l'ensemble des noeuds signés entre [0..1] qui ne sont pas elus prece
        self.r = 0 # Round
        self.p = 0 # [5%..15%] de nombre total des noeuds
        # self.x_ = []
        # self.y_ = []
    
    def round(self):
        self.r+=1
        self.p = int((rd.randint(5,15)*self.nb_nodes)/100)

        # print(f"//////////////////////////////////////////////////\nR={self.r} \nP={self.p}")
    

    def build(self):
        
        #Signature des noeuds entre [0..1]
        for i in range(self.nb_nodes):
            self.nodes.append(rd.random())
        
        # print(self.nodes)
        #Exclure les Cluster-Head elus precedament
        for x in self.nodes :
            if not x in self.CHs :
                self.G.append(x) 
        # print(self.G)
        for i in range(self.nb_nodes*50):
            #Incremente le round et determine aleatoirement le P nombre de noeuds eligible
            self.round()
            self.CHs = []
            while len(self.CHs) < self.p:
                #Choisi au hasard un noeud
                n = rd.choice(self.G) 

                #Calcule T(n)
                Tn = self.p/(1-self.p*(self.r%(1/self.p)))
                
                #Determine le noeud elu
                if n < Tn :
                    self.CHs.append(n)

            self.CH_T.append(self.CHs)
            ndn = len(self.CHs)

            txt0 = f"Round {self.r}"
            txt1 = f"Nombre des noeuds elus :{ndn}"
            txt2 = f"Noeuds elus : {self.CHs}"

            # (x,y) graphe
            # xi = self.r/1000000
            # yi = self.p/1000000
            # self.x_.append(xi)
            # self.y_.append(yi)

            self.viewCH.append(
                    Container(
                       content=Column([Text(value=txt0),Text(value=txt1),Text(value=txt2)]),
                    )
            )
        
        # graphe
        # plt.ylabel("Roundes")
        # plt.xlabel("Nombre des noeuds")
        # plt.plot(self.x_,self.y_)
        # plt.axes([0,10000, 0, 100000])
        # plt.show()

        self.viewX = Column(controls=self.viewCH)



        return self.viewX
 


class viewer(UserControl):
    def btn_click(self, e):
            if f'{self.valIN.value}'.isdigit() and int(self.valIN.value) > 20:
                # self.name = self.valIN.value
                # print(self.valIN.value)
                self.controls.pop()
                self.new_val = NodesCH(self.valIN.value)
                self.valIN.value = ''
                self.valIN.error_text = None
                
                self.tab.controls.append(self.new_val)
                self.controls.append(Column(controls=[self.v1, self.tab]))
        
                self.update()
            else:
                self.valIN.error_text = "Please, enter a correct value"
                self.update()

    def build(self):
        self.tab = []
        self.tab = Column()
        self.valIN = TextField(label="Entrer le nombre total des noeuds > 20", width=350)
        self.v1 = Row(controls=[self.valIN, ElevatedButton("Executer LEACH", on_click=self.btn_click)])
        return Column(controls=[self.v1, self.tab])

def main(page:Page):
    page.title = "LEACH Algorithme"
    page.scroll = "adaptive"
    test = viewer()
    page.add(test)

flet.app(target=main)