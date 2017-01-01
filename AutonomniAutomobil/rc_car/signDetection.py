import cv2

# constants
IMAGE_SIZE = 200.0
MATCH_THRESHOLD = 3

cascade_url = 'frontal_stop_sign_cascade.xml'
img_url = 'stoptest4.jpg'
roundabout_cascade = cv2.CascadeClassifier(cascade_url)
street = cv2.imread(img_url)

# detekcija znaka na slici
gray = cv2.cvtColor(street, cv2.COLOR_RGB2GRAY)
signs = roundabout_cascade.detectMultiScale(
    gray,
    scaleFactor=1.4,
    minNeighbors=3
)

# orb i feature matcher
orb = cv2.ORB()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# kljucne karakteristike za znake koje sluze za odbacivanje lose prepoznatih delova
roadsign = cv2.imread('stop5.jpg', 0)
kp_r, des_r = orb.detectAndCompute(roadsign, None)

# prolazak kroz sve znake
for (x, y, w, h) in signs:

    # vadjenje objekta
    obj = gray[y:y + h, x:x + w]
    ratio = IMAGE_SIZE / obj.shape[1]
    obj = cv2.resize(obj, (int(IMAGE_SIZE), int(obj.shape[0] * ratio)))

    # pronalazenje karakteristika na slici
    kp_o, des_o = orb.detectAndCompute(obj, None)
    if len(kp_o) == 0 or des_o == None: continue

    matches = bf.match(des_r, des_o)

    # obelezavanje detektovanog znaka
    if (len(matches) >= MATCH_THRESHOLD):
        cv2.rectangle(street, (x, y), (x + w, y + h), (255, 0, 0), 2)


cv2.imshow('stop', street)
cv2.waitKey(3000)
cv2.destroyAllWindows()