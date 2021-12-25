import cv2
import os
from PIL import Image
import numpy as np
#Using opencv to train the model with few images with the person's Face
def recognize():
    recognizer=cv2.createLBPHFaceRecognizer()
    path='.//Recognizer'
    path2 ='.//Loading'
    def getimagewithid(path):
        Imagepaths=[os.path.join(path,f) for f in os.listdir(path)]
        faces=[]
        IDs=[]
        for Imagepath in Imagepaths:
            img=Image.open(Imagepath).convert('L')
            img_np=np.array(img,'uint8')
            ID=int(os.path.split(Imagepath)[-1].split('.')[1])
            faces.append(img_np)
            IDs.append(ID)
            cv2.imshow('Trainning..',img_np)
            cv2.waitKey(10)
        return IDs,faces
    def Loading (path2):
        loadingpaths=[os.path.join(path2,f) for  f in os.listdir(path2)]
        loads=[]
        for loadingpath in loadingpaths:
            load = Image.open(loadingpath)
            load_np = np.array(load,'uint8')
            loads.append(load_np)
            cv2.imshow("Face Recognition", load_np)
            cv2.waitKey(60)
    ids ,faces=getimagewithid(path)
    recognizer.train(faces, np.array(ids))
    recognizer.save('.//result//trainning_result.yml')
    Loading(path2)
    cv2.destroyAllWindows()
