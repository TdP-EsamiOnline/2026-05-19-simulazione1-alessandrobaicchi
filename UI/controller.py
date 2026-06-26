import flet as ft

from tstModel import bestArtist


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genereValue = None

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

        self._view.update_page()
    # -----------------------------------------------------------------------------------------------------------------

    def handleCammino(self,e):
        pass