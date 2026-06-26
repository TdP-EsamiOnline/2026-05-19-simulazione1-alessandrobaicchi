from model.model import Model
from model.genere import Genere
mymdl = Model()

g = Genere(7, "Latin")
mymdl.buildGraph(g)
n, e = mymdl.getGraphDetails()
bestArtist, bestScore = mymdl.mostInfluentialArtist()
lista = mymdl.best5Edges()
print(f"Numero nodi: {n}, numero archi: {e}")
print(f"Artista più influente: {bestArtist}, con influenza: {bestScore}")
print("A seguire i top 5 archi:")
for i in range(0, len(lista)):
    print(f"{lista[i][0]} -> {lista[i][1]}, con peso: {lista[i][2]}")

