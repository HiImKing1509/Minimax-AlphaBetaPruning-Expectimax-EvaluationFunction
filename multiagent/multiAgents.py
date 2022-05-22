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
        # Xem xét cả các điểm thức ăn và vị trí các con ma để tác tử phản ứng tốt nhất
        # foodList = currentGameState.getFood().asList()
        
        # # Lúc bắt đầu, khởi tạo khoảng cách cực đại dương
        # initDistance = float('inf')
        
        # # Vòng lặp để phân tích cú pháp qua tất cả các điểm thức ăn trong foodList đã tạo
        # for food in foodList:
        #     # Tính toán khoảng cách sử dụng khoảng cách manhattan từ điểm thức ăn đến vị trí Pacman mới
        #     initDistance = min(initDistance, manhattanDistance(food, newPos))
        #     # Kiểm tra liệu hành động hiện tại là STOP
        #     if Directions.STOP in action:
        #         # Nếu đúng trả về giá trị cực tiểu
        #         return float('-inf')
            
        # # Vòng lặp để phân tích cú pháp qua tất cả các newGhostStates
        # for currentGhostState in newGhostStates:
        #     # Lấy vị trí hiện tại của ghostState
        #     currentGhost = currentGhostState.getPosition()
        #     # Kiểm tra xem vị trí hiện tại của Ghost có trùng với vị trí Pacman hay không
        #     if currentGhost == newPos:
        #         # Trả về giá trị cực tiểu nếu 2 vị trí trùng nhau
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
        
        # Trả về bước di chuyển theo trạng thái trò chơi hiện tại
        return movesList[0]
        
    def minimumValue(self, gameState, height, agentsCount, temp1, temp2):
        # Khởi tạo minVal với giá trị cực đại
        minimalVal = ["", float('inf')]
        
        # Thu thập các nước đi hợp lệ và các trạng thái kế thừa
        ghostMovesList = gameState.getLegalActions(agentsCount)
        
        # Kiểm tra liệu danh sách 'các bước đi của ghost' có rỗng hay không
        if not ghostMovesList:
            # Nếu có trả về evaluationFunction(gameState)
            return self.evaluationFunction(gameState)

        # Duyệt mỗi bước đi trong danh sách 'Các bước đi của ghost'
        for gMove in ghostMovesList:
            successorState = gameState.generateSuccessor(agentsCount, gMove)
            presentMoveList = self.MiniMax(successorState, height, agentsCount + 1, temp1, temp2)

            if type(presentMoveList) is list:
                pMove = presentMoveList[1]
            else:
                pMove = presentMoveList

            # Kiểm tra xem liệu giá trị đó có nhỏ hơn giá trị trong list
            if pMove < minimalVal[1]:
                # Nếu giá trị nhỏ hơn thì đặt lại giá trị minval              
                minimalVal = [gMove, pMove]
            # Kiểm tra liệu giá trị pMove nhỏ hơn giá trị đã truyền vào
            if pMove < temp1:
                # Nếu giá trị nhỏ hơn thì trả về một tập giá trị mới
                return [gMove, pMove]
            # Không thì đặt lại giá trị của nước đi với giá trị tối thiểu của 2 số (temp2, pMove)
            temp2 = min(temp2, pMove)
        # Trả về giá trị nhỏ nhất
        return minimalVal
    
    
    def maximumValue(self, gameState, height, agentsCount, temp1, temp2):
        
        # Khởi tạo minVal với giá trị cực tiểu
        maximalVal = ["", float('-inf')]
        
        # Thu thập các nước đi hợp lệ và các trạng thái kế thừa
        movesList = gameState.getLegalActions(agentsCount)
        
        # Kiểm tra liệu danh sách 'các bước đi' có rỗng hay không
        if not movesList:
            # Nếu có trả về evaluationFunction(gameState)
            return self.evaluationFunction(gameState)

        # Duyệt mỗi bước đi trong danh sách 'Các bước đi của ghost'
        for move in movesList:
            successorState = gameState.generateSuccessor(agentsCount, move)
            presentMoveList = self.MiniMax(successorState, height, agentsCount + 1, temp1, temp2)

            if type(presentMoveList) is list:
                pMove = presentMoveList[1]
            else:
                pMove = presentMoveList

            # Kiểm tra xem liệu giá trị đó có lớn hơn giá trị trong list
            if pMove > maximalVal[1]:
                # Nếu giá trị lớn hơn thì đặt lại giá trị maxval              
                maximalVal = [move, pMove]
            # Kiểm tra liệu giá trị move có lớn hơn giá trị đã truyền vào
            if pMove > temp2:
                # Nếu giá trị lớn hơn thì trả về một tập giá trị mới
                return [move, pMove]
            # Không thì đặt lại giá trị của nước đi với giá trị tối đa của 2 số (temp1, pMove)
            temp1 = max(temp1, pMove)
        # Trả về giá trị lớn nhất
        return maximalVal
    
    def MiniMax(self, gameState, height, agentsCount, temp1, temp2):
        
        # Kiểm tra số lượng tác tử cho trạng thái trò chơi
        if agentsCount >= gameState.getNumAgents():
            # Nếu đúng thì đặt agentsCount = 0
            agentsCount = 0
            # và chiều cao của cây tăng lên 1
            height += 1
            
        # Kiểm tra trạng thái hiện tại của trò chơi
        if (gameState.isWin() or gameState.isLose() or height == self.depth):
            # Trả về Evaluation Function của trạng thái trò chơi
            return self.evaluationFunction(gameState)
        
        # Kiểm tra số lượng tác tử
        elif (agentsCount != 0):
            # Nếu số lượng tác tử khác 0, trả về giá trị nhỏ nhất của hàm
            return self.minimumValue(gameState, height, agentsCount, temp1, temp2)
        else:
            # Ngược lại trả về giá trị lớn nhất của hàm
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
        
        # Kiểm tra trạng thái hiện tại của trò chơi
        if (gameState.isWin() or gameState.isLose() or height == self.depth):
            # Trả về Evaluation Function của trạng thái trò chơi
            return self.evaluationFunction(gameState)
        
        # Khởi tạo max value với giá trị cực tiểu
        maximalVal = float('-inf')
        
        # Đặt bước di chuyển tối đa thành 'Stop'
        maximalMoveValue = "Stop"
        
        # Thu thập các nước đi hợp lệ và các trạng thái kế thừa
        movesList = gameState.getLegalActions(agentsCount)
        
        # Phân tích cú pháp qua danh sách các bước di chuyển
        for move in movesList:
            
            # bước di chuyển ở trạng thái dừng thì bỏ qua vòng lặp
            if move == Directions.STOP:
                continue
            # Lấy trạng thái kế thừa:
            successorState = gameState.generateSuccessor(agentsCount, move)
            
            # Gọi hàm max để nhận giá trị max mong đợi
            temp1 = self.ExpectedMax(successorState, agentsCount+1, height)
            
            # So sánh giá trị max mong đợi với giá trị max cục bộ (local max value)
            if temp1 > maximalVal:
                # Hoán đổi giá trị
                maximalVal = temp1
                maximalMoveValue = move
                
        # Kiểm tra độ sâu của cây
        if height != 0: 
            return maximalVal
        else: 
            return maximalMoveValue         
        
    def expectedValue(self, gameState, agentsCount, height):
        
        # Kiểm tra trạng thái hiện tại của trò chơi
        if (gameState.isWin() or gameState.isLose() or height == self.depth):
            # Trả về Evaluation Function của trạng thái trò chơi
            return self.evaluationFunction(gameState)
        
        # Khởi tạo giá trị ước lượng là 0
        expectedValue = 0
        
        # Thu thập các nước đi hợp lệ và các trạng thái kế thừa
        movesList = gameState.getLegalActions(agentsCount)
        
        # Khởi tạo giá trị xác suất
        probValue = 1.0 / len(movesList)
        
        # Phân tích cú pháp qua danh sách các bước di chuyển
        for move in movesList:
            
            # Bước di chuyển ở trạng thái dừng thì bỏ qua vòng lặp
            if move == Directions.STOP: 
                continue
            # Lấy trạng thái kế thừa:
            successorState = gameState.generateSuccessor(agentsCount, move)
            
            # Gọi hàm ước tính giá trị max
            temp1 = self.ExpectedMax(successorState, agentsCount+1, height)
            
            # Tính toán giá trị mong đợi
            expectedValue += (temp1 * probValue)
            
        return expectedValue
    
    def ExpectedMax (self, gameState, agentsCount, height):
        
        # Kiểm tra số lượng tác tử cho trạng thái trò chơi
        if agentsCount >= gameState.getNumAgents():
            # Nếu đúng thì đặt agentsCount = 0
            agentsCount = 0
            # và chiều cao của cây tăng lên 1
            height += 1
            
        # Kiểm tra độ sâu cây
        if height == self.depth:
            # Nếu kết quả bằng nhau, gọi hàm evaluationFunction cho trạng thái trò chơi
            return self.evaluationFunction(gameState)
        
        
        # Điều kiện cho số lượng tác tử
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
    
    # Lấy danh sách trạng thái của các con Ghost
    ghostStatesList = currentGameState.getGhostStates()
    
    # Lấy danh sách trạng thái các Capsules
    capsulesList = currentGameState.getCapsules()
    
    # Lấy vị trí Pacman đầu tiên
    currentPacmanPosition = currentGameState.getPacmanPosition()
    
    # Lấy số lượng thức ăn cho trạng thái hiện tại
    currentNumFood = currentGameState.getNumFood()
    
    # Lấy điểm trò chơi cho trạng thái hiện tại
    currentScore = currentGameState.getScore()
    
    # Đánh giá các hạt thức ăn còn lại
    remainFood = 1.0 / (currentNumFood + 1.0)
    
    # Khởi tạo khoảng cách ghost ban đầu với giá trị cực đại
    ghostDistance = float('inf')
    
    # Phân tích cú pháp lặp qua danh sách trạng thái các con ghost
    for ghostState in ghostStatesList:
        
        # Lấy vị trí của trạng thái con ghost hiện tại
        currentGhostPosition = ghostState.getPosition()
        
        # Kiểm tra liệu vị trí hiện tại của Pacman có giống vị trí hiên tại của Ghost
        if currentPacmanPosition != currentGhostPosition:
            # Nếu khác, khoảng cách Manhattan giữa vị trí Pacman và Ghost được so sánh với ghostDistance hiện tại và lấy giá trị nhỏ hơn cập nhật cho khoảng cách Ghost mới (ghostDistance)
            ghostDistance = min(ghostDistance, manhattanDistance(currentPacmanPosition, currentGhostPosition))
            
        else:
            # Trả về lỗi là một giá trị cực tiểu
            return float('-inf')
        
        # Đánh giá nghịch đảo của ghostDistance dựa trên độ dài của ghostStatesList và lưu trữ lại lần nữa
        ghostDistance = 1.0 / (1.0 + (ghostDistance / len(ghostStatesList)))
        
        # Khởi tạo khoảng cách capsule ban đầu với giá trị cực đại
        capsuleDistance = float('inf')
        
        # Phân tích cú pháp lặp qua các capsule trong tất cả các Capsules hiện tại
        for capsule in capsulesList:
            
            # Đánh giá khoảng cách Manhattan giữa vị trí Pacman hiện tại và trạng thái Capsule, so sánh với khoảng cách Capsule và lưu trữ nó với giá trị nhỏ hơn
            capsuleDistance = min(capsuleDistance, manhattanDistance(currentPacmanPosition, capsule))
            
        # Đánh giá nghịch đảo của Capsule hiện tại dựa trên độ dài của các Capsule hiện tại và lưu trữ lại lần nữa
        capsuleDistance = 1.0 / (1.0 + len(capsulesList))
        
        """ 
        Trả về giá trị được đánh giá tốt nhất dựa trên:
            + Điểm số (score)
            + Thức ăn còn lại (remain Food)
            + khoảng cách đến con Ghost (Distance from ghost)
            + Khoảng cách đến Capsule (Distance from Capsule)
        """
        return currentScore + remainFood + ghostDistance + capsuleDistance

# Abbreviation
better = betterEvaluationFunction