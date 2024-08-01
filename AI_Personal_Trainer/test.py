import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)

detector = pm.poseDetector()
count_right_arm = 0
count_left_arm = 0
count_right_squat = 0
count_left_squat = 0
dir_right_arm = 0
dir_left_arm = 0
dir_right_squat = 0
dir_left_squat = 0
pTime = 0

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.resize(img, (1280, 720))
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    
    if len(lmList) != 0:
        # 오른팔 감지
        angle_right_arm = detector.findAngle(img, 12, 14, 16)
        per_right_arm = np.interp(angle_right_arm, (210, 310), (0, 100))
        
        # 왼팔 감지
        angle_left_arm = detector.findAngle(img, 11, 13, 15)
        per_left_arm = np.interp(angle_left_arm, (210, 310), (0, 100))

        # 오른쪽 스쿼트 감지
        angle_right_squat = detector.findAngle(img, 24, 26, 28)
        per_right_squat = np.interp(angle_right_squat, (90, 170), (100, 0))

        # 왼쪽 스쿼트 감지
        angle_left_squat = detector.findAngle(img, 23, 25, 27)
        per_left_squat = np.interp(angle_left_squat, (90, 170), (100, 0))

        # 카운트 로직
        if per_right_arm == 100:
            if dir_right_arm == 0:
                count_right_arm += 0.5
                dir_right_arm = 1
        if per_right_arm == 0:
            if dir_right_arm == 1:
                count_right_arm += 0.5
                dir_right_arm = 0

        if per_left_arm == 100:
            if dir_left_arm == 0:
                count_left_arm += 0.5
                dir_left_arm = 1
        if per_left_arm == 0:
            if dir_left_arm == 1:
                count_left_arm += 0.5
                dir_left_arm = 0

        if per_right_squat == 100:
            if dir_right_squat == 0:
                count_right_squat += 0.5
                dir_right_squat = 1
        if per_right_squat == 0:
            if dir_right_squat == 1:
                count_right_squat += 0.5
                dir_right_squat = 0

        if per_left_squat == 100:
            if dir_left_squat == 0:
                count_left_squat += 0.5
                dir_left_squat = 1
        if per_left_squat == 0:
            if dir_left_squat == 1:
                count_left_squat += 0.5
                dir_left_squat = 0
        
        # 화면 오른쪽에 정보 표시
        info_width = 300
        cv2.rectangle(img, (img.shape[1] - info_width, 0), (img.shape[1], img.shape[0]), (245, 117, 16), -1)
        
        # 텍스트 표시
        cv2.putText(img, "REPS", (img.shape[1] - info_width + 15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(img, f"Right Arm: {int(count_right_arm)}", (img.shape[1] - info_width + 15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(img, f"Left Arm: {int(count_left_arm)}", (img.shape[1] - info_width + 15, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(img, f"Right Squat: {int(count_right_squat)}", (img.shape[1] - info_width + 15, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(img, f"Left Squat: {int(count_left_squat)}", (img.shape[1] - info_width + 15, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # 퍼센트 바 표시
        cv2.putText(img, "RIGHT ARM", (img.shape[1] - info_width + 15, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.rectangle(img, (img.shape[1] - info_width + 15, 200), (img.shape[1] - 15, 230), (0, 255, 0), 3)
        cv2.rectangle(img, (img.shape[1] - info_width + 15, 200), (int((img.shape[1] - info_width + 15) + (info_width - 30) * (per_right_arm/100)), 230), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f"{int(per_right_arm)}%", (img.shape[1] - info_width + 20, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.putText(img, "LEFT ARM", (img.shape[1] - info_width + 15, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.rectangle(img, (img.shape[1] - info_width + 15, 270), (img.shape[1] - 15, 300), (0, 255, 0), 3)
        cv2.rectangle(img, (img.shape[1] - info_width + 15, 270), (int((img.shape[1] - info_width + 15) + (info_width - 30) * (per_left_arm/100)), 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f"{int(per_left_arm)}%", (img.shape[1] - info_width + 20, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.putText(img, "RIGHT SQUAT", (img.shape[1] - info_width + 15, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.rectangle(img, (img.shape[1] - info_width + 15, 340), (img.shape[1] - 15, 370), (0, 255, 0), 3)
        cv2.rectangle(img, (img.shape[1] - info_width + 15, 340), (int((img.shape[1] - info_width + 15) + (info_width - 30) * (per_right_squat/100)), 370), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f"{int(per_right_squat)}%", (img.shape[1] - info_width + 20, 365), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.putText(img, "LEFT SQUAT", (img.shape[1] - info_width + 15, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.rectangle(img, (img.shape[1] - info_width + 15, 410), (img.shape[1] - 15, 440), (0, 255, 0), 3)
        cv2.rectangle(img, (img.shape[1] - info_width + 15, 410), (int((img.shape[1] - info_width + 15) + (info_width - 30) * (per_left_squat/100)), 440), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f"{int(per_left_squat)}%", (img.shape[1] - info_width + 20, 435), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (11, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("AI Trainer", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()