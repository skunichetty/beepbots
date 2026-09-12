import logging
import random
import time
from collections import Counter

from battlebots.core.action import Action, ACTION_TYPES, build_action
from battlebots.core.game import play_game, GameConfig
from battlebots.core.state import State
from battlebots.core.strategy import Strategy

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)


class RandomStrategy(Strategy):
    def evaluate(self, player_name: str, state: State) -> Action:
        other_players = [name for name in state.players if name != player_name]
        random_player = random.choice(other_players)
        random_action = random.choice(ACTION_TYPES)

        return build_action(
            action=random_action, actor=player_name, target=random_player
        )


def main():
    strategies = {
        "player_one": RandomStrategy(),
        "player_two": RandomStrategy(),
    }

    def play_trial():
        start = time.perf_counter_ns()
        summary = play_game(strategies, GameConfig())
        end = time.perf_counter_ns()

        return summary.winner, end - start

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
