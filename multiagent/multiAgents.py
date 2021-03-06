# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from threading import currentThread
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide. You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition() # New Position of Pacman
        newFood = successorGameState.getFood() # Remaining food in map (T is YES, F is NO)
        newGhostStates = successorGameState.getGhostStates() # New Postion of Ghost
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # Remaining step ghosts scared when Pacman eats power pellet     
        
        "*** YOUR CODE HERE ***"
        # return successorGameState.getScore()

        food = currentGameState.getFood()
        currentPos = list(successorGameState.getPacmanPosition())
        distance = float("-Inf")

        foodList = food.asList()

        if action == 'Stop':
            return float("-Inf")

        for state in newGhostStates:
            if state.getPosition() == tuple(currentPos) and (state.scaredTimer == 0):
                return float("-Inf")

        for x in foodList:
            tempDistance = -1 * (manhattanDistance(currentPos, x))
            if (tempDistance > distance):
                distance = tempDistance

        return distance
        
        
        ########## New ##########
        # Xem x??t c??? c??c ??i???m th???c ??n v?? v??? tr?? c??c con ma ????? t??c t??? ph???n ???ng t???t nh???t
        # foodList = currentGameState.getFood().asList()
        
        # # L??c b???t ?????u, kh???i t???o kho???ng c??ch c???c ?????i d????ng
        # initDistance = float('inf')
        
        # # V??ng l???p ????? ph??n t??ch c?? ph??p qua t???t c??? c??c ??i???m th???c ??n trong foodList ???? t???o
        # for food in foodList:
        #     # T??nh to??n kho???ng c??ch s??? d???ng kho???ng c??ch manhattan t??? ??i???m th???c ??n ?????n v??? tr?? Pacman m???i
        #     initDistance = min(initDistance, manhattanDistance(food, newPos))
        #     # Ki???m tra li???u h??nh ?????ng hi???n t???i l?? STOP
        #     if Directions.STOP in action:
        #         # N???u ????ng tr??? v??? gi?? tr??? c???c ti???u
        #         return float('-inf')
            
        # # V??ng l???p ????? ph??n t??ch c?? ph??p qua t???t c??? c??c newGhostStates
        # for currentGhostState in newGhostStates:
        #     # L???y v??? tr?? hi???n t???i c???a ghostState
        #     currentGhost = currentGhostState.getPosition()
        #     # Ki???m tra xem v??? tr?? hi???n t???i c???a Ghost c?? tr??ng v???i v??? tr?? Pacman hay kh??ng
        #     if currentGhost == newPos:
        #         # Tr??? v??? gi?? tr??? c???c ti???u n???u 2 v??? tr?? tr??ng nhau
        #         return float('-inf')
            
        # return 1.0 / (1.0 + initDistance)


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        
        
