from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import IMPLEMENT_NODE
from PyFlow.Core.Common import *

class StringUtilitiesLib(FunctionLibraryBase):
    def __init__(self, packageName):
        super(StringUtilitiesLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'StringUtilitiesLib', NodeMeta.KEYWORDS: ['combine', 'concatenate']})
    def combineStrings(str1=('StringPin', ''), str2=('StringPin', ''), separator=('StringPin', '')):
        """Combines two strings with an optional separator."""
        return f"{str1}{separator}{str2}"

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'StringUtilitiesLib', NodeMeta.KEYWORDS: ['lowercase']})
    def toLowerCase(inputString=('StringPin', '')):
        """Converts a string to lowercase."""
        return inputString.lower()

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'StringUtilitiesLib', NodeMeta.KEYWORDS: ['uppercase']})
    def toUpperCase(inputString=('StringPin', '')):
        """Converts a string to uppercase."""
        return inputString.upper()

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'StringUtilitiesLib', NodeMeta.KEYWORDS: ['trim']})
    def trimString(inputString=('StringPin', '')):
        """Trims whitespace from both ends of a string."""
        return inputString.strip()

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'StringUtilitiesLib', NodeMeta.KEYWORDS: ['slice']})
    def sliceString(inputString=('StringPin', ''), start=('IntPin', 0), end=('IntPin', -1)):
        """Slices a string using start and end indices."""
        return inputString[start:end]

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'StringUtilitiesLib', NodeMeta.KEYWORDS: ['contains']})
    def stringContains(mainString=('StringPin', ''), substring=('StringPin', '')):
        """Checks if a string contains a given substring."""
        return substring in mainString

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'StringUtilitiesLib', NodeMeta.KEYWORDS: ['length']})
    def stringLength(inputString=('StringPin', '')):
        """Returns the length of a string."""
        return len(inputString)

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'StringUtilitiesLib', NodeMeta.KEYWORDS: ['replace']})
    def replaceString(inputString=('StringPin', ''), old=('StringPin', ''), new=('StringPin', ''), count=('IntPin', -1)):
        """Replaces occurrences of a substring with a new string."""
        return inputString.replace(old, new, count)

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'StringUtilitiesLib', NodeMeta.KEYWORDS: ['reverse']})
    def reverseString(inputString=('StringPin', '')):
        """Reverses a string."""
        return inputString[::-1]