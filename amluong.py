import cv2
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    cv2.imshow("Anh Duc", frame)
    if cv2.waitKey(1)==ord("q"): #độ trễ 1/1000s, nếu bấm q sẽ thoát
        break

cap.release() #giải phóng webcame
cv2.destroyAllWindows()