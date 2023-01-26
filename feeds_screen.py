
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView

from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock

# ==== Post Container
class PostContent(ModalView):
	
	postdate : Label = ObjectProperty(None)
	postheadline : Label = ObjectProperty(None)
	postnickname : Label = ObjectProperty(None)
	postcontent : Label = ObjectProperty(None)
	
	def on_open(self , * args) :
		Animation(opacity = 1 , duration = 0.2).start(self)
	
	def on_dismiss(self , *args) :
		Animation(opacity = 0 , duration = 0.2).start(self)
	
# ==== Headline Container
class HeadlineContainer(BoxLayout) :
	
	postdate : Label = ObjectProperty(None)
	postnickname : Label = ObjectProperty(None)
	postheadline : Button = ObjectProperty(None)
	
	def __init__(self , **kwargs) :
		super(HeadlineContainer , self).__init__(**kwargs)
		self.postcontent = PostContent()
		

# ==== Posts Feeds Container
class PostFeedsContainer(ScrollView) :
	
	container : GridLayout = ObjectProperty(None)
	
#	def addHeadline(self , data : dict) :
#		self.post_container.bind(minimum_height=self.post_container.setter('height'))


# ==== Main Screen
class FeedsScreen(Screen) :
	
	searchbox : TextInput = ObjectProperty(None)
	viewer : PostFeedsContainer = ObjectProperty(None)
	prevbutton : Button = ObjectProperty(None)
	nextbutton : Button = ObjectProperty(None)
	
	
	hasNext = True
	hasPrev = False
	
	def on_kv_post(self , base_widget):
		Clock.schedule_interval(self.popupNextAndPrevButton , 1 )
	
	def popupNextAndPrevButton(self , interval ):
		if self.viewer.scroll_y < 0.2 and self.nextbutton.opacity < 1 and self.prevbutton.opacity < 1 :
			anim = Animation(opacity = 1 , duration = 0.2)
			anim.start(self.prevbutton)
			anim.start(self.nextbutton)
		if self.viewer.scroll_y > 0.2 and self.nextbutton.opacity > 0 and self.prevbutton.opacity > 0 :
			anim = Animation(opacity = 0 , duration = 0.2)
			anim.start(self.prevbutton)
			anim.start(self.nextbutton)
			
	