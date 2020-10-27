import cv2

cam = cv2.VideoCapture(0)
s, im = cam.read() # captures image
cv2.imwrite("test1.bmp",im) # writes image test.bmp to disk

cam = cv2.VideoCapture(2)
s, im = cam.read() # captures image
cv2.imwrite("test2.bmp",im) # writes image test.bmp to disk
