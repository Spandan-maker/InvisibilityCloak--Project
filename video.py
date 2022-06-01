import cv2
import time
import numpy as np
import keyboard

print("Press ESC or Enter to end")

forcc = cv2.VideoWriter_fourcc(*"XVID")
outputFile = cv2.VideoWriter("output.avi", forcc, 20.0, (640, 480))

cam = cv2.VideoCapture(0)

time.sleep(1)
bg = 0

for i in range(60):
    bg = cv2.imread("mail.png")

while (cam.isOpened()):
    ret, img = cam.read()

    if not ret:
        break

    img = np.flip(img, axis = 1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lowerRed = np.array([0, 120, 50])
    upperRed = np.array([10, 255, 255])
    mask_1 = cv2.inRange(hsv, lowerRed, upperRed)

    lowerRed = np.array([170, 120, 70])
    upperRed = np.array([180, 255, 255])
    mask_2 = cv2.inRange(hsv, lowerRed, upperRed)

    mask_1 = mask_1 + mask_2

    # Mask 1 is red colour (res2)
    # Mask 2 is bg (res1)

    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN,  np.ones((3,3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE,  np.ones((3,3), np.uint8))

    mask_2 = cv2.bitwise_not(mask_1)
    
    res1 = cv2.bitwise_and(img, img, mask = mask_2)
    res2 = cv2.bitwise_and(bg, bg, mask = mask_1)

    final_output = cv2.addWeighted(res1, 1, res2, 1.3, 0)
    outputFile.write(final_output)

    cv2.imshow("magic", final_output)
    cv2.waitKey(1)

    if keyboard.is_pressed("esc") or keyboard.is_pressed("enter"):
        break

cam.release()
#out.release()

cv2.destroyAllWindows()







