from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
import pyautogui
import numpy as np
import cv2
import logging

class FindImageOnScreenNode(NodeBase):
    def __init__(self, name):
        super(FindImageOnScreenNode, self).__init__(name)
        self.imagePath = self.createInputPin(
            'ImagePath', 
            'StringPin', 
            defaultValue="", 
            structure=StructureType.Single,
            constraint=None, 
            structConstraint=None, 
            supportedPinDataTypes=[], 
            group="", 
            foo=None
        )
        self.threshold = self.createInputPin(
            'Threshold', 
            'FloatPin', 
            defaultValue=0.8, 
            structure=StructureType.Single, 
            constraint=None, 
            structConstraint=None, 
            supportedPinDataTypes=[], 
            group="", 
            foo={"constraint": "Input", "VALUE_RANGE": (0, 1)}
        )
        self.scaleRange = self.createInputPin(
            'ScaleRange', 
            'StringPin', 
            defaultValue="", 
            structure=StructureType.Single,
            constraint=None, 
            structConstraint=None, 
            supportedPinDataTypes=[], 
            group=""
        )
        self.scaleStep = self.createInputPin(
            'ScaleStep', 
            'FloatPin', 
            defaultValue=0.1, 
            structure=StructureType.Single, 
            constraint=None, 
            structConstraint=None, 
            supportedPinDataTypes=[], 
            group="", 
            foo={"constraint": "Input", "VALUE_RANGE": (0, 1)}
        )
        self.region = self.createInputPin(
            'Region', 
            'StringPin', 
            defaultValue="", 
            structure=StructureType.Single,
            constraint=None, 
            structConstraint=None, 
            supportedPinDataTypes=[], 
            group=""
        )
        # self.execution = self.createInputPin('Execute', 'ExecPin')

        # Execution pin setup
        self.execution = self.createInputPin('Execute', 'ExecPin', structure=StructureType.Single)
        self.execution.enableOptions(PinOptions.AllowMultipleConnections)
        self.execution.onExecute.connect(self.compute) # Directly connect the execution pin to the compute method

        self.found = self.createOutputPin('Found', 'BoolPin')
        self.centerX = self.createOutputPin('CenterX', 'IntPin')
        self.centerY = self.createOutputPin('CenterY', 'IntPin')
        self.completed = self.createOutputPin('Completed', 'ExecPin')


    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('StringPin')
        helper.addInputDataType('FloatPin')
        helper.addInputDataType('ExecPin')
        helper.addOutputDataType('BoolPin')
        helper.addOutputDataType('IntPin')
        helper.addOutputDataType('ExecPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'ImageProcessing'

    @staticmethod
    def keywords():
        return ['find', 'image', 'screen', 'template matching']

    @staticmethod
    def description():
        return "Finds an image on the screen using template matching."

    def compute(self, *args, **kwargs):
        image_path = self.imagePath.getData()
        threshold = self.threshold.getData()
        scale_range = self.scaleRange.getData()
        scale_step = self.scaleStep.getData()
        region = self.region.getData()

        # Convert scale_range from string to tuple of floats
        try:
            scale_range = tuple(map(float, scale_range.split(',')))
        except ValueError:
            logging.error("Scale range format is incorrect. Expected format: 'min,max'.")
            self.found.setData(False)
            self.completed.call()
            return

        # Parse region if specified, otherwise default to using the whole screen
        region_tuple = None
        if region:
            try:
                region_tuple = tuple(map(int, region.split(',')))
                if len(region_tuple) != 4:
                    logging.error("Region format is incorrect. Expected format: 'x1,y1,x2,y2'.")
                    self.found.setData(False)
                    self.completed.call()
                    return
            except ValueError:
                logging.error("Region format is incorrect. Expected format: 'x1,y1,x2,y2'.")
                self.found.setData(False)
                self.completed.call()
                return
        else:
            region_tuple = (0, 0, pyautogui.size().width, pyautogui.size().height)

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
            resized_template = cv2.resize(edges_template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            if resized_template.shape[0] > edges_screenshot.shape[0] or resized_template.shape[1] > edges_screenshot.shape[1]:
                continue

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

            self.found.setData(True)
            self.centerX.setData(center_x)
            self.centerY.setData(center_y)
            logging.info(f"Found image at: ({center_x}, {center_y})")
        else:
            self.found.setData(False)
            logging.info("Image not found.")

        self.completed.call()
