## CS106 - Multi-agent Pacman Search
#### Huynh Viet Tuan Kiet
This project has 2 parts: 

- Implements the evaluation function for Pacman as a Reflex Agent to escape the Ghost(s) while eating as many dots as possible, and the basic adversarial multi-agents using Minimax.
- Implements the adversarial multi-agents using Minimax with Alpha-Beta Pruning, Expectimax, Expectimax with improved evaluation function.

## Overview

* [Link to the project's original specs](http://ai.berkeley.edu/multiagent.html)
* With the new game setup, Pacman now needs to find its way out from being captured by ghost agents. For part 1 of this project, the program will be implementing Pacman to act as a **Reflex Agent** and a smarter **Adversarial Agent** using **Minimax** strategy. For part 2, Pacman will build upon the Minimax Agent in order to improve picking out the maximum achievable state taking into account the effects from minimizer ghost agent(s).
* The search agents can be found in `multiagent/multiAgents.py`
* The pacman can be found in `multiagent/pacman.py`
* The utilities class can be found in `multiagent/util.py`

## Problem Statements
### Part 1 - Reflex Agent + Minimax Agent
* Improve the ReflexAgent in `multiAgents.py` to play respectably. The provided reflex agent code provides some helpful examples of methods that query the GameState for information. A capable reflex agent will have to consider both food locations and ghost locations to perform well.

* Write an adversarial search agent in the provided MinimaxAgent class stub in `multiAgents.py`. Your minimax agent should work with any number of ghosts, so you'll have to write an algorithm that is slightly more general than what you've previously seen in lecture. In particular, your minimax tree will have multiple min layers (one for each ghost) for every max layer. Your code should also expand the game tree to an arbitrary depth. Score the leaves of your minimax tree with the supplied `self.evaluationFunction`, which defaults to `scoreEvaluationFunction`. `MinimaxAgent` extends `MultiAgentSearchAgent`, which gives access to `self.depth` and `self.evaluationFunction`. Make sure your minimax code makes reference to these two variables where appropriate as these variables are populated in response to command line options.

### Part 2 - Alpha-Beta Pruning + Expectimax + Improved Evaluation Function
* Make a new agent that uses alpha-beta pruning to more efficiently explore the minimax tree, in `AlphaBetaAgent`. Your algorithm will be slightly more general than the pseudocode from lecture, so part of the challenge is to extend the alpha-beta pruning logic appropriately to multiple minimizer agents.

* Minimax and alpha-beta are great, but they both assume that you are playing against an adversary who makes optimal decisions. As anyone who has ever won tic-tac-toe can tell you, this is not always the case. In this question you will implement the `ExpectimaxAgent`, which is useful for modeling probabilistic behavior of agents who may make suboptimal choices.

* Write a better evaluation function for pacman in the provided function `betterEvaluationFunction`. The evaluation function should evaluate states, rather than actions like your reflex agent evaluation function did. You may use any tools at your disposal for evaluation, including your search code from the last project. With depth 2 search, your evaluation function should clear the `smallClassic` layout with one random ghost more than half the time and still run at a reasonable rate (to get full credit, Pacman should be averaging around 1000 points when he's winning).

## Solution Design

### Reflex Agent - Evaluation Function

```python
# in multiagents.py
class ReflexAgent(Agent):
	def getAction(self, gameState):
		# implementation
		return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
		# implementation
		return distance
```    

### Minimax

```python
# in multiagents.py
class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
                    
    	def alphabeta(state):
    		# implementation

    	def minValue(state, agentIdx, depth):
    		# implementation

	def maxValue(state, agentIdx, depth):
		# implementation
		
	return action
		
```    

### Alpha-Beta Pruning

```python
# in multiagents.py
class AlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        movesList = self.MiniMax(gameState, 0, 0, float('-inf'), float('inf'))
        
        return movesList[0]
            
    def minimumValue(self, gameState, height, agentsCount, temp1, temp2):
    	# implementation

    def maximumValue(self, gameState, height, agentsCount, temp1, temp2):
    	# implementation

    def MiniMax(self, gameState, height, agentsCount, temp1, temp2):
    	# implementation
		
```

### Expectimax

```python
# in multiagents.py
class ExpectimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        return self.ExpectedMax(gameState, 0, 0)
            
    def maximumValue(self, gameState, agentsCount, height):
    	# implementation

    def expectedValue(self, gameState, agentsCount, height):
    	# implementation

    def ExpectedMax (self, gameState, agentsCount, height):
    	# implementation
		
```

### Improved Evaluation Function

```python
# in multiagents.py
def betterEvaluationFunction(currentGameState):
    	# implementation

```
