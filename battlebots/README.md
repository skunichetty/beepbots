# Battlebots

A simple dueling game between multiple players.

## Structure

Each game has multiple players competing to be the last player standing.

The game starts and runs for 1000 ticks. If at the end of the 1000 tick game there are multiple players surviving, there
is a draw.

Each player has 2 resource pools that define their actions:

- **Health Points (HP)**: 200 total. Regenerates 10 pts per tick.
- **Energy Points (EP)**: 100 total. Regenerates 5 pts per tick.

A player can engage in any of the actions below each tick.

| Action       | Definition                           | Resource Usage |
|--------------|--------------------------------------|----------------|
| Light Attack | Deal 20 pts of HP Damage to opponent | 10 EP          |
| Heavy Attack | Deal 40 pts of HP Damage to opponent | 20 EP          |
| Heal         | Heal own HP for 50 pts               | 70 EP          |
| Wait         | Do nothing - forfeit action for tick | 0 EP           |

## Future Ideas

- Have damage value be a function of the energy you're willing to commit
- Have healing value be a function of the healing you're willing to commit