from datetime import datetime, date, time
import time
from pathlib import Path

class TypeInfo:
    script_location = Path(__file__).absolute().parent
    scalar_type = ["str", "int", "float", "bool", "time", "date", "object"]
    
    def __init__(self, widget_name, prop_name, tag_name, key):
        self.widget_name = widget_name
        self.prop_name = prop_name
        self.tag_name = tag_name
        self.key = key
        self.properties = ""
        self.extra_data = {}
        
    def get_content(self, value):
        if self.prop_name == None:
            return ""
        field_type = type(value).__name__ 
        
        content = f"""
        <property name="{self.prop_name}">
            <{self.tag_name}>__value__</{self.tag_name}>
        </property>
        """
      

        if self.widget_name == "QComboBox" and "combo_items" in self.extra_data.keys():
            index = -1
            if value in self.extra_data["combo_items"]:
                index = self.extra_data["combo_items"].index(value)
            content = content.replace("__value__", str(index))
        elif self.key == "multichoice":
            if len(self.extra_data["items"]) > 0:
                orientation = "QVBoxLayout"
                if "orientation" in self.extra_data:
                    orientation = self.extra_data["orientation"]
                wType = "QCheckBox"
                if "type" in self.extra_data:
                    wType = self.extra_data["type"]
                    
                content = f"""
                  <widget class="QWidget" name="scrollAreaWidgetContents">
                    <layout class="{orientation}" name="Layout">
                    """
                for item in self.extra_data["items"]:
                    status = "false"
                    if wType == "QRadioButton":
                        status = "true" if item == value else "false"
                    elif wType == "QCheckBox":
                        status = "true" if item in value else "false"
                        
                    content += f"""
                        <item>
                            <widget class="{wType}" name="option_{item}">
                                <property name="text">
                                    <string>{item}</string>
                                </property>
                                <property name="checked">
                                    <bool>{status}</bool>
                                </property>
                            </widget>
                        </item>                 
                        """   
                content += """
                    </layout>
                </widget>
                """
        elif self.key == "images":
            content = """
             <property name="widgetResizable">
                <bool>true</bool>
            </property>
            <widget class="QWidget" name="scrollAreaWidgetContents___name__">
                <property name="styleSheet">
                    <string notr="true">QLabel:hover{background-color: rgb(188, 232, 255);}</string>
                </property>
                <layout class="QHBoxLayout" name="hLayout___name__"> 
                </layout>
            </widget>
            """
        elif self.key == "simplegrid":
            content = self.create_simple_grid(value)
        else:            
            if field_type in TypeInfo.scalar_type:
                if field_type == "bool":
                    content = content.replace("__value__", str(value).lower())
                elif field_type == "time":
                    content = content.replace("__value__", TypeInfo.create_time_value(value))
                elif field_type == "date":
                    content = content.replace("__value__", TypeInfo.create_date_value(value))
                else:
                    content = content.replace("__value__", str(value))
            else:
                content = content.replace("__value__", str(value))

            
            if field_type == "datetime":
                content = TypeInfo.create_datetime_value(value)
            elif field_type == "list":
                content = TypeInfo.create_list_value(value)
            elif field_type == "dict":
                content = TypeInfo.create_dict_value(value)
                
        return content

    def get_prefix(self):
        prefix =  ""
        file_name = ""
        
        if self.key == "list" and ("showTools" not in self.extra_data or self.extra_data["showTools"] == "true"):
            file_name = f"{TypeInfo.script_location}/templates/list_widget_extra_prefix.ui"
        elif self.key == "object":
            file_name = f"{TypeInfo.script_location}/templates/object_extra_prefix.ui"
        elif self.key == "file":
            file_name = f"{TypeInfo.script_location}/templates/file_widget_extra_prefix.ui"
        elif self.key == "image":
            file_name = f"{TypeInfo.script_location}/templates/image_widget_extra_prefix.ui"
        elif self.key == "images":
            file_name = f"{TypeInfo.script_location}/templates/images_widget_extra_prefix.ui"
        elif self.key == "dict" and ("showTools" not in self.extra_data or self.extra_data["showTools"] == "true"):
            file_name = f"{TypeInfo.script_location}/templates/table_widget_extra_prefix.ui"
        elif self.key == "slider" and "showLabel" in self.extra_data:
            file_name = f"{TypeInfo.script_location}/templates/slider_widget_extra_prefix.ui"
        elif self.key == "dial" and "showLabel" in self.extra_data:
            file_name = f"{TypeInfo.script_location}/templates/dial_widget_extra_prefix.ui"
        elif self.key == "simplegrid" and "showPaginator" in self.extra_data:
            file_name = f"{TypeInfo.script_location}/templates/simple_grid_extra_prefix.ui"
        else:
            return ""
        file=open(file_name,"r")
        prefix = file.read()        
        file.close()

        
        return prefix
    
    def get_postfix(self):
        postfix =  ""
        file_name = ""
        if self.key == "list" and ("showTools" not in self.extra_data or self.extra_data["showTools"] == "true"):
            file_name = f"{TypeInfo.script_location}/templates/list_widget_extra_postfix.ui"
        elif self.key == "object":
            file_name = f"{TypeInfo.script_location}/templates/object_extra_postfix.ui"
        elif self.key == "file":
            file_name = f"{TypeInfo.script_location}/templates/file_widget_extra_postfix.ui"
        elif self.key == "image":
            file_name = f"{TypeInfo.script_location}/templates/image_widget_extra_postfix.ui"
        elif self.key == "images":
            file_name = f"{TypeInfo.script_location}/templates/images_widget_extra_postfix.ui"
        elif self.key == "dict" and ("showTools" not in self.extra_data or self.extra_data["showTools"] == "true"):
            file_name = f"{TypeInfo.script_location}/templates/table_widget_extra_postfix.ui"
        elif self.key == "slider" and "showLabel" in self.extra_data:
            file_name = f"{TypeInfo.script_location}/templates/slider_widget_extra_postfix.ui"
        elif self.key == "dial" and "showLabel" in self.extra_data:
            file_name = f"{TypeInfo.script_location}/templates/dial_widget_extra_postfix.ui"
        elif self.key == "simplegrid" and "showPaginator" in self.extra_data:
            file_name = f"{TypeInfo.script_location}/templates/simple_grid_extra_postfix.ui"
        else:
            return ""
        file=open(file_name,"r")
        postfix = file.read()        
        file.close()
        
        return postfix
    
    def set_properties(self, proprty_dict):
        
        self.properties = ""
        widget = ""
        for k, v in proprty_dict.items():
            self.extra_data[k] = v
            originalKey = k;
            k = k.lower()
            if k == "widget":
                widget = v.lower()
                continue    #it handled before
            if k == "combo_items":
                items = v.replace("[", "").replace("]", "").split(";")    
                for item in items:
                    self.properties += f"""            
                        <item>
                            <property name="text">
                                <string>{item}</string>
                            </property>
                        </item>
                    """
                self.extra_data["combo_items"] = items
            elif k == "maximumsize" or k == "minimumsize":
                size = v.replace("[", "").replace("]", "").split(";")  
                self.properties += f"""
                <property name="{originalKey}">
                    <size>
                    <width>{size[0]}</width>
                    <height>{size[1]}</height>
                    </size>
                </property>
                """
            elif k == "geometry":
                size = v.replace("[", "").replace("]", "").split(";")  
                self.properties += f"""
                <property name="geometry">
                    <rect>
                    <x>{size[0]}</x>
                    <y>{size[1]}</y>
                    <width>{size[2]}</width>
                    <height>{size[3]}</height>
                    </rect>
                </property>
                """
            elif widget == "multichoice":
                if k == "items":
                    items = v.replace("[", "").replace("]", "").split(";") 
                    self.extra_data["items"] = items
                elif k == "orientation":
                    self.extra_data[k] = "QVBoxLayout" if v.lower() == "vertical" else "QHBoxLayout"
                elif k == "type":
                    self.extra_data[k] = v
            elif (widget == "qslider" or widget == "qdial") and k == "showlabel":
                self.extra_data[originalKey] = v
            elif widget == "simplegrid":
                if k == "showfiltering":
                     self.properties += f"""
                        <property name="{originalKey}" stdset="0">
                            <string>{v}</string>
                        </property>
                        """
                elif k == "columns":
                    self.properties += f"""            
                        <property name="grid_columns" stdset="0">
                            <string>{','.join(v)}</string>
                        </property>
                    """
            else:
                tag = "string"
                if v.isnumeric():
                    tag = "number"
                elif v.lower() == "true" or v.lower() == "false":
                    tag = "bool"
                elif "::" in v.lower(): 
                    tag = "enum"
                            
                self.properties += f"""            
                    <property name="{originalKey}" stdset="0">
                        <{tag}>{v}</{tag}>
                    </property>
                """

        
    
    def get_properties(self):
        return self.properties
            
    @staticmethod
    def create_dict_value(d: dict):
        dict_value = """
            <property name="alternatingRowColors">
                <bool>true</bool>
            </property>
            <attribute name="horizontalHeaderStretchLastSection">
                <bool>true</bool>
            </attribute>
        """
        for i in range(len(d)):
            dict_value += f"""
                <row>
                    <property name="text">
                        <string>{i + 1}</string>
                    </property>
                </row>
            """
        dict_value += """
            <column>
                <property name="text">
                <string>Key</string>
                </property>
            </column>
            <column>
                <property name="text">
                <string>Value</string>
                </property>
            </column>
        """
        row = 0
        for k, v in d.items():
            dict_value += f"""
                <item row="{row}" column="0">
                    <property name="text">
                    <string>{k}</string>
                    </property>
                </item>
                <item row="{row}" column="1">
                    <property name="text">
                    <string>{v}</string>
                    </property>
                </item>
            """
            row += 1
            
        return dict_value
        
        
    @staticmethod
    def create_list_value(lst: list):
        list_value = ""
        for item in lst:
            list_value += f"""
            <item>
                <property name="text">
                <string>{item}</string>
                </property>
                <property name="flags">
                    <set>ItemIsSelectable|ItemIsEditable|ItemIsDragEnabled|ItemIsUserCheckable|ItemIsEnabled</set>
                </property>
            </item>
            """
            
        return list_value
        
    @staticmethod
    def create_time_value(t: time):
        return f"""
        <hour>{t.hour}</hour>
        <minute>{t.minute}</minute>
        <second>{t.second}</second>
        """

    @staticmethod
    def create_date_value(d: date):
        return f"""
            <year>{d.year}</year>
            <month>{d.month}</month>
            <day>{d.day}</day>
        """

    @staticmethod
    def create_datetime_value(dt: datetime):
        return f"""
        <property name="time">
            <time>
                <hour>{dt.hour}</hour>
                <minute>{dt.minute}</minute>
                <second>{dt.second}</second>
            </time>
        </property>
        <property name="date">
            <date>
                <year>{dt.year}</year>
                <month>{dt.month}</month>
                <day>{dt.day}</day>
            </date>
        </property>
        """
    
    def get_connection(self, name):
        
        file_name = f"{TypeInfo.script_location}/templates/connection_template.ui"
        file=open(file_name,"r")
        connection = file.read()        
        file.close()
        if (self.key == "slider" or self.key == "dial")and "showLabel" in self.extra_data:
            if self.extra_data["showLabel"] == "true":
                connection = connection.replace("__source__", name)
                connection = connection.replace("__signal__", "valueChanged(int)")
                connection = connection.replace("__destination__", f"label_{name}")
                connection = connection.replace("__slot__", "setNum(int)")
                return connection
        return None
    
    def create_simple_grid(self, object_list):

        count = len(object_list) if "showPaginator" not in self.extra_data else min(10, len(object_list))
        is_paginated = "true" if "showPaginator"  in self.extra_data and self.extra_data["showPaginator"] == "true" else "false"
        content = f"""
        <property name="alternatingRowColors">
            <bool>true</bool>
        </property>
        <property name="current_page" stdset="0">
            <string>1</string>
          </property>
        <property name="row_per_page" stdset="0">
            <string>10</string>
        </property>
        <property name="page_count" stdset="0">
            <string>__page_count__</string>
          </property>
        <property name="is_paginated" stdset="0">
            <string>{is_paginated}</string>
          </property>
        
        """
        for col in self.extra_data["columns"]:
            content += f"""
                <column>
                    <property name="text">
                        <string>{col.capitalize()}</string>
                    </property>
                </column>
            """
        content += f"""
                <column>
                    <property name="text">
                        <string>Actions</string>
                    </property>
                </column>
            """
        return content