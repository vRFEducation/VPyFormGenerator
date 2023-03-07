from .TypeInfo import TypeInfo
from .FormLayoutDialogController import FormLayoutDialogController
from pathlib import Path

class VPyGUIGenerator:
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
    script_location = Path(__file__).absolute().parent
    def __init__(self):
        pass
    @classmethod
    def create_gui(cls, obj):
        template_file_name = cls.create_new_template_file(obj)
        
        form = FormLayoutDialogController(obj, template_file_name)
        return form
    
    @classmethod
    def create_new_template_file(cls, obj):
        object_name = obj.__class__.__name__
        template_file_name = f"{object_name}.ui"
        file=open(f"{VPyGUIGenerator.script_location}/templates/formLayoutTemplate.ui","r")
        content = file.read()        
        file.close()
        
        content = content.replace("__title__", object_name)
        # content = content.replace("__width__", "400")
        # content = content.replace("__height__", "300")
        
        widgets = cls.create_widgets(obj)
        
        content = content.replace("__content__", widgets)
        
        template_file = open( template_file_name, 'w' )
        template_file.write( content )
        template_file.close()
        return template_file_name
    
    @classmethod
    def create_widgets(cls, obj):
        widgets = ""
        file=open(f"{VPyGUIGenerator.script_location}/templates/widgets_temaple.ui","r")
        widget_template = file.read()        
        file.close()
        class_prefix = F"_{obj.__class__.__name__}__"
        row = 0
        for k,v in obj.__dict__.items():
            if k.startswith(class_prefix):
                continue
           
            field_type = type(v).__name__
            widget_info = cls.get_widget_for_type(field_type)
            new_widget = ""
            if(widget_info != None):
                new_widget = cls.create_standard_widgets(widget_template, row, widget_info, k)
            else:
                widget_info = cls.get_widget_for_type("object")
                new_widget = cls.create_standard_widgets(widget_template, row, widget_info, k)
                
            new_widget = new_widget.replace("__content__", widget_info.get_content(getattr(obj, k)))            

            

            
            widgets += new_widget
            row += 1
            # print(new_widget)
        # for k,v in obj.__class__.__dict__.items():
        #     print(type(v).__name__)
        #     if(issubclass(type(v), property)):
        #         print(getattr(obj, k))
        return widgets
    
    
    @classmethod
    def get_widget_for_type(cls, type):
        # print(type)
        return cls.type_dict.get(type, None)

    @classmethod
    def create_standard_widgets(cls, widget_template, row, widget_info, name):
        new_widget = widget_template.replace("__row__", str(row))
        new_widget = new_widget.replace("__label__", name.capitalize())
        new_widget = new_widget.replace("__widget__", widget_info.widget_name)
        
        new_widget = new_widget.replace("__key__", widget_info.key)
        new_widget = new_widget.replace("__prop_name__", widget_info.prop_name)
        new_widget = new_widget.replace("__prefix__", widget_info.get_prefix())
        new_widget = new_widget.replace("__postfix__", widget_info.get_postfix())
        new_widget = new_widget.replace("__name__", name)
        return new_widget
        
        
