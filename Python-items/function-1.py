from google.cloud import firestore
client = firestore.Client()
import json


from resume_parser import resumeparse
import os
import tempfile
import urllib
import textract
import requests
from resume_parser import resumeparse
import os
import tempfile
import urllib
import textract
import requests



def hello_firestore(event, context):
    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    document_path = '/'.join(path_parts[1:])

    affected_doc = client.collection(collection_path).document(document_path)
    affected_doc.update({
            u'checking': "checing",
            u'gotUrl':event["value"]['fields']["url"]['stringValue']
        })
   
    
    file_url=event["value"]['fields']["url"]['stringValue']
    fil = urllib.request.urlopen(file_url)
    response=requests.get(file_url)
    fine_name=os.path.join(tempfile.gettempdir(),"metadata.pdf")
    with open(fine_name, 'wb') as f:
        f.write(response.content)
    text = textract.process(fine_name, method='pdfminer',encoding='ascii')    
    data = resumeparse.read_file(fine_name)
    affected_doc.update({
        u'resumeData': data
    })
   
    affected_doc.update({
            u'original': event["value"]['fields']["url"]['stringValue']
        })



   

   