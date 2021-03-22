import math
import time
from multiprocessing.connection import Connection

import kivy
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.dropdown import DropDown
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.uix.widget import Widget

import os
import robots_everywhere.gui.user_info as user_info
import robots_everywhere.settings as settings
import robots_everywhere.gui.connection_info as ci

MAIN_KV_FILE = os.path.join(settings.PROJECT_ROOT_DIR, "robots_everywhere",
                            "gui", "motifact_main.kv")
kivy.require('2.0.0')
Window.size = (600, 800)

conversation = [None] * 100
level_backgrounds = [' ', os.path.join(settings.PROJECT_ROOT_DIR, "robots_everywhere", "gui", "graphics", "nature.jpg"),
                     os.path.join(settings.PROJECT_ROOT_DIR, "robots_everywhere", "gui", "graphics", "desert.jpg"),
                     os.path.join(settings.PROJECT_ROOT_DIR, "robots_everywhere", "gui", "graphics", "city.jpg")]
dynamic_elements = []

class MainScreen(Screen):
    chat_window = ObjectProperty(None)
    user_input = ObjectProperty(None)
    face = ObjectProperty(None)
    progressbar = ObjectProperty(None)
    level_display = ObjectProperty(None)
    send_button = ObjectProperty(None)
    message_type = "text_box"
    level = NumericProperty(1)
    background_image = StringProperty("")

    def add_text(self):
        # ensure that the right type of information is read from previous question
        if self.message_type == 'text_box':
            self.chat_window.send_message(self.user_input.getText())
            # send response trough output pipe
            ci.output_connection.send(self.user_input.getText())
            self.user_input.removeText()
        if self.message_type == 'slider':
            slider_value = self.user_input.getSliderValue()
            anim = Animation(happy=slider_value / 10)
            anim.start(self.face)
            self.chat_window.send_message(str(round(slider_value)))
            # send response trough output pipe
            ci.output_connection.send(slider_value)
        if self.message_type == 'multiple_choice':
            self.chat_window.send_message(self.user_input.getMS())
            # send response trough output pipe
            ci.output_connection.send(self.user_input.getMS())

        # disable send button until animation is done
        self.send_button.disabled = True

        # progressbar animation
        anim = Animation(progress=self.progressbar.progress + 1)
        anim.bind(on_complete=self.enable_button)
        anim.start(self.progressbar)

        # The progressbar is filled up and a new level has ben achieved
        if self.progressbar.progress >= self.progressbar.progress_full:
            self.level += 1
            self.level_display.text = str(self.level)
            anim = Animation(progress=0)
            anim.bind(on_complete=self.enable_button)
            anim.start(self.progressbar)
            self.background_image = level_backgrounds[self.level - 1]
            self.face.normal_color = (1, 1, 1)
            popup = NewLevelPopup()
            popup.current_level = self.level
            popup.open()

    def setup_message(self, message):
        if message[1] == 'text_box':
            self.user_input.addTextBox()
        elif message[1] == 'slider':
            self.user_input.addSlider()
        elif message[1] == 'multiple_choice':
            self.user_input.addMS()
        self.message_type = message[1]
        self.chat_window.send_message_computer(message[0])

    def blink(self, ms):
        anim = Animation(blink=0, duration=.1) + Animation(blink=1, duration=.1)
        anim.start(self.face)

    def bounce(self, ms):
        anim = Animation(offsety=-5, duration=2) + Animation(offsety=5, duration=2)
        anim.start(self.face)

    def follow_mouse(self, ms):
        # left eye
        deltaY = Window.mouse_pos[1] - self.face.center_both_y
        deltaX = Window.mouse_pos[0] - self.face.center_left_x
        angle = math.atan2(deltaY, deltaX) * 180 / math.pi
        self.face.mouse_angle_left = angle
        # right eye
        deltaY = Window.mouse_pos[1] - self.face.center_both_y
        deltaX = Window.mouse_pos[0] - self.face.center_right_x
        angle = math.atan2(deltaY, deltaX) * 180 / math.pi
        self.face.mouse_angle_right = angle

    def enable_button(self, anim, widget):
        self.send_button.disabled = False

    def print_text(self):
        print("hi")


class Input(BoxLayout):

    def addTextBox(self):
        self.clear_widgets()
        self.add_widget(UserTextInput())

    def getText(self):
        for child in self.children:
            return child.text

    def removeText(self):
        for child in self.children:
            child.text = ""

    def addSlider(self):
        self.clear_widgets()
        slider = UserSlider()
        label = SliderLabel()
        slider.addLabel(label)
        self.add_widget(label)
        self.add_widget(slider)

    def getSliderValue(self):
        for child in self.children:
            return child.value

    def addMS(self):
        self.clear_widgets()
        option1 = UserMSButton()
        option1.changeText('yes')
        option1.state = 'down'
        self.add_widget(option1)
        option2 = UserMSButton()
        option2.changeText('no')
        self.add_widget(option2)
        option3 = UserMSButton()
        option3.changeText('maybe')
        self.add_widget(option3)

    def getMS(self):
        for child in self.children:
            if child.state == 'down':
                return child.text


