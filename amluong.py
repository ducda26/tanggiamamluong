import cv2
import time 
import hand as htm

pTime=0 #Thời gian bắt đầu
cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.7) 
#detectionCon=0.7 độ tin cậy phát hiện ra lòng bàn tay là 0.7

while True:
    ret, frame = cap.read()
    frame = detector.findHands(frame) #Tìm bàn tay (phát hiện)
    lmList = detector.findPosition(frame, draw=False) # phát hiện vị trí, đẩy vào list các vị trí
    # print(lmList) đẩy ra vị trí của 21 point (từ 0-20)  trên bàn tay
    
    if len(lmList)!= 0: #Có tín hiệu bàn tay mới bắt đầu làm
        # cần sử dụng 2 ngón trỏ và ngón cái (point 4, và 8)
        print(lmList[4],lmList[8]) # đẩy về giá trị điểm 4 và 8
    
    # viết ra FPS
    cTime = time.time()  # trả về số giây, tính từ 0:0:00 ngày 1/1/1970 theo giờ  utc , gọi là(thời điểm bắt đầu thời gian)
    fps = 1 / (cTime - pTime)  # tính fps Frames per second - đây là  chỉ số khung hình trên mỗi giây
    pTime = cTime
    # show fps lên màn hình
    cv2.putText(frame, f"FPS: {int(fps)}", (150, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    
    cv2.imshow("Anh Duc", frame)
    if cv2.waitKey(1)==ord("q"): #độ trễ 1/1000s, nếu bấm q sẽ thoát
        break

cap.release() #giải phóng webcame
cv2.destroyAllWindows()