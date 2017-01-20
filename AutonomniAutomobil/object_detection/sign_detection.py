import cv2
from keras.applications.resnet50 import ResNet50
import keras.preprocessing.image as kp
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

model = ResNet50(weights='imagenet')

def detect_cars(image):
    # constants
    IMAGE_SIZE = 200.0
    MATCH_THRESHOLD = 3

    #cascade_url = 'frontal_stop_sign_cascade.xml'
    cascade_url = 'cars.xml'
    img_url = 'Cars/car2.jpg'
    roundabout_cascade = cv2.CascadeClassifier(cascade_url)
    street = image #cv2.imread(img_url)
    #street = cv2.resize(street, (300, 300))

    # detekcija znaka na slici
    gray = cv2.cvtColor(street, cv2.COLOR_RGB2GRAY)
    signs = roundabout_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=1
    )
    #print signs
    # orb i feature matcher
    #orb = cv2.ORB()
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # kljucne karakteristike za znake koje sluze za odbacivanje lose prepoznatih delova
    #roadsign = cv2.imread('examples/stop5.jpg', 0)
    #kp_r, des_r = orb.detectAndCompute(roadsign, None)

    # prolazak kroz sve znake
    for (x, y, w, h) in signs:

        # vadjenje objekta
        obj = gray[y:y + h, x:x + w]
        ratio = IMAGE_SIZE / obj.shape[1]
        obj = cv2.resize(obj, (int(IMAGE_SIZE), int(obj.shape[0] * ratio)))

        # pronalazenje karakteristika na slici
        #kp_o, des_o = orb.detectAndCompute(obj, None)
        #if len(kp_o) == 0 or des_o == None: continue

        #matches = bf.match(des_r, des_o)

        # obelezavanje detektovanog znaka
       # if (len(matches) >= MATCH_THRESHOLD):
        cv2.rectangle(street, (x, y), (x + w, y + h), (255, 0, 0), 2)

        reg = kp.img_to_array(cv2.resize(street[y:y+h+1, x:x+w+1], (224, 224)))
        reg = np.expand_dims(reg, axis=0)
        reg = preprocess_input(reg)
        preds = model.predict(reg)
        # decode the results into a list of tuples (class, description, probability)
        # (one such list for each sample in the batch)
        print 'Koordinate: {0}, prepoznato: {1} '.format((x, y, w, h), decode_predictions(preds, top=3)[0])


    return street
    # cv2.imshow('stop', street)
    # cv2.waitKey(3000000)
    # cv2.destroyAllWindows()