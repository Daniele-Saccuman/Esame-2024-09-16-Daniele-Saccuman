import flet as ft
from UI.view import View
from database.DAO import DAO
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def populateLat(self):
        listLat = DAO.getLatitudini()
        minLat = float(listLat[0][0])
        maxLat = float(listLat[0][1])
        return minLat, maxLat

    def populateLng(self):
        listLng = DAO.getLongitudini()
        minLng = float(listLng[0][0])
        maxLng = float(listLng[0][1])
        return minLng, maxLng


    def handle_graph(self, e):
        lat = float(self._view.txt_latitude.value)
        lng = float(self._view.txt_longitude.value)
        shape = self._view.ddshape.value
        minLat, maxLat = self.populateLat()
        minLng, maxLng = self.populateLng()
        if lat is None or lat < minLat or lat > maxLat:
            self._view.create_alert("Latitudine non valida")
            return
        if lng is None or lng < minLng or lng > maxLng:
            self._view.create_alert("Longitudine non valida")
            return
        if shape is None:
            self._view.create_alert("Shape non inserita")
            return

        self._model.buildGraph(shape, lat, lng)
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        self._view.txt_result1.controls.append(
            ft.Text(f"I 5 nodi di grado maggiore sono:"))
        listaBest = self._model.nodiGradoMaggiore()
        for nodo in listaBest:
            self._view.txt_result1.controls.append(ft.Text(f"{nodo[0]} -> degree: {nodo[1]}"))

        self._view.txt_result1.controls.append(
            ft.Text(f"I 5 archi di peso maggiore sono:"))
        listaBest = self._model.archiPesiMaggiori()
        for arco in listaBest:
            self._view.txt_result1.controls.append(ft.Text(f"{arco[0]} <-> {arco[1]} | peso = {arco[2]}"))
        self._view.update_page()

    def handle_path(self, e):
        pass

    def fill_ddshape(self):
        self._listShape = self._model.getShape()
        for shape in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view.update_page()

    def read_shape(self, e):
        if e.control.value is None:
            self._shape = None
        else:
            self._shape = e.control.value



