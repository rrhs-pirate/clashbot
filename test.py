import cv2
import pyautogui
import keyboard



img = cv2.imread('./images/electro-dragon.png')
eyeball = cv2.imread('./images/eyeball.png')


cv2.imshow('dragon', img)
cv2.waitKey(5)

print('Move to top left and press a')
keyboard.wait('a')

left_top = pyautogui.position()


eye_h = eyeball.shape[0]
eye_w = eyeball.shape[1]

res = cv2.matchTemplate(img, eyeball, cv2.TM_CCOEFF_NORMED)

values = cv2.minMaxLoc(res)
max_loc = values[3]

cv2.rectangle(img, max_loc, (max_loc[0] + eye_w, max_loc[1] + eye_h), (255, 0, 255), 3)

pyautogui.moveTo((left_top[0] + max_loc[0], left_top[1] + max_loc[1]), duration=0.25)

cv2.imshow('Dragon', img)
cv2.waitKey(0)