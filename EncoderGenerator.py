import os
import cv2
import pickle
import face_recognition

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://reconnaissance-faciale-e632a-default-rtdb.firebaseio.com/',
    'storageBucket': 'reconnaissance-faciale-e632a.appspot.com'
})

# Impoter les images des employés
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []
employeIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    employeIds.append(int(os.path.splitext(path)[0]))  # Recupère l'id de l'image

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Debut de l'encodage ...")

listImgEncode = findEncodings(imgList)
listImgEncodeEtIds = [listImgEncode, employeIds]
print("Fin de l'encodage")

file = open("EncodeFile.p", "wb")
pickle.dump(listImgEncodeEtIds, file)
file.close()
print("Fichier fermé")

