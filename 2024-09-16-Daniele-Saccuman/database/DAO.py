from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllShapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s2.shape
                          from sighting s2
                          where s2.shape <> ''
                          order by s2.shape desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def getLatitudini():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select max(s.Lat) as maxLat, min(s.Lat) as minLat
                        from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append((row["minLat"], row["maxLat"]))
            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def getLongitudini():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select max(s.Lng) as maxLng, min(s.Lng) as minLng
                        from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append((row["minLng"], row["maxLng"]))
            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def getAllNodes(shape, lat, lng):

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.*
                        from state s, sighting s2 
                        where s2.state = s.id 
                        and s2.shape = %s
                        and s.Lat > %s
                        and s.Lng > %s"""
            cursor.execute(query, (shape, lat, lng))

            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def getAllEdges(lat, lng, shape):

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select st1.id as st1, st2.id as st2, sum(s.duration) as peso
                        from sighting s, state st1, state st2, neighbor n 
                        where st1.Lat > %s
                        and st1.Lng > %s
                        and (s.state = st1.id or s.state = st2.id )
                        and st2.Lat > %s
                        and st2.Lng > %s
                        and s.state = st2.id 
                        and s.shape = %s
                        and n.state1 = st1.id
                        and n.state2 = st2.id 
                        group by st1.id, st2.id"""
            cursor.execute(query, (lat, lng, lat, lng, shape))

            for row in cursor:
                result.append((row["st1"], row["st2"], row["peso"]))
            cursor.close()
            cnx.close()
            return result





