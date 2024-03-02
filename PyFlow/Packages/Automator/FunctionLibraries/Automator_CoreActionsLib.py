from PyFlow.Core.Common import *
from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import IMPLEMENT_NODE
import pyautogui
import random
import cv2
from dotenv import load_dotenv
import numpy as np
import os
from pathlib import Path


# Load environment variables from .env file
load_dotenv()
image_temp_path = os.environ.get('IMG_TEMP_PATH')

# Assuming PyFlow can handle a list of tuples for dropdown generation
clickTypes = [
    ("LEFT_CLICK", "left_click"),
    ("RIGHT_CLICK", "right_click"),
    ("DOUBLE_LEFT_CLICK", "double_left_click"),
    ("DOUBLE_RIGHT_CLICK", "double_right_click"),
    ("NO_CLICK", "no_click")
]

def check_coordinates_within_bounds(x: int, y: int):
    # Get the screen size
    screen_width, screen_height = pyautogui.size()
    
    # Check the coordinates if they're outside the screen bounds
    if x < 0 or  x > screen_width or y < 0 or y > screen_height:
        return False
    return True

def find_image_on_screen(image_path, threshold=0.8, scale_range=(0.5, 2.0), scale_step=0.1, region=None ):
    automator_temp_path = Path(image_temp_path)
    full_image_path = automator_temp_path / image_path

    print(f"full_image_path: {full_image_path}  region: {region}")

    image_path = f"{image_temp_path}/{image_path}"
    
    screenshot = pyautogui.screenshot()

    # Crop the screenshot if region is specified
    if region:
        x1, y1, x2, y2 = region
        screenshot = screenshot.crop((x1, y1, x2, y2))

    screenshot_np = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Canny edge detector to both images
    edges_screenshot = cv2.Canny(screenshot_gray, 100, 200)
    edges_template = cv2.Canny(template, 100, 200)

    best_scale = None
    best_val = -np.inf
    best_loc = None

    # Loop over scales
    for scale in np.arange(scale_range[0], scale_range[1], scale_step):
        # Resize the template at the current scale
        resized_template = cv2.resize(edges_template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        if resized_template.shape[0] > edges_screenshot.shape[0] or resized_template.shape[1] > edges_screenshot.shape[1]:
            # Template is larger than the screenshot, skip
            continue

        # Perform template matching
        result = cv2.matchTemplate(edges_screenshot, resized_template, cv2.TM_CCORR_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > best_val:
            best_val = max_val
            best_loc = max_loc
            best_scale = scale

    if best_val >= threshold:
        # Compute the center of the template
        h, w = (int(edges_template.shape[0] * best_scale), int(edges_template.shape[1] * best_scale))
        center_x = int(best_loc[0] + w / 2)
        center_y = int(best_loc[1] + h / 2)

        # Adjust the coordinates if a region was specified
        if region:
            center_x += x1
            center_y += y1

        print("found ", image_path, " image on: ", (center_x, center_y))
        return (center_x, center_y)
    
    print("didn't find ", image_path, " image!")
    return None

class Automator_CoreActionsLib(FunctionLibraryBase):
    def __init__(self, packageName):
        super(Automator_CoreActionsLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'CoreActions', NodeMeta.KEYWORDS: ['click']})
    def clickAction(imagePath=('StringPin', None),
                    exactX=('IntPin', None), exactY=('IntPin', None),
                    offsetX=('IntPin', 0), offsetY=('IntPin', 0),
                    clickType=('StringPin', "LEFT_CLICK", {"ValueList": clickTypes}),
                    useCursorPosition=('BoolPin', False),
                    regionX1=('IntPin', None), regionY1=('IntPin', None),
                    regionX2=('IntPin', None), regionY2=('IntPin', None),
                    clickAreaX1=('IntPin', None), clickAreaY1=('IntPin', None),
                    clickAreaX2=('IntPin', None), clickAreaY2=('IntPin', None)):
        """
        Performs a click action based on specified parameters.
        """
        # Initialize location
        location = None

        # Determine the exact click location
        if exactX is not None and exactY is not None:
            location = (exactX, exactY)

        # Use current cursor position
        elif useCursorPosition:
            location = pyautogui.position()

        # Default to finding location by image if specified
        elif imagePath:
            location = find_image_on_screen(imagePath, region=(regionX1, regionY1, regionX2, regionY2))

        # Apply offsets to the determined location
        if location:
            location = (location[0] + offsetX, location[1] + offsetY)

        # Adjust and apply click_area logic after offsets
        if all(v is not None for v in [clickAreaX1, clickAreaY1, clickAreaX2, clickAreaY2]):
            if location:
                # Adjust click area by calculated location before selecting a random location
                x1, y1 = location
                area_width = max(clickAreaX1, clickAreaX2) - min(clickAreaX1, clickAreaX2)
                area_height = max(clickAreaY1, clickAreaY2) - min(clickAreaY1, clickAreaY2)
                x2 = area_width + x1
                y2 = area_height + y1
                location = (random.randint(x1, x2), random.randint(y1, y2))

        # Execute the click action at the determined location
        if location:
            x, y = location
            # Check that the coordinates are within screen bounds
            if check_coordinates_within_bounds(x, y):
                try:
                    # Move the cursor and perform click based on clickType
                    pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.5), tween=pyautogui.easeInOutQuad)
                    if clickType == 'left_click':
                        pyautogui.leftClick()
                    elif clickType == 'right_click':
                        pyautogui.rightClick()
                    # Add other click types as needed
                except Exception as e:
                    print(f"Error executing click action: {e}")
            else:
                print("Click location is out of the screen bounds!")
        else:
            print("No valid location found for click action")
