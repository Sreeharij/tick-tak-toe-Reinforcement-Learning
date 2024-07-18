import numpy as np
import pickle
import os
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class State:
    def __init__(self,p1,p2):
        self.board = np.zeros((3,3))
        self.p1 = p1 
        self.p2 = p2 
        self.isEnd = False
        self.boardHash = None 
        
        self.playerSymbol = 1

    def getHash(self):
        self.boardHash = str(self.board.reshape(3,3))
        return self.boardHash
    
    def winner(self):
        for i in range(3):
            row_sum = sum(self.board[i,:])
            col_sum = sum(self.board[:,i])
            if row_sum == 3 or col_sum == 3:
                self.isEnd = True 
                return 1 
            elif row_sum == -3 or col_sum == -3:
                self.isEnd = True
                return -1

        diag_sum = self.board[0,0] + self.board[1,1] + self.board[2,2]
        alt_diag_sum = self.board[0,2] + self.board[1,1] + self.board[2,0]
        if diag_sum == 3 or alt_diag_sum == 3:
            self.isEnd = True
            return 1
        elif diag_sum == -3 or alt_diag_sum == -3:
            self.isEnd = True 
            return -1
        
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        
        self.isEnd = False
        return None 
    
    def availablePositions(self):
        positions = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    positions.append((i,j))
        return positions
    
    def updateState(self,position):
        self.board[position] = self.playerSymbol

        if self.playerSymbol == 1:
            self.playerSymbol = -1
        else:
            self.playerSymbol = 1
        
    def giveReward(self):
        result = self.winner()

        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)
    
    def reset(self):
        self.board = np.zeros((3,3))
        self.boardHash = None 
        self.isEnd = False 
        self.playerSymbol = 1

    def play(self,rounds=1000):
        for i in range(rounds):
            if i%10000 == 0:
                print(f"Finished {i} rounds")
            while not self.isEnd:
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions,self.board,self.playerSymbol)
                self.updateState(p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)

                win = self.winner()

                if win is not None:

                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
                else:
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions,self.board,self.playerSymbol)
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)

                    win = self.winner()
                    if win is not None:

                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break


class Player:
    def __init__(self,name,exp_rate = 0.3):
        self.name = name 
        self.states = []
        self.LEARNING_RATE = 0.2
        self.EXPLORATION_RATE = exp_rate
        self.DECAY_GAMMA = 0.9
        self.states_value = {}

    def getHash(self,board):
        boardHash = str(board.reshape(3,3))
        return boardHash
    
    def chooseAction(self,positions,current_board,symbol):
        if np.random.uniform(0,1) <= self.EXPLORATION_RATE:
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                if self.states_value.get(next_boardHash) is not None:
                    value = self.states_value.get(next_boardHash)
                else:
                    value = 0 
                if value >= value_max:
                    value_max = value 
                    action = p 
        return action
    
    def addState(self,state):
        self.states.append(state)

    def feedReward(self,reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0 
            self.states_value[st] = (1 - self.LEARNING_RATE)*self.states_value[st] + self.LEARNING_RATE * (self.DECAY_GAMMA * reward)
            # reward = self.states_value[st]

    def reset(self):
        self.states = [] 

    
    def savePolicy(self):
        with open(os.path.join(CURRENT_DIRECTORY,"policy")) as f:
            pickle.dump(self.states_value,f)
    def loadPolicy(self):
        with open(os.path.join(CURRENT_DIRECTORY,"policy")) as f:
            self.states_value = pickle.load(f)


p1 = Player("p1")
p2 = Player("p2")
state = State(p1,p2)
print("Training agent...")
state.play(50000)

p1 = Player("computer",exp_rate=0)
p1.loadPolicy()