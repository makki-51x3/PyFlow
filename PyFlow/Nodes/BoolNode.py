from AbstractGraph import *
from Settings import *
from Node import Node
from Qt.QtWidgets import QCheckBox
from Qt.QtWidgets import QSizePolicy
from Qt.QtWidgets import QGraphicsProxyWidget

DESC = """Generic type node.
Boolean type."""


class BoolNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(BoolNode, self).__init__(name, graph, spacings=Spacings)
        self.cb = QCheckBox()
        self.cb.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.cb.stateChanged.connect(lambda: self.on_set_cb_state(self.cb.isChecked()))
        self.output = self.add_output_port('out', DataTypes.Bool)

        def set_data_overloads(data, dirty_propagate=True):
            if type(data) != bool().__class__:
                data = data.lower() in ["true", "1"]
            if data:
                self.cb.setCheckState(QtCore.Qt.Checked)
            else:
                self.cb.setCheckState(QtCore.Qt.Unchecked)
        self.output.set_data_overload = set_data_overloads

        prx_cb = QGraphicsProxyWidget()
        prx_cb.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        prx_cb.setWidget(self.cb)
        self.output.get_container().layout().insertItem(0, prx_cb)

    @staticmethod
    def description():
        return DESC

    @staticmethod
    def get_category():
        return 'GenericTypes'

    def on_set_cb_state(self, state):
        self.output.set_data(state, True)

    def compute(self):
        self.output.set_data(self.cb.isChecked(), False)