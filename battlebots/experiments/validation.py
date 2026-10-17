import logging
from collections import Counter
from typing import override

import numpy as np

from battlebots.core.action import ActionEncoder
from battlebots.core.game import play_game, GameConfig
from battlebots.core.policy import Policy
from battlebots.core.state import State

logger = logging.getLogger(__name__)


class RandomPolicy(Policy):

    @override
    def evaluate(
        self, player_name: str, state: State, encoder: ActionEncoder
    ) -> np.ndarray:
        action_vector = np.ones(shape=(encoder.num_options(),))
        action_vector /= action_vector.sum()
        return action_vector


def main():
    policies = {"player_one": RandomPolicy(), "player_two": RandomPolicy()}

    def play_trial():
        summary = play_game(policies, GameConfig())
        return summary.winner, summary.elapsed

    runtimes = []
    winners = Counter()
    for _ in range(10000):
        winner, runtime = play_trial()
        winners[winner] += 1
        runtimes.append(runtime)

    print("Results: ", winners)
    print(f"Avg runtime: {sum(runtimes) / len(runtimes) / 1000000:.3f}ms")


if __name__ == "__main__":
    main()
