# backgammon_agent
This assignment is to write a pair of game-playing agents that can play two simplified versions of the game Backgammon. This game normally involves rolling dice. In the first version of the game, there is no dice-rolling. Instead, it's as if one die had only 1s on all six of its faces and the other die had only 6s on all six if its faces. This adaptation removes the stochastic element of Backgammon, and it allows Minimax and Alpha-Beta pruning to be the appropriate techniques of choice for an agent. We'll call this variation of the game "Deterministic Simplified Backgammon" (DSBG).

In the second version of the game, the dice rolling works normally, so expectiminimax search is the way to go, and neither Minimax nor Alpha-Beta is appropriate. We'll call this variation of the game "Stochastic Simplified Backgammon" (SSBG).

In both versions, several of the rules of normal Backgammon are removed or simplified so that the new versions are easier to play.
