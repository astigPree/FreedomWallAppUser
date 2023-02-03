
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivy.properties import BooleanProperty , NumericProperty , ObjectProperty , StringProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from data_management import DataManager
from network import *

# === Inputer 
class Inputer(ModalView) :
	
	donebutton : Button = ObjectProperty(None)
	
	textbox : TextInput = ObjectProperty(None)
	textbox_text = StringProperty("")
	text_title = StringProperty("")
	text_size = NumericProperty(18)
	input_length = NumericProperty(0)
	
	contentType = BooleanProperty(True)
	hasScapeLine = BooleanProperty(True)
	
	def on_pre_dismiss(self):
		self.text_title = ""
		self.text_size = 18
		self.input_length = 0
		self.contentType = True
		self.hasScapeLine = True
		
	def get_text(self) -> str :
		return self.textbox.text
	
	def on_open(self):
		Animation(opacity = 1 , duration = 0.2).start(self)
	
	def on_dismiss(self ):
		Animation(opacity = 0 , duration = 0.2).start(self)
	
	def on_kv_post(self , base_widget):
		Clock.schedule_interval(self.checkInputLengthAndText , 1 / 60)
	
	def checkInputLengthAndText(self , interval):
		if self.input_length > 0 :
			if len(self.textbox.text) > self.input_length :
				self.textbox.text = self.textbox.text[:self.input_length]
		if not self.hasScapeLine:
			modifyText = ""
			for letter in self.textbox.text :
				if letter.isspace() :
					modifyText += " "
				else :
					modifyText += letter
			self.textbox.text = modifyText
			
	
# ==== Main Screen
class UploadScreen(Screen) :
	
	nickname : Button = ObjectProperty(None)
	post_title : Button = ObjectProperty(None)
	post_content : Button = ObjectProperty(None)
	
	post_text = ( "What is it all about ?" , "What your thoughts about it ?")
	
	def __init__(self , **kwargs):
		super(UploadScreen , self).__init__(**kwargs)
		self.app_data = DataManager()
		self.inputer = Inputer()
		self.inputer.donebutton.bind(on_release = self.closeInputer )
	
	def closeInputer(self , *args):
		if self.inputer.contentType :
			self.post_content.text = self.inputer.textbox.text
			if not self.post_content.text:
				self.post_content.text =  self.post_text[1]
		else :
			self.post_title.text = self.inputer.textbox.text
			if not self.post_title.text :
				self.post_title.text = self.post_text[0]
		
		self.inputer.dismiss()
	
	def clearData(self):
		self.nickname.text = ""
		self.post_content.text = self.post_text[1]
		self.post_title.text = self.post_text[0]
		

