import cv2
import time


def Main():
  print("Welcome to my App")
  CameraCapture = cv2.VideoCapture(0)
  FpsPrevTime = 0
  
  while CameraCapture.isOpened() :
    ret, frame = CameraCapture.read()
    
    # Flip The Feed
    
    frame = cv2.flip(frame, 1)
    
    # Calculates Fps
    CurrTime = time.time()
    FPS = 1 / (CurrTime - FpsPrevTime)
    FpsPrevTime = CurrTime
    # Display the Fps Counter
    
    cv2.putText(frame, f"FPS: {int(FPS)}", (10, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow("TestApp",frame)
    cv2.waitKey(1)
    
    
    
    # Break Lopp with Q pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break
    
Main()
