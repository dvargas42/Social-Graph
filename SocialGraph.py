import DiGraph
import networkx as nx
#import pylab as plt
import matplotlib.pyplot as plt

try:
    from Tkinter import *
    from Tkinter import ttk
    from Tkinter.filedialog import askopenfilename
    import tkMessageBox

except:
    from tkinter import *
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
    from tkinter import messagebox


class App:

    def __init__(self, window):
        self.window = window
        self.window.title("Social Graph")
        self.window.geometry("900x700")
        # Tornar a janela não redimensionavel
        self.window.resizable(False,False)
        # Criar Grafo dirigido
        self.graph = nx.DiGraph()
        self.sg = SocialGraph()
        self.weight = ["",1,2,3,4,5]
        self.vertex = "Vertices: " + str(self.sg.dg.numVertices())

        myColor1 = "#3a3b3e"
        myColor2 = "#0093dd"

        self.createTabs()
        self.widgetsTab1()
        self.widgetsTab2()
        self.widgetsTab3()
        self.widgetsWindow()


    def createTabs(self):
        tabControl = ttk.Notebook(window)
        #Adicionando cada Aba ao Frame
        self.tab1 = Frame(tabControl)
        self.tab2 = Frame(tabControl)
        self.tab3 = Frame(tabControl)

        tabControl.add(self.tab1, text="Adicionar Relacionamentos")
        tabControl.add(self.tab2, text="Recomendações de Amigos")
        tabControl.add(self.tab3, text="Remover Pessoas")
        tabControl.pack(expand=2, fill='both')


    def widgetsWindow(self):
        # ListBox apresentando um histórico de comandos gerados
        lb2W = Label(self.window, text=" Amigos Recomendados", font="Arial 10 bold")
        lb2W.place(width=150, y=28, x=5)

        self.lbox2W = Listbox(self.window)
        self.lbox2W.place(width=150, height=150, y=60, x=5)

        self.sbar2W = Scrollbar(self.window, command=self.lbox2W.yview)
        self.sbar2W.place(height=150, y=60, x=155)
        #Label Histório de Comandos
        lb1W = Label(self.window, text="Histórico de Comandos", font="Arial 10 bold")
        lb1W.place(height=20, x=5, y=220)
        #listbox do Histórico de Comandos
        self.lbox1W = Listbox(self.window)
        self.lbox1W.place(width=150, height=440, y=250, x=5)
        #ScrolBar do ListBox Histórico de Comandos
        self.sbar1W = Scrollbar(self.window, command=self.lbox1W.yview)
        self.sbar1W.place(height=440, y=250, x=155)

        # Label do mapa de Relacionamento
        lb3W = Label(self.window, text="Mapa de Relacionamentos", font="Arial 11 bold")
        lb3W.place(height=20, y=200, x=450)
        #imagem ue será inserida na label
        self.img = PhotoImage(file="Null.png")
        self.lbImgW = Label(self.window, image=self.img)
        self.lbImgW.place(y=230, x=240)
        #label que representa o número de aresta do grafo
        self.lb4W = Label(self.window, text="Número de Arestas: 0")
        self.lb4W.place(height=30, y=665, x=520)
        #Label que representa o número de vértices de grafo
        self.lb5W = Label(self.window, text="Número de Vertices: 0")
        self.lb5W.place(height=30, y=665, x=680)


    def widgetsTab1(self):
        self.varOp1T1 = StringVar(self.tab1)
        self.varOp1T1.set(self.weight[0])

        # Label Adicionar Lista
        lb1T1 = Label(self.tab1, text="Adicionar Lista", font="Arial 10 bold")
        lb1T1.place(height=20, y=5, x=180)

        #label Local do Arquivo
        lb1T1 = Label(self.tab1, text='Local do Arquivo: ')
        lb1T1.place(height=20, y=35, x=180)

        #Entry para campo de preenchimento do local de arquivo
        self.ent1T1 = Entry(self.tab1, width=150)
        self.ent1T1.place(width=410, height=25, y=35, x=300)

        #Botão Pesquisar para procurar arquivos
        bt1T1 = Button(self.tab1, text="Pesquisar", command=self.fileOpen)
        bt1T1.place(width=80, height= 25, y=35, x=720)

        #Botão para inserir
        bt2T1 = Button(self.tab1, text="Inserir", command=self.setListBox)
        bt2T1.place(width=80, height=25, y=35, x=800)

        #Label Adicionar amigos
        lb2T1 = Label(self.tab1, text="Adicionar Relacionamento", font="Arial 10 bold")
        lb2T1.place(height=20, y=75, x=180)

        #Label Pessoa
        lb3T1 = Label(self.tab1, text='Pessoa: ')
        lb3T1.place(height=20, y=105, x=245)

        #Campo para inserir pessoa
        self.ent2T1 = Entry(self.tab1, width=150)
        self.ent2T1.place(width=90, height=25, y=105, x=300)

        #Label Amigo
        lb4T1 = Label(self.tab1, text='Amigo: ')
        lb4T1.place(height=20, y=105, x=405)

        self.ent3T1 = Entry(self.tab1, width=150)
        self.ent3T1.place(width=80, height=25, y=105, x=460)

        lb5T1 = Label(self.tab1, text='Afinidade: ')
        lb5T1.place(height=20, y=105, x=560)

        #self.ent4T1 = Entry(self.tab1, width=150)
        #self.ent4T1.place(width=80, height=25, y=105, x=630)

        self.ent4T1 = OptionMenu(self.tab1, self.varOp1T1, *self.weight)
        self.ent4T1.config(relief="groove")
        self.ent4T1.place(width=80, height=30, y=105 - 2, x=630)

        self.bt3T1 = Button(self.tab1, text="Trocar", command=self.invertPeople)
        self.bt3T1.place(width=80, height=25, y=105, x=720)

        bt4T1 = Button(self.tab1, text="Inserir", command=self.insertEdge)
        bt4T1.place(width=80, height=25, y=105, x=800)


    def widgetsTab2(self): #Aba Recomendação de Amigos
        hTitle = 5
        hGeneral = hTitle + 30
        options = ("", "dist", "weightedDist")
        self.varOp1T2 = StringVar(self.tab2)
        self.varOp1T2.set(options[0])  # Valor default
        self.varOp2T2 = StringVar(self.tab2)
        self.varOp2T2.set(self.weight[0])

        #Label Recomendação de Amigos
        lb1T2 = Label(self.tab2, text="Recomendação de Amigos", font="Arial 10 bold")
        lb1T2.place(height=20, y=hTitle, x=180)

        #Label Pessoa
        lb2T2 = Label(self.tab2, text='Pessoa: ')
        lb2T2.place(height=20, y=hGeneral, x=245)

        #Entry
        self.ent1T2 = Entry(self.tab2, width=150)
        self.ent1T2.place(width=90, height=25, y=hGeneral, x=300)

        lb3T2 = Label(self.tab2, text='Opção: ')
        lb3T2.place(height=20, y=hGeneral, x=395)

        self.op1T2 = OptionMenu(self.tab2, self.varOp1T2, *options)
        self.op1T2.config(relief="groove")
        self.op1T2.place(width=120, height=30, y=hGeneral - 2, x=445)

        lb3T2 = Label(self.tab2, text='Afinidade: ')
        lb3T2.place(height=20, y=hGeneral, x=570)

        self.op2T2 = OptionMenu(self.tab2, self.varOp2T2, *self.weight)
        self.op2T2.config(relief="groove")
        self.op2T2.place(width=90, height=30, y=hGeneral - 2, x=640)

        bt1T2 = Button(self.tab2, text="Executar", command=self.recommendFriends)
        bt1T2.place(width=85, height=25, y=hGeneral, x=740)

        lb4T2 = Label(self.tab2, text="Menor Caminho", font="Arial 10 bold")
        lb4T2.place(height=20, y=75, x=180)

        lb5T2 = Label(self.tab2, text='Pessoa: ')
        lb5T2.place(height=20, y=105, x=245)

        self.ent2T2 = Entry(self.tab2)
        self.ent2T2.place(width=90, height=25, y=105, x=300)

        lb6T2 = Label(self.tab2, text='Alvo: ')
        lb6T2.place(height=20, y=105, x=400)

        self.ent3T2 = Entry(self.tab2)
        self.ent3T2.place(width=90, height=25, y=105, x=445)

        bt2T2 = Button(self.tab2, text="Executar", command=self.shortestPath)
        bt2T2.place(width=85, height=25, y=105, x=550)

        self.lb7T2 = Label(self.tab2, text='ShotestPath: None')
        self.lb7T2.place(height=20, y=145, x=215)


    def widgetsTab3(self):

        lb1T3 = Label(self.tab3, text="Remover Pessoa", font="Arial 10 bold")
        lb1T3.place(height=20, y=5, x=180)

        lb2T3 = Label(self.tab3, text='Pessoa: ')
        lb2T3.place(height=20, y=35, x=245)

        self.ent1T3 = Entry(self.tab3, width=150)
        self.ent1T3.place(width=160, height=25, y=35, x=300)

        bt1T2 = Button(self.tab3, text="Remover", command=self.removeVertex)
        bt1T2.place(width=80, height=25, y=35, x=470)


    def setListBox(self): #Insere os comandos
        try:
            self.sg.readGraphFile(self.ent1T1.get())
            self.lbox1W.delete(0, 'end') #Apaga o ListBox "Histórico"
            self.makeGraph()
            self.increment()

        except:
            if self.ent1T1.get() == "":
                messagebox.showwarning("Atenção", "Campo 'Pequisar Arquivo' vazio!")
            else:
                messagebox.showerror("Erro", "Extensão de Arquivo errada")


    def fileOpen(self):
        filename = askopenfilename(filetypes=(("text files", "*.txt"), ("all files", "*.*")))  # Permite selecionar um arquivo txt
        self.ent1T1.delete(0, "end")
        self.ent1T1.insert(INSERT, filename)  # Imprime o arquivo selecionado


    def insertEdge(self):
        try:
            temp = open("temp.txt", "w")
            temp.write("add " + str(self.ent2T1.get()) + " " + str(self.ent3T1.get()) + " " + str(self.varOp1T1.get()))
            temp.close()

            self.sg.readGraphFile("temp.txt")
            self.makeGraph()
            self.increment()


        except:
            if (self.ent2T1.get() == "")and(self.ent3T1.get() == "")and(self.varOp1T1.get() == ""):
                messagebox.showwarning("Atenção","Todos os campos estão vazios")
            elif (self.ent2T1.get() == "")and(self.ent3T1.get() == ""):
                messagebox.showwarning("Atenção", "Os campos Pessoa e Amigo estão vazios!")
            elif (self.ent2T1.get() == "")and(self.varOp1T1.get() == ""):
                messagebox.showwarning("Atenção", "Os campos Pessoa e Afinidade estão vazios!")
            elif(self.ent3T1.get() == "")and(self.varOp1T1.get() == ""):
                messagebox.showwarning("Atenção", "Os campos Amigo e Afinidade estão vazios!")
            elif self.ent2T1.get() == "":
                messagebox.showwarning("Atenção", "O campo Pessoa está vazio!")
            elif self.ent3T1.get() == "":
                messagebox.showwarning("Atenção", "O campo Amigo está vazio!")
            elif self.varOp1T1.get() == "":
                messagebox.showwarning("Atenção", "O campo Afinidade está vazio!")


    def removeVertex(self):
        try:
            temp = open("temp.txt", "w")
            temp.write("remove " + str(self.ent1T3.get()))
            temp.close()

            self.sg.readGraphFile("temp.txt")
            self.makeGraph()
            self.increment()
        except:
            if(self.ent1T3.get() == ""):
                messagebox.showwarning("Atenção", "O campo 'Pessoa' está vazio!")


    def invertPeople(self):
        aux = self.ent2T1.get()
        self.ent2T1.delete(0, "end")
        self.ent2T1.insert(0, self.ent3T1.get())
        self.ent3T1.delete(0, "end")
        self.ent3T1.insert(0, aux)
        self.varOp1T1.set("")


    def makeGraph(self):

        for line in range(len(self.sg.linha)):
            self.lbox1W.insert(END, self.sg.linha[line])
            words = self.sg.linha[line].split()

            if words[0] == "add":
                self.graph.add_edge(words[1], words[2], weight=int(words[3][0]))

            elif words[0] == "remove":
                self.graph.remove_node(words[1])

        pos = nx.spring_layout(self.graph, k=1,iterations=100)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, labels)
        nx.draw(self.graph, pos, width=2, node_size=900, node_color="red", edge_color="white", font_size=8, with_labels=True)
        plt.savefig("Add.png", dpi=90, transparent=True)
        plt.clf()

        self.img = PhotoImage(file="Add.png")
        self.lbImgW.configure(image=self.img)


    def recommendFriends(self):
        try:
            self.lbox2W.delete(0, 'end')  # Apaga o ListBox
            list = self.sg.recommendFriends(self.ent1T2.get(), self.varOp1T2.get(), int(self.varOp2T2.get()))
            self.lbox1W.insert(END, "recommendFriends " + str(self.ent1T2.get()) + " " + str(self.varOp1T2.get()) + " " + str(self.varOp2T2.get()))

            for i in list:
                self.lbox2W.insert("end", str(i) + " " + str(list[i]))

        except:
            if (self.ent1T2.get() == "")and(self.varOp1T2.get() == "")and(self.varOp2T2.get() == ""):
                messagebox.showwarning("Atenção","Todos os campos estão vazios")
            elif (self.ent1T2.get() == "")and(self.varOp1T2.get() == ""):
                messagebox.showwarning("Atenção", "Os campos Pessoa e Opção estão vazios!")
            elif (self.ent1T2.get() == "")and(self.varOp2T2.get() == ""):
                messagebox.showwarning("Atenção", "Os campos Pessoa e Afinidade estão vazios!")
            elif(self.varOp1T2.get() == "")and(self.varOp2T2.get() == ""):
                messagebox.showwarning("Atenção", "Os campos Opção e Afinidade estão vazios!")
            elif self.ent1T2.get() == "":
                messagebox.showwarning("Atenção", "O campo Pessoa está vazio!")
            elif self.varOp1T2.get() == "":
                messagebox.showwarning("Atenção", "O campo Opção está vazio!")
            elif self.varOp2T2.get() == "":
                messagebox.showwarning("Atenção", "O campo Afinidade está vazio!")


    def increment(self):
        self.lb4W.configure(text="Número de Arestas: " + str(self.sg.dg.numEdges()))
        self.lb5W.configure(text="Número de Vertices: " + str(self.sg.dg.numVertices()))


    def shortestPath(self):
        try:
            temp = open("temp.txt", "w")
            temp.write("shortestPath " + str(self.ent2T2.get()) + " " + str(self.ent3T2.get()))
            temp.close()

            self.sg.readGraphFile("temp.txt")
            self.lb7T2.configure(text="ShotestPath: " + str(self.sg.list))

        except:
            if (self.ent2T2.get() == "") and (self.ent3T2.get() == ""):
                messagebox.showwarning("Atenção", "Todos os campos estão vazios!")
            elif self.ent2T2.get() == "":
                messagebox.showwarning("Atenção", "O campo Pessoa está vazio!")
            elif self.ent3T2.get() == "":
                messagebox.showwarning("Atenção", "O campo Alvo está vazio!")


