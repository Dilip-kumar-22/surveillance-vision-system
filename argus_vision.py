import cv2, time, pandas
from datetime import datetime

# --- CONFIGURATION ---
# 0 usually maps to the built-in webcam. Change to 1 if using external.
VIDEO_SOURCE = 0 
MIN_AREA = 1000  # Sensitivity: Lower number = more sensitive

first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])

video = cv2.VideoCapture(VIDEO_SOURCE)
print("[*] ARGUS SYSTEM INITIALIZED. WAITING FOR MOTION...")

# Give camera time to warm up
time.sleep(2)

try:
    while True:
        check, frame = video.read()
        status = 0
        
        if not check:
            break

        # Convert to Grayscale (Color is irrelevant for motion)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Blur to remove noise/flicker
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Capture the baseline environment
        if first_frame is None:
            first_frame = gray
            continue

        # Calculate difference (Delta)
        delta_frame = cv2.absdiff(first_frame, gray)
        
        # Threshold: If pixel difference > 30, mark as white (motion)
        thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        # Find contours of the moving objects
        (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv2.contourArea(contour) < MIN_AREA:
                continue
            
            # Motion confirmed
            status = 1
            # Draw tactical box
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        status_list.append(status)
        status_list = status_list[-2:]

        # Record timestamps of entry/exit
        if status_list[-1] == 1 and status_list[-2] == 0:
            times.append(datetime.now())
            print(f"[!] MOTION DETECTED: {datetime.now()}")
        if status_list[-1] == 0 and status_list[-2] == 1:
            times.append(datetime.now())
            print(f"[-] TARGET CLEAR: {datetime.now()}")

        # Display Feeds
        cv2.imshow("Argus Feed (Press 'q' to Quit)", frame)
        # cv2.imshow("Delta Feed", delta_frame) # Uncomment for debugging

        key = cv2.waitKey(1)
        if key == ord('q'):
            if status == 1:
                times.append(datetime.now())
            break

    # Save Log
    print("[*] SAVING SURVEILLANCE LOG...")
    for i in range(0, len(times), 2):
        # Handle case where script ends mid-motion
        if i+1 < len(times):
            df = pandas.concat([df, pandas.DataFrame({"Start": [times[i]], "End": [times[i+1]]})], ignore_index=True)

    df.to_csv("Times.csv")
    print("[*] SYSTEM SHUTDOWN.")

    video.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(f"[!] CRITICAL FAILURE: {e}")
