import cv2
import numpy as np
import datetime

min_contour_width=45 #40  ความละเอียดในการสร้าง rectangle (ของกรอบ Object)
min_contour_height=45 #40 ความละเอียดในการสร้าง rectangle (ของกรอบ Object)

offset=3.5   #10 ค่าความถูกต้อง

# ระดับความสูง-ต่ำ ของครอสไลน์
# line_height=150 #550  บน
# line_height=330 #550  กลาง
line_height=650 #550  ล่าง

matches =[]
cars=0

clock = datetime.datetime.now()

def get_centroid(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1
    return cx,cy
    #return (cx, cy)
        

cap = cv2.VideoCapture('video3.mp4')
#cap = cv2.VideoCapture(0)




cap.set(3,1920)
cap.set(4,1080)

if cap.isOpened():
    ret,frame1 = cap.read()
else:
    ret = False
ret,frame1 = cap.read()
ret,frame2 = cap.read()
    
while ret:
    d = cv2.absdiff(frame1,frame2)
    grey = cv2.cvtColor(d,cv2.COLOR_BGR2GRAY)
    # capblur = cv2.GaussianBlur(grey,(5,5),0) 
    blur = cv2.GaussianBlur(grey,(15,15),0) # (grey,(5,5),0)
    ret , th = cv2.threshold(blur,35,255,cv2.THRESH_BINARY) # (blur,20,255,cv2.THRESH_BINARY)
    ret , th = cv2.threshold(blur,35,255,cv2.THRESH_BINARY) # (blur,20,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(th,np.ones((3,3)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))

    # ชุดคำสั่งสัณฐานวิทยา ประมวลผลภาพกับรูปร่างและโครงสร้างของภาพตามหลักคณิตศาตร์
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel) 
    contours,h = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for(i,c) in enumerate(contours):
        (x,y,w,h) = cv2.boundingRect(c)
        contour_valid = (w >= min_contour_width) and (
            h >= min_contour_height)

        if not contour_valid:
            continue
        cv2.rectangle(frame1,(x-10,y-10),(x+w+10,y+h+10),(255,0,0),2)
    
        cv2.line(frame1, (0, line_height), (2200, line_height), (0,0,255), 3)
        centroid = get_centroid(x, y, w, h)
        matches.append(centroid)
        cv2.circle(frame1,centroid, 5, (0,255,0), -1)
        cx,cy= get_centroid(x, y, w, h)
        for (x,y) in matches:
            if y<(line_height+offset) and y>(line_height-offset):
                cars=cars+1
                matches.remove((x,y))
                print("รถคันที่ : ",  cars)
                
                
    # cv2.line(frame1,(15,20),(70,50),(255,0,0),5)
    cv2.line(frame1, (0, 330), (600000, 2200), (0,250,0), 2)
    
    cv2.rectangle(frame1,(0,5),(1500,90),(255,0,179),-1)

                
    cv2.putText(frame1, "Date Time :  "+ str(clock.now()), (871, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7,# ขนาดฟอนต์
                    (255,255,255), 2) # สี + ความหนาอักษร
    cv2.putText(frame1, "Dev By : Somporn Tongsup", (870, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, # ขนาดฟอนต์
                    (255,0,0), 2) # สี + ความหนาอักษร
    cv2.putText(frame1, "Total amount of cars :  " + str(cars)+"  cars", (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2,# ขนาดฟอนต์
                    (0,0,0), 3) # สี + ความหนาอักษร    
    cv2.drawContours(frame1,contours,-1,(0,0,255),1) # เส้นประกอบรูปร่าง object (รถ)

    cv2.imshow("Vehicle counting system By Somporn  Tongsup" , frame1) # ภาพสีแสดงผล
    # cv2.imshow("Difference" , th)  # ภาพขาวดำ สำหรับประมวลผลภาพกับรูปร่างและโครงสร้างของภาพโดยนำคณิตสัณฐานวิทยา (MM : Mathematical Morphology) https://paoschools.com/python%E0%B8%99%E0%B8%B1%E0%B8%9A%E0%B8%A3%E0%B8%96%E0%B8%AD%E0%B8%B1%E0%B8%88%E0%B8%89%E0%B8%A3%E0%B8%B4%E0%B8%A2%E0%B8%B0/
   

    if cv2.waitKey(1) == ord('q'): 
   

        break
    frame1 = frame2
    ret , frame2 = cap.read()
#print(matches)    
cv2.destroyAllWindows()
cap.release()