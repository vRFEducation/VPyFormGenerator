from PyQt6 import QtWidgets

class WidgetBuilder:
    @classmethod
    def get_cell_widget(cls, info_dict, value):
        widget = None
        if "widget" not in info_dict.keys():
            return None
        widget_name = info_dict["widget"].lower()
        if widget_name == "qslider":
            widget = cls.create_slider(info_dict, value)
        elif widget_name == "qspinbox":
            widget = cls.create_spinbox(info_dict, value)
        elif widget_name == "qdoublespinbox":
            widget = cls.create_doublespinbox(info_dict, value)
        elif widget_name == "qlcdnumber":
            widget = cls.create_lcd(info_dict, value)
        elif widget_name == "qdial":
            widget = cls.create_dial(info_dict, value)
        elif widget_name == "qlabel":
            widget = cls.create_label(info_dict, value)
        elif widget_name == "qlineedit":
            widget = cls.create_line_edit(info_dict, value)
        elif widget_name == "qcheckbox":
            widget = cls.create_checkbox(info_dict, value)
        elif widget_name == "qprogressbar":
            widget = cls.create_progress(info_dict, value)
        elif widget_name in ("qtime", "time", "qtimeedit"):
            widget = cls.create_time(info_dict, value)
        elif widget_name in ("qdate", "date", "qdateedit"):
            widget = cls.create_date(info_dict, value)
        elif widget_name in ("qdatetime", "datetime", "qdatetimeedit"):
            widget = cls.create_datetime(info_dict, value)
        else:
            widget = cls.create_detail_button(info_dict, value)
                


        
        return widget
    
    @classmethod
    def create_slider(cls, info_dict, value):
        widget = QtWidgets.QSlider()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.setValue(value)
        
        if "showLabel" in info_dict.keys() and info_dict["showLabel"] == 'true':
            container = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            layout.addWidget(widget)
            lbl = QtWidgets.QLabel(str(value))
            layout.addWidget(lbl)
            container.setLayout(layout)
            widget.valueChanged.connect(lbl.setNum)
            return container
        return widget
    
    @classmethod
    def create_spinbox(cls, info_dict, value):
        widget = QtWidgets.QSpinBox()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.setValue(value)
        return widget
    
    @classmethod
    def create_doublespinbox(cls, info_dict, value):
        widget = QtWidgets.QDoubleSpinBox()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.setValue(value)
        return widget

    @classmethod
    def create_lcd(cls, info_dict, value):
        widget = QtWidgets.QLCDNumber()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.display(value)
        return widget
    
    @classmethod
    def create_dial(cls, info_dict, value):
        widget = QtWidgets.QDial()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.setValue(value)
        
        if "showLabel" in info_dict.keys() and info_dict["showLabel"] == 'true':
            container = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            layout.addWidget(widget)
            lbl = QtWidgets.QLabel(str(value))
            layout.addWidget(lbl)
            container.setLayout(layout)
            widget.valueChanged.connect(lbl.setNum)
            return container
        return widget        

    @classmethod
    def create_label(cls, info_dict, value):
        widget = QtWidgets.QLabel()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.setText(str(value))
        return widget
    
    @classmethod
    def create_line_edit(cls, info_dict, value):
        widget = QtWidgets.QLineEdit()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.setText(str(value))
        return widget
    
    @classmethod
    def create_progress(cls, info_dict, value):
        widget = QtWidgets.QProgressBar()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.setValue(value)
        return widget
    
    @classmethod
    def create_checkbox(cls, info_dict, value):
        widget = QtWidgets.QCheckBox()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.setChecked(value)
        return widget
    
    @classmethod
    def create_time(cls, info_dict, value):
        widget = QtWidgets.QTimeEdit()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.setTime(value)
        return widget
    
    @classmethod
    def create_date(cls, info_dict, value):
        widget = QtWidgets.QDateEdit()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.setDate(value)
        return widget
    
    @classmethod
    def create_datetime(cls, info_dict, value):
        widget = QtWidgets.QDateTimeEdit()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.setDateTime(value)
        return widget
    
    
    
    @classmethod
    def create_detail_button(cls, info_dict, value):
        widget = QtWidgets.QPushButton()
        for k, v in info_dict.items():
            widget.setProperty(k, v)
        widget.setText(str(value))
        return widget