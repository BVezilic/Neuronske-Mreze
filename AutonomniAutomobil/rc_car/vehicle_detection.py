import cv2

def read_img(path):
    #Calls opencv function for reading image
    return cv2.imread(path, cv2.IMREAD_COLOR)

def show_img(img):
    #Shows image in new window. Press ESC to close it.
    cv2.imshow('put',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def img_to_gray(img):
    #Calls opencv function for transforming image to gray-scale image
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def get_cascade(path):
	#Calls openCv function for creating cascade classifier
	return cv2.CascadeClassifier(path)
	
def detected_cars(cscd,img):
	#Calls openCv function for detecting objects with cascade classifier
	return cscd.detectMultiScale(img, 1.1, 1)

def draw_rectangles(img,cars):
	#Draws rectangles aroung detected objects
	for (x,y,w,h) in cars:
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)