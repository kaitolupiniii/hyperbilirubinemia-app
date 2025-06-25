#!/usr/bin/python3
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

        self.used_once = False  # Pour contrôler l'état d'utilisation

        self.add_widget(Label(text="BTC (percentile) :"))
        self.btc_input = TextInput(multiline=False)
        self.add_widget(self.btc_input)

        self.add_widget(Label(text="BTS (µmol/L) :"))
        self.bts_input = TextInput(multiline=False)
        self.add_widget(self.bts_input)

        self.add_widget(Label(text="Âge (heures) :"))
        self.age_input = TextInput(multiline=False)
        self.add_widget(self.age_input)

        # Signes cliniques sous forme de cases à cocher
        self.add_widget(Label(text="Signes cliniques :"))
        self.signes_cliniques_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        self.signes_checkbox_oui = CheckBox(group='signes')
        self.signes_checkbox_non = CheckBox(group='signes')
        self.signes_cliniques_layout.add_widget(Label(text="Oui"))
        self.signes_cliniques_layout.add_widget(self.signes_checkbox_oui)
        self.signes_cliniques_layout.add_widget(Label(text="Non"))
        self.signes_cliniques_layout.add_widget(self.signes_checkbox_non)
        self.add_widget(self.signes_cliniques_layout)

        # Bouton principal
        self.submit_button = Button(text="Décider")
        self.submit_button.bind(on_press=self.process_decision)
        self.add_widget(self.submit_button)

        # Élément pour contrôle BTS (après première utilisation)
        self.controle_bts_label = Label(text="Résultat du contrôle de la BTS :")
        self.controle_bts_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        self.ctrl_bts_augmenté = CheckBox(group='controle_bts')
        self.ctrl_bts_diminue = CheckBox(group='controle_bts')
        self.ctrl_bts_inf_seuil = CheckBox(group='controle_bts')
        self.controle_bts_layout.add_widget(Label(text="augmenté"))
        self.controle_bts_layout.add_widget(self.ctrl_bts_augmenté)
        self.controle_bts_layout.add_widget(Label(text="diminué mais > seuil"))
        self.controle_bts_layout.add_widget(self.ctrl_bts_diminue)
        self.controle_bts_layout.add_widget(Label(text="< seuil"))
        self.controle_bts_layout.add_widget(self.ctrl_bts_inf_seuil)

    def process_decision(self, instance):
        if not self.used_once:
            try:
                BTC = float(self.btc_input.text)
                BTS = float(self.bts_input.text)
                age = int(self.age_input.text)
                signes_cliniques = self.signes_checkbox_oui.active
            except ValueError:
                self.show_popup("Erreur", "Veuillez entrer des valeurs numériques valides.")
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

            self.show_popup('Recommandation', output_text)

            # Marquer l'utilisation et afficher les options de suivi
            self.used_once = True
            self.add_widget(self.controle_bts_label)
            self.add_widget(self.controle_bts_layout)

        else:
            output_text = ""
            if self.ctrl_bts_augmenté.active:
                output_text += "Poursuivre la PTI, hydrater, associer un traitement adjuvant.\n"
                output_text += "Envisager une EST ou une transfusion si nécessaire."
            elif self.ctrl_bts_diminue.active:
                output_text += "Continuer la PTI, hydrater, compléter le bilan étiologique."
            elif self.ctrl_bts_inf_seuil.active:
                output_text += "Arrêter la PTI, poursuivre l’hydratation.\n"
                output_text += "Contrôler BTC ou BTS à 12h et 24h après l’arrêt.\n"
                output_text += "Compléter un bilan étiologique si besoin."
            else:
                output_text = "Veuillez sélectionner une option de contrôle BTS."

            self.show_popup("Suivi du contrôle BTS", output_text)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

class DecisionApp(App):
    def build(self):
        return DecisionScreen()

if __name__ == "__main__":
    DecisionApp().run()

