class FingersDetector:
    def __init__(self):
        self.tipIndex = [4, 8, 12, 16, 20]
        self.fingers = None

    def detect_fingers(self, lm_list):
        self.fingers = []
        # Thumb
        if lm_list[self.tipIndex[0]][1] > lm_list[self.tipIndex[0] - 1][1]:
            self.fingers.append(True)
        else:
            self.fingers.append(False)

        # Fingers
        for index in range(1, 5):
            if lm_list[self.tipIndex[index]][2] < lm_list[self.tipIndex[index] - 2][2]:
                self.fingers.append(True)
            else:
                self.fingers.append(False)
        return self.fingers

    def is_up_only(self, index_up_fingers):
        index_down_fingers = [index for index in range(5) if index not in index_up_fingers]

        # Only the right fingers are raised
        for index in index_up_fingers:
            if not self.fingers[index]:
                return False

        # The remaining ones are pubescent
        for index in index_down_fingers:
            if self.fingers[index]:
                return False

        return True
    