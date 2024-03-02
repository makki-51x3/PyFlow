from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
import pyautogui
import logging 

class PasteTextNode(NodeBase):
    def __init__(self, name):
        super(PasteTextNode, self).__init__(name)
        self.textToPaste = self.createInputPin('TextToPaste', 'StringPin')
        self.execution = self.createInputPin('Execute', 'ExecPin')
        self.completed = self.createOutputPin('Completed', 'ExecPin')

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
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
        return ['paste', 'text']

    @staticmethod
    def description():
        return "Pastes the specified text to the current cursor location."

    def compute(self, *args, **kwargs):
        text = self.textToPaste.getData()
        pyautogui.typewrite(text)
        logging.info(f"Pasted text: {text}")  # Use logging to log the pasted text
