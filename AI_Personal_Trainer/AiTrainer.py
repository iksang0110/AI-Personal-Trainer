import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)

detector = pm.poseDetector()
count_right = 0
count_left = 0
count_squat = 0
dir_right = 0
dir_left = 0
dir_squat = 0
pTime = 0

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.resize(img, (1280, 720))
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    
    if len(lmList) != 0:
        # 오른팔 감지 (기존 코드)
        angle_right = detector.findAngle(img, 12, 14, 16)
        per_right = np.interp(angle_right, (210, 310), (0, 100))
        bar_right = np.interp(angle_right, (220, 310), (650, 100))

        color_right = (255, 0, 255)
        if per_right == 100:
            color_right = (0, 255, 0)
            if dir_right == 0:
                count_right += 0.5
                dir_right = 1
        if per_right == 0:
            color_right = (0, 255, 0)
            if dir_right == 1:
                count_right += 0.5
                dir_right = 0

        # 왼팔 감지 (기존 코드)
        angle_left = detector.findAngle(img, 11, 13, 15)
        per_left = np.interp(angle_left, (210, 310), (0, 100))
        bar_left = np.interp(angle_left, (220, 310), (650, 100))

        color_left = (255, 0, 255)
        if per_left == 100:
            color_left = (0, 255, 0)
            if dir_left == 0:
                count_left += 0.5
                dir_left = 1
        if per_left == 0:
            color_left = (0, 255, 0)
            if dir_left == 1:
                count_left += 0.5
                dir_left = 0

        # 스쿼트 감지 (새로운 코드)
        angle_squat = detector.findAngle(img, 24, 26, 28)  # 오른쪽 엉덩이, 무릎, 발목
        per_squat = np.interp(angle_squat, (90, 170), (100, 0))
        bar_squat = np.interp(angle_squat, (90, 170), (650, 100))

        color_squat = (255, 0, 255)
        if per_squat == 100:
            color_squat = (0, 255, 0)
            if dir_squat == 0:
                count_squat += 0.5
                dir_squat = 1
        if per_squat == 0:
            color_squat = (0, 255, 0)
            if dir_squat == 1:
                count_squat += 0.5
                dir_squat = 0

        # 오른팔 바 그리기 (기존 코드)
        cv2.rectangle(img, (1100, 100), (1175, 650), color_right, 3)
        cv2.rectangle(img, (1100, int(bar_right)), (1175, 650), color_right, cv2.FILLED)
        cv2.putText(img, f'{int(per_right)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color_right, 4)

        # 왼팔 바 그리기 (기존 코드)
        cv2.rectangle(img, (50, 100), (125, 650), color_left, 3)
        cv2.rectangle(img, (50, int(bar_left)), (125, 650), color_left, cv2.FILLED)
        cv2.putText(img, f'{int(per_left)} %', (50, 75), cv2.FONT_HERSHEY_PLAIN, 4, color_left, 4)

        # 스쿼트 바 그리기 (새로운 코드)
        cv2.rectangle(img, (575, 100), (650, 650), color_squat, 3)
        cv2.rectangle(img, (575, int(bar_squat)), (650, 650), color_squat, cv2.FILLED)
        cv2.putText(img, f'{int(per_squat)} %', (575, 75), cv2.FONT_HERSHEY_PLAIN, 4, color_squat, 4)

        # 오른팔 컬 횟수 그리기
        cv2.rectangle(img, (1000, 600), (1150, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count_right)), (1020, 710), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 10)

        # 왼팔 컬 횟수 그리기
        cv2.rectangle(img, (50, 600), (200, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count_left)), (70, 710), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 10)

        # 스쿼트 횟수 그리기 (새로운 코드)
        cv2.rectangle(img, (525, 600), (675, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count_squat)), (545, 710), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 10)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()