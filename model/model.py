import copy

import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._artists = []
        self._idMapA = {}
        self._mapPopularityArtist = {}  # Dict popolarità del singolo artista

    # --------------------------------------------- DD "Genere" -------------------------------------------------------
    def getGeneri(self):
        return DAO.getGenre()
    # -----------------------------------------------------------------------------------------------------------------

    # --------------------------------------------- DD "Artist" -------------------------------------------------------
    def getArtists(self):
        return self._artists
    # -----------------------------------------------------------------------------------------------------------------

    # ----------------------------------------------- Grafo -----------------------------------------------------------
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
            pop = DAO.getArtistPopularity(a, genere)
            self._mapPopularityArtist[a] = pop


        # Confronto due artisti alla volta (di self._artists, quindi già filtrati per genere)

        # Ciclo triangolare per generare ogni coppia di artisti UNA sola volta.
        # ---------------------------------------------------------------
        # i scorre tutti gli indici della lista degli artisti.
        # j parte da i+1, quindi considera solo gli elementi SUCCESSIVI.
        #
        # Questo evita:
        #   - duplicati (A,B) e poi (B,A)
        #   - confronti inutili (A,A)
        #   - raddoppio degli archi quando pop1 == pop2
        #
        # Esempio con 4 artisti: [A, B, C, D]
        # Coppie generate:
        #   (A,B), (A,C), (A,D),
        #   (B,C), (B,D),
        #   (C,D)
        #
        # Coppie NON generate:
        #   (B,A), (C,A), (D,A), ...
        #
        # Risultato: ogni coppia è unica → grafo corretto e senza archi in eccesso.

        for i in range(len(self._artists)):
            for j in range(i + 1, len(self._artists)):
                a1 = self._artists[i]
                a2 = self._artists[j]

                if DAO.haveCommonCustomer(a1, a2, genere):

                    pop1 = self._mapPopularityArtist[a1]
                    pop2 = self._mapPopularityArtist[a2]
                    peso = pop1 + pop2

                    #print("COPPIA:", a1.ArtistId, a2.ArtistId, "pop1:", pop1, "pop2:", pop2)

                    if pop1 > pop2:
                        self._graph.add_edge(a1, a2, weight=peso)
                    elif pop2 > pop1:
                        self._graph.add_edge(a2, a1, weight=peso)
                    else:
                        self._graph.add_edge(a1, a2, weight=peso)
                        self._graph.add_edge(a2, a1, weight=peso)

    # Scrivo il "solito" metodo per sapere il numero di nodi e archi del grafo.
    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)
    # -----------------------------------------------------------------------------------------------------------------


    # ----------------------------------------------- Statistiche -----------------------------------------------------
    def mostInfluentialArtist(self):
        bestScore = 0
        bestArtist = None
        for a in self._artists:
            outW = self._graph.out_degree(a, weight='weight')
            inW = self._graph.in_degree(a, weight='weight')
            influential = outW - inW

            if influential > bestScore:
                bestScore = influential
                bestArtist = a
        return bestArtist, bestScore

    def best5Edges(self):
        listaEdges = [(u, v, data['weight']) for (u, v, data) in self._graph.edges(data=True)]

        listaEdges.sort(key=lambda x: x[2], reverse=True)
        return listaEdges[0:5]

        # Costruisco una lista di archi in forma semplificata usando una list comprehension.
        # -------------------------------------------------------------------------------
        # self._graph.edges(data=True) restituisce un EdgeView: una sequenza di tuple del tipo
        #   (u, v, {"weight": valore})
        #
        # La list comprehension trasforma ogni elemento in una tupla più comoda:
        #   (u, v, peso)
        #
        # Vantaggi della list comprehension:
        #   • è più compatta e leggibile rispetto al ciclo for tradizionale
        #   • evita append manuali → codice più pulito e pythonico
        #   • rende immediato l’ordinamento per peso (x[2])
        #   • crea una snapshot statica degli archi, utile per sorting e slicing
        #
        # Struttura generale della list comprehension:
        #   [ espressione  for variabili in iterabile ]
        #
        # Nel nostro caso:
        #   espressione → (u, v, data["weight"])
        #   variabili   → (u, v, data)
        #   iterabile   → self._graph.edges(data=True)
        #
        # Risultato: listaEdges = [(nodo1, nodo2, peso), ...]
    # -----------------------------------------------------------------------------------------------------------------


    # --------------------------------------------- Ricorsione --------------------------------------------------------
    """
        Trova il cammino semplice più lungo con pesi strettamente crescenti,
        partendo dall'artista selezionato dall'utente.

        Flusso:
        1. Inizializzo la soluzione ottima (bestPath, bestLength).
        2. Creo la lista 'parziale' che rappresenta il cammino attuale.
        3. Avvio la ricorsione passando pesoPrecedente = -1
           (qualsiasi arco è valido come primo arco).
        4. Al termine, ritorno il bestPath trovato.
        """
    def trovaCammino(self, startArtist):
        """
                Trova il cammino semplice più lungo con pesi strettamente crescenti,
                partendo dall'artista selezionato dall'utente.

                Flusso:
                1. Inizializzo la soluzione ottima (bestPath, bestLength).
                2. Creo la lista 'parziale' che rappresenta il cammino attuale.
                3. Avvio la ricorsione passando pesoPrecedente = -1
                   (qualsiasi arco è valido come primo arco).
                4. Al termine, ritorno il bestPath trovato.
                """

        # Inizializzo la soluzione ottima
        self._bestPath = []         # Miglior cammino trovato finora
        self._bestLength = 0        # Lunghezza del miglior cammino

        # Lista soluzione parziale
        parziale = [startArtist]    # Cammino attuale: parto dall'artista selezionato

        # Avvio della DFS: peso precedente = -1 (così qualsiasi peso va bene per il primo arco)
        self._ricorsione(parziale, -1)

        return self._bestPath


    def _ricorsione(self, parziale, pesoPrecedente):
        """
            Ricorsione DFS che esplora tutti i cammini semplici con pesi strettamente crescenti.

            La funzione segue la struttura classica del Prof:
            1) Condizione di ottimalità:
               - Se il cammino attuale è più lungo della best, aggiorno la best.
               - Uso deepcopy per congelare la soluzione (regola del Prof).

            2) Condizione di terminazione:
               - Non esiste una condizione esplicita: la ricorsione termina quando
                 non ci sono più successori validi da aggiungere.
               - Terminazione naturale della DFS.

            3) Ricorsione:
               - Per ogni successore del nodo corrente:
                   * calcolo il peso dell'arco
                   * verifico i vincoli:
                       - peso strettamente crescente
                       - cammino semplice (niente ripetizioni)
                   * se valido:
                       - aggiungo il nodo al cammino
                       - richiamo ricorsivamente
                       - rimuovo il nodo (backtracking)
            """

        # 1) Condizioni di ottimalità: aggiorno la best solo se migliora
        if len(parziale) > self._bestLength:
            self._bestLength = len(parziale)
            self._bestPath = copy.deepcopy(parziale)    # Copia "profonda"

        # 2) Nodo corrente del cammino
        nodoCorrente = parziale[-1]

        # Prendo i successori del nodo corrente. Il testo parla di "cammino" quindi devo seguire gli archi nella
        # direzione che hanno nel grafo (è ORIENTATO), non devo usare neighbors o predecessors: devo usare successors.

        # 3) Ricorsione
        vicini = self._graph.successors(nodoCorrente)
        for v in vicini:
            pesoCorrente = self._graph[nodoCorrente][v]["weight"]

            # Vincoli del problema:
            # - peso strettamente crescente;
            # - cammino semplice (v non deve essere già nel cammino).
            if pesoCorrente > pesoPrecedente and v not in parziale:
                parziale.append(v)                          # Scelta
                self._ricorsione(parziale, pesoCorrente)    # Ricorsione
                parziale.pop()                              # Backtracking
    # -----------------------------------------------------------------------------------------------------------------