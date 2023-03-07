
    
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import pyqtSlot


class FormLayoutDialogController(QtWidgets.QDialog):
    scalar_type = ["str", "int", "float", "bool", "time", "date"]

    def __init__(self, obj, template_file_name):
        super(FormLayoutDialogController, self).__init__()
        uic.loadUi(template_file_name, self)
        self.resize(self.sizeHint().width(), self.size().height() );
        self.connect_predefined_slots()
        self.obj = obj
    
    
    def connect_predefined_slots(self):     
        for w in self.children():
            is_list_button = w.property("for_list")
            if is_list_button != None:
                if w.objectName().startswith("add"):
                    w.clicked.connect(self.listAddButtonClicked)
                else:
                    w.clicked.connect(self.listDeleteButtonClicked)
                continue
            
            is_detail_button = w.property("for_object")
            if is_detail_button != None:
                w.clicked.connect(self.objectDetailButtonClicked)
                continue
            
            is_table_button = w.property("for_table")
            if is_table_button != None:
                if w.objectName().startswith("tableAdd"):
                    w.clicked.connect(self.tableAddButtonClicked)
                else:
                    w.clicked.connect(self.tableDeleteButtonClicked)
                continue


    @pyqtSlot()
    def reject(self):
        super().reject()

    @pyqtSlot()
    def accept(self):
        for w in self.children():
            field_name = w.property("field_name")
            
            if field_name != None:
                key = w.property("key")
                field = w.property("prop_name")
                if(key in FormLayoutDialogController.scalar_type):
                    if key == "bool":
                        setattr(self.obj, field_name, str(w.property(field)).capitalize())
                    else:
                        setattr(self.obj, field_name, w.property(field))
                elif(field == "list"):
                    lst = []
                    for i in range(len(w)):
                        lst.append(w.item(i).text())
                    setattr(self.obj, field_name, lst)
                elif(field == "dict"):
                    dc = {}
                    for r in range(w.rowCount()):
                        dc[w.item(r, 0).text()] = w.item(r, 1).text()
                    setattr(self.obj, field_name, dc)
                elif(field == "datetime"):
                     setattr(self.obj, field_name, w.dateTime())
        super().accept()
        
    @pyqtSlot()
    def listAddButtonClicked(self):
        list_name = self.sender().property("for_list")
        list_widget = self.get_widget(list_name)
        lineEdit_widget = self.get_widget("lineEdit_"+list_name)
        if list_widget != None and lineEdit_widget != None:
            list_widget.addItem(lineEdit_widget.text())
            lineEdit_widget.clear()
        

    @pyqtSlot()
    def listDeleteButtonClicked(self):
        list_name = self.sender().property("for_list")
        list_widget = self.get_widget(list_name)
        if list_widget != None and list_widget.currentItem() != None:
            list_widget.takeItem(list_widget.row(list_widget.currentItem()))
        

    @pyqtSlot()
    def objectDetailButtonClicked(self):
        object_name = self.sender().property("for_object")
        from .VPyGUIGenerator import VPyGUIGenerator
        dialog = VPyGUIGenerator.create_gui(getattr(self.obj, object_name))
        dialog.exec()
        label_widget = self.get_widget(object_name)
        label_widget.setText(str(getattr(self.obj, object_name)))


    def get_widget(self, name):
        for w in self.children():
            if(w.objectName() == name):
                return w        
        return None
    
    @pyqtSlot()
    def tableAddButtonClicked(self):
        table_name = self.sender().property("for_table")
        table_widget = self.get_widget(table_name)
        key_widget = self.get_widget("key_"+table_name)
        value_widget = self.get_widget("value_"+table_name)

        row = table_widget.rowCount()
        table_widget.insertRow(row)
        table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(key_widget.text()))
        table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(value_widget.text()))
        key_widget.clear()
        value_widget.clear()
    
    
        

    
    @pyqtSlot()
    def tableDeleteButtonClicked(self):
        table_name = self.sender().property("for_table")
        table_widget = self.get_widget(table_name)
        table_widget.removeRow(table_widget.currentRow())
    

