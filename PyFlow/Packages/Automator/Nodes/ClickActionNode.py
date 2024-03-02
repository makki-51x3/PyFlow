from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
import pyautogui
import random
import logging
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper


class ClickActionNode(NodeBase):
    def __init__(self, name):
        super(ClickActionNode, self).__init__(name)

        # Input pins
        self.createInputPin('x_offset', 'IntPin', defaultValue=0)
        self.createInputPin('y_offset', 'IntPin', defaultValue=0)
        self.createInputPin('exact_x', 'IntPin', defaultValue=-1)  # -1 indicates not used
        self.createInputPin('exact_y', 'IntPin', defaultValue=-1)  # -1 indicates not used
        self.createInputPin('use_cursor_position', 'BoolPin', defaultValue=False)
        self.createInputPin('click_area', 'StringPin', defaultValue="")  # Updated to use a string tuple
        self.createInputPin('click_type', 'StringPin', defaultValue="left_click")

        # Execution pins
        self.execution = self.createInputPin('Execute', 'ExecPin')
        self.completed = self.createOutputPin('Completed', 'ExecPin')

        # Connect the execution pin to the compute method
        self.execution.onExecute.connect(self.compute)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('IntPin')
        helper.addInputDataType('BoolPin')
        helper.addInputDataType('StringPin')
        helper.addInputDataType('ExecPin')
        helper.addOutputDataType('ExecPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'UserActions'

    @staticmethod
    def keywords():
        return ['click', 'mouse', 'action']

    @staticmethod
    def description():
        return "Performs a mouse click action based on specified parameters."
    
    def compute(self, *args, **kwargs):
        x_offset = self.getPinByName('x_offset').getData()
        y_offset = self.getPinByName('y_offset').getData()
        exact_x = self.getPinByName('exact_x').getData()
        exact_y = self.getPinByName('exact_y').getData()
        use_cursor_position = self.getPinByName('use_cursor_position').getData()
        click_area = self.getPinByName('click_area').getData()
        click_type = self.getPinByName('click_type').getData()

        location = None

        # Adjust and apply click_area logic if specified
        if click_area:
            try:
                click_area_x1, click_area_y1, click_area_x2, click_area_y2 = map(int, click_area.split(','))
                area_width = abs(click_area_x2 - click_area_x1)
                area_height = abs(click_area_y2 - click_area_y1)
                location = (random.randint(min(click_area_x1, click_area_x2) + x_offset, min(click_area_x1, click_area_x2) + area_width + x_offset),
                            random.randint(min(click_area_y1, click_area_y2) + y_offset, min(click_area_y1, click_area_y2) + area_height + y_offset))
            except ValueError:
                logging.error("Invalid click area coordinates")

        # Determine the exact click location
        if exact_x >= 0 and exact_y >=0:
            location = (exact_x, exact_y)
        elif use_cursor_position:
            location = pyautogui.position()

        # Execute the click action
        if location:  
            if not click_area: 
                location = (location[0] + x_offset, location[1] + y_offset)
                
            x, y = location
            if 0 <= x <= pyautogui.size().width and 0 <= y <= pyautogui.size().height:
                try:
                    pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.5))
                    if click_type == 'left_click':
                        pyautogui.click(button='left')
                    elif click_type == 'right_click':
                        pyautogui.click(button='right')
                    elif click_type == 'double_left_click':
                        pyautogui.doubleClick(button='left')
                    elif click_type == 'double_right_click':
                        pyautogui.doubleClick(button='right')
                    # Additional click types can be handled here
                except Exception as e:
                    logging.error(f"Error executing click action: {e}")
            else:
                logging.error("Click location is out of screen bounds.")
        else:
            logging.error("No valid location found for click action.")

        self.completed.call()
