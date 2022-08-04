import cv2
import numpy as np
import pyautogui

import DrawUtils
import FingersDetector
import HandLandMarks
import MouseAction
import PermissionForActionsMouse

###########
detector = HandLandMarks.HandDetector(max_hands=1)
drawing_utils = DrawUtils.DrawUtils()
fingers_position = FingersDetector.FingersDetector()
mouse_actions = MouseAction.MouseAction()
permission = PermissionForActionsMouse.PermissionForActionsMouse()

indentOfScreen = 150
cursorSpeed = 1.5

weightCam, heightCam = 640, 480
widthScreen, heightScreen = pyautogui.size()

camID = 0
cam = cv2.VideoCapture(camID)
cam.set(3, weightCam)
cam.set(4, heightCam)
###########

while True:
    # Find hand landmarks
    success, img = cam.read()

    if not detector.find_hands(img):
        # Display
        drawing_utils.display_img(img)
        continue

    lmList = detector.find_position(img)

    # Draw skeleton hand and control points
    img = drawing_utils.draw_skeleton_hands(img, detector.get_results_multi_hand_landmarks())
    img = drawing_utils.draw_hand_control_points(img, lmList)

    # Check which fingers are up
    fingers_position.detect_fingers(lmList)

    # Only Index Finger : Moving Mode
    if fingers_position.is_up_only([1]):
        # Get the tip of the index fingers
        index_fingers_x, index_fingers_y = lmList[8][1:]

        # Selecting the control finger
        img = drawing_utils.draw_circle(img, index_fingers_x, index_fingers_y)

        # Convert Coordinates for Screen
        screen_index_fingers_x = np.interp(index_fingers_x,
                                           (indentOfScreen, weightCam - indentOfScreen),
                                           (0, widthScreen * cursorSpeed))

        screen_index_fingers_y = np.interp(index_fingers_y,
                                           (indentOfScreen, heightCam - indentOfScreen),
                                           (0, heightScreen * cursorSpeed))

        # Move Mouse
        mouse_actions.moving_mode(screen_index_fingers_x, screen_index_fingers_y)

    # Both Index and middle fingers are up : Clicking Left Mode
    if fingers_position.is_up_only([1, 2]):
        # Get the tip of the index and middle fingers
        index_fingers_x, index_fingers_y = lmList[8][1:]
        middle_fingers_x, middle_fingers_y = lmList[12][1:]

        # Find the distance between the index and middle finger
        distance = detector.find_distance(8, 12)

        # DrawUtils a line between the corresponding fingers
        img = drawing_utils.draw_line_distance_fingers(img,
                                                       index_fingers_x,
                                                       index_fingers_y,
                                                       middle_fingers_x,
                                                       middle_fingers_y)

        # Click mouse if distance short and delay in pressing expired
        if permission.permission_for_mouse_left_click(distance):
            # Highlighting the click response
            img = drawing_utils.draw_circle(img,
                                            (index_fingers_x + middle_fingers_x) // 2,
                                            (index_fingers_y + middle_fingers_y) // 2,
                                            r=0,
                                            g=255,
                                            b=0)

            # Mouse left click
            mouse_actions.click_left_mode()

    # Both Index and middle fingers are up : Clicking Right Mode
    if fingers_position.is_up_only([0, 1]):
        # Get the tip of the index and thumb fingers
        thumb_fingers_x, thumb_fingers_y = lmList[4][1:]
        index_fingers_x, index_fingers_y = lmList[8][1:]

        # Find the distance between your index finger and thumb
        distance = detector.find_distance(4, 8)

        # DrawUtils a line between the corresponding fingers
        img = drawing_utils.draw_line_distance_fingers(img,
                                                       thumb_fingers_x,
                                                       thumb_fingers_y,
                                                       index_fingers_x,
                                                       index_fingers_y)

        # Click mouse if distance short and delay in pressing expired
        if permission.permission_for_mouse_right_click(distance):
            # Highlighting the click response
            img = drawing_utils.draw_circle(img,
                                            (thumb_fingers_x + index_fingers_x) // 2,
                                            (thumb_fingers_y + index_fingers_y) // 2,
                                            r=0,
                                            g=255,
                                            b=0)

            # Mouse right click
            mouse_actions.click_right_mode()

    # Output of the original image and all geometries
    drawing_utils.display_img(img)