class SocialGraph(object):

    def __init__(self, file = None):
        self.dg = DiGraph.DiGraph()
        if file != None:
            self.readGraphFile(file)

    def readGraphFile(self, file):
        self.file = open(file, "r")
        self.linha = [] #Foi acrescentado para gerar o histórico de comandos
        self.peso = []

        for line in self.file:
            line = line.split(" ")


            if line[0] == "add":
                self.dg.addEdge(line[1], line[2], int(line[3]))
                linha = str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + " " + str(line[3][0])
                self.linha = self.linha + [linha]
                self.peso = self.peso + [int(line[3])]
                print(linha)
                print("addEdge: (True) - " + str(self.dg.numEdges()) + " edges, " + str(self.dg.numVertices()) + " vertices")
                print()


            elif line[0] == "showFriends":
                print(line[0], line[1].replace("\n", ""))
                control = self.dg.adjacentTo(line[1].replace("\n", ""))
                print(str(str(control).replace("(", "<")).replace(")", ">"))

            elif line[0] == "recommendFriends":
                print(line[0], line[1], line[2], line[3].replace("\n", ""))
                print(self.recommendFriends(line[1], line[2], int(line[3])))

            elif line[0] == "shortestPath":
                print(line[0], line[1], line[2].replace("\n", ""))
                path = self.dg.Dijkstra2(line[1], line[2].replace("\n", ""))
                self.list = dict()

                for item in path:
                    self.list[item] = self.dg.getDist(item)

                print(self.list)

            elif line[0] == "remove":
                linha = str(line[0]) + " " + str(line[1].replace("\n", ""))
                self.linha = self.linha + [linha]
                print(linha)
                self.dg.removeVertex(line[1].replace("\n", ""))
                print("remove: (True) - ",self.dg.numEdges()," edges, ",self.dg.numVertices()," vertices")
                print()

    def recommendFriends(self, personOfInterest, option, topK):
        if option == "dist":
            itens = topK
            dist = self.dg.Dijkstra(personOfInterest)
            dist.pop(personOfInterest) #Remove a personOfInterest do dicionário
            friends = self.dg.adjacentTo(personOfInterest)
            order1 = dict()
            order2 = dict()

            for item in friends:
                dist.pop(item.getVertex())

            aux = sorted(dist, key = dist.get)[0]
            for key in sorted(dist, key = dist.get):
                order1[key] = dist[key]
                itens -= 1
                if (dist[aux] == dist[key]) and (itens > 0):
                    topK += 1
                aux = key

            for i in order1:
                if (topK > 0) and (dist[i] != float("inf")):
                    order2[i] = order1[i]
                    topK -= 1
            return order2


        elif option == "weightedDist":
            itens = topK
            dist = self.dg.Dijkstra(personOfInterest)
            dist.pop(personOfInterest)  # Remove a personOfInterest do dicionário
            friends = self.dg.adjacentTo(personOfInterest)
            order1 = dict()
            order2 = dict()

            for item in friends:
                dist.pop(item.getVertex())

            for key in dist:
                dist[key] = dist[key]*(self.dg.numEdges()-len(self.dg.incomingEdges(key)))

            aux = sorted(dist, key=dist.get)[0]
            for key in sorted(dist, key = dist.get):
                order1[key] = dist[key]
                itens -= 1
                if (dist[aux] == dist[key]) and (itens > 0):
                    topK += 1
                aux = key

            for i in order1:
                if (topK > 0) and (dist[i] != float("inf")):
                    order2[i] = order1[i]
                    topK -= 1
            return order2


def main(args=None):
    Application = App(window)
    window.mainloop()

if __name__ == '__main__':
    window = Tk()
    main()
