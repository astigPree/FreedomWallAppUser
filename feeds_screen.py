
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

import network , data_management

# ==== Post Container
class PostContent(ModalView):
	
	postdate : Label = ObjectProperty(None)
	postheadline : Label = ObjectProperty(None)
	postnickname : Label = ObjectProperty(None)
	postcontent : Label = ObjectProperty(None)
	
	def update(self , date : str, nickname : str , headline : str , content : str) :
		self.postdate.text = date
		self.postnickname.text = nickname
		self.postheadline.text = headline
		self.postcontent.text = content
	
	def on_open(self , * args) :
		Animation(opacity = 1 , duration = 0.2).start(self)
	
	def on_dismiss(self , *args) :
		Animation(opacity = 0 , duration = 0.2).start(self)
	
# ==== Headline Container
class HeadlineContainer(BoxLayout) :
	
	postdate : Label = ObjectProperty(None)
	postnickname : Label = ObjectProperty(None)
	postheadline : Button = ObjectProperty(None)
	
	data = None
	display = ( "date", "nickname" , "headline" , "content" )
	
	def __init__(self , **kwargs) :
		super(HeadlineContainer , self).__init__(**kwargs)
		self.postcontent = PostContent()
	
	def update(self , data : dict ) :
		self.data = data
		self.postdate.text = data[self.display[0]]
		self.postnickname.text = data[self.display[1]]
		self.postheadline.text = data[self.display[2]]
		self.postcontent.update(
			date=data[self.display[0]] , 
			nickname=data[self.display[1]] , 
			headline=data[self.display[2]] , 
			content=data[self.display[3]] )

# ==== Posts Feeds Container
class PostFeedsContainer(ScrollView) :
	
	container : GridLayout = ObjectProperty(None)
	
	def addHeadline(self , data : dict) :
		widget = HeadlineContainer()
		widget.update( data )
		self.container.add_widget(widget)
		self.container.bind(minimum_height=self.container.setter('height'))
	

# ==== Main Screen
class FeedsScreen(Screen) :
	
	# Design Attrib
	searchbox : TextInput = ObjectProperty(None)
	viewer : PostFeedsContainer = ObjectProperty(None)
	prevbutton : Button = ObjectProperty(None)
	nextbutton : Button = ObjectProperty(None)
	
	# Backend Attrib
	hasNext = True
	hasPrev = False
	
	
	def on_kv_post(self , base_widget):
		Clock.schedule_interval(self.popupNextAndPrevButton , 1 )
	
	
	def popupNextAndPrevButton(self , interval ):
		if self.viewer.scroll_y < 0.2 and self.nextbutton.opacity < 1 and self.prevbutton.opacity < 1 :
			self.prevbutton.disabled = self.hasPrev
			self.nextbutton.disabled = self.hasNext
			anim = Animation(opacity = 1 , duration = 0.2)
			anim.start(self.prevbutton)
			anim.start(self.nextbutton)
		if self.viewer.scroll_y > 0.2 and self.nextbutton.opacity > 0 and self.prevbutton.opacity > 0 :
			self.prevbutton.disabled = self.hasPrev
			self.nextbutton.disabled = self.hasNext
			anim = Animation(opacity = 0 , duration = 0.2)
			anim.start(self.prevbutton)
			anim.start(self.nextbutton)
			
	