import json
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.answer = None
        self.prompt = None
        self.index_list_cards = 0
        self.list_cards = self.get_list_cards()
        self.get_data_from_current_card()

        self.define_page_layout()
        # by default it will show the answer, overwrite it with ? by rerunning get_answer with hidden=True.
        self.labelAnswer.setText(self.get_answer(hidden=True))

    def get_answer(self, hidden=False):
        if hidden:
            answer = '?'
        else:
            answer = self.answer
        return f'Answer: {answer}'

    def get_prompt(self):
        return f'Prompt: {self.prompt}'

    def restart(self):
        self.index_list_cards = -1
        self.get_next_question()

    def increment_index(self):
        self.index_list_cards += 1

    def get_next_question(self):
        self.increment_index()
        self.get_data_from_current_card()
        self.labelAnswer.setText(self.get_answer(hidden=True))
        self.labelPrompt.setText(self.get_prompt())

    def show_answer(self):
        self.labelAnswer.setText(self.get_answer())

    def get_data_from_current_card(self):

        try:
            dict_data = self.list_cards[self.index_list_cards]
        except IndexError:
            dict_data = {'name': 'Finished', 'answer': '', 'hint': '', 'evidence': ''}

        self.prompt, self.answer, self.hint, self.evidence = dict_data['name'], dict_data['answer'], dict_data['hint'], \
                                                             dict_data['evidence']

    def get_list_cards(self):
        return json.load(open('flashcards.json'))['cards']

    def define_page_layout(self):

        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("flashcards")

        self.layout_page = QVBoxLayout()
        self.layout_page.setContentsMargins(0, 0, 0, 0)
        self.layout_page.setSpacing(20)

        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.setContentsMargins(0, 0, 0, 0)
        self.layout_buttons.setSpacing(20)

        self.layout_page.addLayout(self.layout_buttons)

        self.buttonNextCard = QtWidgets.QPushButton(self)
        self.buttonNextCard.setText("Next Card")
        self.buttonNextCard.clicked.connect(self.get_next_question)
        self.layout_buttons.addWidget(self.buttonNextCard)

        self.buttonShowAnswer = QtWidgets.QPushButton(self)
        self.buttonShowAnswer.setText("Show Answer")
        self.buttonShowAnswer.clicked.connect(self.show_answer)
        self.layout_buttons.addWidget(self.buttonShowAnswer)

        self.buttonRestart = QtWidgets.QPushButton(self)
        self.buttonRestart.setText("Restart")
        self.buttonRestart.clicked.connect(self.restart)
        self.layout_buttons.addWidget(self.buttonRestart)

        self.layout_cards = QVBoxLayout()
        self.layout_cards.setContentsMargins(0, 0, 0, 0)
        self.layout_cards.setSpacing(20)

        self.layout_page.addLayout(self.layout_cards)

        self.labelPrompt = QtWidgets.QLabel(self)
        self.labelPrompt.setText(self.get_prompt())
        self.labelPrompt.setWordWrap(True)
        self.layout_cards.addWidget(self.labelPrompt)

        self.labelAnswer = QtWidgets.QLabel(self)
        self.labelAnswer.setText(self.get_answer())
        self.labelAnswer.setWordWrap(True)
        self.layout_cards.addWidget(self.labelAnswer)

        widget = QWidget()
        widget.setLayout(self.layout_page)
        self.setCentralWidget(widget)


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()
