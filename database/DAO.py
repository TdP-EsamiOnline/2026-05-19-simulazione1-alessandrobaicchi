from database.DB_connect import DBConnect
from model.artist import Artist
from model.genere import Genere


class DAO():
    def __init__(self):
        pass

    # =================================== DD "Category" ==============================================
    @staticmethod
    def getGenre():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("""
                    select *
                    from genre g 
                    """)

        cursor.execute(query)

        for row in cursor:
            results.append(Genere(**row))

        cursor.close()
        conn.close()
        return results

    # =================================================================================================

    # ========================================== Nodi grafo ===========================================
    @staticmethod
    def getArtistsByGenre(genere):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("""
                    select ar.ArtistId, ar.Name 
                    from track t, album al, artist ar 
                    where t.AlbumId = al.AlbumId and al.ArtistId = ar.ArtistId 
                    and t.GenreId = %s
                    group by ar.ArtistId, ar.Name 
                     """)

        cursor.execute(query, (genere.GenreId,))

        for row in cursor:
            results.append(Artist(**row))

        cursor.close()
        conn.close()
        return results

        # NOTE CHIRURGICHE — getArtistsByGenre(genere)
        # ------------------------------------------------
        # La query:
        #   select ar.ArtistId, ar.Name
        #   ...
        #   group by ar.ArtistId, ar.Name
        #
        # restituisce PIÙ RIGHE:
        #   • una riga per ogni artista che ha almeno un brano del genere scelto.
        #
        # cursor = conn.cursor(dictionary=True):
        #   • ogni riga del risultato viene restituita come DIZIONARIO.
        #   • Esempio di row:
        #         {"ArtistId": 22, "Name": "U2"}
        #
        # for row in cursor:
        #   • serve perché la query produce MULTIPLE righe.
        #   • ogni row è un dict con le colonne selezionate.
        #
        # Artist(**row):
        #   • costruisce un oggetto Artist passando i campi del dict come parametri.
        #   • equivale a:
        #         Artist(ArtistId=row["ArtistId"], Name=row["Name"])
        #
        # results.append(Artist(**row)):
        #   • aggiunge alla lista un oggetto Artist per ogni riga trovata.
        #   • results diventa una LISTA di oggetti Artist.
        #
        # Differenza rispetto a getArtistPopularity():
        #   • getArtistsByGenre → PIÙ righe → serve il ciclo for.
        #   • getArtistPopularity → UNA sola riga → si usa fetchone() e NON il ciclo.
        #
        # Il metodo ritorna:
        #   results = [Artist(...), Artist(...), Artist(...), ...]
        #   cioè la lista degli artisti appartenenti al genere selezionato.

    # =================================================================================================

    # ========================================== Nodi archi ===========================================
    @staticmethod
    def getArtistPopularity(artist):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        # results = []
        query = ("""
                    select count(*) as pop
                    from invoiceline il, track t, album al
                    where il.TrackId = t.TrackId
                    and t.AlbumId = al.AlbumId
                    and al.ArtistId = %s
                 """)

        cursor.execute(query, (artist.ArtistId,))
        # In questo caso il risultato della query è un singolo valore,
        # ovvero la popolarità dell'artista (artist) passato come parametro.
        # Per questo non ciclo "come al solito", perché qui non ho una lista
        # di risultati, ma un singolo risultato (è un numero).
        row = cursor.fetchone()

        # for row in cursor:
        #     results.append(Artist(**row))

        cursor.close()
        conn.close()
        return row["pop"]   # E' un intero

    # NOTE CHIRURGICHE — getArtistPopularity(artist)
    # ------------------------------------------------
    # La query con COUNT(*) restituisce SEMPRE UNA SOLA RIGA:
    #   pop = numero totale di acquisti dei brani dell'artista.
    #
    # cursor.fetchone():
    #   • NON usa un ciclo perché la query produce una sola riga.
    #   • Restituisce un dizionario (grazie a dictionary=True).
    #   • Esempio: {"pop": 37}
    #
    # row["pop"]:
    #   • Accede al valore della colonna "pop".
    #   • "pop" è l'alias definito nella query SQL:
    #         select count(*) as pop
    #   • row["pop"] è quindi un INTERO (la popolarità).
    #
    # Il metodo deve restituire direttamente row["pop"]:
    #   • niente liste
    #   • niente append
    #   • niente cicli
    #
    # Nel Model:
    #   self._pop[artist] = DAO.getPopularity(artist)
    # crea un dizionario {Artist -> popolarità}.

    # =================================================================================================