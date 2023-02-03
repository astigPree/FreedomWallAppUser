__version__ = "0.0.1"
	

from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager , FadeTransition
from kivy.uix.modalview import ModalView

from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.core.text import LabelBase as CoreLabel
from kivy.animation import Animation

from KVScreens.feeds_screen import FeedsScreen
from KVScreens.upload_screen import UploadScreen


# ===== Settings Widget
class SettingWidget(ModalView):
	
	def on_open(self ) :
		Animation(opacity = 1 , duration = 0.2).start(self)
	
	def on_dismiss(self ) :
		Animation(opacity = 0 , duration = 0.2).start(self)
	

# ===== Screen Holder
class ScreensHolder(ScreenManager) :
	transition = FadeTransition( duration = .2)

# ===== Main Widget
class MainWidget(BoxLayout) :
	
	logo = "Files/transparent.png"
	
	screens_holder : ScreensHolder = ObjectProperty(None)
	
	def __init__(self , **kwargs):
		super(MainWidget , self).__init__(**kwargs)
		self.settingspopup = SettingWidget()
	
	def on_kv_post(self , base_widget) :
		self.screens_holder.add_widget(FeedsScreen(name="feeds"))
		self.screens_holder.add_widget(UploadScreen(name="upload"))

	
# ===== Main Application
class MyApp(MDApp) :
	
	def build(self):
		Builder.load_file("KVDesign/upload_screen.kv")
		Builder.load_file("KVDesign/feeds_screen.kv")
		return Builder.load_file("KVDesign/main_design.kv")

if __name__ == "__main__":
	CoreLabel.register(name="mainfont" , fn_regular="Fonts/mainfont.ttf")
	CoreLabel.register(name="headlinefont" , fn_regular="Fonts/headlinefont.otf")
	CoreLabel.register(name="textfont" , fn_regular="Fonts/textfont.ttf")
	MyApp().run()