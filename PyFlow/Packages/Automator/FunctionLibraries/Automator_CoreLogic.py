from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import IMPLEMENT_NODE
from PyFlow.Core.Common import *
import numpy as np
import cv2
import pyautogui
import inspect

class Automator_CoreLogic(FunctionLibraryBase):
    def __init__(self, packageName):
        super(Automator_CoreLogic, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False, {"constraint": "Output", "structConstraint": "Output"}),
                    meta={NodeMeta.CATEGORY: 'ImageProcessingLib', NodeMeta.KEYWORDS: ['image', 'search']})
    def findImageOnScreen(image_path=('StringPin', ""), threshold=('FloatPin', 0.8), scale_range=('StringPin', "0.5,2.0"), scale_step=('FloatPin', 0.1), region=('StringPin', "")):
        """
        Finds an image on the screen using template matching.
        
        Parameters:
        - image_path: Path to the image file.
        - threshold: Matching threshold.
        - scale_range: Scale range to search for the image, provided as a string "min,max".
        - scale_step: Step size for scaling.
        - region: Optional region (x1, y1, x2, y2) within the screen to search for the image, provided as a string "x1,y1,x2,y2". If not specified, the whole screen is used.
        
        Returns:
        - Success: Bool indicating if the image was found.
        - CenterX: X coordinate of the center of the found image.
        - CenterY: Y coordinate of the center of the found image.
        """
        # Convert scale_range from string to tuple of floats
        try:
            scale_range = tuple(map(float, scale_range.split(',')))
        except ValueError:
            print("Scale range format is incorrect. Expected format: 'min,max'.")
            return False, 0, 0  # Default failure output

        # Parse region if specified, otherwise default to using the whole screen
        region_tuple = None
        if region:
            try:
                region_tuple = tuple(map(int, region.split(',')))
                if len(region_tuple) != 4:
                    print("Region format is incorrect. Expected format: 'x1,y1,x2,y2'.")
                    return False, 0, 0
            except ValueError:
                print("Region format is incorrect. Expected format: 'x1,y1,x2,y2'.")
                return False, 0, 0
        else:
            region_tuple = (0, 0, pyautogui.size().width, pyautogui.size().height)

        print(f"image_path: {image_path}  region: {region}")

        # Use the specified region or the whole screen for the screenshot
        if region_tuple:
            x1, y1, x2, y2 = region_tuple
            screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
        else:
            screenshot = pyautogui.screenshot()

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
                continue

            # Perform template matching
            result = cv2.matchTemplate(edges_screenshot, resized_template, cv2.TM_CCORR_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > best_val:
                best_val = max_val
                best_loc = max_loc
                best_scale = scale

        if best_val >= threshold:
            h, w = resized_template.shape[:2]
            center_x = best_loc[0] + w // 2
            center_y = best_loc[1] + h // 2

            print("found ", image_path, " image on: ", (center_x, center_y))
            return True, center_x, center_y
        
        print("didn't find ", image_path, " image!")
        return False, 0, 0  # Default failure output