class UserTextInput(TextInput):
    pass


class UserSlider(Slider):
    slider_label = ObjectProperty(None)

    def addLabel(self, widget):
        self.slider_label = widget
        self.slider_label.text = str(round(self.value))

    def update_label(self):
        self.slider_label.text = str(round(self.value))


class SliderLabel(Label):
    pass


class UserMSButton(ToggleButton):

    def changeText(self, option_text):
        self.text = option_text
        self.group = 'choice'


class ChatWindow(BoxLayout):
    conversation_counter = 0

    def send_message(self, message):
        text_message = TextMessage()
        text_message.add_text(message)
        text_row = TextRow()
        text_row.add_widget(EmptyMessage())
        text_row.add_widget(text_message)
        self.add_widget(text_row)
        self.parent.scroll_to(text_row)

    def send_message_computer(self, message):
        text_message = TextMessage()
        text_message.add_text(message)
        self.add_widget(text_message)
        self.parent.scroll_to(text_message)

class TextRow(BoxLayout):
    pass


class TextMessage(Label):
    message = StringProperty(None)

    def fillName(self):
        if '[NAME]' in self.message:
            print("HI")
            self.message = self.message.replace("[NAME]", user_info.user_name)
            self.text = self.message

    def add_text(self, m):
        self.message = m
        print(self.message)
        self.text = self.message


class EmptyMessage(Label):
    pass


class ImageMessage(Label):

    def fillName(self):
        pass


class NewLevelPopup(Popup):
    pass


class SettingsScreen(Screen):
    pass


class ProfileScreen(Screen):
    pass


class Manager(ScreenManager):
    main_screen = ObjectProperty(None)

    def start(self, dt):
        pass
        # text_1 = TextMessage()
        # text_1.add_text("Hi there! My name is Motus! What is your name?")
        # dynamic_elements.append(text_1)
        # conversation[0] = ['text_box', text_1]
        # text_2 = TextMessage()
        # text_2.add_text("Nice to meet you [NAME]! What do you think of this awesome picture?")
        # dynamic_elements.append(text_2)
        # image = ImageMessage()
        # conversation[1] = ['text_box', text_2, image]
        # text_3 = TextMessage()
        # text_3.add_text("I think so to :)")
        # dynamic_elements.append(text_3)
        # text_4 = TextMessage()
        # text_4.add_text("How would you rate you day uptill now?")
        # conversation[2] = ['slider', text_3, text_4]
        # text_5 = TextMessage()
        # text_5.add_text("Would you recommend this app?")
        # conversation[3] = ['multiple_choice', text_5]
        # text_6 = TextMessage()
        # text_6.add_text("okkiii byeeee")
        # conversation[4] = ['text_box', text_6]
        # for i in range(4, len(conversation) - 1):
        #     text = TextMessage()
        #     conversation[i] = ['text_box', text]
        # self.main_screen.add_response()


class MotiFactApp(App):
    theme_color = (255/255, 183/255, 3/255)
    main_builder = None

    def change_body(self, source):
        self.main_builder.main_screen.face.body = source

    def change_moustache(self, source):
        self.main_builder.main_screen.face.moustache = source

    def change_hat(self, source):
        self.main_builder.main_screen.face.hat = source

    def change_background(self, background):
        self.main_builder.main_screen.background_image = background
        self.main_builder.main_screen.face.normal_color = (1, 1, 1)

    def change_theme(self, color):
        print('nice')
        self.theme_color = color
        self.main_builder.main_screen.theme_color = self.theme_color
        self.main_builder.settings.theme_color = self.theme_color
        self.main_builder.profile.theme_color = self.theme_color
        for widget in dynamic_elements:
            widget.theme_color = self.theme_color

    def setup_connection(self, conn_to_questions: Connection, conn_to_output: Connection):
        ci.question_connection = conn_to_questions
        ci.output_connection = conn_to_output

    def retrieve_questions(self, dt):
        print("checking for incoming messages... ")
        if ci.question_connection.poll():
            message = ci.question_connection.recv()
            print(message)
            self.main_builder.main_screen.setup_message(message)

    def build(self):
        self.main_builder = Builder.load_file(MAIN_KV_FILE)
        Clock.schedule_once(self.main_builder.start, 0)
        Clock.schedule_interval(self.main_builder.main_screen.blink, 5)
        Clock.schedule_interval(self.main_builder.main_screen.bounce, 4)
        Clock.schedule_interval(self.main_builder.main_screen.follow_mouse, .05)
        Clock.schedule_interval(self.retrieve_questions, 1)
        return self.main_builder


if __name__ == '__main__':
    MotiFactApp().run()
