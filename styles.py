STYLES = {
    "main_window": """
        QMainWindow {
            background-color: #f5f5f5;
        }
    """,
    
    "button": """
        QPushButton {
            background-color: #4a86e8;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #3a76d8;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
    """,
    
    "menu_button": """
        QPushButton {
            background-color: #6aa84f;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #5a984f;
        }
    """,
    
    "status_bar": """
        QStatusBar {
            background-color: #e8e8e8;
            color: #333333;
            padding: 5px;
        }
    """,
    
    "group_box": """
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
    """
}