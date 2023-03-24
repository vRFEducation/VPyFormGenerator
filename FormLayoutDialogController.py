
    
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import pyqtSlot


class FormLayoutDialogController(QtWidgets.QDialog):
    scalar_type = ["str", "int", "float", "bool", "time", "date", "slider", "dial"]

    def __init__(self, obj, template_file_name):
        super(FormLayoutDialogController, self).__init__()
        uic.loadUi(template_file_name, self)
        self.resize(self.sizeHint().width(), self.size().height() );
        self.connect_predefined_slots()
        self.obj = obj
        self.__objectListDict = {}
        self.finalize_ui();
        
    
    
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
            
            is_filter_list = w.property("for_list_filter")
            if is_filter_list != None:
                if w.objectName().startswith("listFilter"):
                    w.textChanged.connect(self.listFilterChanged)
                continue
            
            is_filter_table = w.property("for_table_filter")
            if is_filter_table != None:
                if w.objectName().startswith("tableFilter"):
                    w.textChanged.connect(self.tableFilterChanged)
                continue
            
            is_grid_paginator = w.property("for_grid")
            if is_grid_paginator != None:
                if w.objectName().startswith("btnFirstPage"):
                    w.clicked.connect(self.simpleGridFirstPageButtonClicked)
                elif w.objectName().startswith("btnPrevPage"):
                    w.clicked.connect(self.simpleGridPreviousPageButtonClicked)
                elif w.objectName().startswith("btnNextPage"):
                    w.clicked.connect(self.simpleGridNextPageButtonClicked)
                elif w.objectName().startswith("btnLastPage"):
                    w.clicked.connect(self.simpleGridLastPageButtonClicked)
                elif w.objectName().startswith("cmbPageCount"):
                    w.currentIndexChanged.connect(self.simpleGridPageCountComboChanged)
                continue

    def finalize_ui(self):
        for w in self.children():
            prop_name = w.property('prop_name')
            if prop_name == 'simplegrid':
                w.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
                field = w.property("field_name")
                self.__objectListDict[field] = getattr(self.obj, field)
                

    
    @pyqtSlot()
    def reject(self):
        super().reject()

    @pyqtSlot()
    def accept(self):
        for w in self.children():
            field_name = w.property("field_name")
            if field_name == "sample":
                q = 10
            if field_name != None:
                key = w.property("key")
                field = w.property("prop_name")
                if key == "progressbar":
                    continue
                if key == "multichoice":
                  selected_items = self.get_selected_items(w)
                  setattr(self.obj, field_name, selected_items)
                elif(key in FormLayoutDialogController.scalar_type):
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
                elif(key == "combo"):
                    setattr(self.obj, field_name, w.property("currentText"))
                elif key == 'simplegrid':
                    grid_name = w.property("field_name")
                    self.presave_grid_data(grid_name)
                    setattr(self.obj, field_name, self.__objectListDict[field_name])

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
    
    def get_selected_items(self, items):
        widgets = items.findChildren(QtWidgets.QCheckBox)
        if len(widgets) == 0:
            widgets = items.findChildren(QtWidgets.QRadioButton)        
            for ch in widgets:
                if ch.isChecked():
                    return ch.text()
        result = []
        for ch in widgets:
            if ch.isChecked():
                result.append(ch.text())
        return result

    @pyqtSlot()
    def listFilterChanged(self):
        list_name = self.sender().property("for_list_filter")
        list_widget = self.get_widget(list_name)
        text = self.sender().property("text").lower()
        for i in range(list_widget.count()):
            list_widget.item(i).setHidden(text not in list_widget.item(i).text().lower())
        
    @pyqtSlot()
    def tableFilterChanged(self):
        table_name = self.sender().property("for_table_filter")
        table = self.get_widget(table_name)
        filter = self.sender().property("text").lower()
        for i in range(table.rowCount()):
            text = table.item(i, 0).text().lower()
            table.setRowHidden(i, filter not in text)

    @pyqtSlot()
    def simpleGridFirstPageButtonClicked(self):
        self.change_grid_page(self.sender, "first")
    
    @pyqtSlot()
    def simpleGridPreviousPageButtonClicked(self):
        self.change_grid_page(self.sender, "previous")

    
    @pyqtSlot()
    def simpleGridNextPageButtonClicked(self):
        self.change_grid_page(self.sender, "next")
    
    @pyqtSlot()
    def simpleGridLastPageButtonClicked(self):
        self.change_grid_page(self.sender, "last")

    @pyqtSlot()
    def simpleGridPageCountComboChanged(self):
        self.change_grid_page(self.sender, "row_per_page")
        
        
    def change_grid_page(self, sender, action):
        grid_name = sender().property("for_grid")
        grid = self.get_widget(grid_name)
        spn_page = self.get_widget(f"spnPageNumber_{grid_name}")
        self.enable_widgets((f"btnFirstPage_{grid_name}", f"btnPrevPage_{grid_name}", f"btnLastPage_{grid_name}",f"btnNextPage_{grid_name}"))
        fieldname = grid.property("field_name")
        datasource = self.__objectListDict[fieldname]

        
        self.presave_grid_data(grid_name)
        
        current_page = int(grid.property("current_page"))
        page_count = int(grid.property("page_count"))
        row_per_page = int(grid.property("row_per_page"))
        
                
        grid.clearContents()

        if action == "first":
            current_page = 1
            self.disable_widgets((f"btnFirstPage_{grid_name}", f"btnPrevPage_{grid_name}"))
        elif action == "previous":
            current_page -= 1
            if current_page == 1:
                self.disable_widgets((f"btnFirstPage_{grid_name}", f"btnPrevPage_{grid_name}"))
        elif action == "next":
            current_page += 1
            if current_page == page_count:
                self.disable_widgets((f"btnLastPage_{grid_name}", f"btnNextPage_{grid_name}"))
        elif action == "last":
            current_page = page_count
            self.disable_widgets((f"btnLastPage_{grid_name}",f"btnNextPage_{grid_name}"))
        elif action == "row_per_page":
            current_page = 1
            row_per_page = int(sender().currentText())
            import math
            page_count = math.ceil(len(datasource) / row_per_page)
            spn_page.setMaximum(page_count)
            spn_page.setSuffix(f"/{page_count}")
            if page_count > 1:
                self.disable_widgets((f"btnFirstPage_{grid_name}", f"btnPrevPage_{grid_name}"))
            else:
                self.disable_widgets((f"btnFirstPage_{grid_name}", f"btnPrevPage_{grid_name}", f"btnLastPage_{grid_name}",f"btnNextPage_{grid_name}"))
        
        start = (current_page - 1) * row_per_page
        end = current_page * row_per_page 
        end = end if end < len(datasource) else len(datasource)
        grid.setRowCount(end - start)
        for r in range(start, end):
            obj = datasource[r]
            for c in range(grid.columnCount()):
                label = grid.horizontalHeaderItem(c).text()
                field =  ''.join([label[:1].lower(), label[1:]])
                value = getattr(obj, field)
                item = QtWidgets.QTableWidgetItem(str(value))
                if type(value).__name__ not in FormLayoutDialogController.scalar_type:
                    item.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
                grid.setItem(r - start, c, item)
                
        
        spn_page.setValue(int(current_page))
        grid.setProperty("current_page", current_page)
        grid.setProperty("page_count", page_count )
        grid.setProperty("row_per_page", row_per_page)
        
    def presave_grid_data(self, grid_name):
        grid = self.get_widget(grid_name)
        fieldname = grid.property("field_name")
        datasource = self.__objectListDict[fieldname]

        is_paginated = bool(grid.property("is_paginated"))
        current_page = int(grid.property("current_page"))
        row_per_page = int(grid.property("row_per_page")) if is_paginated else len(datasource)
            
        start = (current_page - 1) * row_per_page
        end = current_page * row_per_page 
        end = end if end < len(datasource) else len(datasource)
        for r in range(start, end):
            obj = datasource[r]
            for c in range(grid.columnCount()):
                label = grid.horizontalHeaderItem(c).text()
                field =  ''.join([label[:1].lower(), label[1:]])
                field_type = type(getattr(obj, field)).__name__
                if field_type not in FormLayoutDialogController.scalar_type:
                    continue
                value = grid.item(r - start, c).text()
                setattr(obj, field, str(value))
        
    def disable_widgets(self, names):
        for name in names:
            w = self.get_widget(name)
            w.setEnabled(False)
    
    def enable_widgets(self, names):
        for name in names:
            w = self.get_widget(name)
            w.setEnabled(True)
    
            