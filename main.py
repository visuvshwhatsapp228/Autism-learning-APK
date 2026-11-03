import math
import os
import csv
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle

TAMIL_VOWELS = list("அஆஇஈஉஊஎஏஐஒஓஔ")
TAMIL_CONSONANTS = list("கஙசஞடணதநபமயரலவழளறன")
TAMIL_SIGNS = ["", "ா", "ி", "ீ", "ு", "ூ", "ெ", "ே", "ை", "ொ", "ோ", "ௌ"]
TAMIL_LETTERS = TAMIL_VOWELS + [
    consonant + sign for consonant in TAMIL_CONSONANTS for sign in TAMIL_SIGNS
] + ["ஃ"]

MODES = {
    "Numbers": list("0123456789"),
    "Capital A-Z": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    "Small a-z": list("abcdefghijklmnopqrstuvwxyz"),
    "Symbols": list("+-×÷=<>@#$%&!?.,:;()[]{}₹"),
    "Tamil": TAMIL_LETTERS,
}
PALETTE = [
    (1.00, 0.88, 0.48, 1), (0.55, 0.76, 1.00, 1),
    (0.62, 0.94, 0.80, 1), (1.00, 0.65, 0.65, 1),
    (0.78, 0.70, 1.00, 1),
]


class OrbitArea(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = MODES["Capital A-Z"][:]
        self.angle = 0.0
        self.speed = 0.12
        self.animation_on = True
        self.selected = None
        self.character_buttons = []
        self.selected_label = Label(
            text="", font_name="Roboto", font_size=sp(180),
            bold=True, color=(1, 1, 1, 1),
            halign="center", valign="middle",
            size_hint=(1, 1), pos_hint={"x": 0, "y": 0},
        )
        self.add_widget(self.selected_label)
        self.bind(size=self.redraw, pos=self.redraw)
        Clock.schedule_interval(self.update_frame, 1 / 60)

    def update_frame(self, dt):
        if not self.animation_on:
            return
        self.angle = (self.angle + self.speed) % 360
        if self.selected is None:
            self.place_characters()
        else:
            pulse = 1.0 + 0.015 * math.sin(self.angle * math.pi / 60.0)
            self.selected_label.font_size = min(self.width, self.height) * 0.44 * pulse

    def set_mode(self, mode_name):
        self.items = MODES[mode_name][:]
        self.selected = None
        self.selected_label.text = ""
        self.rebuild_characters()

    def rebuild_characters(self):
        for button in self.character_buttons:
            self.remove_widget(button)
        self.character_buttons = []
        total = len(self.items)
        button_size = dp(48) if total > 100 else dp(66)
        font_size = sp(18) if total > 100 else sp(27)
        for index, character in enumerate(self.items):
            button = Button(
                text=character, font_name="Roboto", font_size=font_size,
                bold=True, size_hint=(None, None),
                size=(button_size, button_size),
                background_normal="", background_down="",
                background_color=(0.12, 0.17, 0.25, 1),
                color=PALETTE[index % len(PALETTE)],
            )
            button.bind(on_release=lambda instance, value=character: self.select_character(value))
            self.character_buttons.append(button)
            self.add_widget(button)
        self.redraw()

    def redraw(self, *args):
        if self.width <= 0 or self.height <= 0:
            return
        with self.canvas.before:
            self.canvas.before.clear()
            Color(0.055, 0.080, 0.135, 1)
            Rectangle(pos=self.pos, size=self.size)
        self.selected_label.text = self.selected or ""
        self.place_characters()

    def place_characters(self):
        if not self.character_buttons or self.width <= 0 or self.height <= 0:
            return
        count = len(self.character_buttons)
        cx, cy = self.center
        radius = min(self.width, self.height) * 0.36
        for index, button in enumerate(self.character_buttons):
            if self.selected is not None:
                button.opacity = 0
                button.disabled = True
                continue
            theta = math.radians(self.angle + index * 360.0 / count)
            button.pos = (
                cx + math.cos(theta) * radius - button.width / 2,
                cy + math.sin(theta) * radius - button.height / 2,
            )
            button.opacity = 1
            button.disabled = False

    def select_character(self, character):
        if character not in self.items:
            return
        self.selected = character
        self.selected_label.text = character
        self.selected_label.font_size = min(self.width, self.height) * 0.44
        self.place_characters()
        App.get_running_app().on_character_selected(character)

    def play(self):
        self.selected = None
        self.selected_label.text = ""
        self.place_characters()

    def pass_character(self):
        if not self.items:
            return
        current = self.items.index(self.selected) if self.selected in self.items else -1
        self.select_character(self.items[(current + 1) % len(self.items)])

    def set_animation(self, enabled):
        self.animation_on = enabled
        if not enabled and self.selected:
            self.selected_label.font_size = min(self.width, self.height) * 0.44


class TabletLearningApp(App):
    def build(self):
        self.title = "Autism Student Learning"
        self.mode_name = "Capital A-Z"
        self.voice_enabled = False
        self.tts = None
        self.history = []

        # Tuned for 12-inch landscape tablets; Kivy dp keeps controls scalable.
        Window.fullscreen = "auto"
        Window.clearcolor = (0.055, 0.080, 0.135, 1)

        root = FloatLayout()
        self.orbit = OrbitArea(size_hint=(0.68, 1), pos_hint={"x": 0.16, "y": 0})
        root.add_widget(self.orbit)

        self.left_panel = BoxLayout(
            orientation="vertical", spacing=dp(9), padding=(dp(7), dp(10)),
            size_hint=(None, 0.96), width=dp(132),
            pos_hint={"x": 0.005, "center_y": 0.5},
        )
        self.add_button(self.left_panel, "▶  PLAY", (0.08, 0.34, 0.20, 1), self.play, 68)
        self.add_button(self.left_panel, "⏭  PASS", (0.10, 0.28, 0.62, 1), self.pass_character, 68)
        for mode, label in [
            ("Numbers", "123  NUMBERS"),
            ("Capital A-Z", "ABC  CAPITAL"),
            ("Small a-z", "abc  SMALL"),
            ("Symbols", "#$%  SYMBOLS"),
            ("Tamil", "தமிழ்"),
        ]:
            self.add_button(
                self.left_panel, label, (0.18, 0.23, 0.34, 1),
                lambda instance, selected_mode=mode: self.change_mode(selected_mode), 58
            )
        root.add_widget(self.left_panel)

        self.right_panel = BoxLayout(
            orientation="vertical", spacing=dp(12), padding=(dp(7), dp(10)),
            size_hint=(None, 0.96), width=dp(138),
            pos_hint={"right": 0.995, "center_y": 0.5},
        )
        self.animation_button = self.add_button(
            self.right_panel, "ANIMATION\\nON", (0.38, 0.16, 0.62, 1),
            self.toggle_animation, 78
        )
        self.voice_button = self.add_button(
            self.right_panel, "VOICE\\nOFF", (0.25, 0.30, 0.40, 1),
            self.toggle_voice, 72
        )
        self.add_button(
            self.right_panel, "TEACHER\\nSETTINGS", (0.25, 0.30, 0.40, 1),
            self.open_settings, 78
        )
        self.add_button(
            self.right_panel, "EXPORT\\nREPORT", (0.25, 0.30, 0.40, 1),
            self.export_report, 72
        )
        root.add_widget(self.right_panel)

        self.orbit.rebuild_characters()
        Window.bind(on_keyboard=self.on_keyboard)
        return root

    def add_button(self, panel, text, color, callback, height):
        button = Button(
            text=text, size_hint=(1, None), height=dp(height),
            font_size=sp(13), bold=True, color=(1, 1, 1, 1),
            background_normal="", background_down="", background_color=color,
        )
        button.bind(on_release=callback)
        panel.add_widget(button)
        return button

    def change_mode(self, mode_name):
        self.mode_name = mode_name
        self.orbit.set_mode(mode_name)

    def play(self, *args):
        self.orbit.play()

    def pass_character(self, *args):
        self.orbit.pass_character()

    def toggle_animation(self, *args):
        enabled = not self.orbit.animation_on
        self.orbit.set_animation(enabled)
        self.animation_button.text = "ANIMATION\\nON" if enabled else "ANIMATION\\nOFF"

    def toggle_voice(self, *args):
        if not self.voice_enabled:
            try:
                from plyer import tts
                self.tts = tts
                self.voice_enabled = True
                self.voice_button.text = "VOICE\\nON"
            except Exception:
                self.voice_button.text = "VOICE\\nNOT AVAILABLE"
        else:
            self.voice_enabled = False
            self.tts = None
            self.voice_button.text = "VOICE\\nOFF"

    def on_character_selected(self, character):
        self.history.append([
            datetime.now().isoformat(timespec="seconds"), self.mode_name, character
        ])
        if self.voice_enabled and self.tts:
            try:
                self.tts.speak(text=character)
            except Exception:
                pass

    def open_settings(self, *args):
        content = BoxLayout(orientation="vertical", spacing=dp(14), padding=dp(18))
        content.add_widget(Label(
            text="Character movement speed", size_hint_y=None, height=dp(34)
        ))
        slider = Slider(min=0.02, max=0.70, value=self.orbit.speed,
                        size_hint_y=None, height=dp(54))
        slider.bind(value=lambda instance, value: setattr(self.orbit, "speed", value))
        content.add_widget(slider)
        content.add_widget(Label(
            text="Use slow movement and adjust to the student's comfort.",
            size_hint_y=None, height=dp(54)
        ))
        close_button = Button(text="CLOSE", size_hint_y=None, height=dp(54))
        content.add_widget(close_button)
        popup = Popup(title="Teacher Settings", content=content,
                      size_hint=(0.70, 0.48), auto_dismiss=True)
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def export_report(self, *args):
        report_path = os.path.join(self.user_data_dir, "student_learning_report.csv")
        try:
            with open(report_path, "w", newline="", encoding="utf-8-sig") as report_file:
                writer = csv.writer(report_file)
                writer.writerow(["Date and time", "Learning mode", "Selected character"])
                writer.writerows(self.history)
            Popup(
                title="Report saved",
                content=Label(text="Report saved in the app's private storage.\\n"
                                   "Android Share / Save As can be added in a later release."),
                size_hint=(0.78, 0.40),
            ).open()
        except OSError as error:
            Popup(title="Export error", content=Label(text=str(error)),
                  size_hint=(0.78, 0.35)).open()

    def on_keyboard(self, window, key, scancode, codepoint, modifiers):
        if codepoint:
            for candidate in (codepoint, codepoint.upper(), codepoint.lower()):
                if candidate in self.orbit.items:
                    self.orbit.select_character(candidate)
                    return True
        return False


if __name__ == "__main__":
    TabletLearningApp().run()
