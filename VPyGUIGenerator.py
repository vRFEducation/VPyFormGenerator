from .TypeInfo import TypeInfo
from .FormLayoutDialogController import FormLayoutDialogController
from pathlib import Path

class VPyGUIGenerator:
    __connections = ""
    type_dict = {
        "str": TypeInfo("QLineEdit", "text", "string", "str"),
        "int": TypeInfo("QSpinBox", "value", "number", "int"),
        "float": TypeInfo("QDoubleSpinBox", "value", "double", "float"),
        "bool": TypeInfo("QCheckBox", "checked", "bool", "bool"),
        "list": TypeInfo("QListWidget", "list", "string", "list"),
        "date": TypeInfo("QDateEdit", "date", "date", "date"),
        "time": TypeInfo("QTimeEdit", "time", "time", "time"),
        "datetime": TypeInfo("QDateTimeEdit", "datetime", "datetime", "datetime"),
        "dict" : TypeInfo("QTableWidget", "dict", "string", "dict"),
        "object": TypeInfo("QLabel", "text", "string", "object")
    }
    
    widget_dict = {
        "qslider": TypeInfo("QSlider", "value", "number", "slider"),
        "qlineedit": TypeInfo("QLineEdit", "text", "string", "lineedit"),
        "qpushbutton": TypeInfo("QPushButton", "text", "", ""),
        "qcombobox": TypeInfo("QComboBox", "currentIndex", "number", "combo"),
        "qradiobutton": TypeInfo("QRadioButton", "checked", "bool", "radio"),
        "qcheckbox": TypeInfo("QCheckBox", "checked", "bool", "bool"),
        "qspinbox": TypeInfo("QSpinBox", "value", "number", "int"),
        "qdoublespinbox": TypeInfo("QDoubleSpinBox", "value", "double", "double"),
        "qcommandlinkbutton": TypeInfo("QCommandLinkButton", "", "", ""),
        "qbuttonbox": TypeInfo("QButtonBox", "", "", ""),
        "qlistview": TypeInfo("QListView", "", "", ""),
        "qtreeview": TypeInfo("QTreeView", "", "", ""),
        "qtableview": TypeInfo("QTableView", "", "", ""),
        "qgroupbox": TypeInfo("QGroupBox", "", "", ""),
        "qtabwidget": TypeInfo("qtabwidget", "", "", ""),
        "qfontcombobox": TypeInfo("QFontComboBox", "", "", ""),
        "qplaintextedit": TypeInfo("QPlainTextEdit", "", "", ""),
        "qdial": TypeInfo("QDial", "value", "number", "dial"),
        "qcalendarwidget": TypeInfo("QCalendarWidget", "", "", ""),
        "qlcdnumber": TypeInfo("QLCDNumber", "value", "double", "lcd"),
        "qprogressbar": TypeInfo("QProgressBar", "value", "number", "progressbar"),
        "qlabel": TypeInfo("QLabel", "text", "string", "label"),
        "multichoice": TypeInfo("QScrollArea", "multichoice", "checkbox", "multichoice"),
        "qlistwidget": TypeInfo("QListWidget", "list", "string", "list"),
        "list": TypeInfo("QListWidget", "list", "string", "list"),
        "table" : TypeInfo("QTableWidget", "dict", "string", "dict"),
        "qtablewidget" : TypeInfo("QTableWidget", "dict", "string", "dict"),
        "object": TypeInfo("QLabel", "text", "string", "object"),
        "date": TypeInfo("QDateEdit", "date", "date", "date"),
        "time": TypeInfo("QTimeEdit", "time", "time", "time"),
        "datetime": TypeInfo("QDateTimeEdit", "datetime", "datetime", "datetime"),
        "qdate": TypeInfo("QDateEdit", "date", "date", "date"),
        "qtime": TypeInfo("QTimeEdit", "time", "time", "time"),
        "qdatetime": TypeInfo("QDateTimeEdit", "datetime", "datetime", "datetime"),
        "simplegrid" : TypeInfo("QTableWidget", "simplegrid", "list", "simplegrid"),        
    }
    
    script_location = Path(__file__).absolute().parent
    __group_widgets = {}
    
    def __init__(self):
        pass
        
    @classmethod
    def create_gui(cls, obj, overwrite = True):
        template_file_name = cls.create_new_template_file(obj)        
        form = FormLayoutDialogController(obj, template_file_name, overwrite)
        return form
    
    @classmethod
    def create_new_template_file(cls, obj):
        cls.__connections = ""

        object_name = obj.__class__.__name__
        template_file_name = f"{object_name}.ui"
        file=open(f"{VPyGUIGenerator.script_location}/templates/formLayoutTemplate.ui","r")
        content = file.read()        
        file.close()
        
        content = content.replace("__title__", object_name)
        
        widgets = cls.create_widgets(obj)
        
        content = content.replace("__content__", widgets)
        content = content.replace("__connections__", cls.__connections)
        
        template_file = open( template_file_name, 'w' )
        template_file.write( content )
        template_file.close()
        return template_file_name
    
    @classmethod
    def create_widgets(cls, obj):
        cls.__group_widgets = {}

        widgets = ""
        file=open(f"{VPyGUIGenerator.script_location}/templates/widgets_temaple.ui","r")
        widget_template = file.read()        
        file.close()
        class_prefix = F"_{obj.__class__.__name__}__"
        row = 0
        # collect public fields 
        for k,v in obj.__dict__.items():
            if k.startswith(class_prefix) or k == "v_id":
                continue
           
            field_type = type(v).__name__
            widget_info = cls.type_dict.get(field_type, None)
            new_widget = ""
            if(widget_info != None):
                new_widget = cls.create_standard_widgets(widget_template, row, widget_info, k)
            else:
                widget_info = cls.type_dict.get("object", None)
                new_widget = cls.create_standard_widgets(widget_template, row, widget_info, k)
                
            new_widget = new_widget.replace("__content__", widget_info.get_content(getattr(obj, k)))            
            
            widgets += new_widget
            row += 1
        # collect properties
        property_dict = (dict(obj.__class__.__dict__))
        
        for k, v in property_dict.items():
            if type(v) != property:
                continue
            if v.fset != None:
                if len(v.fset.__annotations__) > 0:
                    an  = v.fset.__annotations__
                    mydict = {}
                    for kk, vv in an.items():
                        newValue = vv.replace("::", "$%^")
                        mydict = dict((k1.strip(), v1.strip()) for k1,v1 in 
                                      (item.split(':') for item in newValue.split(',')))
                        for k2,v2 in mydict.items():
                            if "$%^" in v2:
                                mydict[k2] = v2.replace("$%^", "::")
                                
                        if mydict["widget"].lower() == "simplegrid":
                            value = getattr(obj, k)
                            if len(value) == 0:
                                continue

                            sample_type = type(value[0])
                            for o in value:
                                if type(o) != sample_type:
                                    raise TypeError("All objects inside list must have same type")
                            mydict["columns"] = cls.get_grid_columns(value[0])
                        widget_info = cls.widget_dict[mydict["widget"].lower()]
                        tmp_row = "__row__" if  "group" in mydict else row
                        new_widget = cls.create_custom_widgets(mydict, widget_info, widget_template, tmp_row, k)
            elif property_dict[v].fget != None:
                pass

            value = ""
            try:
                value = getattr(obj, k)
            except:
                if (widget_info.tag_name == "number" or widget_info.tag_name == "double") and value == '':
                     value = 0
                elif widget_info.tag_name == "bool" and value == '':
                    value = "false"
                else:
                    value = ""
            
            new_widget = new_widget.replace("__content__", widget_info.get_content(value))
            new_widget = new_widget.replace("__value__", str(value))
            
            if mydict["widget"].lower() == "simplegrid":
                import math
                page_count = math.ceil(len(value) / 10)
                new_widget = new_widget.replace("__page_count__", str(page_count))
                new_widget = new_widget.replace("__maximum__", str(page_count))

            
            connection = widget_info.get_connection(k)
            if connection != None:
                cls.__connections += connection
            if "group" in mydict:
                group_name = mydict["group"]
                if group_name not in cls.__group_widgets:
                    cls.__group_widgets[group_name] = []
                cls.__group_widgets[group_name].append(new_widget)
            else:
                widgets += new_widget
                row += 1

        if len(cls.__group_widgets) > 0:
            groups = cls.add_group_to_form(row)
            widgets += groups
        
            
            
        return widgets

    @classmethod
    def create_custom_widgets(cls, property_dict, widget_info, widget_template, row, name):
        
        if "widget" not in property_dict or property_dict["widget"].lower() not in cls.widget_dict:
            raise TypeError(f"Invalid widget for property '{name}'")
        widget_info.set_properties(property_dict)
        new_widget = widget_template.replace("__row__", str(row))
        new_widget = new_widget.replace("__label__", name.capitalize())
        new_widget = new_widget.replace("__widget__", widget_info.widget_name)        
        
        new_widget = new_widget.replace("__key__", widget_info.key)
        new_widget = new_widget.replace("__prefix__", widget_info.get_prefix())
        new_widget = new_widget.replace("__postfix__", widget_info.get_postfix())
        new_widget = new_widget.replace("__properties__", widget_info.get_properties())
        new_widget = new_widget.replace("__name__", name)
        if widget_info.prop_name != None:
            new_widget = new_widget.replace("__prop_name__", widget_info.prop_name)
        return new_widget
        
    @classmethod
    def create_standard_widgets (cls, widget_template, row, widget_info, name):
        new_widget = widget_template.replace("__row__", str(row))
        new_widget = new_widget.replace("__label__", name.capitalize())
        new_widget = new_widget.replace("__widget__", widget_info.widget_name)
        
        new_widget = new_widget.replace("__key__", widget_info.key)
        new_widget = new_widget.replace("__prop_name__", widget_info.prop_name)
        new_widget = new_widget.replace("__prefix__", widget_info.get_prefix())
        new_widget = new_widget.replace("__postfix__", widget_info.get_postfix())
        new_widget = new_widget.replace("__properties__", widget_info.get_properties())
        new_widget = new_widget.replace("__name__", name)
        return new_widget
    
    @classmethod
    def get_grid_columns(cls, obj):
        columns = []
        class_prefix = F"_{obj.__class__.__name__}__"
        
        for k,v in obj.__dict__.items():
            if not k.startswith(class_prefix):
                columns.append(k)
                
        property_dict = (dict(obj.__class__.__dict__))
        for k, v in property_dict.items():
            if type(v) != property:
                continue
            if v.fset != None:
                if len(v.fset.__annotations__) > 0:
                    columns.append(k)

        return columns
    
    @classmethod    
    def add_group_to_form(cls, row):
        result = ""
        file=open(f"{VPyGUIGenerator.script_location}/templates/tab_widget_tamplate.ui","r")
        result = file.read()        
        file.close()
        result = result.replace("__tab_row__", str(row))
        
        file=open(f"{VPyGUIGenerator.script_location}/templates/tab_child_template.ui","r")
        tab_template = file.read()        
        file.close()
        
        tabs = ""
        for k, widgets in cls.__group_widgets.items():
            tab = tab_template.replace("__name__", k)
            row = 0
            content = ""
            for w in widgets:
                w = w.replace("__row__", str(row))
                content += w
                row += 1
            tab = tab.replace("__content__", content)
            tabs += tab
        
        result = result.replace("__tabs__", tabs)
        return result

        
        