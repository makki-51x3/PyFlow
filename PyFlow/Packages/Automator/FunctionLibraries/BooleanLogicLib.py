from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import IMPLEMENT_NODE
from PyFlow.Core.Common import *

class BooleanLogicLib(FunctionLibraryBase):
    def __init__(self, packageName):
        super(BooleanLogicLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('ListPin', []), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'BooleanLogicLib', NodeMeta.KEYWORDS: ['filter', 'condition']})
    def filterCollection(collection=('ListPin', []), condition=('FunctionPin', lambda x: True)):
        filtered_collection = [item for item in collection if condition(item)]
        return filtered_collection

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'BooleanLogicLib', NodeMeta.KEYWORDS: ['and']})
    def logicalAnd(bool1=('BoolPin', False), bool2=('BoolPin', False)):
        """Performs a logical AND operation on two boolean values."""
        return bool1 and bool2

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'BooleanLogicLib', NodeMeta.KEYWORDS: ['or']})
    def logicalOr(bool1=('BoolPin', False), bool2=('BoolPin', False)):
        """Performs a logical OR operation on two boolean values."""
        return bool1 or bool2

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'BooleanLogicLib', NodeMeta.KEYWORDS: ['not']})
    def logicalNot(bool1=('BoolPin', False)):
        """Performs a logical NOT operation on a boolean value."""
        return not bool1

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), nodeType=NodeTypes.Pure, meta={NodeMeta.CATEGORY: 'BooleanLogicLib', NodeMeta.KEYWORDS: ['xor']})
    def logicalXor(bool1=('BoolPin', False), bool2=('BoolPin', False)):
        """Performs a logical XOR operation on two boolean values."""
        return bool1 != bool2
