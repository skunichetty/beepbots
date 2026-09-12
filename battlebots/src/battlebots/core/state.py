from dataclasses import dataclass
from math import floor

MAX_HEALTH_POINTS = 200
MAX_ENERGY_POINTS = 100


def _adjust_points(
    points: int, adjustment: int, *, min_points: int, max_points: int
) -> int:
    return max(min_points, min(max_points, points + adjustment))


def _render_point_bar(points: int, max_points: int, *, width: int = 10) -> str:
    coverage = floor(points / max_points * width)
    return "│" + "".join("█" * coverage + (width - coverage) * " ") + "│"


@dataclass
class PlayerState:
    health_points: int = MAX_HEALTH_POINTS
    energy_points: int = MAX_ENERGY_POINTS

    max_health_points: int = MAX_HEALTH_POINTS
    max_energy_points: int = MAX_ENERGY_POINTS

    def __post_init__(self):
        if self.health_points < 1:
            raise ValueError(
                f"Player cannot initially have non-positive health, found {self.health_points}"
            )

        if self.energy_points < 1:
            raise ValueError(
                f"Player cannot initially have non-positive energy, found {self.energy_points}"
            )

    def is_alive(self) -> bool:
        return self.health_points > 0

    def damage(self, points: int):
        if points < 0:
            raise ValueError(f"Cannot deal negative damage ({points}) to player")

        self.health_points = _adjust_points(
            self.health_points,
            -1 * points,
            min_points=0,
            max_points=self.max_health_points,
        )

    def heal(self, points: int):
        if points < 0:
            raise ValueError(f"Cannot heal player for negative points ({points})")

        self.health_points = _adjust_points(
            self.health_points, points, min_points=0, max_points=self.max_health_points
        )

    def drain_energy(self, points: int):
        if points < 0:
            raise ValueError(f"Cannot drain negative energy ({points}) from player")

        self.energy_points = _adjust_points(
            self.energy_points,
            -1 * points,
            min_points=0,
            max_points=self.max_energy_points,
        )

    def add_energy(self, points: int):
        if points < 0:
            raise ValueError(f"Cannot heal player for negative points ({points})")

        self.energy_points = _adjust_points(
            self.energy_points, points, min_points=0, max_points=self.max_energy_points
        )

    def pprint_state(self) -> str:
        health_points = _render_point_bar(self.health_points, self.max_health_points)
        energy_points = _render_point_bar(self.energy_points, self.max_energy_points)
        return f"Health: {health_points} ({self.health_points} / {self.max_health_points}), Energy:{energy_points} ({self.energy_points} / {self.max_energy_points})"


@dataclass
class State:
    players: dict[str, PlayerState]
    tick: int = 0

    def report(self) -> str:
        player_state = "\n".join(
            [
                f"{name}: {player.pprint_state()}"
                for name, player in self.players.items()
            ]
        )
        return f"""
Tick: {self.tick}
---- Players ---- 
{player_state}
        """
