import cv2

# Main Function

def Main ():
    CameraCapture = cv2.VideoCapture(0)
    while CameraCapture.isOpened():
        ret,frame = CameraCapture.read()
        CameraFeed = frame
        
        FlippedFeed = cv2.flip(CameraFeed,1)
        cv2.imshow("Camera Feed",FlippedFeed)
        
        # cv2.imshow("Camera Feed",frame)
        
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    CameraCapture.release()
    cv2.destroyAllWindows()
Main()



