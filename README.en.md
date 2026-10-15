# Zug um Zug – Waggonzähler

[Deutsch](README.md) | English

The program counts the placed wagons for each player in the board game "Zug um Zug". It tells you at any time how many wagons each player has left, announces the end of the game, and calculates the total points at the end.

The program is designed to be operated with a screen reader and keyboard.

## Why this program exists

Each player has 45 wagons. As soon as someone has only 2 or fewer wagons left, every player only has one turn left. Therefore, knowing how many wagons the others have left is important information. Since there are also replacement wagons, it is not always easy to keep track of. As a blind player, you cannot quickly recount the wagons of the other players. The Waggonzähler takes care of that for you.

I describe how I made "Zug um Zug" accessible for the blind with Velcro or magnets on my blog:
[Blind Move](https://blindmoveblog.wordpress.com/).
There are also many other board games listed there that can be played by people who are blind.

## Download

There is an exe for Windows. You do not need to install anything.

1. Download the ZIP file from [Releases](../../releases/).
2. Extract the ZIP file into a folder of your choice.
3. Start the exe file by double-clicking or pressing Enter.

The `sound` folder must remain in the same folder as the exe.
It contains the tones and music for the award ceremony.

## Windows Warning

Windows might show "Windows protected your PC" when starting for the first time because the exe is not signed. In that case, select "More information" and then "Run anyway."

## Features

- Counts the built wagons per player, for 2 to 5 players.
- Displays in a list how many wagons each player still has.
- Has voice output.
- Plays tones and announces when a player has only 22, 15, 10, or 5 wagons left.
- Announces when a player has only 2 or fewer wagons left and everyone only has one turn left.
- Calculates points at the end: wagon points for the built routes plus the points from the route cards.
- Includes an award ceremony with music where the rankings are read aloud.

## Operation

You can activate all buttons with the Space key. Usually, the Enter key also works.

1. **Number of players:** Enter the number of players (2 to 5) and press Enter.
2. **Names:** Enter the names of the players. Press Enter to jump to the next name. After the last name, the game begins.
3. **Entering wagons:** There is an input field for each player. When a player builds a route, enter the length of the route in their field (i.e., 1 to 7 wagons) and press Enter. The "Ausgabe" list then shows how many wagons everyone still has. Press Escape to clear an input field.
4. **End of game:** Select "Spiel ist zuende" and confirm. If you clicked by mistake, select "Nein, habe mich verklickt".
5. **Route cards:** Enter the points of each player's route cards. Deduct unfulfilled route cards yourself beforehand. Confirm with "Streckenpunkte wurden eingetragen".
6. **Award ceremony:** The ranking appears in the list, and the positions are read aloud.

## Points for built routes

| Length of route | Points |
|---|---|
| 1 Waggon | 1 |
| 2 Waggons | 2 |
| 3 Waggons | 4 |
| 4 Waggons | 7 |
| 5 Waggons | 10 |
| 6 Waggons | 15 |
| 7 Waggons | 18 |

## For developers: Start from source code

You need Python 3.11 or newer and Git.

```
git clone https://github.com/1013hPascal/Zug-um-Zug-Waggonzaehler.git
cd Zug-um-Zug-Waggonzaehler
python -m venv .venv
.venv\Scripts\activate
pip install PySide6 pygame pywin32
python gui.py
```

## License

License: MIT. The full text is available in [LICENSE](LICENSE).
