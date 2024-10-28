
from database.DAO import DAO
import networkx as nx




class Model:
    def __init__(self):
        self._listShape = []
        self._listLat = []
        self._listLng = []
        self._grafo = nx.Graph()
        self._nodi = []
        self._idMap = {}

    def getShape(self):
        self._listShape = DAO.getAllShapes()
        return self._listShape

    def getLat(self):
        self._listLat = DAO.getLatitudini()
        return self._listLat

    def getLng(self):
        self._listLng = DAO.getLongitudini()
        return self._listLng

    def buildGraph(self, shape, lat, lng):
        self._nodi = DAO.getAllNodes(shape, lat, lng)
        for s in self._nodi:
            self._idMap[s.id] = s

        self._grafo.add_nodes_from(self._nodi)
        self._archi = DAO.getAllEdges(lat, lng, shape)
        for e in self._archi:
            s1 = self._idMap[e[0]]
            s2 = self._idMap[e[1]]
            peso = e[2]
            if s1 in self._grafo.nodes and s2 in self._grafo.nodes:
                if self._grafo.has_edge(s1, s2):
                    self._grafo[s1][s2]['weight'] += peso
                else:
                    self._grafo.add_edge(s1, s2, weight = peso)

    def nodiGradoMaggiore(self):
        listaNodi = []
        listaBest = []
        for stato in self._grafo.nodes():
            grado = self._grafo.degree(stato)
            listaNodi.append((stato, grado))
        listaNodi.sort(key=lambda x: x[1], reverse=True)
        conta = 0
        for a in range(0, len(listaNodi)):
            if conta <= 4:
                listaBest.append(listaNodi[a])
                conta = conta + 1
        return listaBest

    def archiPesiMaggiori(self):
        listaArchi = []
        listaBest = []
        for uscente, entrante in self._grafo.edges():
            pesoArco = self._grafo[uscente][entrante]["weight"]
            listaArchi.append((uscente, entrante, pesoArco))
        listaArchi.sort(key=lambda x: x[2], reverse=True)
        conta = 0
        for a in range(0, len(listaArchi)):
            if conta <= 4:
                listaBest.append(listaArchi[a])
                conta = conta + 1
        return listaBest

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)


