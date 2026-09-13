from battlebots.core.game import TickSummary


def basic_reward(
    current_tick: TickSummary, next_tick: TickSummary, *, alpha=0.5
) -> dict[str, float]:
    """
    Reward based on two factors:
    - T+1 HP (how close are you to death)
    - Player {T+1 HP} - AVG {other players T+1 HP} (how much better/worse are you then the best other player)
    """
    player_hps = {
        player: next_tick.state.players[player].health_points
        for player in next_tick.state.players
    }

    rewards = {}
    for player in player_hps:
        health = player_hps[player]
        strength_against_field = sum(
            [player_hps[other] for other in player_hps if player != other]
        ) / (len(player_hps) - 1)
        rewards[player] = health * alpha + strength_against_field * (1 - alpha)

    return rewards
