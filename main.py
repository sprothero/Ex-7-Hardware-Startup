import os
from kivy.core.window import Window
import pygame
import spidev
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers

# ------------------------- all imports -------------------------
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from datetime import datetime
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.animation import AnimationTransition
from kivy.graphics import Color, Rectangle
from kivy.uix.slider import Slider
from threading import Thread
# -----------------------------------------------------------------

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

spi = spidev.SpiDev()

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)
# Init a 200 steps per revolution stepper on Port 0

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'

Builder.load_file('main.kv')
Window.clearcolor = (0.7, 0.7, 0.7, 1)
# Initial Window Color


class ProjectNameGUI(App):

    def build(self):
        return SCREEN_MANAGER
# Launches Window Manager

# -----------------------------------------------------------------


class MainScreen(Screen):
    button_state = ObjectProperty(None)

    def start_control_switch(self):
        if self.start_text() == 'Off':
            self.startButton.text = "Stop"


        elif self.start_text() == 'On':
            self.startButton.text = "Start"

    def start_text(self):
        if self.startButton.text == "Start":
            return 'Off'

        elif self.startButton.text == "Stop":
            return 'On'


# ----------------- Screen Declarations -----------------------
Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
# -------------------------------------------------------------


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()
# MixPanel Events


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
# Execute GUI