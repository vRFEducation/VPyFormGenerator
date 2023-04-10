
    
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtCore import pyqtSlot
from pathlib import Path



class FormLayoutDialogController(QtWidgets.QDialog):
    scalar_type = ["str", "int", "float", "bool", "time", "date", "slider", "dial", "lineedit"]
    script_location = Path(__file__).absolute().parent

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
                    w.setIcon(QtGui.QIcon(f"{FormLayoutDialogController.script_location}/icons/save.png"))
                elif w.objectName().startswith("del"):
                    w.clicked.connect(self.listDeleteButtonClicked)
                    w.setIcon(QtGui.QIcon(f"{FormLayoutDialogController.script_location}/icons/del.png"))
                    clear_all_acion = QtWidgets.QWidgetAction(w)
                    clear_all_acion.setText("Clear All")
                    clear_all_acion.setProperty("for_list", is_list_button)
                    clear_all_acion.triggered.connect(self.clear_all_action_triggered)
                    menu = QtWidgets.QMenu()
                    menu.addAction(clear_all_acion)
                    w.setMenu(menu)
                elif w.objectName().startswith("lineEdit"):
                    w.editingFinished.connect(self.listAddButtonClicked)
                continue
            
            is_detail_button = w.property("for_object")
            if is_detail_button != None:
                w.clicked.connect(self.objectDetailButtonClicked)
                w.setIcon(QtGui.QIcon(f"{FormLayoutDialogController.script_location}/icons/detail.png"))
                continue
            
            is_table_button = w.property("for_table")
            if is_table_button != None:
                if w.objectName().startswith("tableAdd"):
                    w.clicked.connect(self.tableAddButtonClicked)
                    w.setIcon(QtGui.QIcon(f"{FormLayoutDialogController.script_location}/icons/save.png"))
                else:
                    w.clicked.connect(self.tableDeleteButtonClicked)
                    w.setIcon(QtGui.QIcon(f"{FormLayoutDialogController.script_location}/icons/del.png"))
                    clear_all_acion = QtWidgets.QWidgetAction(w)
                    clear_all_acion.setText("Clear All")
                    clear_all_acion.setProperty("for_table", is_table_button)
                    clear_all_acion.triggered.connect(self.clear_all_table_action_triggered)
                    menu = QtWidgets.QMenu()
                    menu.addAction(clear_all_acion)
                    w.setMenu(menu)

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
                elif w.objectName().startswith("btnAddNew"):
                    w.clicked.connect(self.simpleGridAddNewButtonClicked)
                    w.setIcon(QtGui.QIcon(f"{FormLayoutDialogController.script_location}/icons/add.png"))


    def finalize_ui(self):
        for w in self.children():
            prop_name = w.property('prop_name')
            if prop_name == 'simplegrid':
                w.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
                page_count = int(w.property("page_count"))
                grid_name = w.property("field_name")

                if page_count > 1:
                    self.disable_widgets((f"btnFirstPage_{grid_name}", f"btnPrevPage_{grid_name}"))
                else:
                    self.disable_widgets((f"btnFirstPage_{grid_name}", f"btnPrevPage_{grid_name}", f"btnLastPage_{grid_name}",f"btnNextPage_{grid_name}"))
        

                field = w.property("field_name")
                self.__objectListDict[field] = getattr(self.obj, field)
                self.add_grid_action(field)
                tmp_filtering = w.property("showFiltering")
                if tmp_filtering!= None and tmp_filtering.lower() == "true":
                    self.add_grid_filter(field)

    
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
        self.add_item_to_list(list_name)
    
    def add_item_to_list(self, list_name):
        list_widget = self.get_widget(list_name)
        lineEdit_widget = self.get_widget("lineEdit_"+list_name)
        if list_widget != None and lineEdit_widget != None:
            text = lineEdit_widget.text().strip()
            if text != "":
                list_widget.addItem(text)                
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

        if action != "refresh":
            self.presave_grid_data(grid_name)
        
        current_page = int(grid.property("current_page"))
        page_count = int(grid.property("page_count"))
        row_per_page = int(grid.property("row_per_page"))
        
                

        if action == "first":
            current_page = 1
        elif action == "previous":
            current_page -= 1
        elif action == "next":
            current_page += 1
        elif action == "last":
            current_page = page_count
        elif action in ("row_per_page", "refresh"):
            current_page = 1 if action != "refresh" else current_page
            row_per_page = int(sender().currentText()) if action != "refresh" else row_per_page
            import math
            page_count = math.ceil(len(datasource) / row_per_page)
            if current_page > page_count:
                current_page = page_count
            spn_page.setMaximum(page_count)
            spn_page.setSuffix(f"/{page_count}")
            if page_count > 1:
                self.disable_widgets((f"btnFirstPage_{grid_name}", f"btnPrevPage_{grid_name}"))
            else:
                self.disable_widgets((f"btnFirstPage_{grid_name}", f"btnPrevPage_{grid_name}", f"btnLastPage_{grid_name}",f"btnNextPage_{grid_name}"))
        
        if current_page == 1:
                self.disable_widgets((f"btnFirstPage_{grid_name}", f"btnPrevPage_{grid_name}"))
        if current_page == page_count:
                self.disable_widgets((f"btnLastPage_{grid_name}", f"btnNextPage_{grid_name}"))
        
        spn_page.setValue(int(current_page))
        grid.setProperty("current_page", current_page)
        grid.setProperty("page_count", page_count )
        grid.setProperty("row_per_page", row_per_page)
        
        self.load_simple_grid_data(grid_name)
        
    
    def load_simple_grid_data(self, grid_name):
        grid = self.get_widget(grid_name)
        current_page = int(grid.property("current_page"))
        row_per_page = int(grid.property("row_per_page"))
        fieldname = grid.property("field_name")
        datasource = self.__objectListDict[fieldname]

        grid.clearContents()
        start = (current_page - 1) * row_per_page
        end = current_page * row_per_page 
        end = end if end < len(datasource) else len(datasource)
        grid.setRowCount(end - start)
        for r in range(start, end):
            obj = datasource[r]
            for c in range(grid.columnCount() - 1):
                label = grid.horizontalHeaderItem(c).text()
                field =  ''.join([label[:1].lower(), label[1:]])
                value = getattr(obj, field)
                item = QtWidgets.QTableWidgetItem(str(value))
                if type(value).__name__ not in FormLayoutDialogController.scalar_type:
                    item.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
                grid.setItem(r - start, c, item)
        self.add_grid_action(grid_name)

        
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
            for c in range(grid.columnCount() - 1):
                label = grid.horizontalHeaderItem(c).text()
                field =  ''.join([label[:1].lower(), label[1:]])
                field_type = type(getattr(obj, field)).__name__
                if field_type not in FormLayoutDialogController.scalar_type:
                    continue
                value = grid.item(r - start, c).text()
                setattr(obj, field, str(value))
        
    def add_grid_action(self, grid_name):
        grid = self.get_widget(grid_name)
        fieldname = grid.property("field_name")
        datasource = self.__objectListDict[fieldname]

             
        current_page = int(grid.property("current_page"))
        page_count = int(grid.property("page_count"))
        row_per_page = int(grid.property("row_per_page"))
        
        start = 0
        end = current_page * row_per_page 
        end = end if end < len(datasource) else len(datasource)
        
        col = grid.columnCount() - 1
        for r in range(start, end):
            container = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            edit_button = QtWidgets.QPushButton("")
            delete_button = QtWidgets.QPushButton("")
            layout.addWidget(edit_button)
            layout.addWidget(delete_button)     
            layout.setContentsMargins(0, 0, 0, 0)       
            container.setLayout(layout)
            index = (current_page - 1)* row_per_page + r
            edit_button.setProperty("index", index)
            delete_button.setProperty("index", index)
            edit_button.setProperty("field_name", fieldname)
            delete_button.setProperty("field_name", fieldname)
            edit_button.setProperty("for_grid", grid_name)
            delete_button.setProperty("for_grid", grid_name)
            edit_button.setIcon(QtGui.QIcon(f"{FormLayoutDialogController.script_location}/icons/edit.png"))
            delete_button.setIcon(QtGui.QIcon(f"{FormLayoutDialogController.script_location}/icons/del.png"))
            
            edit_button.clicked.connect(self.simplegrid_editbutton_clicked)
            delete_button.clicked.connect(self.simplegrid_deletebutton_clicked)
            grid.setCellWidget(r, col, container)
            
                
    def simplegrid_deletebutton_clicked(self):
        index = self.sender().property("index")
        fieldname = self.sender().property("field_name")
        datasource = self.__objectListDict[fieldname]
        result = self.delete_confirmation(datasource[index])
        if result == 16384: # yes pressed    
            datasource.remove(datasource[index])
            grid_name = self.sender().property("for_grid")        
            grid = self.get_widget(grid_name)
            # grid.removeRow(index)
            # print(datasource)
            self.change_grid_page(self.sender, "refresh") 
            # current_page = int(grid.property("current_page"))
            # page_count = int(grid.property("page_count"))
            # row_per_page = int(grid.property("row_per_page"))
            # grid.clearContents()
            # start = (current_page - 1) * row_per_page
            # end = current_page * row_per_page 
            # end = end if end < len(datasource) else len(datasource)
            # grid.setRowCount(end - start)
            # for r in range(start, end):
            #     obj = datasource[r]
            #     for c in range(grid.columnCount() - 1):
            #         label = grid.horizontalHeaderItem(c).text()
            #         field =  ''.join([label[:1].lower(), label[1:]])
            #         value = getattr(obj, field)
            #         item = QtWidgets.QTableWidgetItem(str(value))
            #         if type(value).__name__ not in FormLayoutDialogController.scalar_type:
            #             item.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
            #         grid.setItem(r - start, c, item)
            # self.add_grid_action(grid_name)
        
    def simplegrid_editbutton_clicked(self):
        index = self.sender().property("index")
        fieldname = self.sender().property("field_name")
        datasource = self.__objectListDict[fieldname]

        from .VPyGUIGenerator import VPyGUIGenerator
        dialog = VPyGUIGenerator.create_gui(datasource[index])
        dialog.exec()
        
        grid_name = self.sender().property("for_grid")        
        grid = self.get_widget(grid_name)
        current_page = int(grid.property("current_page"))
        page_count = int(grid.property("page_count"))
        row_per_page = int(grid.property("row_per_page"))
        start = (current_page - 1) * row_per_page

        obj = datasource[index]
        for c in range(grid.columnCount() - 1):
            label = grid.horizontalHeaderItem(c).text()
            field =  ''.join([label[:1].lower(), label[1:]])
            value = getattr(obj, field)
            item = QtWidgets.QTableWidgetItem(str(value))
            if type(value).__name__ not in FormLayoutDialogController.scalar_type:
                item.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
            grid.setItem(index - start, c, item)
            
    def simpleGridAddNewButtonClicked(self):
        grid_name = self.sender().property("for_grid")
        grid = self.get_widget(grid_name)
        field_name = grid.property("field_name")
        datasource = self.__objectListDict[field_name]
        obj = type(datasource[0])()
        
        from .VPyGUIGenerator import VPyGUIGenerator
        dialog = VPyGUIGenerator.create_gui(obj)
        result = dialog.exec()
        if result == 1: # ok pressed
            datasource.append(obj)
            self.change_grid_page(self.sender, "refresh")
        
        
    def disable_widgets(self, names):
        for name in names:
            w = self.get_widget(name)
            w.setEnabled(False)
    
    def enable_widgets(self, names):
        for name in names:
            w = self.get_widget(name)
            w.setEnabled(True)
            
    def delete_confirmation(self, obj):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Question)
        msg.setText("Are you sure?!")
        msg.setWindowTitle("Confirm")
        msg.setDetailedText(str(obj))
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

        retval = msg.exec()
        return retval
    
    def add_grid_filter(self, grid_name):
        grid = self.get_widget(grid_name) 
        fieldname = grid.property("field_name")
        datasource = self.__objectListDict[fieldname]
        columns = grid.property("grid_columns")
        if columns == None:
            return
        columns = columns.split(",")
        grid.insertRow(0)
        for c in range(len(columns)):
            widget = QtWidgets.QLineEdit()
            widget.setPlaceholderText("Filter " + columns[c])
            widget.setFrame(False)
            widget.setProperty("for_grid", grid_name)
            grid.setCellWidget(0, c, widget)
        
    def clear_all_action_triggered(self):
        list_name = self.sender().property("for_list")
        list_widget = self.get_widget(list_name)
        if list_widget != None:
            list_widget.clear()
            
    def clear_all_table_action_triggered(self):
        table_name = self.sender().property("for_table")
        table_widget = self.get_widget(table_name)
        if table_widget != None:
            table_widget.clearContents()
            table_widget.setRowCount(0)
    
            