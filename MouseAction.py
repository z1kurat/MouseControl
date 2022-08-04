import pyautogui
import win32api
import win32con

widthScreen, heightScreen = pyautogui.size()
previousX, previousY = 0, 0
currentX, currentY = 0, 0


class MouseAction:
    def __init__(self, smoothening=10):
        self.smoothening = smoothening

    def moving_mode(self, coordinate_x, coordinate_y):
        # Smoothen Values
        global widthScreen, heightScreen, previousX, previousY, currentX, currentY

        currentX = previousX + (coordinate_x - previousX) / self.smoothening
        currentY = previousY + (coordinate_y - previousY) / self.smoothening

        # Move Mouse
        win32api.SetCursorPos((widthScreen - int(currentX), int(currentY)))
        previousX, previousY = currentX, currentY

    @staticmethod
    def click_left_mode():
        # Left click mouse
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    @staticmethod
    def click_right_mode():
        # Right click mouse
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    def draw_mode(self):
        pass
