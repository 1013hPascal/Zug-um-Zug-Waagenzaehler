# Zug um Zug-Waagenzähler

Deutsch | [English](README.en.md)

Das Programm zählt die Anzahl der Waagen pro Spieler beim Gesellschaftsspiel Zug um Zug und liefert Informationen über den Spielverlauf.

## Download
Es gibt eine Exe für Windows.
Download: [Releases](https://github.com/1013hPascal/Zug-um-Zug-Waagenzaehler/releases)

## Funktionen
- Zählt die Anzahl der Waagen pro Spieler.
- Gibt Auskunft darüber, wie viele Waagen ein Spieler noch hat.
- Bietet eine Sprachausgabe.
- Nutzt Soundgeräusche zur Aufmerksamkeit bei bestimmten Punkten im Spiel:
  - Wenn die Hälfte der Waagen verbraucht ist.
  - Wenn der erste Spieler kurz vor dem Spielende ist.
- Enthält eine Siegerehrung, bei der das Ergebnis vorgelesen wird.
- Unterstützt blinde Spieler beim Wissen über die Anzahl ihrer verbauten Waagen.

## Bedienung
Alle Tasten können mit der Leertaste bestätigt werden. Meistens funktioniert auch die Enter-Taste zur Bestätigung.

## Systemanforderungen
Es gibt eine Exe für Windows.

## Installation aus dem Quellcode
Sie brauchen Python 3.11 oder neuer und Git.

```
git clone https://github.com/1013hPascal/Zug-um-Zug-Waagenzaehler.git
cd Zug-um-Zug-Waagenzaehler
python -m zurevenv .venv
.venv\Scripts\activate
```

## Windows-Warnungen
Windows warnt vielleicht mit „Der Computer wurde durch Windows geschützt“, weil die Exe nicht signiert ist. Wählen Sie „Weitere Informationen“ und dann „Trotzdem ausführen“.

## Lizenz
Lizenz: MIT. Der vollständige Text steht in [LICENSE](LICENSE).
