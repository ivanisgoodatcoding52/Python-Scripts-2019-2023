import cv2
import numpy as np

# Global variables to store the coordinates of the clicked point and the selected contour
state = {"clicked_point": None, "selected_contour": None}

def calculate_distance(known_width, focal_length, pixel_width):
    return (known_width * focal_length) / pixel_width

def convert_inches_to_cm(inches):
    return inches * 2.54

def convert_inches_to_meters(inches):
    return inches * 0.0254

def mouse_callback(event, x, y, flags, param):
    global state

    if event == cv2.EVENT_LBUTTONDOWN:
        state["clicked_point"] = (x, y)
        state["selected_contour"] = None  # Reset selected contour when a new point is clicked

def main():
    # Constants
    known_width_inches = 8.0  # Width of the object in inches (you need to measure this)
    focal_length = 800.0  # Focal length of your camera (you need to calibrate this)

    # Initialize the camera
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera

    # Create a window and set the mouse callback function
    cv2.namedWindow("Distance Measurement")
    cv2.setMouseCallback("Distance Measurement", mouse_callback)

    measurements_taken = False  # Flag to track if measurements have been taken

    while True:
        # Capture a frame
        ret, frame = cap.read()

        # Example: Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Example: Apply GaussianBlur to reduce noise and improve accuracy
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Example: Use Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Example: Find contours in the edged image
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Example: Filter contours based on area (you may need to adjust this threshold)
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]

        if state["clicked_point"] is not None:
            # Example: Draw a circle at the clicked point
            cv2.circle(frame, state["clicked_point"], 5, (0, 0, 255), -1)

            # Example: Find the closest contour to the clicked point if there are valid contours
            if valid_contours:
                state["selected_contour"] = min(valid_contours, key=lambda cnt: cv2.pointPolygonTest(cnt, state["clicked_point"], True))

        if state["selected_contour"] is not None and not measurements_taken:
            # Example: Calculate the width of the object in pixels
            (x, y, w, h) = cv2.boundingRect(state["selected_contour"])
            pixel_width = w

            # Example: Calculate the distance
            distance_inches = calculate_distance(known_width_inches, focal_length, pixel_width)

            # Example: Convert distance to other units
            distance_cm = convert_inches_to_cm(distance_inches)
            distance_meters = convert_inches_to_meters(distance_inches)

            # Format the measurement information into a single line
            measurement_line = f"Distance: {distance_inches:.2f} inches, {distance_cm:.2f} cm, {distance_meters:.2f} meters"

            # Print the measurement information to the console
            print(measurement_line)

            # Set the flag to indicate that measurements have been taken
            measurements_taken = True
        elif state["selected_contour"] is None:
            # Reset the flag when no contour is selected
            measurements_taken = False

        # Display the frame
        cv2.imshow("Distance Measurement", frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
