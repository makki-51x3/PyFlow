

from PyFlow.Core.Common import *
import pyautogui
import time
import logging 

def prepareNode(node):
    node.createInputPin(pinName="inExec", dataType="ExecPin", foo=node.processNode)
    node.createOutputPin(pinName="outExec", dataType="ExecPin")
    node.createInputPin(pinName="textToPaste", dataType="StringPin", defaultValue="default text to paste!", foo=None, structure=StructureType.Single, constraint=None, structConstraint=None, supportedPinDataTypes=[], group="")

def compute(node):
    textToPaste = node.getData("textToPaste")
    time.sleep(2)
    pyautogui.typewrite(textToPaste)
    logging.info(f"Pasted text: {textToPaste}")  # Use logging to log the pasted text
    node["outExec"].call()
