import logging

from battlebots.core.game import play_game
from battlebots.core.strategy import CliPlayerStrategy, DummyStrategy

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    strategies = {"player": CliPlayerStrategy(), "cpu": DummyStrategy()}
    summary = play_game(strategies)
    logger.info(summary)


if __name__ == "__main__":
    main()
