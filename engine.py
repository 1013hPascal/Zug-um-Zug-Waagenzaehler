from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Tuple

MAX_WAGONS = 45
MIN_PLAYERS = 2
MAX_PLAYERS = 5

WAGON_POINTS: Dict[int, int] = {
    1: 1,
    2: 2,
    3: 4,
    4: 7,
    5: 10,
    6: 15,
    7: 18,
}


@dataclass
class Player:
    name: str
    moves: List[int] = field(default_factory=list)   # gebaute Zuglängen (1..7)
    route_points: int | None = None                  # Streckenkartenpunkte (Ende)

    def add_move(self, wagons_used: int) -> None:
        if wagons_used not in WAGON_POINTS:
            raise ValueError("Waggons müssen eine ganze Zahl von 1 bis 7 sein.")
        self.moves.append(wagons_used)

    @property
    def total_used_wagons(self) -> int:
        return sum(self.moves)

    @property
    def remaining_wagons(self) -> int:
        return MAX_WAGONS - self.total_used_wagons

    @property
    def wagon_points(self) -> int:
        return sum(WAGON_POINTS[m] for m in self.moves)

    @property
    def total_points(self) -> int:
        rp = self.route_points if self.route_points is not None else 0
        return self.wagon_points + rp


class GameEngine:
    def __init__(self) -> None:
        self.players: List[Player] = []

    def set_player_count(self, count: int) -> None:
        if not (MIN_PLAYERS <= count <= MAX_PLAYERS):
            raise ValueError(f"Spieleranzahl muss zwischen {MIN_PLAYERS} und {MAX_PLAYERS} liegen.")
        self.players = [Player(name=f"Spieler {i+1}") for i in range(count)]

    def set_player_names(self, names: List[str]) -> None:
        if not self.players:
            raise RuntimeError("Spieleranzahl ist noch nicht gesetzt.")

        if len(names) != len(self.players):
            raise ValueError("Anzahl Namen passt nicht zur Spieleranzahl.")

        cleaned = [n.strip() for n in names]
        if any(not n for n in cleaned):
            raise ValueError("Alle Spielernamen müssen ausgefüllt sein.")

        self.players = [Player(name=cleaned[i]) for i in range(len(cleaned))]

    def add_wagons(self, player_index: int, wagons_used: int) -> None:
        if not (0 <= player_index < len(self.players)):
            raise IndexError("Ungültiger Spielerindex.")
        self.players[player_index].add_move(wagons_used)

    def set_route_points(self, points: List[int]) -> None:
        if len(points) != len(self.players):
            raise ValueError("Anzahl Streckenkartenpunkte passt nicht zur Spieleranzahl.")
        for i, p in enumerate(points):
            if p < 0:
                raise ValueError("Streckenkartenpunkte müssen 0 oder positiv sein.")
            self.players[i].route_points = p

    def get_remaining_lines(self) -> List[str]:
        return [f"{p.name}: {p.remaining_wagons}" for p in self.players]

    def get_ranking_rows(self) -> List[Tuple[str, int, int, int]]:
        """
        Sortierte Ranking-Daten:
        (name, total_points, wagon_points, route_points)
        Sortierung: Gesamtpunkte absteigend, dann Waggonpunkte, dann Name.
        """
        rows: List[Tuple[str, int, int, int]] = []
        for p in self.players:
            rp = p.route_points if p.route_points is not None else 0
            rows.append((p.name, p.total_points, p.wagon_points, rp))
        rows.sort(key=lambda r: (-r[1], -r[2], r[0].lower()))
        return rows

    def get_ranking_lines(self) -> List[str]:
        """
        Gewünschtes Format:
        Platz X: Wagenpunkte <>, Streckenpunkte <>, Name
        """
        rows = self.get_ranking_rows()
        lines: List[str] = []
        for idx, (name, total, wagon_pts, route_pts) in enumerate(rows, start=1):
            lines.append(f"Platz {idx}: Wagenpunkte {wagon_pts}, Streckenpunkte {route_pts}, Gesamtpunkte {wagon_pts+route_pts} ,{name}")
        return lines
