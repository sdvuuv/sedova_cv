import cv2
import mss                    
import pyautogui as pag
import time
import numpy as np
from core import Object
        
player = Object("\Objects\dino.png", "dino")
player_thresh = Object(r"\Objects\thresh.png", 'thresh_crop')
player_thresh2 = Object(r"\Objects\thresh2.png", 'thresh_crop')
enemies = [Object("\Objects\cact1.png", "cact1"), Object("\Objects\cact2.png", "cact2"), Object("\Objects\cact4.png", 'cact4'), Object("\Objects\cact_small_1.png", "cact_small_1"), Object("\Objects\cact_small_2.png", "cact_small_2"), Object("\Objects\cact_small_3.png", "cact_small_3"), Object("\Objects\eagle.png", "eagle" )]
sct = mss.mss() 
                     
startTime = time.time()
prevTime = time.time() 
original_y = 0
speedRate = 12         
distanceThreshold = 110              
is_down = False

while True:
    img = np.array(sct.grab((0, 0, 1920, 1080)))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if player.match(img): 
        topleft_x_dino = int(player.location[0][0])
        topleft_x_crop = int(player.location[0][0] + 1.2*player.width)
        topleft_y = int(player.location[0][1] - 2 * player.height)
        topleft_y_dino = int(player.location[0][1] - 3 * player.height)
        bottomRight_x = int(player.location[1][0] + 9 * player.width)
        bottomRight_x_dino = int(player.location[1][0] + 0.2 * player.width)
        bottomRight_y = int(player.location[1][1]) 
        break        
img_orig_dino = np.array(sct.grab((topleft_x_dino, topleft_y_dino, bottomRight_x_dino, bottomRight_y)))
img_orig_crop = np.array(sct.grab((topleft_x_crop, topleft_y, bottomRight_x, bottomRight_y)))

img_crop = cv2.cvtColor(img_orig_crop, cv2.COLOR_BGR2GRAY)
img_dino = cv2.cvtColor(img_orig_dino, cv2.COLOR_BGR2GRAY)
img_crop = cv2.bitwise_not (img_crop) 
img_dino = cv2.bitwise_not (img_dino) 

__ , thresh_crop = cv2.threshold(img_crop, 80, 255, cv2.THRESH_BINARY)
thresh_crop =  cv2.erode (thresh_crop, None, iterations= 1 ) 
thresh_crop =  cv2.dilate (thresh_crop, None, iterations= 2  )

__ , thresh_dino = cv2.threshold(img_dino, 80, 255, cv2.THRESH_BINARY)
thresh_dino =  cv2.erode (thresh_dino, None, iterations= 1 ) 
thresh_dino =  cv2.dilate (thresh_dino, None, iterations= 2  )
cnts, _ = cv2.findContours(thresh_dino, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for i, cnt in enumerate( cnts): 
        x, y, w, h = cv2.boundingRect(cnt)      
        player_thresh.match(thresh_dino)
        print(player_thresh.location[0])
        print(len(cnts))
        if w == 42:
            dino_x = x + w//2 
while True:  
    img_orig_dino = np.array(sct.grab((topleft_x_dino, topleft_y_dino, bottomRight_x_dino, bottomRight_y)))
    img_orig_crop  = np.array(sct.grab((topleft_x_crop, topleft_y, bottomRight_x, bottomRight_y)))
    
    img_crop = cv2.cvtColor(img_orig_crop, cv2.COLOR_BGR2GRAY)
    img_dino = cv2.cvtColor(img_orig_dino, cv2.COLOR_BGR2GRAY)
    img_crop = cv2.bitwise_not (img_crop) 
    img_dino = cv2.bitwise_not (img_dino) 

    __ , thresh_crop = cv2.threshold(img_crop, 80, 255, cv2.THRESH_BINARY)
    thresh_crop =  cv2.erode (thresh_crop, None, iterations= 1)
    thresh_crop =  cv2.dilate (thresh_crop, None, iterations= 2)
    
    __ , thresh_dino = cv2.threshold(img_dino, 80, 255, cv2.THRESH_BINARY)
    thresh_dino =  cv2.erode (thresh_dino, None, iterations= 1 ) 
    thresh_dino =  cv2.dilate (thresh_dino, None, iterations= 2  )
    
    cnts, _ = cv2.findContours(thresh_crop, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    cnts_dino, _ = cv2.findContours(thresh_dino, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    for i, cnt in enumerate( cnts): 
        x, y, w, h = cv2.boundingRect(cnt)    
        if x < distanceThreshold:
             pag.press('space')     
    player_thresh.match(thresh_dino)
    if not player_thresh.location:
        player_thresh2.match(thresh_dino)
        player_thresh = player_thresh2
    print(f"{len(cnts_dino)} : {player_thresh.location[0][1]}")

    cv2.imshow("Screen", thresh_crop)  
    cv2.imshow("Screen2", thresh_dino)  
    
    if(cv2.waitKey(1) == ord('q')): 
        break    
    
    pag.keyUp('down')   
            
    if time.time() - startTime < 180 and time.time() - prevTime > 5:
        distanceThreshold += speedRate   
        prevTime = time.time() 
         
    cv2.imshow("Screen", thresh_crop)  
    cv2.imshow("Screen2", thresh_dino)  
    
    if(cv2.waitKey(1) == ord('q')): 
        break
     