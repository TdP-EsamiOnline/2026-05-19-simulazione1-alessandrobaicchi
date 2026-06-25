import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genereValue = None

    # ------------------------------- DD "Genere" ------------------------------------
    def fillDDGenre(self):
        generi = self._model.getGeneri()
        generiDDGeneriOptions = list(map(lambda x : ft.dropdown.Option(data=x, key=x.Name,
                                                                on_click=self._choiceGenere),
                                                                generi))
        self._view._ddGenre.options = generiDDGeneriOptions
        self._view.update_page()

    def _choiceGenere(self,e):
        self._genereValue = e.control.data
    # --------------------------------------------------------------------------------

    def handleCreaGrafo(self, e):
        pass

    def handleCreaGrafo(self,e):
        pass

    def handleCammino(self,e):
        pass