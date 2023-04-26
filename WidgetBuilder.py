from PyQt6 import QtWidgets, QtCore, QtGui

class WidgetBuilder:
    @classmethod
    def get_cell_widget(cls, info_dict, grid, column, action_trigger_handler):
        widget = None
        if "widget" not in info_dict.keys():
            return None
        min_size = None
        if "minimumSize" in info_dict.keys():
            min_size = info_dict["minimumSize"].replace("[", "").replace("]", "").split(";")  
            info_dict.pop("minimumSize")
        widget_name = info_dict["widget"].lower()
        if widget_name == "qslider":
            widget = cls.create_slider(info_dict, column)
        elif widget_name == "qspinbox":
            widget = cls.create_spinbox(info_dict, column)
        elif widget_name == "qdoublespinbox":
            widget = cls.create_doublespinbox(info_dict, column)
        elif widget_name == "qlcdnumber":
            widget = cls.create_lcd(info_dict, column)
        elif widget_name == "qdial":
            widget = cls.create_dial(info_dict, column)
        elif widget_name == "qlabel":
            widget = cls.create_label(info_dict, column)
        elif widget_name == "qlineedit":
            widget = cls.create_line_edit(info_dict, column)
        elif widget_name == "qcheckbox":
            widget = cls.create_checkbox(info_dict, column)
        elif widget_name == "qprogressbar":
            widget = cls.create_progress(info_dict, column)
        elif widget_name in ("qtime", "time", "qtimeedit"):
            widget = cls.create_time(info_dict, column)
        elif widget_name in ("qdate", "date", "qdateedit"):
            widget = cls.create_date(info_dict, column)
        elif widget_name in ("qdatetime", "datetime", "qdatetimeedit"):
            widget = cls.create_datetime(info_dict, column)
        elif widget_name == "qcombobox":
            widget = cls.create_combobox(info_dict, column)
        else:
            widget = cls.create_line_edit(info_dict, column)
            # widget = cls.create_detail_button(info_dict, value)
        if min_size != None:
            widget.setMinimumSize(int(min_size[0]), int(min_size[1]))
                
        grid_name = grid.objectName()
        widget.setProperty("for_column", column)
        widget.setProperty("for_grid", grid_name)
        widget.setObjectName(f"filter_for_{grid_name}_{column}")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        widget.setSizePolicy(sizePolicy)
        
        if(widget_name in ("qslider", "qdial")):
            w = widget
            if len(widget.children()) > 0:
                w = widget.children()[1]
            w.setProperty("for_column", column)
            w.setProperty("for_grid", grid_name)
            w.setObjectName(f"filter_for_{grid_name}_{column}")
        
        container = cls.add_option(widget, action_trigger_handler)
        container.setParent(grid.parent())
        container.setProperty("filter_name", f"filter_for_{grid_name}_{column}")
        
        return container
                
        # return widget
    @classmethod
    def add_option(cls, widget, action_trigger_handler):
        container = QtWidgets.QWidget(widget.parent())
        widget.setParent(container)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0);
        
        more_button = QtWidgets.QToolButton(container)
        more_button.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        more_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        more_button.setMaximumSize(13, 100)
        layout.addWidget(more_button)
        
        menu = QtWidgets.QMenu(more_button)
        menu.setProperty("for_filter_", widget.objectName())
        menu.setProperty("for_grid", widget.property("for_grid"))
        

        action_type = widget.property("action_type")
        actions_list = []
        if action_type in ("numeric", "inner_numeric") :
            equal_action = cls.creat_widget_action(menu, "==", "eq")
            not_equal_action = cls.creat_widget_action(menu, "!=", "ne")
            less_action = cls.creat_widget_action(menu, "<=", "lte")
            greater_action = cls.creat_widget_action(menu, ">=", "gte")
            actions_list.append(equal_action)
            actions_list.append(not_equal_action)
            actions_list.append(less_action)
            actions_list.append(greater_action)
            equal_action.setChecked(True)
            if action_type == "inner_numeric": # used for slider and dial with label
                widget.children()[1].setProperty("filter_type", "eq")
                widget.setObjectName(widget.children()[1].objectName())
            else:
                widget.setProperty("filter_type", "eq")
        elif action_type == "string":
            contains_action = cls.creat_widget_action(menu, "Contains", "contains")
            not_contains_action = cls.creat_widget_action(menu, "Not Contains", "not_contains")
            startswith_action = cls.creat_widget_action(menu, "Starts With", "startswith")
            endswith_action = cls.creat_widget_action(menu, "Ends With", "endswith")
            equal_action = cls.creat_widget_action(menu, "Equal", "eq")
            actions_list.append(contains_action)
            actions_list.append(not_contains_action)
            actions_list.append(startswith_action)
            actions_list.append(endswith_action)
            actions_list.append(equal_action)
            contains_action.setChecked(True)
            widget.setProperty("filter_type", "contains")
        elif action_type == "combo":
            equal_action = cls.creat_widget_action(menu, "Equal", "eq")
            not_equal_action = cls.creat_widget_action(menu, "Not Equal", "ne")
            actions_list.append(equal_action)
            actions_list.append(not_equal_action)
            equal_action.setChecked(True)
            widget.setProperty("filter_type", "eq")
        
        for action in actions_list:
            action.triggered.connect(action_trigger_handler)
        menu.addActions(actions_list)
        more_button.setMenu(menu)
        menu.setProperty("for_filter", widget.objectName())
        container.setLayout(layout)
        return container
    
    @classmethod
    def creat_widget_action(cls, menu, text, filter):
        action = QtGui.QAction()
        action.setText(text)
        action.setCheckable(True)
        action.setParent(menu)
        action.setProperty("filter_type", filter)
        
        return action
 
    
    @classmethod
    def create_slider(cls, info_dict, value):
        widget = QtWidgets.QSlider()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        
        # widget.setValue(value)
        widget.setProperty("action_type", "numeric")
        if "showLabel" in info_dict.keys() and info_dict["showLabel"] == 'true':
            container = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            layout.setContentsMargins(0,0,0,0)
            layout.addWidget(widget)
            lbl = QtWidgets.QLabel("0")
            layout.addWidget(lbl)
            container.setLayout(layout)
            widget.valueChanged.connect(lbl.setNum)
            container.setProperty("action_type", "inner_numeric")
            return container
        return widget
    
    @classmethod
    def create_spinbox(cls, info_dict, value):
        widget = QtWidgets.QSpinBox()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        # widget.setValue(value)
        widget.setProperty("action_type", "numeric")
        return widget
    
    @classmethod
    def create_doublespinbox(cls, info_dict, value):
        widget = QtWidgets.QDoubleSpinBox()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        # widget.setValue(value)
        widget.setProperty("action_type", "numeric")
        return widget

    @classmethod
    def create_lcd(cls, info_dict, value):
        widget = QtWidgets.QLCDNumber()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        # widget.display(value)
        return widget
    
    @classmethod
    def create_dial(cls, info_dict, value):
        widget = QtWidgets.QDial()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.setProperty("action_type", "numeric")
        # widget.setValue(value)
        
        if "showLabel" in info_dict.keys() and info_dict["showLabel"] == 'true':
            container = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            layout.addWidget(widget)
            lbl = QtWidgets.QLabel(str(value))
            layout.addWidget(lbl)
            container.setLayout(layout)
            widget.valueChanged.connect(lbl.setNum)
            container.setProperty("action_type", "inner_numeric")

            return container
        return widget        

    @classmethod
    def create_label(cls, info_dict, value):
        widget = QtWidgets.QLabel()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        # widget.setText(str(value))
        return widget
    
    @classmethod
    def create_line_edit(cls, info_dict, value):
        widget = QtWidgets.QLineEdit()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        # widget.setText(str(value))
        widget.setClearButtonEnabled(True)
        widget.setFrame(False)
        widget.setPlaceholderText(f"Filter {value}")
        widget.setProperty("action_type", "string")
        return widget
    
    @classmethod
    def create_progress(cls, info_dict, value):
        widget = QtWidgets.QProgressBar()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        # widget.setValue(value)
        return widget
    
    @classmethod
    def create_checkbox(cls, info_dict, value):
        widget = QtWidgets.QCheckBox()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        # widget.setChecked(value)
        widget.setProperty("action_type", "boot")
        return widget
    
    @classmethod
    def create_time(cls, info_dict, value):
        widget = QtWidgets.QTimeEdit()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        # widget.setTime(value)
        widget.setProperty("action_type", "numeric")
        return widget
    
    @classmethod
    def create_date(cls, info_dict, value):
        widget = QtWidgets.QDateEdit()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        # widget.setDate(value)
        widget.setProperty("action_type", "numeric")
        return widget
    
    @classmethod
    def create_datetime(cls, info_dict, value):
        widget = QtWidgets.QDateTimeEdit()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        # widget.setDateTime(value)
        widget.setProperty("action_type", "numeric")
        return widget
    
    
    @classmethod
    def create_combobox(cls, info_dict, value):
        widget = QtWidgets.QComboBox()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        # widget.setDateTime(value)
        if "combo_items" in info_dict.keys():
            items = info_dict["combo_items"].replace("[", "").replace("]", "").split(";")  
            widget.addItems(items)
        widget.setCurrentIndex(-1)
        widget.setProperty("action_type", "combo")
            
        return widget
    
    
    @classmethod
    def create_detail_button(cls, info_dict, value):
        widget = QtWidgets.QPushButton()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        # widget.setText(str(value))
        return widget