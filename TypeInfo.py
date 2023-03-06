from datetime import datetime, date, time
import time
from pathlib import Path

class TypeInfo:
    script_location = Path(__file__).absolute().parent
    scalar_type = ["str", "int", "float", "bool", "time", "date", "object"]
    
    def __init__(self, widget_name, prop_name, tag_name, key ):
        self.widget_name = widget_name
        self.prop_name = prop_name
        self.tag_name = tag_name
        self.key = key
        
    def get_content(self, value):
        field_type = type(value).__name__ 
        
        content = f"""
        <property name="{self.prop_name}">
            <{self.tag_name}>__value__</{self.tag_name}>
        </property>
        """
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
        
        if self.key == "list":
            file_name = f"{TypeInfo.script_location}/list_widget_extra_prefix.ui"
        elif self.key == "object":
            file_name = f"{TypeInfo.script_location}/object_extra_prefix.ui"
        elif self.key == "dict":
            file_name = f"{TypeInfo.script_location}/table_widget_extra_prefix.ui"
        else:
            return ""
        file=open(file_name,"r")
        prefix = file.read()        
        file.close()

        
        return prefix
    
    def get_postfix(self):
        postfix =  ""
        file_name = ""
        if self.key == "list":
            file_name = f"{TypeInfo.script_location}/list_widget_extra_postfix.ui"
        elif self.key == "object":
            file_name = f"{TypeInfo.script_location}/object_extra_postfix.ui"
        elif self.key == "dict":
            file_name = f"{TypeInfo.script_location}/table_widget_extra_postfix.ui"
        else:
            return ""
        file=open(file_name,"r")
        postfix = file.read()        
        file.close()
        
        return postfix
            
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
            

