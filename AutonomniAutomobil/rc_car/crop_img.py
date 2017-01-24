import cv2
img = cv2.imread("C:\\Users\\Komp\\Desktop\\NM\\TestGitCars\\Cars\\orb_feature.jpg")
# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
crop_img = cv2.resize(img,(1000, 1000))
cv2.imshow("cropped", crop_img)
cv2.waitKey(0)