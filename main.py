#!/usr/bin/python3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup

class DecisionScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.add_widget(Label(text="BTC (percentile) :"))
        self.btc_input = TextInput(multiline=False)
        self.add_widget(self.btc_input)

        self.add_widget(Label(text="BTS (µmol/L) :"))
        self.bts_input = TextInput(multiline=False)
        self.add_widget(self.bts_input)

        self.add_widget(Label(text="Âge (heures) :"))
        self.age_input = TextInput(multiline=False)
        self.add_widget(self.age_input)

        self.add_widget(Label(text="Signes cliniques (oui/non) :"))
        self.signes_input = TextInput(multiline=False)
        self.add_widget(self.signes_input)

        self.submit_button = Button(text="Décider")
        self.submit_button.bind(on_press=self.process_decision)
        self.add_widget(self.submit_button)
        
    def process_decision(self, instance):
        try:
            BTC = float(self.btc_input.text)
            BTS = float(self.bts_input.text)
            age = int(self.age_input.text)
            signes_cliniques = self.signes_input.text.strip().lower() == "oui"
        except ValueError:
            self.show_popup("Erreur","Veuillez entrer des valeurs numériques correctes.")
            return

        output_text = ""

        if BTC > 75:
            output_text += "Effectuer une BTS.\n"

            if BTS > 100:
                if age <= 24 or signes_cliniques:
                    output_text += "\nPremière situation :\n- Débuter une PTI (Photothérapie Intensive).\n"
                    output_text += "- Évaluer l'indication d'une EST (Exsanguino-Transfusion).\n"
                    output_text += "- Contrôler une BTS à H4 après le début de la PTI.\n"
                elif age > 24 and not signes_cliniques:
                    output_text += "\nDeuxième situation :\n- Débuter une PTI de 12 heures.\n"
                    output_text += "- Contrôler une BTS à H6 après le début de la PTI.\n"

                output_text += "\nRéaliser un bilan étiologique :\n- Numération réticulocytes\n- Groupe Coombs\n- Dosage G6PD\n"
                
        else:
            output_text = "BTC inférieur ou égal à 75 : pas d'indication immédiate pour BTS."

        self.show_popup('Recommandation',output_text)
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

class DecisionApp(App):
    def build(self):
        return DecisionScreen()

if __name__ == "__main__":
    DecisionApp().run()
