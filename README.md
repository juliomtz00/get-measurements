# get-measurements
Map selected pixels from a 2D image captured by a monocular camera to 3D world points in a vision sensor coordinate frame.

Create a program that maps selected pixels from a 2D image captured by a monocular camera to 3D world points in a vision sensor coordinate frame. You will then use these 3D world points to perform 3D measurements on flat surface objects.

Materials required include a personal computer, a mouse or trackpad, a monocular camera (such as a laptop webcam), internet connectivity for Python library installation, Python ≥ 3.10, and recommended libraries like OpenCV, NumPy, and ArgParse.

The problem involves manually selecting pixels from an acquired image and calculating various measurements, including distances between consecutive points (P0P1, P1P2, P2P3, P3P4) and the perimeter (P0P1 + P1P2 + P2P3 + P3P4) of the selected points.

The methodology uses trigonometric equations to convert pixel coordinates into real-world measurements. The OpenCV library is employed to capture and process real-time video, and built-in functions allow users to select points on the video stream. Pythagorean theorem is used to calculate distances.

Points are saved in a list, and the program computes the measurements and displays them in the terminal. Users can delete points by holding the control key and end the program by pressing "Q." A screenshot can be saved with the "S" key.

The program requires knowledge of the distance between two planes (z-axis) and the camera's parallel alignment with the reference plane for accurate measurements.

Overall, the program enables 3D measurements of flat objects using a monocular camera, though the focal length of the camera must be determined experimentally, and correct alignment between planes is crucial for accuracy.
