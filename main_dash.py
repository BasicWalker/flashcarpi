from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import NumericProperty
from threading import Thread
import time
import random



class CarPiWidget(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 0.5)

    def update(self, *args):
        self.ids.speed.text = str(speed_data)
        print(speed_data)
    

class CarPiApp(App):

    def build(self):
        return CarPiWidget()

def speedgen():
    global speed_data
    while True:
        time.sleep(0.1)
        speed_data = random.randint(0,100)



if __name__=="__main__":
    speed_data = 0
    get_speed_thread = Thread(target = speedgen)
    get_speed_thread.daemon = True
    get_speed_thread.start()
    CarPiApp().run()
