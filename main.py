import os
import pickle
import numpy as np
from matplotlib import pyplot as plt
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://reconnaissance-faciale-e632a-default-rtdb.firebaseio.com/',
    'storageBucket': 'reconnaissance-faciale-e632a.appspot.com'
})

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Ressources/background.png')
bucket = storage.bucket()

# Impoter les modes images commes une liste
folderModePath = 'Ressources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# charger les informations
file = open("EncodeFile.p", "rb")
listImgEncodeEtIds = pickle.load(file)
file.close()

listImgEncode, ids = listImgEncodeEtIds
print(ids)

counter = 0
modeType = 0
idEmploye = -1
imgEmploye = []
while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(listImgEncode, encodeFace)
        faceDis = face_recognition.face_distance(listImgEncode, encodeFace)
        # print("Correspondence: ", matches)
        # print("Distance: ", faceDis)

        matcheIndex = np.argmin(faceDis)
        if matches[matcheIndex]:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

            idEmploye = ids[matcheIndex]
            if counter == 0:
                counter = 1
                modeType = 1

    if counter != 0:

        if counter == 1:
            # Recupérer les infos employé
            infoEmploye = db.reference(f'Employes/{idEmploye}').get()
            print(infoEmploye)

            # Recupérer l'image de l'employé
            blob = bucket.get_blob(f'Images/{idEmploye}.png')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgEmploye = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

            # Mettre à jour les informations
            datePointage = datetime.strptime(infoEmploye['dernier_pointage'], "%Y-%m-%d %H:%M:%S")
            seconde = (datetime.now() - datePointage).total_seconds()
            if seconde > 30:
                ref = db.reference(f'Employes/{idEmploye}')
                infoEmploye['total_pointage'] += 1

                ref.child('total_pointage').set(infoEmploye['total_pointage'])
                ref.child('dernier_pointage').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        counter += 1

    # cv2.imshow("Webcam", img)
    cv2.imshow("Reconnaissance faciale", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

plt.imshow(imgEmploye)
plt.show()
