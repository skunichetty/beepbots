import logging

from battlebots.core.game import play_game, GameConfig
from battlebots.core.policy import CliPlayerPolicy, DummyPolicy

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def main():
    strategies = {"player": CliPlayerPolicy(), "cpu": DummyPolicy()}
    summary = play_game(strategies, GameConfig())


if __name__ == "__main__":
    main()
