import cv2
import mediapipe as mp
import time

# FPS Counter variables
previous_time = 0

def FPSCalculator(frame):
    global previous_time
    current_time = time.time()
    
    # Skip calculation on first frame
    if previous_time != 0:
        fps = int(1 / (current_time - previous_time))
        cv2.putText(frame, f"FPS: {fps}", (0, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 1)
    
    # Update for next frame
    previous_time = current_time
    return frame

class MediaPipe:
    def __init__(self, static_mode=False, max_hands=2, detection_conf=0.5, tracking_conf=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def process_frame(self, frame):
        # Process the frame with MediaPipe and Helps With Performance
        frame.flags.writeable = False
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        # Convert back to BGR
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        
        # Draw hand landmarks if detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        return frame, results

class CameraCapture:
    def __init__(self, CameraID, WindowName):
        self.CameraID = CameraID
        self.WindowName = WindowName
        self.hand_tracker = MediaPipe()  # Initialize MediaPipe hand tracker
        
    def MainVideoCapture(self):
        CameraFeed = cv2.VideoCapture(self.CameraID)
        while CameraFeed.isOpened():
            Succes, frame = CameraFeed.read()
            if not Succes:
                print("Ignoring empty frame")
                continue
            
            # Flip and process frame
            FlippedFrame = cv2.flip(frame, 1)
            
            # Process with MediaPipe
            processed_frame, _ = self.hand_tracker.process_frame(FlippedFrame)
            
            # Add FPS counter
            processed_frame = FPSCalculator(processed_frame)
            
            # Display result
            cv2.imshow(self.WindowName, processed_frame)
            
            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            
        CameraFeed.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # User input Settings
    CameraInputID = int(input("Please enter your Camera-WebCam InputID (0 for default): "))
    WindowTitleName = input("Please enter your window Title Name: ")
    
    ApplicationCapture = CameraCapture(CameraInputID, WindowTitleName)
    ApplicationCapture.MainVideoCapture()


# ** Code Order
# ---->Imports Library
# ----------> 1.Calculates FPS
# -------------> 2.Uses Mediapipe Library
# ---------------> 3.Takes Camera Feed Capture
# Finally The Main Loop and uses the last three Steps (1 - 3) In order