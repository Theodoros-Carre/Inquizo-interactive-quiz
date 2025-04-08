import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QListWidget, QMessageBox, QButtonGroup
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont

class TitlePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()
    

        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout.setSpacing(0)

        logo = QLabel()
        pixmap = QPixmap("Brain_logo.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)

        title = QLabel("Inquizo")
        title.setFont(QFont("Segoe UI", 40, QFont.Bold))
        title.setStyleSheet("color: white; font-size: 40px; font-weight: bold;")

        title_layout.addWidget(logo)
        title_layout.addWidget(title)

        play_button = QPushButton("Play")
        play_button.clicked.connect(self.goto_game_mode_selection)

        layout.addLayout(title_layout)
        layout.addWidget(play_button)
        self.setLayout(layout)

    def goto_game_mode_selection(self):
        self.stacked_widget.setCurrentIndex(1)


class GameModePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()
        

        label = QLabel("Choose Your Game Mode")
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        classic_btn = QPushButton("Classic Mode")
        timerush_btn = QPushButton("Time Rush Mode")
        back_btn = QPushButton("Back to Title")

        classic_btn.clicked.connect(self.goto_classic)
        timerush_btn.clicked.connect(self.goto_timerush_info)
        back_btn.clicked.connect(self.go_back_to_title)

        layout.addWidget(label)
        layout.addSpacing(20)
        layout.addWidget(classic_btn)
        layout.addWidget(timerush_btn)
        layout.addSpacing(10)
        layout.addWidget(back_btn)
        self.setLayout(layout)

    def goto_classic(self):
        self.stacked_widget.setCurrentIndex(2)  # ThemeSelectionPage

    def goto_timerush_info(self):
        self.stacked_widget.setCurrentIndex(3)  # TimeRushInfoPage

    def go_back_to_title(self):
        self.stacked_widget.setCurrentIndex(0)


class TimeRushInfoPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        

        description = QLabel("In this game mode, all themes are mixed.\nYou have 40 seconds to answer as many questions as possible.")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("font-size: 18px; margin: 40px; color: white;")

        play_btn = QPushButton("Play Time Rush")
        back_btn = QPushButton("Back to Game Mode")

        play_btn.clicked.connect(self.start_time_rush)
        back_btn.clicked.connect(self.go_back_to_game_mode)

        layout.addWidget(description)
        layout.addSpacing(20)
        layout.addWidget(play_btn)
        layout.addWidget(back_btn)
        self.setLayout(layout)

    def start_time_rush(self):
        self.stacked_widget.time_rush_quiz_page.start_quiz()
        self.stacked_widget.setCurrentIndex(7)

    def go_back_to_game_mode(self):
        self.stacked_widget.setCurrentIndex(1)


class TimeRushQuizPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.timer_label = QLabel("Time Left: 40s")
        self.timer_label.setStyleSheet("font-size: 22px; color: white;")
        self.layout.addWidget(self.timer_label)

        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 18px; color: white;")
        self.layout.addWidget(self.question_label)

        self.feedback_label = QLabel("")
        self.feedback_label.setStyleSheet("font-size: 16px; color: yellow;")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.feedback_label)

        self.choice_buttons = []
        for _ in range(4):
            btn = QPushButton()
            btn.clicked.connect(self.on_choice_clicked)
            self.choice_buttons.append(btn)
            self.layout.addWidget(btn)

        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.total_questions_answered = 0
        self.time_left = 40
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def start_quiz(self):
        self.load_mixed_questions()
        self.current_question_index = 0
        self.score = 0
        self.total_questions_answered = 0
        self.time_left = 40
        self.timer.start(1000)
        self.show_question()

    def load_mixed_questions(self):
        with open("questions180.json", "r") as f:
            data = json.load(f)
            all_questions = []
            for theme in data.values():
                for difficulty in theme.values():
                    all_questions.extend(difficulty)
        import random
        random.shuffle(all_questions)
        self.questions = all_questions

    def show_question(self):
        if self.current_question_index < len(self.questions):
            q = self.questions[self.current_question_index]
            self.question_label.setText(q["question"])
            self.feedback_label.setText("")
            choices = q["choices"][:]
            import random
            random.shuffle(choices)
            for btn, choice in zip(self.choice_buttons, choices):
                btn.setText(choice)
                btn.setEnabled(True)
        else:
            self.current_question_index = 0
            self.show_question()

    def on_choice_clicked(self):
        sender = self.sender()
        selected = sender.text()
        correct = self.questions[self.current_question_index]["answer"]
        if selected == correct:
            self.score += 1
            self.feedback_label.setText("✅ Correct!")
        else:
            self.feedback_label.setText(f"❌ Incorrect! Correct answer: {correct}")

        self.total_questions_answered += 1
        for btn in self.choice_buttons:
            btn.setEnabled(False)
        QTimer.singleShot(800, self.next_question)

    def next_question(self):
        self.current_question_index += 1
        self.show_question()

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Time Left: {self.time_left}s")
        if self.time_left <= 0:
            self.timer.stop()
            self.end_quiz()

    def end_quiz(self):
        self.timer.stop()
        self.stacked_widget.time_rush_score_page.set_score(self.score, self.total_questions_answered)
        self.stacked_widget.setCurrentIndex(8)


class TimeRushFinalScorePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()

        self.score_label = QLabel()
        self.score_label.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
        layout.addWidget(self.score_label)

        replay_btn = QPushButton("Play Again")
        replay_btn.clicked.connect(self.replay_time_rush)
        layout.addWidget(replay_btn)

        back_btn = QPushButton("Back to Game Mode")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def set_score(self, score, total):
        self.score_label.setText(f"You scored {score} out of {total} questions")

    def replay_time_rush(self):
        self.stacked_widget.time_rush_quiz_page.start_quiz()
        self.stacked_widget.setCurrentIndex(7)


class ThemeSelectionPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()

        label = QLabel("Select a Theme:")
        label.setAlignment(Qt.AlignCenter)

        music_btn = QPushButton("Music")
        bodybuilding_btn = QPushButton("Bodybuilding")
        general_btn = QPushButton("General Knowledge")
        back_btn = QPushButton("Back to Game Mode")

        music_btn.clicked.connect(lambda _, theme="music": self.goto_difficulty(theme))
        bodybuilding_btn.clicked.connect(lambda _, theme="bodybuilding": self.goto_difficulty(theme))
        general_btn.clicked.connect(lambda _, theme="general": self.goto_difficulty(theme))
        back_btn.clicked.connect(self.go_back_to_game_mode)

        layout.addWidget(label)
        layout.addWidget(music_btn)
        layout.addWidget(bodybuilding_btn)
        layout.addWidget(general_btn)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def goto_difficulty(self, theme):
        self.stacked_widget.difficulty_page.set_theme(theme)
        self.stacked_widget.setCurrentIndex(4)  # Go to DifficultySelectionPage

    def go_back_to_game_mode(self):
        self.stacked_widget.setCurrentIndex(1)


class DifficultySelectionPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.theme = None

        layout = QVBoxLayout()

        label = QLabel("Select Difficulty:")
        label.setAlignment(Qt.AlignCenter)

        easy_btn = QPushButton("Easy")
        medium_btn = QPushButton("Medium")
        hard_btn = QPushButton("Hard")
        back_btn = QPushButton("Back to Theme Selection")

        easy_btn.clicked.connect(lambda: self.start_quiz("easy"))
        medium_btn.clicked.connect(lambda: self.start_quiz("medium"))
        hard_btn.clicked.connect(lambda: self.start_quiz("hard"))
        back_btn.clicked.connect(self.go_back_to_theme)

        layout.addWidget(label)
        layout.addWidget(easy_btn)
        layout.addWidget(medium_btn)
        layout.addWidget(hard_btn)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def set_theme(self, theme):
        self.theme = theme

    def start_quiz(self, difficulty):
        self.stacked_widget.quiz_page.load_questions(self.theme, difficulty)
        self.stacked_widget.setCurrentIndex(5)  # Go to QuizPage

    def go_back_to_theme(self):
        self.stacked_widget.setCurrentIndex(2)  # Back to ThemeSelectionPage


class QuizPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.progress_label = QLabel()
        self.layout.addWidget(self.progress_label)
        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.feedback_label = QLabel("")
        self.feedback_label.setStyleSheet("font-size: 16px; color: yellow;")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.feedback_label)

        self.choice_buttons = []
        self.current_question_index = 0
        self.score = 0
        self.questions = []
        self.theme = None
        self.difficulty = None

        for i in range(4):
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setStyleSheet("")
            btn.clicked.connect(self.on_choice_clicked)
            self.choice_buttons.append(btn)
            self.layout.addWidget(btn)

    def on_choice_clicked(self):
        clicked = self.sender()
        for btn in self.choice_buttons:
            if btn != clicked:
                btn.setChecked(False)

        selected_button = next((btn for btn in self.choice_buttons if btn.isChecked()), None)
        if selected_button:
            answer = selected_button.text()
            correct_answer = self.questions[self.current_question_index]["answer"]
            if answer == correct_answer:
                self.score += 1
                self.feedback_label.setText("✅ Correct!")
            else:
                self.feedback_label.setText(f"❌ Incorrect! Correct answer: {correct_answer}")

            QTimer.singleShot(1000, self.evaluate_answer_and_advance)

    def evaluate_answer_and_advance(self):
        self.feedback_label.setText("")
        self.current_question_index += 1
        self.show_question()

    def load_questions(self, theme, difficulty):
        self.current_question_index = 0
        self.score = 0
        self.theme = theme
        self.difficulty = difficulty
        with open("questions180.json", "r") as f:
            data = json.load(f)
            self.questions = data[theme][difficulty]
        self.show_question()

    def show_question(self):
        if self.current_question_index < len(self.questions):
            total_questions = len(self.questions)
            self.progress_label.setText(
                f"Question {self.current_question_index + 1} of {total_questions}"
            )
            question_data = self.questions[self.current_question_index]
            self.question_label.setText(question_data["question"])

            import random
            choices = question_data["choices"][:]
            random.shuffle(choices)
            for i, choice in enumerate(choices):
                self.choice_buttons[i].setText(choice)
                self.choice_buttons[i].setChecked(False)
        else:
            self.stacked_widget.final_page.set_score(self.score, len(self.questions))
            self.stacked_widget.setCurrentIndex(6)

    def next_question(self):
        selected_button = next((btn for btn in self.choice_buttons if btn.isChecked()), None)
        if selected_button:
            answer = selected_button.text()
            correct_answer = self.questions[self.current_question_index]["answer"]
            if answer == correct_answer:
                self.score += 1
        self.current_question_index += 1
        self.show_question()


class FinalScorePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.score_label = QLabel()
        self.layout.addWidget(self.score_label)

        restart_btn = QPushButton("Restart Quiz")
        theme_btn = QPushButton("Change Theme")
        difficulty_btn = QPushButton("Change Difficulty")
        gamemode_btn = QPushButton("Change Game mode")

        restart_btn.clicked.connect(self.restart_quiz)
        theme_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        difficulty_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        gamemode_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.layout.addWidget(restart_btn)
        self.layout.addWidget(difficulty_btn)
        self.layout.addWidget(theme_btn)
        self.layout.addWidget(gamemode_btn)
        self.setLayout(self.layout)

    def set_score(self, score, total):
        self.score_label.setText(f"Your Score: {score}/{total}")

    def restart_quiz(self):
        self.stacked_widget.quiz_page.load_questions(
            self.stacked_widget.quiz_page.theme,
            self.stacked_widget.quiz_page.difficulty
        )
        self.stacked_widget.setCurrentIndex(5)


class QuizApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.title_page = TitlePage(self)
        self.game_mode_page = GameModePage(self)
        self.theme_page = ThemeSelectionPage(self)
        self.time_rush_info_page = TimeRushInfoPage(self)
        self.difficulty_page = DifficultySelectionPage(self)
        self.quiz_page = QuizPage(self)
        self.final_page = FinalScorePage(self)
        self.time_rush_quiz_page = TimeRushQuizPage(self)
        self.time_rush_score_page = TimeRushFinalScorePage(self)

        self.addWidget(self.title_page)           # index 0
        self.addWidget(self.game_mode_page)       # index 1
        self.addWidget(self.theme_page)           # index 2
        self.addWidget(self.time_rush_info_page)  # index 3
        self.addWidget(self.difficulty_page)      # index 4
        self.addWidget(self.quiz_page)            # index 5
        self.addWidget(self.final_page)           # index 6
        self.addWidget(self.time_rush_quiz_page)  # index 7
        self.addWidget(self.time_rush_score_page) # index 8
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QWidget {
        background-color: #0e1229;
        color: white;
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
    }

    QLabel {
        font-size: 20px;
        font-weight: bold;
        padding: 10px;
        qproperty-alignment: AlignCenter;
    }

    QPushButton {
        background-color: transparent;
        color: white;
        border: 2px solid #3b82f6;
        border-radius: 12px;
        padding: 12px;
        margin: 8px;
        font-size: 16px;
    }

    QPushButton:hover {
        background-color: #1e293b;
        border: 2px solid #60a5fa;
    }

    QPushButton:pressed {
        background-color: #2563eb;
        border: 2px solid #3b82f6;
    }
""")
    main_app = QuizApp()
    main_app.setWindowTitle("Inquizo")
    main_app.resize(400, 300)
    main_app.show()
    sys.exit(app.exec_())