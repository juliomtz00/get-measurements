'''
get-measurements.py

USAGE:
python3 get-measurements.py --cam_index 1 --Z 1.04 

    Obtains a real world measurement between two selected points chosen from the camera view, with a minimal error between them.
    The focal length must be known or aproximated in order to obtain a more accurate value.

Authors:
+ Julio Enrique Martinez Robledo- julio.martinezr@udem.edu

Institution: Universidad de Monterrey
Subject: Computational Vision
Lecturer: Dr. Andrés Hernández Gutiérrez

Date of creation: March 3rd 2023
Last update: March 7th 2023
'''

# Import needed libraries in the code.
import numpy as np
import cv2
import argparse

# Calculate the focal length of the camera, aproximated by on-site testing.
# Must be changed if camera is not the tested one.
focal_length = 970 # Value given in pixels

# Create a dictionary and list to save the coordinates of clicked points.
image_features = dict()
image_features["coordinates"] = list()


# Parse user's arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('--cam_index', type=int, default=1,help="Index value for the Camera")
parser.add_argument('--Z', type=float, default=1, help="Measured length in the z-axis")
#parser.add_argument('--cal_file', type=str, help="Name of the calibration file")
args = parser.parse_args()


def compute_line_segments():

    '''
    Compute the line between the two selected points in the camera window, 
    and displays it in color green for the user to see.

            Parameters:
                    Global Variables

            Returns:
                    None
    '''

    # Loop through the coordinate of each clicked pixel.
    for coordinate, icoord in zip(image_features["coordinates"], range(len(image_features["coordinates"]))):
        
        # When the coordinates chosen are more than one, compute the line between them.
        if icoord >=1:
            cv2.line(img=frame, pt1=temp_coordinate, pt2 = coordinate, color=(0,255,0), thickness=2)

        # Draw a circle on the clicked pixel.
        cv2.circle(img=frame, center = coordinate, radius=3, color=(0,255,0),thickness=1)
        temp_coordinate = coordinate

    # Visualize current frame.
    cv2.imshow("Current frame", frame)

def compute_perimeter():

    '''
    Compute the perimeter between the drawn lines, obtaining the distance 
    between the points.
    The function gets the distance between points in x-axis and y-axis and
    gets the exact distance in each plane, to then turn calculate the real
    distance by using the Pythagorean Theorem.
    Finally, calculate the total perimeter by adding the previously calcu-
    lated values.

            Parameters:
                    Global Variables

            Returns:
                    None
    '''
    total_length_list = []
    sorted_list = []
    calc_coordinates = [display_vision_analytic_metrics(image_features["coordinates"][i][0],image_features["coordinates"][i][1]) for i in range(len(image_features["coordinates"]))]
    total_perimeter = 0
    print("\nLINE SEGMENTS SELECTION ORDER")

    for i in range(len(calc_coordinates)-1):
        line_length_x = abs(calc_coordinates[i][0] - calc_coordinates[i+1][0])
        line_length_y = abs(calc_coordinates[i][1] - calc_coordinates[i+1][1])
        total_length = np.sqrt(line_length_x**2+line_length_y**2)
        total_length_list.append(total_length)
        sorted_list.append(total_length)
        print(f"- DISTANCE OF LINE SEGMENT (P({str(i)})P({str(i+1)})): {str(total_length)}")
        total_perimeter += total_length
    
    sorted_list.sort()
 
    print("\nLINE SEGMENTS ASCENDING ORDER")
    for i in range(len(sorted_list)):
        for j in range(len(total_length_list)):
            if total_length_list[j] == sorted_list[i]:
                print(f"- DISTANCE OF LINE SEGMENT (P({str(j)})P({str(j+1)})): {str(sorted_list[i])}")
                break

    print(f"\nTOTAL PERIMETER (P(0)P({str(len(calc_coordinates)-1)})): {str(total_perimeter)}\n")
    


def display_vision_analytic_metrics(x,y):

    '''
    Calculate the metrics of the chosen points using calculus and the focal
    length with the previous defined-in-class equations.
    All points are calculated with reference to the global plane.

            Parameters:
                    x (float): selected coordinate in pixels for the x-axis
                    y (float): selected coordinate in pixels for the y-axis
            Returns:
                    xg (float): analyzed metric coordinated in meters for 
                    the x-axis in reference to the global plane.
                    yg (float): analyzed metric coordinated in meters for 
                    the y-axis in reference to the global plane.
    '''

    xg = ((image_width/2 - x)/focal_length)*args.Z
    yg = ((y - image_height/2)/focal_length)*args.Z

    return xg,yg


#Get image coordinates

def get_pixel_coordinates(event,x,y,flags,params):
    '''
    Obtain the coordinated for the live video depending on the clicks
    generated by the user on real-time.

            Parameters:
                    event (str): event clicked by the user according to the
                    opencv library
                    x (float): selected coordinate in pixels for the x-axis
                    y (float): selected coordinate in pixels for the y-axis
                    flags (int): generated value for events
                    params : parameters
            Returns:
                    None
    '''

    global coordinates 
    print(f"Current selected pixel (x,y): {x,y}")

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Left button pressed. Pixel clicked (x,y): {x,y}")
        image_features['coordinates'].append((x,y))

    elif event == cv2.EVENT_LBUTTONDBLCLK:
        print("Left button was double clicked")
    
    elif event == cv2.EVENT_RBUTTONDOWN:
        print("Right button pressed")

    elif event == cv2.EVENT_MBUTTONDOWN:
        print("Middle button pressed")

    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            print("Scroll up activated")
        else:
            print("Scroll down activated")
    elif flags == cv2.EVENT_FLAG_CTRLKEY:
        print(flags)
        image_features['coordinates'] = list()
    
# Create a new window
cv2.namedWindow("Current frame", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Current frame",get_pixel_coordinates)

# Create a video capture object for video streaming
camera_index = args.cam_index
video_capture = cv2.VideoCapture(camera_index)

# Save previous list length or previous total clicked points
plen = 0

# Calculate the image measurements of the camera through the functions of the opencv library.
image_width = float(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
image_height = float(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("IMAGE MEASUREMENTS: height: "+str(image_height)+", width: "+str(image_width))

# If camera opens correctly
while(video_capture.isOpened()):
    #Get the current frame and pass it on to 'frame''
    #If the current frame cannot be captured, ret = 0
    ret,frame = video_capture.read()

    # If ret=0
    if not ret:
        print("Frame missed!")

    compute_line_segments()
    
    # Call function only if a new point is selected
    if len(image_features["coordinates"])!=plen:
        compute_perimeter()

    # Save new list length as previous one.
    plen = len(image_features["coordinates"])
    
    # Retrieve the pressed key
    key = cv2.waitKey(1)

    # If the pressed key was 's''
    #the current image is saved into disk
    if key == ord('s'):
        cv2.imwrite("current_frame.png", frame)
    
    # If the pressed key was  'd''
    # the program finishes
    elif key == ord("q"):
        break

#Close video capture object
video_capture.release()

#Close all windows
cv2.destroyAllWindows()
