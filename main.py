from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import AsyncImage
from kivy.clock import Clock

import json
import plugingen as ApiPluginGenerator
import modelsearcher

class AutocompleteTextInput(TextInput):
    def __init__(self, model_list, **kwargs):
        super().__init__(**kwargs)
        self.model_list = model_list
        self.dropdown = DropDown()
        self.submodel_dropdown = DropDown()
        self.bind(on_text_validate=self.on_text_validate)
        self.bind(text=self.on_text_change)

    def on_text_validate(self, instance):
        self.add_model()

    def on_text_change(self, instance, value):
        self.dropdown.clear_widgets()
        for model in self.model_list:
            if value.lower() in model.lower():
                btn = Button(text=model, size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.set_text(btn.text))
                self.dropdown.add_widget(btn)
        if self.dropdown.children:
            self.dropdown.open(self)

    def add_model(self):
        model_name = self.text.strip()
        if model_name:
            # Simulate finding submodels
            available_submodels = self.find_submodels(model_name)
            if available_submodels:
                self.show_submodel_popup(available_submodels)
            else:
                self.generate_plugin(model_name)

    def find_submodels(self, model_name):
        # Simulate finding available submodels
        return ["Submodel 1", "Submodel 2", "Submodel 3"]

    def show_submodel_popup(self, submodels):
        submodel_popup = Popup(title='Select Submodel', size_hint=(None, None), size=(400, 300))
        submodel_layout = BoxLayout(orientation='vertical', spacing=10)
        for submodel in submodels:
            btn = Button(text=submodel, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.generate_plugin(self.text, btn.text))
            submodel_layout.add_widget(btn)
        submodel_popup.content = submodel_layout
        submodel_popup.open()

   
    def on_text_validate(self, instance):
        self.add_model()

    def on_text_change(self, instance, value):
        self.dropdown.clear_widgets()
        for model in self.model_list:
            if value.lower() in model.lower():
                btn = Button(text=model, size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.set_text(btn.text))
                self.dropdown.add_widget(btn)
        if self.dropdown.children:
            self.dropdown.open(self)

    def add_model(self):
        model_name = self.text.strip()
        if model_name:
            self.loading_widget = LoadingWidget()
            self.add_widget(self.loading_widget)
            self.loading_widget.start_loading()

            Clock.schedule_once(self.generate_plugin, 2) 

    def generate_plugin(self, dt):
        self.remove_widget(self.loading_widget)
        
class LoadingWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.size_hint = (None, None)
        self.size = (200, 40)

        self.loading_icon = AsyncImage(source='loading.gif')  # Replace with the path to your loading icon
        self.loading_text = Label(text='Generating...', size_hint_x=None, width=100)

        self.add_widget(self.loading_icon)
        self.add_widget(self.loading_text)

    def start_loading(self):
        self.loading_text.text = 'Generating...'
        self.loading_icon.anim_delay = 0.1
        self.loading_icon.anim_loop = True
        self.loading_icon.reload()
        
class MyApp(App):
    def build(self):
        model_list = [
            "Amazon Lex",
            "Rasa NLU",
            "Rasa Core",
            "Google AI's Meena",
            "Microsoft's Turing",
            "Facebook's Blenderbot",
            "Google's Bard",
            "OpenAI's GPT-3",
            "OpenAI's ChatGPT",
            "Hugging Face's DialoGPT",
            "Hugging Face's Blenderbot",
            "ChatGPT-J",
            "ChatDolphin",
            "Jurassic-1 Jumbo"
        ]
        layout = BoxLayout(orientation='vertical', padding=10)
        autocomplete_input = AutocompleteTextInput(model_list, multiline=False)
        layout.add_widget(autocomplete_input)
        return layout

class LoadingWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.size_hint = (None, None)
        self.size = (200, 40)

        self.loading_icon = AsyncImage(source='loading.gif')  # Replace with the path to your loading icon
        self.loading_text = Label(text='Generating...', size_hint_x=None, width=100)

        self.add_widget(self.loading_icon)
        self.add_widget(self.loading_text)

    def start_loading(self):
        self.loading_text.text = 'Generating...'
        self.loading_icon.anim_delay = 0.1
        self.loading_icon.anim_loop = True
        self.loading_icon.reload()

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='Main UI'))
        
        # Add API Button
        add_api_button = Button(text='Add API', on_release=self.show_add_api_popup)
        self.add_widget(add_api_button)
        
        # Progress Bar
        self.progress_bar = ProgressBar(max=100)
        self.add_widget(self.progress_bar)
        
        self.available_tokens = 100  # Replace with actual available tokens
        self.update_progress_bar()
        
        self.api_plugin_generator = ApiPluginGenerator.ApiPluginGenerator()  # Create an instance of the generator
        self.model_searcher = modelsearcher.ModelSearcher()  # Create an instance of the model searcher

    def show_add_api_popup(self, instance):
        popup_content = BoxLayout(orientation='vertical')
        api_name_input = TextInput(hint_text='Enter API Name')
        add_button = Button(text='Add API', on_release=lambda x: self.add_api(api_name_input.text))
        popup_content.add_widget(api_name_input)
        popup_content.add_widget(add_button)
        
        popup = Popup(title='Add API', content=popup_content, size_hint=(None, None), size=(300, 200))
        popup.open()

    def add_api(self, api_name):
        # Generate the plugin using the plugin generator
        self.api_plugin_generator.add_api(api_name)
        
        # Update progress bar
        self.update_progress_bar()
        
        # Update UI with new plugin information, settings, etc.
        # ...

    def update_progress_bar(self):
        self.progress_bar.value = self.available_tokens
class MyApp(App):
    def build(self):
        return MainWindow()

if __name__ == '__main__':
    MyApp().run()
