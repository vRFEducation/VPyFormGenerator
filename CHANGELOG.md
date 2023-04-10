# Changelog

## v0.1.0

### Added or Changed
- Create simple UI based on field(s) inside classes
- Simple types such as int, bool, double, string supported via appropriate widgets
- Some complex types such as lists and dictionaries also supported
    - Widgets to manipulate lists and dictionaries also added automatically
- time, date and datetime also support in this version
- Objects inside other objects also support and user can view/edit inner objects in seperate dialog
- 2-way bindings supported and changes applied automatically to source object


## v0.2.0

### Added or Changed
- Support for properties added 
- Widgets can be customized via annotation of setter in property
- Predefined widgets for types can changed based on developer opinion
    - QDial, QSlider, QProgressBar, QLabel, QCheckBox, QComboBox supported
    - A value label also attached to QSlider and QDial for display current value
- MultiChoice widget added 
    - End user can select 1 item from a set of options(QRadioButton List)
    - End user can select multiple items from a set of options(QCheckBox List)
    - Orientation can be customized 
    - ScrollBar will be added automatically
- Developers can hide/show tools section of List and Table items in previous version
- 2-way bindings supported and changes applied automatically to source object

## v0.3.0

### Added or Changed
- Support for DateTime, Date, Time added to properties
- Object presentation via label and detail button added to properties
- minimumSize, maximumSize and geometry properties supported(with specific value notation)
- Filtering add to list and table used for dictionaties
- Grid widget added to library in order to show list of objects in grid format
    - Pagination added to grid
    - change number of rows in grid added

## v0.3.0

### Added or Changed
- CRUD operations support completely in SimpleGrid
- Clear All option added to list and table
- Icons added to add, detele, edit and new buttons for better look and feel
