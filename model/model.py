import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._artists = []
        self._idMapA = {}

    # -------------------------------------- DD "Genere" ---------------------------------------
    def getGeneri(self):
        return DAO.getGenre()
    # ------------------------------------------------------------------------------------------

    # --------------------------------------- Grafo --------------------------------------------
    def buildGraph(self, genere):
        self._graph.clear()
        self._artists = DAO.getArtistsByGenre(genere)

        # Creo la "solita" idMap
        for a in self._artists:
            self._idMapA[a.ArtistId] = a

        # CREO IL GRAFO

        # NODI
        # Aggiungo i nodi al grafo
        self._graph.add_nodes_from(self._artists)

        # ARCHI
        # Associo ad ogni artista che forma il grafo (che quindi ha passato la selezione sul "Genere musicale")
        # la sua popolarità (pop)
        for a in self._artists:
            pop = DAO.getArtistPopularity(a)
            self._popularity[a] = pop


    # ------------------------------------------------------------------------------------------
