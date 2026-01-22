import cv2
import mediapipe as mp
from numpy.version import release

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7
)

cap  = cv2.VideoCapture(0)

def fingers_up(hand_landmarks):
    tips = [4,8,12,16,20]
    pip = [3,6,10,14,18]
    fingers = []


    for tip, joint in zip(tips, pip):
        if hand_landmarks[tip].y < hand_landmarks.landmark[joint].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers



while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)


    gesture = "Unknown"

    if   results.multi_hand_landmarks:
        hands =  results.multi_hand_landmarks[0]
        finger_state = fingers_up(hands)

        if finger_state == [0,0,0,0, 0]:
            gesture = "BLM"
        elif finger_state == [1,0,0,0, 0]:
            gesture = "Thumbs up"
        elif finger_state == [1,1,1, 0,0]:
            gesture = 'Serbian'
        elif finger_state == [1,1,1,1,1]:
            gesture = 'Elon'
        elif finger_state == [0,0,1,0,0]:
            gesture = 'Fuk u'

    cv2.putText(frame,gesture,(30,50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.imshow("Hand Gesture",frame)

    if  cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cap.release()
    cv2.destroyAllWindows()


