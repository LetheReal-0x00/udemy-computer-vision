import cv2
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
from PIL import Image

img = cv2.imread('../DATA/dog_backpack.jpg')
fix_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

def draw_circle(event, x, y, flags, params):
    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(fix_img,(x,y),100,(255,0,0),thickness=5)

cv2.namedWindow(winname="doggo")
cv2.setMouseCallback("doggo",draw_circle)

while True:
    cv2.imshow('doggo',fix_img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()