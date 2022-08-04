import time


class PermissionForActionsMouse:
    def __init__(self, distance_left_click=30, distance_right_click=30, delay_in_pressing=0.3):
        self.distanceLeftClick = distance_left_click
        self.distanceRightClick = distance_right_click
        self.delayInPressing = delay_in_pressing
        self.previousTimeLeftClick = 0
        self.previousTimeRightClick = 0

    def permission_for_mouse_left_click(self, distance):
        # Added permission to left-Click
        current_time_click = time.time()
        delay = current_time_click - self.previousTimeLeftClick

        print(delay)
        if distance < self.distanceLeftClick and delay > self.delayInPressing:
            self.previousTimeLeftClick = current_time_click
            return True

        return False

    def permission_for_mouse_right_click(self, distance):
        # Added permission to right-Click
        current_time_click = time.time()
        delay = current_time_click - self.previousTimeRightClick

        if distance < self.distanceRightClick and delay > self.delayInPressing:
            self.previousTimeRightClick = current_time_click
            return True

        return False
