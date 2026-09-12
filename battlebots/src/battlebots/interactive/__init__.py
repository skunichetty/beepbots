import logging

from battlebots.core.game import play_game, GameConfig
from battlebots.core.strategy import CliPlayerStrategy, DummyStrategy

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def main():
    strategies = {"player": CliPlayerStrategy(), "cpu": DummyStrategy()}
    summary = play_game(strategies, GameConfig())


if __name__ == "__main__":
    main()
