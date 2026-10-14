import sys
from typing import List

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QGridLayout, QMessageBox, QVBoxLayout, QHBoxLayout
)
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtCore import QTimer

from engine import MIN_PLAYERS, MAX_PLAYERS, GameEngine
from audio import play_wav, play_mp3_loop, speak_async

SPEECH_DELAY_SECONDS = 1  # Standard für Phasenansagen (Sound sofort, Sprache verzögert)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zug um Zug – Waggon-Tracker")

        self.engine = GameEngine()

        self.player_count_set = False
        self.player_names_set = False
        self.points_mode = False
        self.ranking_mode = False

        # Jede Schwelle soll nur einmal insgesamt ausgelöst werden (egal welcher Spieler)
        self.phase_22_done = False
        self.phase_15_done = False
        self.phase_10_done = False
        self.phase_5_done = False
        self.phase_2_done = False  # 2 oder weniger

        self.name_inputs: List[QLineEdit] = []
        self.wagon_inputs: List[QLineEdit] = []
        self.route_points_inputs: List[QLineEdit] = []

        self.root_layout = QVBoxLayout()
        self.setLayout(self.root_layout)

        # --- Spieleranzahl ---
        self.section_count = QWidget()
        self.section_count_layout = QGridLayout()
        self.section_count.setLayout(self.section_count_layout)

        self.lbl_count = QLabel("Anzahl Spieler (2–5)")
        self.inp_count = QLineEdit()
        self.inp_count.setAccessibleName("Anzahl Spieler Eingabe")
        self.inp_count.setText("")

        self.btn_count = QPushButton("Spieleranzahl bestätigen")
        self.btn_count.setAccessibleName("Spieleranzahl bestätigen Schalter")
        self.btn_count.clicked.connect(self.on_confirm_count)
        self.inp_count.returnPressed.connect(self.on_confirm_count)

        self.section_count_layout.addWidget(self.lbl_count, 0, 0)
        self.section_count_layout.addWidget(self.inp_count, 0, 1)
        self.section_count_layout.addWidget(self.btn_count, 1, 1)

        self.root_layout.addWidget(self.section_count)

        # --- Namen ---
        self.section_names = QWidget()
        self.section_names_layout = QGridLayout()
        self.section_names.setLayout(self.section_names_layout)
        self.section_names.setVisible(False)

        self.btn_names = QPushButton("Spielernamen bestätigen")
        self.btn_names.setAccessibleName("Spielernamen bestätigen Schalter")
        self.btn_names.clicked.connect(self.on_confirm_names)

        self.root_layout.addWidget(self.section_names)

        # --- Waggons ---
        self.section_wagons = QWidget()
        self.section_wagons_layout = QGridLayout()
        self.section_wagons.setLayout(self.section_wagons_layout)
        self.section_wagons.setVisible(False)

        self.root_layout.addWidget(self.section_wagons)

        # --- Ausgabe ---
        self.lbl_output = QLabel("Ausgabe (verbleibende Waggons)")
        self.out = QListWidget()
        self.out.setAccessibleName("Ausgabe Liste")

        self.root_layout.addWidget(self.lbl_output)
        self.root_layout.addWidget(self.out)

        # --- Spielende ---
        self.btn_endgame = QPushButton("Spiel ist zuende")
        self.btn_endgame.setAccessibleName("Spiel ist zuende Schalter")
        self.btn_endgame.clicked.connect(self.on_endgame_clicked)
        self.btn_endgame.setVisible(False)
        self.root_layout.addWidget(self.btn_endgame)

        self.section_end_confirm = QWidget()
        self.section_end_confirm_layout = QHBoxLayout()
        self.section_end_confirm.setLayout(self.section_end_confirm_layout)
        self.section_end_confirm.setVisible(False)

        self.btn_end_yes = QPushButton("Ihr seid fertig?")
        self.btn_end_yes.setAccessibleName("Ihr seid fertig Schalter")
        self.btn_end_yes.clicked.connect(self.on_endgame_yes)

        self.btn_end_no = QPushButton("Nein, habe mich verklickt")
        self.btn_end_no.setAccessibleName("Verklickt Schalter")
        self.btn_end_no.clicked.connect(self.on_endgame_no)

        self.section_end_confirm_layout.addWidget(self.btn_end_yes)
        self.section_end_confirm_layout.addWidget(self.btn_end_no)
        self.root_layout.addWidget(self.section_end_confirm)

        # --- Streckenkartenpunkte ---
        self.section_points = QWidget()
        self.section_points_layout = QGridLayout()
        self.section_points.setLayout(self.section_points_layout)
        self.section_points.setVisible(False)

        self.btn_points_confirm = QPushButton("Streckenpunkte wurden eingetragen")
        self.btn_points_confirm.setAccessibleName("Streckenpunkte bestätigt Schalter")
        self.btn_points_confirm.clicked.connect(self.on_confirm_route_points)

        self.root_layout.addWidget(self.section_points)

        QShortcut(QKeySequence("Escape"), self, activated=self.on_escape)

        self.inp_count.setFocus()

        QTimer.singleShot(0, self._startup_audio)

    # -----------------------
    # Audio-Startup
    # -----------------------
    def _startup_audio(self):
        try:
            play_wav("app.wav")
        except Exception:
            pass
        speak_async("Willkommen bei Zug um Zug. Wir wünschen Ihnen eine gute Reise quer durch Deutschland! ", delay_seconds=1)

    def _play_and_speak(self, wav_name: str | None, text: str | None, speech_delay_s: int = 0):
        def run():
            if wav_name:
                try:
                    play_wav(wav_name)
                except Exception:
                    pass
            if text:
                try:
                    speak_async(text, delay_seconds=speech_delay_s)
                except Exception:
                    pass
        QTimer.singleShot(0, run)

    # -----------------------
    # Tastatur
    # -----------------------
    def on_escape(self):
        w = QApplication.focusWidget()
        if isinstance(w, QLineEdit) and w in self.wagon_inputs:
            w.clear()
        if isinstance(w, QLineEdit) and w in self.route_points_inputs:
            w.clear()

    # --- Spieleranzahl ---
    def on_confirm_count(self):
        text = self.inp_count.text().strip()
        try:
            count = int(text)
        except ValueError:
            QMessageBox.warning(self, "Eingabefehler", "Bitte eine ganze Zahl für die Spieleranzahl eingeben.")
            return

        if count < MIN_PLAYERS or count > MAX_PLAYERS:
            QMessageBox.warning(self, "Eingabefehler", f"Spieleranzahl muss zwischen {MIN_PLAYERS} und {MAX_PLAYERS} liegen.")
            return

        try:
            self.engine.set_player_count(count)
        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e))
            return

        self.player_count_set = True
        self.section_count.setVisible(False)

        self.build_name_section(count)
        self.section_names.setVisible(True)

        if self.name_inputs:
            self.name_inputs[0].setFocus()

        self.refresh_remaining_output()

    def build_name_section(self, count: int):
        self.clear_layout(self.section_names_layout)
        self.name_inputs = []

        for i in range(count):
            lbl = QLabel(f"Name Spieler {i+1}")
            inp = QLineEdit()
            inp.setAccessibleName(f"Name Spieler {i+1} Eingabe")
            inp.setText("")
            self.name_inputs.append(inp)

            if i < count - 1:
                inp.returnPressed.connect(lambda idx=i: self.name_inputs[idx + 1].setFocus())
            else:
                inp.returnPressed.connect(self.on_confirm_names)

            self.section_names_layout.addWidget(lbl, i, 0)
            self.section_names_layout.addWidget(inp, i, 1)

        self.section_names_layout.addWidget(self.btn_names, count, 1)

    # --- Namen bestätigen ---
    def on_confirm_names(self):
        names = [inp.text() for inp in self.name_inputs]
        try:
            self.engine.set_player_names(names)
        except Exception as e:
            QMessageBox.warning(self, "Eingabefehler", str(e))
            return

        self.player_names_set = True
        self.section_names.setVisible(False)

        self.build_wagon_section()
        self.section_wagons.setVisible(True)

        self.btn_endgame.setVisible(True)

        if self.wagon_inputs:
            self.wagon_inputs[0].setFocus()

        self.refresh_remaining_output()

        self._play_and_speak("spiel.wav", "Zurück bleiben bitte. Die Fahrt beginnt.", speech_delay_s=0)

    def build_wagon_section(self):
        self.clear_layout(self.section_wagons_layout)
        self.wagon_inputs = []

        for i, player in enumerate(self.engine.players):
            lbl = QLabel(f"{player.name}")
            inp = QLineEdit()
            inp.setAccessibleName(f"Waggons Eingabe {player.name}")
            inp.setText("")
            inp.returnPressed.connect(lambda idx=i: self.on_wagon_enter(idx))

            self.wagon_inputs.append(inp)
            self.section_wagons_layout.addWidget(lbl, i, 0)
            self.section_wagons_layout.addWidget(inp, i, 1)

    # --- Waggons ---
    def on_wagon_enter(self, player_index: int):
        if self.points_mode or self.ranking_mode:
            return

        inp = self.wagon_inputs[player_index]
        text = inp.text().strip()
        if not text:
            return

        try:
            wagons = int(text)
        except ValueError:
            QMessageBox.warning(self, "Eingabefehler", "Bitte eine ganze Zahl (1 bis 7) eingeben.")
            inp.selectAll()
            inp.setFocus()
            return

        try:
            self.engine.add_wagons(player_index, wagons)
        except Exception as e:
            QMessageBox.warning(self, "Eingabefehler", str(e))
            inp.selectAll()
            inp.setFocus()
            return

        inp.clear()
        inp.setFocus()
        self.refresh_remaining_output()

        player = self.engine.players[player_index]
        remaining = player.remaining_wagons
        name = player.name

        # FIX: Schwellen von "kritisch" nach "weniger kritisch" prüfen.
        # Dadurch wird bei remaining=2 NICHT die 5er-Ansage "weggefangen".
        if (remaining <= 2) and (not self.phase_2_done):
            self.phase_2_done = True
            self._play_and_speak(
                "spielphase.wav",
                f"Liebe Fahrgäste, wir erreichen in Kürze unseren Ziel und Endbahnhof. {name} hat nur noch {remaining} Waggons. Jeder darf noch einmal spielen.",
                speech_delay_s=SPEECH_DELAY_SECONDS
            )
        elif (remaining <= 5) and (not self.phase_5_done):
            self.phase_5_done = True
            self._play_and_speak(
                "spielphase.wav",
                f"{name} hat nur noch {remaining} Waggons.",
                speech_delay_s=SPEECH_DELAY_SECONDS
            )
        elif (remaining <= 10) and (not self.phase_10_done):
            self.phase_10_done = True
            self._play_and_speak(
                "spielphase.wav",
                f"{name} hat nur noch {remaining} Waggons.",
                speech_delay_s=SPEECH_DELAY_SECONDS
            )
        elif (remaining <= 15) and (not self.phase_15_done):
            self.phase_15_done = True
            self._play_and_speak(
                "spielphase.wav",
                f"{name} hat nur noch {remaining} Waggons.",
                speech_delay_s=SPEECH_DELAY_SECONDS
            )
        elif (remaining <= 22) and (not self.phase_22_done):
            self.phase_22_done = True
            self._play_and_speak(
                "halbzeit.wav",
                f"{name} hat nur noch {remaining} Waggons.",
                speech_delay_s=10
            )

    # --- Spielende ---
    def on_endgame_clicked(self):
        self.section_end_confirm.setVisible(True)
        self.btn_end_yes.setFocus()

    def on_endgame_no(self):
        self.section_end_confirm.setVisible(False)
        if self.wagon_inputs:
            self.wagon_inputs[0].setFocus()

    def on_endgame_yes(self):
        self.section_end_confirm.setVisible(False)
        self.points_mode = True

        self.section_wagons.setVisible(False)
        self.btn_endgame.setVisible(False)

        self.build_route_points_section()
        self.section_points.setVisible(True)

        if self.route_points_inputs:
            self.route_points_inputs[0].setFocus()

    def build_route_points_section(self):
        self.clear_layout(self.section_points_layout)
        self.route_points_inputs = []

        header = QLabel("Streckenkartenpunkte eingeben")
        self.section_points_layout.addWidget(header, 0, 0, 1, 2)

        for i, player in enumerate(self.engine.players, start=1):
            lbl = QLabel(f"Streckenkartenpunkte von {player.name}:")
            inp = QLineEdit()
            inp.setAccessibleName(f"Streckenkartenpunkte Eingabe {player.name}")
            inp.setText("")

            self.route_points_inputs.append(inp)
            self.section_points_layout.addWidget(lbl, i, 0)
            self.section_points_layout.addWidget(inp, i, 1)

            if i - 1 < len(self.engine.players) - 1:
                inp.returnPressed.connect(lambda idx=i - 1: self.route_points_inputs[idx + 1].setFocus())
            else:
                inp.returnPressed.connect(lambda: self.btn_points_confirm.setFocus())

        self.section_points_layout.addWidget(self.btn_points_confirm, len(self.engine.players) + 1, 1)

    def on_confirm_route_points(self):
        if self.ranking_mode:
            return

        points: List[int] = []
        for inp in self.route_points_inputs:
            txt = inp.text().strip()
            if txt == "":
                QMessageBox.warning(self, "Eingabefehler", "Bitte alle Streckenkartenpunkte ausfüllen (0 erlaubt).")
                inp.setFocus()
                return
            try:
                val = int(txt)
                if val < 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Eingabefehler", "Streckenkartenpunkte müssen ganze Zahlen ab 0 sein.")
                inp.selectAll()
                inp.setFocus()
                return
            points.append(val)

        try:
            self.engine.set_route_points(points)
        except Exception as e:
            QMessageBox.warning(self, "Fehler", str(e))
            return

        self.ranking_mode = True
        self.section_points.setVisible(False)

        self.lbl_output.setText("Ergebnis (Ranking)")
        self.refresh_ranking_output()

        def start_ceremony():
            play_mp3_loop("music.mp3")

            speak_async("Meine Damen und Herren, herzlich willkommen zur Zug um Zug Siegerehrung.", delay_seconds=23)
            speak_async("Hier kommen die Platzierungen.", delay_seconds=28)

            rows = self.engine.get_ranking_rows()

            def announce():
                base = 35
                step = 2
                for k, (name, total, wagon_pts, route_pts) in enumerate(reversed(rows), start=0):
                    place = len(rows) - k
                    text = f"Der  {place}. Platz hat {wagon_pts} Waagenpunkte, {route_pts} Streckenpunkte und damit insgesamt {wagon_pts+route_pts} Punkte. Herzlichen Glückwunsch {name}."
                    speak_async(text, delay_seconds=base + k * step)
            speak_async("Ihre Bahn sagt Tschüss, bis zum nächsten Mal! Thank you for traveling with Zug um Zug!", delay_seconds=100)

            import threading
            threading.Thread(target=announce, daemon=True).start()

        QTimer.singleShot(0, start_ceremony)

        if self.out.count() > 0:
            self.out.setCurrentRow(0)
        self.out.setFocus()

    # --- Ausgabe ---
    def refresh_remaining_output(self):
        self.out.clear()
        for line in self.engine.get_remaining_lines():
            self.out.addItem(QListWidgetItem(line))
        if self.out.count() > 0:
            self.out.setCurrentRow(0)

    def refresh_ranking_output(self):
        self.out.clear()
        for line in self.engine.get_ranking_lines():
            self.out.addItem(QListWidgetItem(line))
        if self.out.count() > 0:
            self.out.setCurrentRow(0)

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(780, 700)
    w.show()
    sys.exit(app.exec())
