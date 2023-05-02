import datetime
import json
import sys

import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget


class ScoreKeeper():

    def __init__(self, filename='flashcard_answerdata.json'):
        self.filename = filename

    def load_data(self):
        self.df = pd.DataFrame(json.load(open(self.filename))).T

    def report_answer(self, index, iscorrect):

        self.load_data()

        if index not in self.df.index.values:
            # dict_values = dict()
            # dict_values[index] = self.get_blank_entry()
            # self.df.append(dict_values)

            self.df.loc[index, :] = self.get_blank_entry()

        str_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if iscorrect:
            self.df.loc[index, 'numbercorrect'] = str(1 + int(self.df.loc[index, 'numbercorrect']))
            self.df.loc[index, 'datetimescorrect'].append(str_datetime)
        else:
            self.df.loc[index, 'numberincorrect'] = str(1 + int(self.df.loc[index, 'numberincorrect']))
            self.df.loc[index, 'datetimesincorrect'].append(str_datetime)

        self.save()

    def save(self):
        self.df.T.to_json(self.filename)

    def get_blank_entry(self):
        dict_values = dict()
        dict_values['numbercorrect'] = "0"
        dict_values['numberincorrect'] = "0"
        dict_values['datetimescorrect'] = []
        dict_values['datetimesincorrect'] = []
        return dict_values


# %%

class MyWindow(QMainWindow):
    def __init__(self, scorekeeper=ScoreKeeper()):
        super(MyWindow, self).__init__()

        self.scorekeeper = scorekeeper
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
        self.labelLastActionDescriptor.setText(f"Clicked restart, restarting the deck.")

    def increment_index(self):
        self.index_list_cards += 1

    def get_next_question(self):
        self.increment_index()
        self.get_data_from_current_card()
        self.labelAnswer.setText(self.get_answer(hidden=True))
        self.labelPrompt.setText(self.get_prompt())
        self.labelLastActionDescriptor.setText(f"Switched to a new question, consider the answer then click show.")

    def show_answer(self):
        self.labelAnswer.setText(self.get_answer())
        self.labelLastActionDescriptor.setText(f"Showing answer, please indicate if you got the answer correct")

    def get_data_from_current_card(self):

        try:
            dict_data = self.list_cards[self.index_list_cards]
        except IndexError:
            dict_data = {'name': 'Finished', 'answer': '', 'hint': '', 'evidence': '', 'index': ''}

        self.prompt, self.answer, self.hint, self.evidence, self.cardindex = dict_data['name'], dict_data['answer'], \
                                                                             dict_data['hint'], \
                                                                             dict_data['evidence'], dict_data['index']

    def get_list_cards(self):
        return json.load(open('flashcards.json'))['cards']

    def mark_correct(self):
        self.scorekeeper.report_answer(self.cardindex, True)
        self.labelLastActionDescriptor.setText(f"question: {self.cardindex} marked correct")

    def mark_incorrect(self):
        self.scorekeeper.report_answer(self.cardindex, False)
        self.labelLastActionDescriptor.setText(f"question: {self.cardindex} marked incorrect")

    def define_page_layout(self):

        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("flashcards")

        ## Define the layouts

        self.layout_page = QVBoxLayout()
        self.layout_page.setContentsMargins(10, 10, 10, 10)
        self.layout_page.setSpacing(20)

        self.layout_lastactiondetails = QHBoxLayout()
        self.layout_lastactiondetails.setContentsMargins(10, 10, 10, 10)
        self.layout_lastactiondetails.setSpacing(20)

        self.layout_buttonsrow1 = QHBoxLayout()
        self.layout_buttonsrow1.setContentsMargins(10, 10, 10, 10)
        self.layout_buttonsrow1.setSpacing(20)

        self.layout_buttonsrow2 = QHBoxLayout()
        self.layout_buttonsrow2.setContentsMargins(10, 10, 10, 10)
        self.layout_buttonsrow2.setSpacing(20)

        self.layout_cards = QVBoxLayout()
        self.layout_cards.setContentsMargins(10, 10, 10, 10)
        self.layout_cards.setSpacing(20)

        ## Define the ui elements and their parameters.

        self.buttonNextCard = QtWidgets.QPushButton(self)
        self.buttonNextCard.setText("Next Card")
        self.buttonNextCard.clicked.connect(self.get_next_question)

        self.buttonShowAnswer = QtWidgets.QPushButton(self)
        self.buttonShowAnswer.setText("Show Answer")
        self.buttonShowAnswer.clicked.connect(self.show_answer)

        self.buttonRestart = QtWidgets.QPushButton(self)
        self.buttonRestart.setText("Restart")
        self.buttonRestart.clicked.connect(self.restart)

        self.buttonCorrect = QtWidgets.QPushButton(self)
        self.buttonCorrect.setText("Correct")
        self.buttonCorrect.clicked.connect(self.mark_correct)

        self.buttonIncorrect = QtWidgets.QPushButton(self)
        self.buttonIncorrect.setText("Incorrect")
        self.buttonIncorrect.clicked.connect(self.mark_incorrect)

        self.labelLastActionDescriptor = QtWidgets.QLabel(self)
        self.labelLastActionDescriptor.setText("")

        self.valueLastActionDescriptor = QtWidgets.QLabel(self)
        self.valueLastActionDescriptor.setText("")
        self.valueLastActionDescriptor.setWordWrap(True)

        self.labelPrompt = QtWidgets.QLabel(self)
        self.labelPrompt.setText(self.get_prompt())
        self.labelPrompt.setWordWrap(True)

        self.labelAnswer = QtWidgets.QLabel(self)
        self.labelAnswer.setText(self.get_answer())
        self.labelAnswer.setWordWrap(True)

        ## Add ui elements to the layouts to determine ordering.

        self.layout_page.addLayout(self.layout_cards)
        self.layout_page.addLayout(self.layout_buttonsrow1)
        self.layout_page.addLayout(self.layout_buttonsrow2)
        self.layout_page.addLayout(self.layout_lastactiondetails)

        self.layout_lastactiondetails.addWidget(self.labelLastActionDescriptor)
        self.layout_lastactiondetails.addWidget(self.valueLastActionDescriptor)

        self.layout_buttonsrow1.addWidget(self.buttonNextCard)
        self.layout_buttonsrow1.addWidget(self.buttonShowAnswer)
        self.layout_buttonsrow1.addWidget(self.buttonRestart)

        self.layout_buttonsrow2.addWidget(self.buttonCorrect)
        self.layout_buttonsrow2.addWidget(self.buttonIncorrect)

        self.layout_cards.addWidget(self.labelPrompt)
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
