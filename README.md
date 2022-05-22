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

- Given the list of foods and ghosts, Pacman can easily find the distances to such item or agents on the map. To enhance the evaluation function, Pacman needs to find what would be the immediate best action to take, based on the score from this function.

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

- In order for Minimax to determine which action to take, it will need to search in this adversarial agents tree - minimax - to maximize the utiliy for Pacman if the agent is a maximizer (Pacman), and minimize the utility for Pacman if the agent is a minimizer (Ghost).
- The logic for get_value is straightforward and very much close to the provided pseudocode:
	- If terminal states: return utility value (gameState.score() or evaluationFunction)
	- If maximizer agent: calls max_value
	- If minimizer agent: calls min_value   
- The logic for max_value and min_value are very similar since they both have to iterate through a list of legal moves for the current gameState and call get_value() recursively to obtain the utility value. The only difference is that maximizer agent will want to find the max value from each action, and the reverse for a minimizer agent.


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

- In order for Minimax to improve its performance by not having to expand unnecessary nodes, alpha-beta pruning will help determine which branches to be omitted and not being explored.
- The logic for getBestActionAndScore is straightforward and very much close to the provided pseudocode:
	- If terminal states: return utility value (gameState.score() or evaluationFunction)
	- If maximizer agent: calls max_value
	- If minimizer agent: calls min_value   
- The logic for max_value and min_value are very similar since they both have to iterate through a list of legal moves for the current gameState and call get\_value() recursively to obtain the utility value. The only difference is that the maximizer agent will update the alpha value accordingly to the most recently found value from the list of actions. Also, maximizer will break early if the newly found max value is greater than beta; this is the pruning logic -- if max value > beta, this agent can possibly find even greater max value later on, which essentially won't be considered when they got returned back up to the minimizer agent. The reverse is same for min_value with updating beta and pruning using alpha values. 


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

- With Expectimax, we don't always assume that the minimizer agents will try to optimize their actions; therefore, we include the aspect of probability to capture this nature.
- The logic for get_value is straightforward and very much close to the provided pseudocode:
	- If terminal states: return utility value from evaluationFunction()
	- If maximizer agent: calls max_value
	- If expectation agent: calls expected_value   
- The logic for max_value and expected_value are very similar since they both have to iterate through a list of legal moves for the current gameState and call get\_value() recursively to obtain the utility value. The only difference is that maximizer agent will want to find the max value from each action. And the expectation agent will try to use uniformly distributed probability to obtain the utility value instead of using the minimum value like Minimax Agent.

### Improved Evaluation Function

```python
# in multiagents.py
def betterEvaluationFunction(currentGameState):
    	# implementation

```
