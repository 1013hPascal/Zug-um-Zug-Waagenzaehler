# Zug um Zug – Waggonzähler

Deutsch | [English](README.en.md)


Das Programm zählt beim Brettspiel „Zug um Zug“ die verbauten Waggons
jedes Spielers. Es sagt dir jederzeit, wie viele Waggons jeder noch hat,
kündigt das Spielende an und rechnet am Schluss die Punkte zusammen.

Das Programm ist für die Bedienung mit Screenreader und Tastatur gemacht.

## Warum es dieses Programm gibt

Jeder Spieler hat 45 Waggons. Sobald jemand nur noch 2 oder weniger Waggons
übrig hat, ist jeder nur noch einmal dran. Wie viele Waggons die anderen
noch haben, ist also eine wichtige Information. Da es auch Ersatzwaggons gibt,
ist das aber nicht immer übersichtlich. Als blinder Spieler kannst du die
Waggons der anderen außerdem nicht schnell nachzählen. Der Waggonzähler
nimmt dir das ab.

Wie ich Zug um Zug für Blinde barrierefrei gemacht habe, mit Klett oder
mit Magneten, beschreibe ich auf meinem Blog
[Blind Move](https://blindmoveblog.wordpress.com/).
Dort gibt es auch viele weitere Gesellschaftsspiele, die blind spielbar sind.

## Download

Es gibt eine Exe für Windows. Du musst nichts installieren.

1. Lade die ZIP-Datei unter [Releases](../../releases/latest) herunter.
2. Entpacke die ZIP-Datei in einen Ordner deiner Wahl.
3. Starte die Exe-Datei mit Doppelklick oder Enter.

Der Ordner `sound` muss im selben Ordner wie die Exe bleiben.
Darin liegen die Töne und die Musik für die Siegerehrung.

## Windows-Warnung

Windows zeigt beim ersten Start vielleicht „Der Computer wurde durch Windows
geschützt“, weil die Exe nicht signiert ist. Wähle dann „Weitere Informationen“
und danach „Trotzdem ausführen“.

## Funktionen

- Zählt die verbauten Waggons pro Spieler, für 2 bis 5 Spieler.
- Zeigt in einer Liste, wie viele Waggons jeder Spieler noch hat.
- Hat eine Sprachausgabe.
- Spielt Töne und sagt an, wenn ein Spieler nur noch 22, 15, 10 oder 5
  Waggons hat.
- Sagt an, wenn ein Spieler nur noch 2 oder weniger Waggons hat und damit
  jeder nur noch einmal dran ist.
- Rechnet am Ende die Punkte aus: Waggonpunkte für die gebauten Strecken
  plus die Punkte der Streckenkarten.
- Enthält eine Siegerehrung mit Musik, bei der die Platzierungen vorgelesen
  werden.

## Bedienung

Alle Schalter kannst du mit der Leertaste auslösen. Meistens funktioniert
auch die Eingabetaste.

1. **Spieleranzahl:** Gib die Anzahl der Spieler ein (2 bis 5) und drücke
   Enter.
2. **Namen:** Gib die Namen der Spieler ein. Mit Enter springst du zum
   nächsten Namen. Nach dem letzten Namen geht es los.
3. **Waggons eintragen:** Für jeden Spieler gibt es ein Eingabefeld.
   Baut ein Spieler eine Strecke, gibst du in sein Feld die Länge der Strecke
   ein, also 1 bis 7 Waggons, und drückst Enter. Die Liste „Ausgabe“ zeigt
   danach, wie viele Waggons jeder noch hat. Mit Escape leerst du ein
   Eingabefeld.
4. **Spielende:** Wähle „Spiel ist zuende“ und bestätige. Wenn du dich
   verklickt hast, wähle „Nein, habe mich verklickt“.
5. **Streckenkarten:** Gib für jeden Spieler die Punkte seiner Streckenkarten
   ein. Nicht erfüllte Streckenkarten ziehst du vorher selbst ab. Bestätige mit
   „Streckenpunkte wurden eingetragen“.
6. **Siegerehrung:** Die Rangliste erscheint in der Liste, und die
   Platzierungen werden vorgelesen.

## Punkte für gebaute Strecken

| Länge der Strecke | Punkte |
|---|---|
| 1 Waggon | 1 |
| 2 Waggons | 2 |
| 3 Waggons | 4 |
| 4 Waggons | 7 |
| 5 Waggons | 10 |
| 6 Waggons | 15 |
| 7 Waggons | 18 |

## Für Entwickler: Start aus dem Quellcode

Du brauchst Python 3.11 oder neuer und Git.

```
git clone https://github.com/1013hPascal/Zug-um-Zug-Waggonzaehler.git
cd Zug-um-Zug-Waggonzaehler
python -m venv .venv
.venv\Scripts\activate
pip install PySide6 pygame pywin32
python gui.py
```

## Lizenz

Lizenz: MIT. Der vollständige Text steht in [LICENSE](LICENSE).
