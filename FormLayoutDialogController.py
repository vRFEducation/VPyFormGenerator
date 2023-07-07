from .WidgetBuilder import WidgetBuilder    
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtCore import pyqtSlot
from pathlib import Path

class FormLayoutDialogController(QtWidgets.QDialog):
    scalar_type = ["str", "int", "float", "bool", "time", "date", "slider", "dial", "lineedit"]
    script_location = Path(__file__).absolute().parent

    def __init__(self, obj, template_file_name, overwrite):
        super(FormLayoutDialogController, self).__init__()
        uic.loadUi(template_file_name, self)
        self.resize(self.sizeHint().width(), self.size().height() );
        self.connect_predefined_slots(self)
        self.obj = obj
        self.__objectListDict = {}
        self.__filteredObjectListDict = {}
        self.__grids_filters = {}
        self.__grid_filter = []
        self.__reset_mode_active = False
        self.__overwrite = overwrite
        self.__edited_obj = None
        self.__edited_grid_obj = {}
        self.__deleted_grid_obj = {}
        self.finalize_ui(self)
    
    def connect_predefined_slots(self, parent):     
        for w in parent.children():
            if len(w.children()) > 0:
                self.connect_predefined_slots(w)
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
                    
            is_file_widget_button = w.property("for_file_widget")
            if is_file_widget_button != None:
                w.clicked.connect(self.fileWidgetButtonClicked)
                file_widget = self.get_widget(w.property("for_file_widget"))
                type = file_widget.property("type")
                if type == None or type.lower() not in("save", "folder"):
                    type = "open"
                w.setIcon(QtGui.QIcon(f"{FormLayoutDialogController.script_location}/icons/{type}.png"))
                w.setProperty("type", type)
                filters = file_widget.property("filters")
                w.setProperty("filters", filters)                
                continue
            
            is_image_widget_link = w.property("for_image_widget")
            if is_image_widget_link != None:
                if w.objectName().startswith("lblChangeImage"):
                    w.linkActivated.connect(self.imageWidgetChangeButtonClicked)
                elif w.objectName().startswith("lblRemoveImage"):
                    w.linkActivated.connect(self.imageWidgetRemoveButtonClicked)

                continue




    def finalize_ui(self, parent):
        for w in parent.children():
            if len(w.children()) > 0:
                self.finalize_ui(w)
            
            key = w.property('key')
            if key == 'simplegrid':
                w.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
                page_count = int(w.property("page_count"))
                grid_name = w.property("field_name")

                if page_count > 1:
                    self.disable_widgets((f"btnFirstPage_{grid_name}", f"btnPrevPage_{grid_name}"))
                else:
                    self.disable_widgets((f"btnFirstPage_{grid_name}", f"btnPrevPage_{grid_name}", f"btnLastPage_{grid_name}",f"btnNextPage_{grid_name}"))
        

                field = w.property("field_name")
                datasource = getattr(self.obj, field)
                self.__objectListDict[field] = []
                self.__filteredObjectListDict[field] = []
                tmp_id = 0
                for obj in datasource:
                    obj.v_id = tmp_id
                    tmp_id += 1
                    self.__objectListDict[field].append(obj)
                    self.__filteredObjectListDict[field].append(obj)
                self.load_simple_grid_data(grid_name)
            elif key == "image":
                ispath = w.property("ispath")
                w.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                                 QtWidgets.QSizePolicy.Policy.MinimumExpanding))
                image = None
                if ispath == None or ispath:
                    filename = w.text()
                    if not QtCore.QFile.exists(w.text()):
                        filename = f"{FormLayoutDialogController.script_location}/icons/notfound.png"
                    image = QtGui.QPixmap(filename)
                else:
                    image = QtGui.QPixmap()
                    image.loadFromData(self.obj.photo)
                self.load_image(w, image)
                
                options_visible = w.property("options")
                if options_visible != None and not options_visible:
                    field = w.property("field_name")
                    option_widget = self.get_widget(f"options_for_{field}")
                    option_widget.setVisible(False)
                    
                    
                    
                
    
    @pyqtSlot()
    def reject(self):
        super().reject()

    @pyqtSlot()
    def accept(self):
        obj = self.obj
        if not self.__overwrite:
            if self.__edited_obj == None:
                self.__edited_obj = type(self.obj)()
            obj = self.__edited_obj
        
        widget_list = self.findChildren(QtWidgets.QWidget, options= QtCore.Qt.FindChildOption.FindChildrenRecursively)
        for w in widget_list:
            
            field_name = w.property("field_name")
            if field_name != None:
                key = w.property("key")
                field = w.property("prop_name")
                if key == "progressbar":
                    continue
                if key == "multichoice":
                  selected_items = self.get_selected_items(w)
                  setattr(obj, field_name, selected_items)
                elif(key in FormLayoutDialogController.scalar_type):
                    if key == "bool":   
                        setattr(obj, field_name, str(w.property(field)).capitalize())
                    else:
                        setattr(obj, field_name, w.property(field))
                elif(field == "list"):
                    lst = []
                    for i in range(len(w)):
                        lst.append(w.item(i).text())
                    setattr(obj, field_name, lst)
                elif(field == "dict"):
                    dc = {}
                    for r in range(w.rowCount()):
                        dc[w.item(r, 0).text()] = w.item(r, 1).text()
                    setattr(obj, field_name, dc)
                elif(field == "datetime"):
                     setattr(obj, field_name, w.dateTime())
                elif(key == "combo"):
                    setattr(obj, field_name, w.property("currentText"))
                elif key == 'simplegrid':
                    grid_name = w.property("field_name")
                    grid_obj_edited =  grid_name in self.__edited_grid_obj
                    grid_obj_deleted =  grid_name in self.__deleted_grid_obj
                    index = 0
                    datasource = self.__objectListDict[grid_name]
                    
                    while index < len(datasource):
                        tmp_obj = datasource[index]
                        if grid_obj_deleted and tmp_obj.v_id in self.__deleted_grid_obj[grid_name]:
                            datasource.remove(tmp_obj)
                            continue                            
                        if grid_obj_edited and tmp_obj.v_id in self.__edited_grid_obj[grid_name]:
                            datasource[index] = self.__edited_grid_obj[grid_name][tmp_obj.v_id]
                        index += 1
                        if hasattr(tmp_obj, "v_id"):
                            del tmp_obj.v_id
                    setattr(obj, field_name, datasource)
                elif(key == "file"):
                    setattr(obj, field_name, w.property(field))
                elif(key == "image"):
                    ispath = w.property("ispath")
                    if ispath == None or ispath :
                        setattr(obj, field_name, w.property("path"))
                    else:
                        pixmap = w.pixmap()
                        ba = QtCore.QByteArray()
                        buff = QtCore.QBuffer(ba)
                        buff.open(QtCore.QIODevice.OpenModeFlag.WriteOnly) 
                        ok = pixmap.save(buff, "PNG")
                        setattr(obj, field_name, ba.data())
                        buff.close
                        




        super().accept()
        
    @pyqtSlot()
    def imageWidgetRemoveButtonClicked(self):
        widget_name = self.sender().property("for_image_widget")
        label = self.get_widget(widget_name) 
        label.setProperty("path", "")
        label.setText(' ')
    
    @pyqtSlot()
    def imageWidgetChangeButtonClicked(self):
        widget_name = self.sender().property("for_image_widget")
        filename = ""
        filters = "Image Files (*.jpg; *.png; *.gif; *.bmp)"
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,widget_name.capitalize(), "", filters)
        if filename == '':
            return
        label = self.get_widget(widget_name)
        field_name = label.property("field_name")
        if label != None:
            ispath = label.property("ispath")
            image = None
            if ispath == None or ispath:
                if not QtCore.QFile.exists(filename):
                    filename = f"{FormLayoutDialogController.script_location}/icons/notfound.png"
                image = QtGui.QPixmap(filename)
                label.setProperty("path", filename)
                self.load_image(label, image)
            else:
                with open(filename, 'rb') as file:
                    data = file.read()
                    image = QtGui.QPixmap()
                    image.loadFromData(data)                    
                    
            self.load_image(label, image)
                    
                    

                
                
    def load_image(self, label, image):
        w = label.width()
        h = label.height()
        label.setPixmap(image.scaled(w,h,QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        
    @pyqtSlot()
    def fileWidgetButtonClicked(self):
        type =  self.sender().property("type")
        widget_name = self.sender().property("for_file_widget")
        filename = ""
        filters = "All Files (*)"
        tmp_filters = self.sender().property("filters")
        filters = tmp_filters if tmp_filters != None else filters
        if type == "save":
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,widget_name.capitalize(), "", filters)
        elif type == "folder":
            filename = QtWidgets.QFileDialog.getExistingDirectory(self,widget_name.capitalize(), "")
        else:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,widget_name.capitalize(), "", filters)
        
        line_edit = self.get_widget(widget_name)
        if line_edit != None:
            line_edit.setText(filename)
            
        
        
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
        obj = getattr(self.obj, object_name)
        from .VPyGUIGenerator import VPyGUIGenerator
        dialog = VPyGUIGenerator.create_gui(obj, self.__overwrite)
        result = dialog.exec()
        if result == 0:
            return
        text_to_display = ""
        if not self.__overwrite:
            if self.get_edited_obj() == None:
                self.__edited_obj = type(self.obj)()
            setattr(self.__edited_obj, object_name, dialog.get_edited_obj())
            text_to_display = str(getattr(self.__edited_obj, object_name))
        else:
            text_to_display= str(getattr(self.obj, object_name))
        label_widget = self.get_widget(object_name)
        label_widget.setText(text_to_display)


    def get_widget(self, name, parent = None):
        if parent == None:
            parent = self
        for w in parent.children():
            if len(w.children()) > 0:
                res= self.get_widget(name, w)
                if res != None:
                    return res
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
        if grid_name == None:
            grid_name = sender().parent().property("for_grid")
        grid = self.get_widget(grid_name)
        spn_page = self.get_widget(f"spnPageNumber_{grid_name}")
        self.enable_widgets((f"btnFirstPage_{grid_name}", f"btnPrevPage_{grid_name}", f"btnLastPage_{grid_name}",f"btnNextPage_{grid_name}"))
        fieldname = grid.property("field_name")

        if action not in  ("refresh", "reset"):
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
        elif action in ("row_per_page", "refresh", "reset"):
            current_page = 1 if action != "refresh" else current_page
            row_per_page = row_per_page if action != "row_per_page" else int(sender().currentText())
            import math
            valid_row_count = len(self.__filteredObjectListDict[fieldname])
            if grid_name in self.__deleted_grid_obj:
                valid_row_count -= len(self.__deleted_grid_obj[grid_name])
            page_count = math.ceil(valid_row_count / row_per_page)
            if current_page > page_count:
                current_page = page_count   
            spn_page.setMaximum(page_count)
            spn_page.setSuffix(f"/{page_count}")
            if page_count > 1:
                if current_page == 1:
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
        tmp_filtering = grid.property("showFiltering")
        tmp_start = 1 if tmp_filtering!= None and tmp_filtering.lower() == "true" else 0

        for r in range(tmp_start, grid.rowCount()):
            grid.removeRow(tmp_start)

        fieldname = grid.property("field_name")
        datasource = self.__filteredObjectListDict[fieldname]
        if len(datasource) == 0:
            return
       
        current_page = int(grid.property("current_page"))
        row_per_page = int(grid.property("row_per_page"))
        # datasource = self.__objectListDict[fieldname]

        
        if tmp_filtering!= None and tmp_filtering.lower() == "true":
            if fieldname not in self.__grid_filter:
                self.add_grid_filter(fieldname)
      
        
        start = (current_page - 1) * row_per_page
        end = current_page * row_per_page 
        end = end if end < len(datasource) else len(datasource)
        count = row_per_page

        grid_obj_deleted = grid_name in self.__deleted_grid_obj

        rows_to_pass = (current_page - 1) * row_per_page
        r = -1
        while rows_to_pass > 0 and r < len(datasource):
            r += 1
            if grid_obj_deleted and  datasource[r].v_id in self.__deleted_grid_obj[grid_name]:
                continue
            rows_to_pass -= 1
        r += 1    
        while count > 0 and r < len(datasource):
            obj = datasource[r]
            r += 1
            if grid_obj_deleted and obj.v_id in self.__deleted_grid_obj[grid_name]:
                continue
            grid.insertRow(grid.rowCount())
            
            if grid_name in self.__edited_grid_obj:
                if obj.v_id in self.__edited_grid_obj[grid_name]:
                    obj = self.__edited_grid_obj[grid_name][obj.v_id]


            for c in range(grid.columnCount() - 1):
                label = grid.horizontalHeaderItem(c).text()
                field =  ''.join([label[:1].lower(), label[1:]])
                value = getattr(obj, field)
                item = QtWidgets.QTableWidgetItem(str(value))
                if type(value).__name__ not in FormLayoutDialogController.scalar_type:
                    item.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
                grid.setItem(grid.rowCount() - 1, c, item)
            count -= 1
            tmp_cell = QtWidgets.QTableWidgetItem(str(obj.v_id))
            grid.setItem(grid.rowCount() - 1, grid.columnCount() - 1, tmp_cell)

        self.add_grid_action(grid_name)


        
    def presave_grid_data(self, grid_name):
        return
        grid = self.get_widget(grid_name)
        fieldname = grid.property("field_name")
        datasource = self.__filteredObjectListDict[fieldname]

        is_paginated = bool(grid.property("is_paginated"))
        current_page = int(grid.property("current_page"))
        row_per_page = int(grid.property("row_per_page")) if is_paginated else len(datasource)
            
        start = (current_page - 1) * row_per_page
        end = current_page * row_per_page 
        end = end if end < len(datasource) else len(datasource)
        tmp_filtering = grid.property("showFiltering")
        bias = 0
        if tmp_filtering!= None and tmp_filtering.lower() == "true":
            bias = 1

        for r in range(start, end):
            obj = datasource[r]
            for c in range(grid.columnCount() - 1):
                label = grid.horizontalHeaderItem(c).text()
                field =  ''.join([label[:1].lower(), label[1:]])
                field_type = type(getattr(obj, field)).__name__
                if field_type not in FormLayoutDialogController.scalar_type:
                    continue
                value = grid.item(r - start + bias, c).text()
                setattr(obj, field, str(value))
        
    def add_grid_action(self, grid_name):
        grid = self.get_widget(grid_name)
        fieldname = grid.property("field_name")
              
        row_bias = 0
        tmp_filtering = grid.property("showFiltering")
        if tmp_filtering!= None and tmp_filtering.lower() == "true":
            row_bias = 1            
        
        col = grid.columnCount() - 1
        row_count = grid.rowCount()
        for r in range(row_bias, row_count):
            container = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            edit_button = QtWidgets.QPushButton("")
            delete_button = QtWidgets.QPushButton("")
            layout.addWidget(edit_button)
            layout.addWidget(delete_button)     
            layout.setContentsMargins(0, 0, 0, 0)       
            container.setLayout(layout)
            v_id = int (grid.item(r, col).text())
            edit_button.setProperty("v_id", v_id)
            edit_button.setProperty("row_id", r)
            delete_button.setProperty("v_id", v_id)            
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
        index = self.sender().property("v_id")
        fieldname = self.sender().property("field_name")
        datasource = self.__filteredObjectListDict[fieldname]
        obj_to_delete = None
        for o in datasource:
            if o.v_id == index:
                obj_to_delete = o
                break

        result = self.delete_confirmation(obj_to_delete)
        if result == 16384: # yes pressed    
            # obj_to_delete.v_is_removed = True
            if fieldname not in self.__deleted_grid_obj:
                self.__deleted_grid_obj[fieldname] = []
            self.__deleted_grid_obj[fieldname].append(obj_to_delete.v_id)
 
            self.change_grid_page(self.sender, "refresh") 
        
    def simplegrid_editbutton_clicked(self):
        index = self.sender().property("v_id")
        fieldname = self.sender().property("field_name")
        grid_name = self.sender().property("for_grid")        

        datasource = self.__filteredObjectListDict[fieldname]
        obj_to_edit = None
        for o in datasource:
            if o.v_id == index:
                obj_to_edit = o
                break
        if grid_name in self.__edited_grid_obj:
            if obj_to_edit.v_id in self.__edited_grid_obj[grid_name]:
                obj_to_edit = self.__edited_grid_obj[grid_name][obj_to_edit.v_id]
 

        from .VPyGUIGenerator import VPyGUIGenerator
        dialog = VPyGUIGenerator.create_gui(obj_to_edit, overwrite = False)
        result = dialog.exec()
        if result == 0:
            return
        
        grid = self.get_widget(grid_name)
        current_page = int(grid.property("current_page"))
        page_count = int(grid.property("page_count"))
        row_per_page = int(grid.property("row_per_page"))
        start = (current_page - 1) * row_per_page

        obj = dialog.get_edited_obj()
        obj.v_id = obj_to_edit.v_id
        if grid_name not in self.__edited_grid_obj:
            self.__edited_grid_obj[grid_name] = {}
        self.__edited_grid_obj[grid_name][obj.v_id] = obj
        
        r = self.sender().property("row_id")        

        for c in range(grid.columnCount() - 1):
            label = grid.horizontalHeaderItem(c).text()
            field =  ''.join([label[:1].lower(), label[1:]])
            value = getattr(obj, field)
            item = QtWidgets.QTableWidgetItem(str(value))
            if type(value).__name__ not in FormLayoutDialogController.scalar_type:
                item.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
            grid.setItem(r, c, item)
            
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
            obj.v_id = len(self.__objectListDict[field_name])
            self.__filteredObjectListDict[field_name] = self.__objectListDict[field_name]
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
        
        grid =  self.get_widget(grid_name) 
        fieldname = grid.property("field_name")
        # datasource = self.__objectListDict[fieldname]
        datasource = self.__filteredObjectListDict[fieldname]
        if len(datasource) == 0:
            return
        columns = grid.property("grid_columns")
        if columns == None:
            return

        grid.insertRow(0)
        vHeader = grid.verticalHeader()       
        vHeader.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        hHeader = grid.horizontalHeader()       

        columns = columns.split(",")

        property_dict = (dict(datasource[0].__class__.__dict__))
        column_widget = {}
        for k, v in property_dict.items():
            if type(v) != property or v.fset == None:
                continue
            if len(v.fset.__annotations__) == 0:
                continue
            an  = v.fset.__annotations__
            mydict = {}
            for kk, vv in an.items():
                newValue = vv.replace("::", "$%^")
                mydict = dict((k1.strip(), v1.strip()) for k1,v1 in 
                                (item.split(':') for item in newValue.split(',')))
                for k2,v2 in mydict.items():
                    if "$%^" in v2:
                        mydict[k2] = v2.replace("$%^", "::")
            column_widget[k] = mydict
            

        
        
        for c in range(len(columns)):
            widget = None
            col = columns[c]
            # tmp_filter_key = f"{fieldname}_{col}"
            # if tmp_filter_key in self.__grid_filter_widgets.keys():
            #     widget = self.__grid_filter_widgets[tmp_filter_key]
            # else:
            if col in column_widget.keys():
                widget = WidgetBuilder.get_cell_widget(column_widget[col], grid, col, self.filter_actions_triggered)
            else:
                widget = QtWidgets.QLineEdit()
            # self.__grid_filter_widgets[tmp_filter_key] = widget

        
            filter_name = widget.property("filter_name")
            filter_widget = self.get_widget(filter_name)
            t = type(filter_widget)
            if t in (QtWidgets.QLineEdit,):
                filter_widget.textChanged.connect(self.lineedit_filter_changed) 
            elif t in (QtWidgets.QSpinBox, QtWidgets.QDoubleSpinBox):
                filter_widget.valueChanged.connect(self.spinbox_filter_changed)
            elif t in (QtWidgets.QDial, QtWidgets.QSlider):
                filter_widget.sliderReleased.connect(self.slider_dial_filter_changed)
            elif t is QtWidgets.QComboBox:
                filter_widget.currentIndexChanged.connect(self.combobox_filter_changed)                
            elif t is QtWidgets.QCheckBox:
                filter_widget.toggled.connect(self.checkbox_filter_changed)     
            elif t in (QtWidgets.QDateTimeEdit, QtWidgets.QDateEdit, QtWidgets.QTimeEdit):
                filter_widget.dateTimeChanged.connect(self.dateTime_filter_changed)     

                
            

            grid.setCellWidget(0, c, widget)
            c += 1
        reset_filter_button = self.create_reset_button_for_grid_filter(grid_name)
        grid.setCellWidget(0, len(columns), reset_filter_button)
        self.__grid_filter.append(fieldname)
        
    def create_reset_button_for_grid_filter(self, grid_name):
        reset_filter_button = QtWidgets.QToolButton()
        reset_filter_button.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        reset_filter_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        reset_filter_button.setIcon(QtGui.QIcon(f"{FormLayoutDialogController.script_location}/icons/reset.png"))
        reset_filter_button.clicked.connect(self.reset_filter_button_clicked)
        reset_filter_button.setText("Reset")
        reset_filter_button.setProperty("for_grid", grid_name)
        
        menu = QtWidgets.QMenu(reset_filter_button)
        menu.setProperty("for_grid", grid_name)
        
        and_action = WidgetBuilder.creat_widget_action(menu, "AND", "AND")
        and_action.triggered.connect(self.filter_combination_changed)
        and_action.setProperty("for_grid", grid_name)
        and_action.setChecked(True)
        and_action.setObjectName(f"AND_filter_{grid_name}")
        
        
        or_action = WidgetBuilder.creat_widget_action(menu, "OR", "OR")
        or_action.triggered.connect(self.filter_combination_changed)
        or_action.setProperty("for_grid", grid_name)
        
        menu.addAction(and_action)
        menu.addAction(or_action)
        reset_filter_button.setMenu(menu)
        if grid_name not in self.__grids_filters.keys():
            self.__grids_filters[grid_name] = {}
        self.__grids_filters[grid_name]['filter_combination'] = "AND"
       
        return reset_filter_button
        
    def clear_all_action_triggered(self):
        list_name = self.sender().property("for_list")
        list_widget = self.get_widget(list_name)
        if list_widget != None:
            list_widget.clear()
    
    def filter_actions_triggered(self):
        w = self.sender()
        menu = w.parent()
        actions = menu.children()
        for act in actions:
            if act != w and act.isChecked():
                act.setChecked(False)
        w.setChecked(True)
        filter_widget = self.get_widget(menu.property('for_filter'))
        if filter_widget != None:
            filter_widget.setProperty("filter_type", w.property("filter_type"))
            filter = self.update_grid_filter(filter_widget)
            filter['type'] =  w.property("filter_type")
            grid_name = filter_widget.property("for_grid")
            self.do_grid_filtering(grid_name)

        
            
    def clear_all_table_action_triggered(self):
        table_name = self.sender().property("for_table")
        table_widget = self.get_widget(table_name)
        if table_widget != None:
            table_widget.clearContents()
            table_widget.setRowCount(0)
        
    pyqtSlot()
    def reset_filter_button_clicked(self):
        self.__reset_mode_active = True
        grid_name = self.sender().property("for_grid")
        filters = self.__grids_filters[grid_name]
        if len(filters) == 1 and 'filter_combination' in filters:
            action = self.get_widget(f"AND_filter_{grid_name}")
            if not action.isChecked():
                action.trigger()
            self.__reset_mode_active = False
            return        
        
        grid = self.get_widget(grid_name)
        for c in range(grid.columnCount() - 1):
            w = grid.cellWidget(0, c)
            self.reset_widget(w)
        self.__filteredObjectListDict[grid_name] = self.__objectListDict[grid_name]
        
        del self.__grids_filters[grid_name]
        self.__grids_filters[grid_name] = {}
        action = self.get_widget(f"AND_filter_{grid_name}")
        # if not action.isChecked():
        action.trigger()
        action.setChecked(True)
        
            
        
        self.change_grid_page(self.sender, "reset")
        self.__reset_mode_active = False
        
    def reset_widget(self, w):
        t = type(w)
        if t in (QtWidgets.QLineEdit,):
            w.setText("")
        elif t in (QtWidgets.QSlider, QtWidgets.QSpinBox, QtWidgets.QDoubleSpinBox, QtWidgets.QDial):
            w.setValue(0)
        elif t is QtWidgets.QComboBox:
            w.setCurrentIndex(-1)
        elif t in (QtWidgets.QWidget,):
            for c in w.children():
                self.reset_widget(c)
    
    def update_grid_filter(self, w):
        column = w.property("for_column")
        grid_name = w.property("for_grid")
        
        if grid_name not in self.__grids_filters.keys():
            self.__grids_filters[grid_name] = {}
        if column not in self.__grids_filters[grid_name]:
            self.__grids_filters[grid_name][column] = {}
        self.__grids_filters[grid_name][column]['type'] = w.property("filter_type")
        return self.__grids_filters[grid_name][column]
    
    def remove_grid_filter(self, w):
        column = w.property("for_column")
        grid_name = w.property("for_grid")
        
        if grid_name in self.__grids_filters.keys():
            if column in self.__grids_filters[grid_name]:
                del self.__grids_filters[grid_name][column]
        
        

        
    @pyqtSlot()
    def lineedit_filter_changed(self):
        w = self.sender()
        filter = self.update_grid_filter(w)
        text = w.text()
        grid_name = w.property("for_grid")
        if len(text) == 0 and 'value' in filter.keys():
            column = w.property("for_column")
            del self.__grids_filters[grid_name][column]
        else:
            filter['value'] = text
        if not self.__reset_mode_active:
            self.do_grid_filtering(grid_name)
        
       
    
    @pyqtSlot()
    def spinbox_filter_changed(self):
        w = self.sender()
        filter = self.update_grid_filter(w)
        filter['value'] = w.value()
        grid_name = w.property("for_grid")
        self.do_grid_filtering(grid_name)
    
    @pyqtSlot()
    def combobox_filter_changed(self):
        w = self.sender()
        filter = self.update_grid_filter(w)
        if w.currentIndex() == -1:
            self.remove_grid_filter(w)
        else:
            filter['value'] = w.currentText()
        grid_name = w.property("for_grid")
        if not self.__reset_mode_active:
            self.do_grid_filtering(grid_name)
            
       
    @pyqtSlot()
    def slider_dial_filter_changed(self):
        w = self.sender()
        filter = self.update_grid_filter(w)
        filter['value'] = w.value()
        grid_name = w.property("for_grid")
        if not self.__reset_mode_active:
            self.do_grid_filtering(grid_name)
    @pyqtSlot()
    def checkbox_filter_changed(self):
        w = self.sender()
        filter = self.update_grid_filter(w)
        filter['value'] = w.isChecked()
        grid_name = w.property("for_grid")
        if not self.__reset_mode_active:
            self.do_grid_filtering(grid_name)
            
    @pyqtSlot()
    def dateTime_filter_changed(self):
        w = self.sender()
        filter = self.update_grid_filter(w)
        if type(w) == QtWidgets.QDateTimeEdit:
            filter['value'] = w.dateTime()
        elif type(w) == QtWidgets.QDateEdit:
            filter['value'] = w.date()
        elif type(w) == QtWidgets.QTimeEdit:
            filter['value'] = w.time()
        grid_name = w.property("for_grid")
        if not self.__reset_mode_active:
            self.do_grid_filtering(grid_name)
    
    def do_grid_filtering(self, grid_name):
        filters = self.__grids_filters[grid_name]
        grid = self.get_widget(grid_name)
        datasource = self.__objectListDict[grid_name]
        if len(filters) == 1 and 'filter_combination' in filters:
            self.__filteredObjectListDict[grid_name] = datasource
            self.change_grid_page(self.sender, "reset")
            return
        if len(datasource) == grid.rowCount() - 1 :
            return
        combination = filters['filter_combination']
        
        grid_obj_edited =  grid_name in self.__edited_grid_obj
        grid_obj_deleted =  grid_name in self.__deleted_grid_obj
        index = 0
        updated_datasource = []
        while index < len(datasource):
            obj = datasource[index]
            if grid_obj_deleted and obj.v_id in self.__deleted_grid_obj[grid_name]:
                index += 1
                continue                            
            elif grid_obj_edited and obj.v_id in self.__edited_grid_obj[grid_name]:
                updated_datasource.append(self.__edited_grid_obj[grid_name][obj.v_id])
            else:
                updated_datasource.append(obj)
            
            index += 1
            
        result = []
        if combination == "OR":
            for obj in updated_datasource:
                for col,filter in filters.items():
                    if col == 'filter_combination' or 'value' not in filter or 'type' not in filter:
                        continue
                    entered_value = filter['value']
                    filter_type = filter['type']
                    value = getattr(obj, col)

                    if obj in result:
                        continue                    
                    
                    if filter_type == "contains":
                        if entered_value in value:
                            result.append(obj)
                    elif filter_type == "not_contains":
                        if entered_value not in value:
                            result.append(obj)
                    elif filter_type == "startswith":
                        if value.startswith(entered_value):
                            result.append(obj)
                    elif filter_type == "endswith":
                        if value.endswith(entered_value):
                            result.append(obj)
                    elif filter_type == "eq":
                        if value == entered_value:
                            result.append(obj)
                    elif filter_type == "ne" :
                        if value != entered_value:
                            result.append(obj)
                    elif filter_type == "lte" :
                        if value <= entered_value:
                            result.append(obj)
                    elif filter_type == "gte" :
                        if value >= entered_value:
                            result.append(obj)
        elif combination == "AND":
            for obj in updated_datasource:
                condition_met = True
                for col,filter in filters.items():
                    if col == 'filter_combination' or 'value' not in filter or 'type' not in filter:
                        continue
                    entered_value = filter['value']
                    filter_type = filter['type']
                    value = getattr(obj, col)

                    if filter_type == "contains":
                        condition_met = condition_met and entered_value  in value
                    elif filter_type == "not_contains" :
                        condition_met = condition_met and entered_value not in value
                    elif filter_type == "startswith" :
                        condition_met = condition_met and value.startswith(entered_value) 
                    elif filter_type == "endswith" :
                        condition_met = condition_met and value.endswith(entered_value)
                    elif filter_type == "eq" :
                        condition_met = condition_met and value == entered_value
                    elif filter_type == "ne" :
                        condition_met = condition_met and  value != entered_value
                    elif filter_type == "lte" :
                        condition_met = condition_met and value <= entered_value
                    elif filter_type == "gte" :
                        condition_met = condition_met and value >= entered_value
                    
                if condition_met:
                    result.append(obj)                            
                            
        self.__filteredObjectListDict[grid_name] = result
        self.change_grid_page(self.sender, "reset")
        
    def filter_combination_changed(self):
        
        w = self.sender()
        filter_combination = w.property("filter_type")
        grid_name = w.property("for_grid")
        
        menu = w.parent()
        actions = menu.children()
        for act in actions:
            if act != w and act.isChecked():
                act.setChecked(False)
            

        if grid_name not in self.__grids_filters.keys():
            self.__grids_filters[grid_name] = {}
        self.__grids_filters[grid_name]["filter_combination"] = filter_combination
        if not self.__reset_mode_active:
            self.do_grid_filtering(grid_name)

    def get_edited_obj(self):
        return self.__edited_obj