class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        def alphabeta(state):
            bestValue, bestAction = None, None
            print(state.getLegalActions(0))
            value = []
            for action in state.getLegalActions(0):
                #value = max(value,minValue(state.generateSuccessor(0, action), 1, 1))
                succ  = minValue(state.generateSuccessor(0, action), 1, 1)
                value.append(succ)
                if bestValue is None:
                    bestValue = succ
                    bestAction = action
                else:
                    if succ > bestValue:
                        bestValue = succ
                        bestAction = action
            print(value)
            return bestAction

        def minValue(state, agentIdx, depth):
            if agentIdx == state.getNumAgents():
                return maxValue(state, 0, depth + 1)
            value = None
            for action in state.getLegalActions(agentIdx):
                succ = minValue(state.generateSuccessor(agentIdx, action), agentIdx + 1, depth)
                if value is None:
                    value = succ
                else:
                    value = min(value, succ)

            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)


        def maxValue(state, agentIdx, depth):
            if depth > self.depth:
                return self.evaluationFunction(state)
            value = None
            for action in state.getLegalActions(agentIdx):
                succ = minValue(state.generateSuccessor(agentIdx, action), agentIdx + 1, depth)
                if value is None:
                    value = succ
                else:
                    value = max(value, succ)
                
            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)

        action = alphabeta(gameState)

        return action

        # def minimax_search(state, agentIndex, depth):
        #     # if in min layer and last ghost
        #     if agentIndex == state.getNumAgents():
        #         # if reached max depth, evaluate state
        #         if depth == self.depth:
        #             return self.evaluationFunction(state)
        #         # otherwise start new max layer with bigger depth
        #         else:
        #             return minimax_search(state, 0, depth + 1)
        #     # if not min layer and last ghost
        #     else:
        #         moves = state.getLegalActions(agentIndex)
        #         # if nothing can be done, evaluate the state
        #         if len(moves) == 0:
        #             return self.evaluationFunction(state)
        #         # get all the minimax values for the next layer with each node being a possible state after a move
        #         next = (minimax_search(state.generateSuccessor(agentIndex, m), agentIndex + 1, depth) for m in moves)

        #         # if max layer, return max of layer below
        #         if agentIndex == 0:
        #             return max(next)
        #         # if min layer, return min of layer below
        #         else:
        #             return min(next)
        # # select the action with the greatest minimax value
        # result = max(gameState.getLegalActions(0), key=lambda x: minimax_search(gameState.generateSuccessor(0, x), 1, 1))

        # return result     

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        
        movesList = self.MiniMax(gameState, 0, 0, float('-inf'), float('inf'))
        
        # Tr??? v??? b?????c di chuy???n theo tr???ng th??i tr?? ch??i hi???n t???i
        return movesList[0]
        
    def minimumValue(self, gameState, height, agentsCount, temp1, temp2):
        # Kh???i t???o minVal v???i gi?? tr??? c???c ?????i
        minimalVal = ["", float('inf')]
        
        # Thu th???p c??c n?????c ??i h???p l??? v?? c??c tr???ng th??i k??? th???a
        ghostMovesList = gameState.getLegalActions(agentsCount)
        
        # Ki???m tra li???u danh s??ch 'c??c b?????c ??i c???a ghost' c?? r???ng hay kh??ng
        if not ghostMovesList:
            # N???u c?? tr??? v??? evaluationFunction(gameState)
            return self.evaluationFunction(gameState)

        # Duy???t m???i b?????c ??i trong danh s??ch 'C??c b?????c ??i c???a ghost'
        for gMove in ghostMovesList:
            successorState = gameState.generateSuccessor(agentsCount, gMove)
            presentMoveList = self.MiniMax(successorState, height, agentsCount + 1, temp1, temp2)

            if type(presentMoveList) is list:
                pMove = presentMoveList[1]
            else:
                pMove = presentMoveList

            # Ki???m tra xem li???u gi?? tr??? ???? c?? nh??? h??n gi?? tr??? trong list
            if pMove < minimalVal[1]:
                # N???u gi?? tr??? nh??? h??n th?? ?????t l???i gi?? tr??? minval              
                minimalVal = [gMove, pMove]
            # Ki???m tra li???u gi?? tr??? pMove nh??? h??n gi?? tr??? ???? truy???n v??o
            if pMove < temp1:
                # N???u gi?? tr??? nh??? h??n th?? tr??? v??? m???t t???p gi?? tr??? m???i
                return [gMove, pMove]
            # Kh??ng th?? ?????t l???i gi?? tr??? c???a n?????c ??i v???i gi?? tr??? t???i thi???u c???a 2 s??? (temp2, pMove)
            temp2 = min(temp2, pMove)
        # Tr??? v??? gi?? tr??? nh??? nh???t
        return minimalVal
    
    
    def maximumValue(self, gameState, height, agentsCount, temp1, temp2):
        
        # Kh???i t???o minVal v???i gi?? tr??? c???c ti???u
        maximalVal = ["", float('-inf')]
        
        # Thu th???p c??c n?????c ??i h???p l??? v?? c??c tr???ng th??i k??? th???a
        movesList = gameState.getLegalActions(agentsCount)
        
        # Ki???m tra li???u danh s??ch 'c??c b?????c ??i' c?? r???ng hay kh??ng
        if not movesList:
            # N???u c?? tr??? v??? evaluationFunction(gameState)
            return self.evaluationFunction(gameState)

        # Duy???t m???i b?????c ??i trong danh s??ch 'C??c b?????c ??i c???a ghost'
        for move in movesList:
            successorState = gameState.generateSuccessor(agentsCount, move)
            presentMoveList = self.MiniMax(successorState, height, agentsCount + 1, temp1, temp2)

            if type(presentMoveList) is list:
                pMove = presentMoveList[1]
            else:
                pMove = presentMoveList

            # Ki???m tra xem li???u gi?? tr??? ???? c?? l???n h??n gi?? tr??? trong list
            if pMove > maximalVal[1]:
                # N???u gi?? tr??? l???n h??n th?? ?????t l???i gi?? tr??? maxval              
                maximalVal = [move, pMove]
            # Ki???m tra li???u gi?? tr??? move c?? l???n h??n gi?? tr??? ???? truy???n v??o
            if pMove > temp2:
                # N???u gi?? tr??? l???n h??n th?? tr??? v??? m???t t???p gi?? tr??? m???i
                return [move, pMove]
            # Kh??ng th?? ?????t l???i gi?? tr??? c???a n?????c ??i v???i gi?? tr??? t???i ??a c???a 2 s??? (temp1, pMove)
            temp1 = max(temp1, pMove)
        # Tr??? v??? gi?? tr??? l???n nh???t
        return maximalVal
    
    def MiniMax(self, gameState, height, agentsCount, temp1, temp2):
        
        # Ki???m tra s??? l?????ng t??c t??? cho tr???ng th??i tr?? ch??i
        if agentsCount >= gameState.getNumAgents():
            # N???u ????ng th?? ?????t agentsCount = 0
            agentsCount = 0
            # v?? chi???u cao c???a c??y t??ng l??n 1
            height += 1
            
        # Ki???m tra tr???ng th??i hi???n t???i c???a tr?? ch??i
        if (gameState.isWin() or gameState.isLose() or height == self.depth):
            # Tr??? v??? Evaluation Function c???a tr???ng th??i tr?? ch??i
            return self.evaluationFunction(gameState)
        
        # Ki???m tra s??? l?????ng t??c t???
        elif (agentsCount != 0):
            # N???u s??? l?????ng t??c t??? kh??c 0, tr??? v??? gi?? tr??? nh??? nh???t c???a h??m
            return self.minimumValue(gameState, height, agentsCount, temp1, temp2)
        else:
            # Ng?????c l???i tr??? v??? gi?? tr??? l???n nh???t c???a h??m
            return self.maximumValue(gameState, height, agentsCount, temp1, temp2)
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        return self.ExpectedMax(gameState, 0, 0)
        
    def maximumValue(self, gameState, agentsCount, height):
        
        # Ki???m tra tr???ng th??i hi???n t???i c???a tr?? ch??i
        if (gameState.isWin() or gameState.isLose() or height == self.depth):
            # Tr??? v??? Evaluation Function c???a tr???ng th??i tr?? ch??i
            return self.evaluationFunction(gameState)
        
        # Kh???i t???o max value v???i gi?? tr??? c???c ti???u
        maximalVal = float('-inf')
        
        # ?????t b?????c di chuy???n t???i ??a th??nh 'Stop'
        maximalMoveValue = "Stop"
        
        # Thu th???p c??c n?????c ??i h???p l??? v?? c??c tr???ng th??i k??? th???a
        movesList = gameState.getLegalActions(agentsCount)
        
        # Ph??n t??ch c?? ph??p qua danh s??ch c??c b?????c di chuy???n
        for move in movesList:
            
            # b?????c di chuy???n ??? tr???ng th??i d???ng th?? b??? qua v??ng l???p
            if move == Directions.STOP:
                continue
            # L???y tr???ng th??i k??? th???a:
            successorState = gameState.generateSuccessor(agentsCount, move)
            
            # G???i h??m max ????? nh???n gi?? tr??? max mong ?????i
            temp1 = self.ExpectedMax(successorState, agentsCount+1, height)
            
            # So s??nh gi?? tr??? max mong ?????i v???i gi?? tr??? max c???c b??? (local max value)
            if temp1 > maximalVal:
                # Ho??n ?????i gi?? tr???
                maximalVal = temp1
                maximalMoveValue = move
                
        # Ki???m tra ????? s??u c???a c??y
        if height != 0: 
            return maximalVal
        else: 
            return maximalMoveValue         
        
    def expectedValue(self, gameState, agentsCount, height):
        
        # Ki???m tra tr???ng th??i hi???n t???i c???a tr?? ch??i
        if (gameState.isWin() or gameState.isLose() or height == self.depth):
            # Tr??? v??? Evaluation Function c???a tr???ng th??i tr?? ch??i
            return self.evaluationFunction(gameState)
        
        # Kh???i t???o gi?? tr??? ?????c l?????ng l?? 0
        expectedValue = 0
        
        # Thu th???p c??c n?????c ??i h???p l??? v?? c??c tr???ng th??i k??? th???a
        movesList = gameState.getLegalActions(agentsCount)
        
        # Kh???i t???o gi?? tr??? x??c su???t
        probValue = 1.0 / len(movesList)
        
        # Ph??n t??ch c?? ph??p qua danh s??ch c??c b?????c di chuy???n
        for move in movesList:
            
            # B?????c di chuy???n ??? tr???ng th??i d???ng th?? b??? qua v??ng l???p
            if move == Directions.STOP: 
                continue
            # L???y tr???ng th??i k??? th???a:
            successorState = gameState.generateSuccessor(agentsCount, move)
            
            # G???i h??m ?????c t??nh gi?? tr??? max
            temp1 = self.ExpectedMax(successorState, agentsCount+1, height)
            
            # T??nh to??n gi?? tr??? mong ?????i
            expectedValue += (temp1 * probValue)
            
        return expectedValue
    
    def ExpectedMax (self, gameState, agentsCount, height):
        
        # Ki???m tra s??? l?????ng t??c t??? cho tr???ng th??i tr?? ch??i
        if agentsCount >= gameState.getNumAgents():
            # N???u ????ng th?? ?????t agentsCount = 0
            agentsCount = 0
            # v?? chi???u cao c???a c??y t??ng l??n 1
            height += 1
            
        # Ki???m tra ????? s??u c??y
        if height == self.depth:
            # N???u k???t qu??? b???ng nhau, g???i h??m evaluationFunction cho tr???ng th??i tr?? ch??i
            return self.evaluationFunction(gameState)
        
        
        # ??i???u ki???n cho s??? l?????ng t??c t???
        if (agentsCount != self.index):
            return self.expectedValue(gameState, agentsCount, height)
        else:
            return self.maximumValue(gameState, agentsCount, height)
        
        return 'None'
        
        
