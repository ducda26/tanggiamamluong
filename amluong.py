import cv2
import time
import math
import hand as htm

# Thư viện pycaw
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

pTime = 0  # Thời gian bắt đầu
cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.7)
# detectionCon=0.7 độ tin cậy phát hiện ra lòng bàn tay là 0.7

# Code mẫu thư viện pycaw (điều chỉnh âm thanh)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()  # Phạm vi âm lượng
# print(volRange)
# print(type(volRange))

# print(volRange[0])
# print(volRange[1])
minVol = volRange[0]
maxVol = volRange[1]


while True:
    ret, frame = cap.read()
    frame = detector.findHands(frame)  # Tìm bàn tay (phát hiện)
    # phát hiện vị trí, đẩy vào list các vị trí
    lmList = detector.findPosition(frame, draw=False)
    # print(lmList) đẩy ra vị trí của 21 point (từ 0-20)  trên bàn tay

    if len(lmList) != 0:  # Có tín hiệu bàn tay mới bắt đầu làm
        # cần sử dụng 2 ngón trỏ và ngón cái (point 4, và 8)
        # print(lmList[4], lmList[8])  # đẩy về giá trị điểm 4 và 8
        x1, y1 = lmList[4][1], lmList[4][2]  # get tọa độ đầu ngón cái
        x2, y2 = lmList[8][1], lmList[8][2]  # get tọa độ đầu ngón trỏ

        # vẽ 2 đường tròn trên 2 đầu ngón cái và ngón trỏ
        cv2.circle(frame, (x1, y1), 15, (255, 0, 255), -1)
        cv2.circle(frame, (x2, y2), 15, (255, 0, 255), -1)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # vẽ đường tròn giữa 2 đường thằng nối ngón cái và ngón giữa
        cx, cy = (x1+x2)//2, (y1+y2)//2  # xác định tâm
        cv2.circle(frame, (cx, cy), 15, (255, 0, 255), -1)

        # xác định độ dài đoạn thẳng nối từ ngón trái đến ngón trỏ
        # 1 phút Toán học =))
        length = math.hypot(x2-x1, y2-y1)
        # print(length)  # độ dài tay tôi vào khoảng 25 đến 250

        # dải âm lượng từ -65,25 đến 0
        # -60: thay đổi -60 thì âm thanh máy tính thay đổi (-65,25-->0)
        volume.SetMasterVolumeLevel(-60.0, None)

    # viết ra FPS
    # trả về số giây, tính từ 0:0:00 ngày 1/1/1970 theo giờ  utc , gọi là(thời điểm bắt đầu thời gian)
    cTime = time.time()
    # tính fps Frames per second - đây là  chỉ số khung hình trên mỗi giây
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # show fps lên màn hình
    cv2.putText(frame, f"FPS: {int(fps)}", (150, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Anh Duc", frame)
    if cv2.waitKey(1) == ord("q"):  # độ trễ 1/1000s, nếu bấm q sẽ thoát
        break

cap.release()  # giải phóng webcame
cv2.destroyAllWindows()
