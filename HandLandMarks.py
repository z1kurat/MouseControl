import math

import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.maxHands = max_hands
        self.detectionCon = detection_con
        self.trackCon = track_con
        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)

        self.lmList = None
        self.results = None

    def find_hands(self, img):
        # Determines the presence of a hand in the frame
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            return True
        return False

    def find_position(self, img, hand_index=0):
        # Calculation of the position of control points on the camera
        h, w, c = img.shape
        self.lmList = []

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_index]
            for index, lm in enumerate(my_hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([index, cx, cy])
        return self.lmList

    def find_distance(self, p1, p2):
        # Search for the distance between the specified control points
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        length = math.hypot(x2 - x1, y2 - y1)
        return length

    def get_lm_list(self):
        return self.lmList

    def get_results_multi_hand_landmarks(self):
        return self.results.multi_hand_landmarks
