import time

import cv2
import mediapipe as mp


class DrawUtils:
    def __init__(self, show_fps=True):
        self.mpDraw = mp.solutions.drawing_utils
        self.mpHands = mp.solutions.hands
        self.showFPS = show_fps
        self.previousTime = 0

    def draw_skeleton_hands(self, img, multi_hand_landmarks):
        # Output of lines connecting control points
        for handLms in multi_hand_landmarks:
            self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    @staticmethod
    def draw_hand_control_points(img, lm_list):
        # Output of points at control positions
        for coordinates in lm_list:
            x, y = coordinates[1:]
            cv2.circle(img, (x, y), 5, (255, 0, 255), cv2.FILLED)

        return img

    @staticmethod
    def draw_line_distance_fingers(img, x1, y1, x2, y2, r=15, t=3):
        # Highlighting the distance between the specified fingers and notification and triggering
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
        cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)

        return img

    @staticmethod
    def draw_circle(img, x1, y1, radius=15, r=255, g=0, b=255):
        cv2.circle(img, (x1, y1), radius, (r, g, b), cv2.FILLED)

        return img

    def display_img(self, img):
        if self.showFPS:
            current_time = time.time()
            fps = 1 / (current_time - self.previousTime)
            self.previousTime = current_time

            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Hand Tracking", img)
        cv2.waitKey(1)
