import os
import requests
from requests import Session

#zeep imports
from zeep import Client
from zeep.transports import Transport

import ipRecordFactory
import logconf
import sslcontext


#ruta de el archivo wsdl
url = 'ProsurIPRecordWS.wsdl'
#todos los metodos del WS requieren un usuario como segundo parametro 
user = 'ecu_usr'

def obtenerClienteWS():
    """Retorna un objeto cliente, este sirve como un manejador que permite llamar
    a los metodos del IPRECORDWS"""
    #con el certificado adecuado se ejecutaran las subsecuentes instrucciones
    with sslcontext.pfx_to_pem('clientEC.pfx', 'Ea6@3H') as cert:
        #crea una sesión 
        session = Session()
        #deshabilitar la verificación SSL
        session.verify = False
        session.cert = cert
        transport = Transport(session=session)
        #el objeto cliente que permite interactuar con el WS
        client = Client(
            url, 
            transport=transport
        )

        return client
    

def enviarSignos():
    """Consulta los signos distintivos y los envia al WS"""
    client = obtenerClienteWS()
    signos = ipRecordFactory.obtenerSignosDistintivos()

    for signo in signos:
        # obteniendo el tipo de objeto ipRecord
        ipRecordType = client.get_type('ns0:ipRecord')
        # obteniendo el tipo de objeto disticntiveSign
        distinctiveSignType = client.get_type('ns0:distinctiveSign')
        # extendiendo el tipo ipRecord a distinctiveSign
        distinctiveSignType.extend(ipRecordType)
        # llenado datos en un signo distintivo a enviar
        signo = distinctiveSignType(
            onapiId=signo["onapiid"],
            applicationId=signo["applicationid"],
            recordType=signo["recordtype"],
            nationalPresentationDate=signo["nationalpresentationdate"],
            nationalPublishingDate=signo["nationalpublishingdate"],
            title=signo["title"],
            applicantName=signo["applicantname"],
            statusId=signo["statusid"],
            ipRecordDetailLink=signo["iprecorddetaillink"],
            files=signo["filedata"],
            ipRecordFilesService=signo["iprecordfilesservice"],
            distinctiveSignType=signo["distinctivesigntype"],
            presentationType=signo["distinctivesigntype"],
            registrationDate=signo["registrationdate"],
            expiration=signo["expiration"],
            niceClasses=signo["niceclasses"],
            logoDescription=signo["logodescription"]
        )
        #client.service.createRecord(signo, user)
    return


#metodo principal
def main():
    
    enviarSignos()

if __name__ == "__main__":
    main()

