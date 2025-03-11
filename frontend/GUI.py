from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout,QPushButton, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

env_vars= dotenv_values(".env")
ASSISTANT_NAME= env_vars.get("ASSISTANT")
current_dir= os.getcwd()
old_chat_message=""
temp_dir_path= rf"{current_dir}/frontend/Files"
graphics_dir_path= rf"{current_dir}/frontend/Graphics"

def answer_modifier(answer):
    lines= answer.split('\n')
    non_empty_lines= [line for line in lines if line.strip()]
    modified_answer="\n".join(non_empty_lines)
    return modified_answer

def query_modifier(query):
    new_query = query.lower().strip()
    query_words= new_query.split()
    question_words=["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]

    if any(word+" " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query= new_query[:-1]+"?"
        else:
            new_query +="?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query= new_query[:-1]+"."
        else:
            new_query +="."
    
    return new_query.capitalize()

def set_microphone_status(command):
    with open(rf'{temp_dir_path}/Mic.data','w', encoding='utf-8') as file:
        file.write(command)

def get_microphone_status():
    with open(rf'{temp_dir_path}/Mic.data','r', encoding='utf-8') as file:
        status=file.read()
    return status

def set_assistant_status(status):
    with open(rf'{temp_dir_path}/Status.data','w',encoding='utf-8') as file:
        file.write(status)

def get_assistant_status():
    with open(rf'{temp_dir_path}/Status.data','r',encoding='utf-8') as file:
        status=file.read()
    return status

def mic_button_initialised():
    set_microphone_status("True")

def mic_button_closed():
    set_microphone_status("False")

def graphics_directory_path(filename):
    path= rf'{graphics_dir_path}/{filename}'
    return path

def temp_directory_path(filename):
    path= rf'{temp_dir_path}/{filename}'
    return path

def show_text_to_screen(text):
    with open(rf'{temp_dir_path}/Responses.data','w', encoding='utf-8') as file:
        file.write(text)

class ChatSection(QWidget):

    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-100)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        
        # Ensure the stylesheet is valid
        self.setStyleSheet("background-color: black;")  # Valid background color
        
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")  # Ensure this is valid
        movie= QMovie(graphics_directory_path('assistant.gif'))
        max_gif_size_W= 480
        max_gif_size_H= 270
        movie.setScaledSize(QSize(max_gif_size_W,max_gif_size_H))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)
        self.label= QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-right: 195px; border: none; margin-top: -30px;")  # Corrected '16x' to '16px'
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        layout.setSpacing(-10)
        layout.addWidget(self.gif_label)
        font= QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.load_messages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
            QScrollBar: vertical {
            border: white;
            background: black;  
            width: 5px;     
            margin: 0px 0px 0px 0px;   
            border-radius: 5px;         
            }
        """)
    def load_messages(self):
        global old_chat_message

        with open(temp_directory_path('Responses.data'), "r", encoding='utf-8') as file:
            messages= file.read()

            if None==messages:
                pass
            elif len(messages)<=1:
                pass
            elif str(old_chat_message)==str(messages):
                pass
            else:
                self.add_message(message=messages, color='White')
                old_chat_message=messages
    def SpeechRecogText(self):
        with open(temp_directory_path('Status.data'),"r", encoding='utf-8') as file:
            messages=file.read()
            self.label.setText(messages)
    
    def load_icon(self, path, width=60, height=60):
        pixmap= QPixmap(path)
        new_pixmap=pixmap.scaled(width,height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if not self.toggled:
            self.load_icon(graphics_directory_path('mic_on.png'), 60, 60)
            mic_button_initialised()
        else:
            self.load_icon(graphics_directory_path('mic_off.png'), 60, 60)
            mic_button_closed()
        
        self.toggled = not self.toggled

    def add_message(self, message, color):
        cursor= self.chat_text_edit.textCursor()
        format= QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message+"\n")
        self.chat_text_edit.setTextCursor(cursor)

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop=QApplication.desktop()
        screen_width=desktop.screenGeometry().width()
        screen_height=desktop.screenGeometry().height()
        content_layout=QVBoxLayout()
        content_layout.setContentsMargins(0,0,0,0)
        gif_label= QLabel()
        movie= QMovie(graphics_directory_path('assistant.gif'))
        gif_label.setMovie(movie)
        max_gif_size_H= int(screen_width/16*9)
        movie.setScaledSize(QSize(screen_width,max_gif_size_H))
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.icon_label=QLabel()
        pixmap=QPixmap(graphics_directory_path('mic_on.png'))
        new_pixmap=pixmap.scaled(60,60)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(150,150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled=True
        self.toggle_icon()
        self.icon_label.mousePressEvent=self.toggle_icon
        self.label=QLabel("")
        self.label.setStyleSheet("color: white; font-size: 16px; margin-bottom: 0;")
        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment= Qt.AlignCenter)
        content_layout.setContentsMargins(0,0,0,150)
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")
        self.timer= QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
    
    def SpeechRecogText(self):
        with open(temp_directory_path("Status.data"),"r", encoding='utf-8') as file:
            messages= file.read()
            self.label.setText(messages)
    
    def load_icon(self, path, width=60, height=60):
        pixmap= QPixmap(path)
        new_pixmap = pixmap.scaled(width,height)
        self.icon_label.setPixmap(new_pixmap)
    
    def toggle_icon(self, event=None):
        if not self.toggled:
            self.load_icon(graphics_directory_path('mic_on.png'), 60, 60)
            mic_button_initialised()
        else:
            self.load_icon(graphics_directory_path('mic_off.png'), 60, 60)
            mic_button_closed()
        
        self.toggled = not self.toggled

class MessageScreen(QWidget):

    def __init__(self,parent= None):
        super().__init__(parent)
        desktop=QApplication.desktop()
        screen_width=desktop.screenGeometry().width()
        screen_height= desktop.screenGeometry().height()
        layout= QVBoxLayout()
        label= QLabel("")
        layout.addWidget(label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)

class CustomTopBar(QWidget):

    def __init__(self,parent,stacked_widget):
        super().__init__(parent)
        self.initUI()
        self.current_screen=None
        self.stacked_widget= stacked_widget

    def initUI(self):
        self.setFixedHeight(50)
        layout=QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        home_button= QPushButton()
        home_icon=QIcon(graphics_directory_path("home.png"))
        home_button.setIcon(home_icon)
        message_button= QPushButton()
        message_icon= QIcon(graphics_directory_path("Chats.png"))
        message_button.setIcon(message_icon)
        minimize_button=QPushButton()
        minimize_icon= QIcon(graphics_directory_path('minimize2.png'))
        minimize_button.setIcon(minimize_icon)
        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(graphics_directory_path('maximize.png'))
        self.restore_icon= QIcon(graphics_directory_path('minimize.png'))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        close_button = QPushButton()
        close_icon= QIcon(graphics_directory_path('close.png'))
        close_button.setIcon(close_icon)
        line_frame= QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color: black;")
        title_label=QLabel(f"{str(ASSISTANT_NAME).capitalize()}")
        title_label.setStyleSheet("""
            color: black; 
            font-size: 18px; 
            background-color: white; 
            padding: 5px;  /* Add padding for better spacing */
            border-radius: 5px;  /* Rounded corners */
            """)
        button_width = 50  # Set a fixed width of 50 pixels for buttons
        home_button.setFixedWidth(button_width)
        message_button.setFixedWidth(button_width)
        minimize_button.setFixedWidth(button_width)
        self.maximize_button.setFixedWidth(button_width)
        close_button.setFixedWidth(button_width)
        home_button.setStyleSheet("height: 100px; line-height: 100px; border-radius: 5px; background-color: white; color:black;")
        message_button.setStyleSheet("height: 100px; line-height: 100px; border-radius: 5px; background-color: white; color: black;")
        minimize_button.setStyleSheet("height: 100px; line-height: 100px; border-radius: 5px; background-color: white;")
        self.maximize_button.setStyleSheet("height: 100px; line-height: 100px; border-radius: 5px; background-color: white;")
        close_button.setStyleSheet("height: 100px; line-height: 100px; border-radius: 5px; background-color: white;")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        minimize_button.clicked.connect(self.minimize_window)
        self.maximize_button.clicked.connect(self.maximize_window)
        close_button.clicked.connect(self.close_window)
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)
        self.draggable= True
        self.offset=None

    def paint_event(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimize_window(self):
        self.parent().showMinimized()
    
    def maximize_window(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.restore_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.maximize_icon)
    
    def close_window(self):
        self.parent().close()

    def mouse_press_event(self, event):
        if self.draggable:
            self.offset=event.pos()
    
    def mouse_move_event(self,event):
        if self.draggable and self.offset:
            new_pos = event.globalPos()-self.offset
            self.parent().move(new_pos)
    
    def show_message_screen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        message_screen=MessageScreen(self)
        layout=self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen=message_screen
    
    def show_initial_screen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        
        initial_screen=InitialScreen(self)
        layout=self.parent().layout()
        if layout is not None:
            layout.addWidget(initial_screen)
        self.current_screen=initial_screen

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        desktop=QApplication.desktop()
        screen_width=int(desktop.screenGeometry().width() * 0.5)  # Convert to int
        screen_height=int(desktop.screenGeometry().height() * 0.5)  # Convert to int
        stacked_widget=QStackedWidget(self)
        initial_screen= InitialScreen()
        message_screen=MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        self.setGeometry(0,0,screen_width, screen_height)
        self.setStyleSheet("background-color: black;")
        top_bar= CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

def graphical_user_interface():
        app=QApplication(sys.argv)
        window=MainWindow()
        window.show()
        sys.exit(app.exec())

if __name__=="__main__":
    graphical_user_interface()