# def betterEvaluationFunction(currentGameState):
#     """
#     Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
#     evaluation function (question 5).

#     DESCRIPTION: <write something here so we know what you did>
#     """
#     "*** YOUR CODE HERE ***"
#     #util.raiseNotDefined()
#     newPos = currentGameState.getPacmanPosition()
#     newFood = currentGameState.getFood()
#     newGhostStates = currentGameState.getGhostStates()
#     newCapsules = currentGameState.getCapsules()
#     newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

#     closestGhost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
#     if newCapsules:
#         closestCapsule = min([manhattanDistance(newPos, caps) for caps in newCapsules])
#     else:
#         closestCapsule = 0

#     if closestCapsule:
#         closest_capsule = -3 / closestCapsule
#     else:
#         closest_capsule = 100

#     if closestGhost:
#         ghost_distance = -2 / closestGhost
#     else:
#         ghost_distance = -500

#     foodList = newFood.asList()
#     if foodList:
#         closestFood = min([manhattanDistance(newPos, food) for food in foodList])
#     else:
#         closestFood = 0

#     return -2 * closestFood + ghost_distance - 10 * len(foodList) + closest_capsule

# # Abbreviation
# better = betterEvaluationFunction
def betterEvaluationFunction(currentGameState):
    
    # L???y danh s??ch tr???ng th??i c???a c??c con Ghost
    ghostStatesList = currentGameState.getGhostStates()
    
    # L???y danh s??ch tr???ng th??i c??c Capsules
    capsulesList = currentGameState.getCapsules()
    
    # L???y v??? tr?? Pacman ?????u ti??n
    currentPacmanPosition = currentGameState.getPacmanPosition()
    
    # L???y s??? l?????ng th???c ??n cho tr???ng th??i hi???n t???i
    currentNumFood = currentGameState.getNumFood()
    
    # L???y ??i???m tr?? ch??i cho tr???ng th??i hi???n t???i
    currentScore = currentGameState.getScore()
    
    # ????nh gi?? c??c h???t th???c ??n c??n l???i
    remainFood = 1.0 / (currentNumFood + 1.0)
    
    # Kh???i t???o kho???ng c??ch ghost ban ?????u v???i gi?? tr??? c???c ?????i
    ghostDistance = float('inf')
    
    # Ph??n t??ch c?? ph??p l???p qua danh s??ch tr???ng th??i c??c con ghost
    for ghostState in ghostStatesList:
        
        # L???y v??? tr?? c???a tr???ng th??i con ghost hi???n t???i
        currentGhostPosition = ghostState.getPosition()
        
        # Ki???m tra li???u v??? tr?? hi???n t???i c???a Pacman c?? gi???ng v??? tr?? hi??n t???i c???a Ghost
        if currentPacmanPosition != currentGhostPosition:
            # N???u kh??c, kho???ng c??ch Manhattan gi???a v??? tr?? Pacman v?? Ghost ???????c so s??nh v???i ghostDistance hi???n t???i v?? l???y gi?? tr??? nh??? h??n c???p nh???t cho kho???ng c??ch Ghost m???i (ghostDistance)
            ghostDistance = min(ghostDistance, manhattanDistance(currentPacmanPosition, currentGhostPosition))
            
        else:
            # Tr??? v??? l???i l?? m???t gi?? tr??? c???c ti???u
            return float('-inf')
        
        # ????nh gi?? ngh???ch ?????o c???a ghostDistance d???a tr??n ????? d??i c???a ghostStatesList v?? l??u tr??? l???i l???n n???a
        ghostDistance = 1.0 / (1.0 + (ghostDistance / len(ghostStatesList)))
        
        # Kh???i t???o kho???ng c??ch capsule ban ?????u v???i gi?? tr??? c???c ?????i
        capsuleDistance = float('inf')
        
        # Ph??n t??ch c?? ph??p l???p qua c??c capsule trong t???t c??? c??c Capsules hi???n t???i
        for capsule in capsulesList:
            
            # ????nh gi?? kho???ng c??ch Manhattan gi???a v??? tr?? Pacman hi???n t???i v?? tr???ng th??i Capsule, so s??nh v???i kho???ng c??ch Capsule v?? l??u tr??? n?? v???i gi?? tr??? nh??? h??n
            capsuleDistance = min(capsuleDistance, manhattanDistance(currentPacmanPosition, capsule))
            
        # ????nh gi?? ngh???ch ?????o c???a Capsule hi???n t???i d???a tr??n ????? d??i c???a c??c Capsule hi???n t???i v?? l??u tr??? l???i l???n n???a
        capsuleDistance = 1.0 / (1.0 + len(capsulesList))
        
        """ 
        Tr??? v??? gi?? tr??? ???????c ????nh gi?? t???t nh???t d???a tr??n:
            + ??i???m s??? (score)
            + Th???c ??n c??n l???i (remain Food)
            + kho???ng c??ch ?????n con Ghost (Distance from ghost)
            + Kho???ng c??ch ?????n Capsule (Distance from Capsule)
        """
        return currentScore + remainFood + ghostDistance + capsuleDistance

# Abbreviation
better = betterEvaluationFunction