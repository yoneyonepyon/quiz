#!/usr/bin/env python3

import csv
from random import shuffle
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from functools import partial

font_name = 'NotoSansJP-Light.otf'


class DisplayLayout(BoxLayout):

    def show_answer(self, *largs):
        label = self.label
        answer = self.answer
        label.text = answer

    def next_quiz(self, *largs):
        if self.index < len(self.quizzes):
            self.index += 1
        else:
            self.index = 0

        index = self.index
        quizzes = self.quizzes
        question, answer = quizzes[index]

        self.answer = answer
        anagram = list(answer)
        shuffle(anagram)

        label = self.label
        label.text = "".join(anagram)

        label2 = self.label2
        label2.text = question

    def __init__(self, quizzes=[],  **kwargs):
        shuffle(quizzes)  # まずは混ぜよ
        self.quizzes = quizzes
        question, answer = quizzes[0]
        self.index = 0
        # このあたりは後で直す
        self.answer = answer
        anagram = list(answer)
        shuffle(anagram)
        self.label = Label(text="".join(anagram),
                           font_size=100,
                           font_name=font_name)
        self.label2 = Label(text=question,
                            font_size=20,
                            font_name=font_name)
        super(DisplayLayout, self).__init__(**kwargs)
        self.add_widget(self.label)
        self.add_widget(self.label2)


class ControlLayout(BoxLayout):

    def __init__(self, display=None, **kwargs):
        super(ControlLayout, self).__init__(**kwargs)
        btn_add100 = Button(text='答えを見る',
                            font_name=font_name,
                            on_press=partial(display.show_answer))
        btn_minus500 = Button(text='次の問題へ',
                              font_name=font_name,
                              on_press=partial(display.next_quiz))

        self.add_widget(btn_add100)
        self.add_widget(btn_minus500)


class Main(App):

    def build(self):
        # 問題を開く
        with open('問題.csv', 'r', encoding="utf-8") as f:
            quizzes = [row for row in csv.reader(f)]

        display = DisplayLayout(quizzes=quizzes,
                                orientation='vertical')
        layout = ControlLayout(display=display,
                               size_hint=(1, None),
                               height=50)

        root = BoxLayout(orientation='vertical')
        root.add_widget(display)
        root.add_widget(layout)

        return root


if __name__ == "__main__":
    Main().run()
