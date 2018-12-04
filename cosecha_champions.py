
import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


###Credenciales de la cuenta de Twitter########################
#Poner aqui las credenciales de su cuenta privada, caso contrario la API bloqueara esta cuenta de ejemplo
ckey = "DtkCxWmUf7LvAIrfz3jlEA7NU"
csecret = "RVdMWSo5FCgfKm9osyMNIJEHElwGNDCXUDMJxFratdz6LLmEZm"
atoken = "999027624109334528-VNrIPYknAppss15u3lx5g79bdiih0nr"
asecret = "I3s3yBy2DwJLib9EVtUmAeMfjKE5HPuZmJRs18j48kSvn"
#####################################

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            #Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
            #a guardar en documento en la base de datos
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('champions')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['champions']
    
#Aqui sedefine el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(track=["champions league"])
twitterStream.filter(locations=[-12.17,35.97,30.36,66.8])
