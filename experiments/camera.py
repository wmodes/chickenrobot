import cv2

# max resolution of the hbv-1615 is 1280x1024


cam1 = cv2.VideoCapture(0)
cam1.set(3, 1280)
cam1.set(4, 1024)
s, im = cam1.read() # captures image
cv2.imwrite("test1.bmp",im) # writes image test.bmp to disk

# cam2 = cv2.VideoCapture(2)
# cam2.set(3, 1280)
# cam2.set(4, 1024)
# s, im = cam2.read() # captures image
# cv2.imwrite("test2.bmp",im) # writes image test.bmp to disk
