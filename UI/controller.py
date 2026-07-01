import flet as ft

from tstModel import bestArtist


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genereValue = None
        self._artistValue = None

    # ---------------------------------------------- DD "Genere" ------------------------------------------------------
    def fillDDGenre(self):
        generi = self._model.getGeneri()
        generiDDGeneriOptions = list(map(lambda x : ft.dropdown.Option(data=x, key=x.Name,
                                                                on_click=self._choiceGenere),
                                                                generi))
        self._view._ddGenre.options = generiDDGeneriOptions
        self._view.update_page()

    def _choiceGenere(self,e):
        self._genereValue = e.control.data
    # -----------------------------------------------------------------------------------------------------------------

    # -------------------------------------- Pulsante "Crea Grafo" ----------------------------------------------------
    def handleCreaGrafo(self, e):
        genere = self._genereValue
        self._model.buildGraph(genere)
        nNodi, nArchi = self._model.getGraphDetails()
        bestArtist, bestScore = self._model.mostInfluentialArtist()
        listaTop5 = self._model.best5Edges()

        # Stampo il grafo
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente!",color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodi}",color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nArchi}",color="green"))

        # Stampo statistiche del grafo
        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {bestArtist}, "
                                                      f"con influenza: {bestScore}", color="green"))
        self._view.txt_result.controls.append(ft.Text("A seguire il Top 5 archi:", color="green"))
        for i in range(len(listaTop5)):
            self._view.txt_result.controls.append(ft.Text(f"{listaTop5[i][0]} -> {listaTop5[i][1]}, "
                                                          f"con peso: {listaTop5[i][2]}", color="green"))

        self.fillDDArtist()
        self._view.update_page()
    # -----------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------- DD "Artist" ------------------------------------------------------
    def fillDDArtist(self):
        artisti = self._model.getArtists()
        artistiDDArtistiOptions = list(map(lambda x: ft.dropdown.Option(data=x, key=x.Name,
                                                                          on_click=self._choiceArtist),
                                             artisti))
        self._view._ddArtist.options = artistiDDArtistiOptions
        self._view.update_page()

    def _choiceArtist(self, e):
        self._artistValue = e.control.data
    # -----------------------------------------------------------------------------------------------------------------


    # ------------------------------------------------ Ricorsione -----------------------------------------------------
    def handleCammino(self,e):
        """
            Gestisce il pulsante "Trova Cammino" del Punto 2 della simulazione Chinook.

            Flusso operativo:
            1. Recupero l'artista selezionato dall'utente nel menu a tendina.
               Questo artista rappresenta il nodo di partenza del cammino.

            2. Invoco il Model tramite:
                   bestPath = self._model.trovaCammino(artist)
               Il Model esegue la ricorsione DFS e restituisce il cammino semplice
               più lungo con pesi strettamente crescenti, come richiesto dal testo.

               Nota:
               Il Model garantisce già:
               - cammino semplice (nessuna ripetizione di artisti)
               - pesi strettamente crescenti
               - massima lunghezza del cammino
               Qui nel Controller ci limitiamo a stampare il risultato.

            3. Pulisco l'area di testo della View e stampo:
               - una frase introduttiva che indica l'artista di partenza
               - tutti gli artisti del cammino, uno per riga

               Il testo dell'esame richiede di mostrare il cammino semplice
               di lunghezza massima. La stampa dei pesi non è richiesta.

            4. Aggiorno la pagina della View per rendere visibile il risultato.
            """

        # 1) Artista selezionato dall'utente
        artist = self._artistValue

        # 2) Chiamata al Model: ottengo il cammino semplice più lungo
        bestPath = self._model.trovaCammino(artist)

        # 3) Stampa del cammino nella View
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Il cammino semplice di lunghezza massima partendo "
                                                      f"dall'artista {artist} è il seguente:", color="green"))

        # Stampo ogni artista del cammino, uno per riga
        for i in range(len(bestPath)):
            self._view.txt_result.controls.append(ft.Text(f"{bestPath[i]}", color="green"))

        # 4) Aggiorno la pagina
        self._view.update_page()
    # -----------------------------------------------------------------------------------------------------------------