import cv2
import time 

pTime=0 #Thời gian bắt đầu
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
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