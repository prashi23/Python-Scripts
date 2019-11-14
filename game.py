from math import *
import random
import time
from copy import deepcopy


class BigGameState:
    def __init__(self):
        self.board = [[0 for i in range(10)] for j in range(10)]
        self.curr = 1
        # At the root pretend the player just moved is player 2,
        # so player 1 will have the first move
        self.playerJustMoved = 2
        self.ended = False
        # to put * in __str__
        self.last_move = None
        self.last_curr = None

    def Clone(self):
        return deepcopy(self)

    def DoMove(self, move):
        # 1 2 3
        # 4 5 6
        # 7 8 9
        winning_pairs = [[],  # 0
                         [[2, 3], [5, 9], [4, 7]],  # for 1
                         [[1, 3], [5, 8]],  # for 2
                         [[1, 2], [5, 7], [6, 9]],  # for 3
                         [[1, 7], [5, 6]],  # for 4
                         [[1, 9], [2, 8], [3, 7], [4, 6]],  # for 5
                         [[3, 9], [4, 5]],  # for 6
                         [[1, 4], [5, 3], [8, 9]],  # for 7
                         [[7, 9], [2, 5]],  # for 8
                         [[7, 8], [1, 5], [3, 6]],  # for 9
                         ]
        if not isinstance(move, int) or 1 < move > 9 or \
                self.board[self.curr][move] != 0:
            raise ValueError
        self.playerJustMoved = 3 - self.playerJustMoved
        self.board[self.curr][move] = self.playerJustMoved
        for index1, index2 in winning_pairs[move]:
            if self.playerJustMoved == self.board[self.curr][index1] == \
                    self.board[self.curr][index2]:
                self.ended = True
        self.last_move = move
        self.last_curr = self.curr
        self.curr = move

    def GetMoves(self):
        if self.ended:
            return []
        return [i for i in range(1, 10) if self.board[self.curr][i] == 0]

    def GetResult(self, playerjm):
        # Get the game result from the viewpoint of playerjm.
        for bo in self.board:
            for x, y, z in [(1, 2, 3), (4, 5, 6), (7, 8, 9),
                            (1, 4, 7), (2, 5, 8), (3, 6, 9),
                            (1, 5, 9), (3, 5, 7)]:
                if bo[x] == bo[y] == bo[z]:
                    if bo[x] == playerjm:
                        return 1.0
                    elif bo[x] != 0:
                        return 0.0
        if not self.GetMoves():
            return 0.5 # draw
        raise ValueError

    def _one_board_string(self, a, row):
        return ''.join([' ' + '.XO'[self.board[a][i+row]] for i in range(3)])

    def _three_board_line(self, index, row):
        return '┃' + ''.join([self._one_board_string(i + index, row) + ' ┃' for i in range(3)])

    def __repr__(self):
        # ┏━━━━━━━┳━━━━━━━┳━━━━━━━┓
        # ┃ . . . ┃ . . . ┃ . . . ┃
        # ┃ . . . ┃ X . X ┃ . . O ┃
        # ┃ . X . ┃ . . O ┃ . . . ┃
        # ┣━━━━━━━╋━━━━━━━╋━━━━━━━┫
        # ┃ . . . ┃ . . . ┃*X X X ┃
        # ┃ X . O ┃ . . . ┃ O . O ┃
        # ┃ . . O ┃ . . . ┃ . . . ┃
        # ┣━━━━━━━╋━━━━━━━╋━━━━━━━┫
        # ┃ . . . ┃ . O . ┃ . O . ┃
        # ┃ . . . ┃ . . . ┃ . . X ┃
        # ┃ . . . ┃ . . . ┃ . . X ┃
        # ┗━━━━━━━┻━━━━━━━┻━━━━━━━┛
        s = '┏━━━━━━━┳━━━━━━━┳━━━━━━━┓\n'
        for i in [1, 4, 7]:
            for j in [1, 4, 7]:
                s += self._three_board_line(i, j) + '\n'
            if i != 7:
                s += '┣━━━━━━━╋━━━━━━━╋━━━━━━━┫\n'
            else:
                s += '┗━━━━━━━┻━━━━━━━┻━━━━━━━┛\n'
        # Hack: by rows and colums of move and current board
        # calculate place to put '*' so it is visible
        c = self.last_curr - 1
        c_c = c % 3
        c_r = c // 3
        m_c = (self.last_move - 1) % 3
        m_r = (self.last_move - 1)// 3
        p = 26 + c_r * (26 * 4) + c_c * 8 + m_r * 26 + m_c * 2 + 1
        s = s[:p] + '*' + s[p+1:]
        return s


class OXOState:
    def __init__(self):
        self.playerJustMoved = 2
        self.ended = False
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def Clone(self):
        return deepcopy(self)

    def DoMove(self, move):
        #  0 1 2
        #  3 4 5
        #  6 7 8
        winning_pairs = [[[1, 2], [4, 8], [3, 6]],  # for 0
                         [[0, 2], [4, 7]],  # for 1
                         [[0, 1], [4, 6], [5, 8]],  # for 2
                         [[0, 6], [4, 5]],  # for 3
                         [[0, 8], [1, 7], [2, 6], [3, 5]],  # for 4
                         [[2, 8], [3, 4]],  # for 5
                         [[0, 3], [4, 2], [7, 8]],  # for 6
                         [[6, 8], [1, 4]],  # for 7
                         [[6, 7], [0, 4], [2, 5]],  # for 6
                         ]
        if not isinstance(move, int) or 0 < move > 8 or \
                self.board[move] != 0:
            raise ValueError
        self.playerJustMoved = 3 - self.playerJustMoved
        self.board[move] = self.playerJustMoved
        for index1, index2 in winning_pairs[move]:
            if self.playerJustMoved == self.board[index1] == self.board[index2]:
                self.ended = True

    def GetMoves(self):
        return [] if self.ended else [i for i in range(9) if self.board[i] == 0]

    def GetResult(self, playerjm):
        for (x, y, z) in [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
                          (2, 5, 8), (0, 4, 8), (2, 4, 6)]:
            if self.board[x] == self.board[y] == self.board[z]:
                if self.board[x] == playerjm:
                    return 1.0
                elif self.board[x] != 0:
                    return 0.0
        if self.GetMoves() == []:
            return 0.5  # draw
        raise ValueError

    def __repr__(self):
        s = ""
        for i in range(9):
            s += '.XO'[self.board[i]]
            if i % 3 == 2: s += "\n"
        return s


class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """

    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves()  # future child nodes
        self.playerJustMoved = state.playerJustMoved  # the only part of the state that the Node needs later

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + sqrt(
            2 * log(self.visits) / c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(
            self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose=False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()

        # Select
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m, state)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []:  # while state is non-terminal
            state.DoMove(random.choice(state.GetMoves()))

        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(
                node.playerJustMoved))  # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

    # Output some information about the tree - can be omitted
    # if (verbose):
    #     print(rootnode.TreeToString(0))
    # else:
    #     print(rootnode.ChildrenToString())

    return sorted(rootnode.childNodes, key=lambda c: c.visits)[
        -1].move  # return the move that was most visited


def HumanPlayer(state):
    moves = state.GetMoves()
    while True:
        try:
            m = int(input("Your move " + str(moves) + " : "))
            if m in moves:
                return m
        except ValueError:
            pass


def RandomPlayer(state):
    return random.choice(state.GetMoves())


def negamax(board, color, depth):  # ##################################################
    moves = board.GetMoves()
    if not moves:
        x = board.GetResult(board.playerJustMoved)
        if x == 0.0:
            print('negamax ERROR:')
            print(board)
            print(board.playerJustMoved)
            print(board.curr, board.ended)
            print(board.GetMoves())
            raise ValueError
        if x == 0.5:
            return 0.0, None
        if color == 1 and board.playerJustMoved == 1:
            return 1.0, None
        else:
            return -1.0, None
    if depth == 0:
        return 0.0, None
    v = float("-inf")
    best_move = []
    for m in moves:
        new_board = board.Clone()
        new_board.DoMove(m)
        x, _ = negamax(new_board, -color, depth - 1)
        x = - x
        if x >= v:
            if x > v:
                best_move = []
            v = x
            best_move.append(m)
    if depth >=8:
        print(depth, v, best_move)
    return v, best_move


def NegamaxPlayer(game):
        best_moves = game.GetMoves()
        if len(best_moves) != 9:
            _, best_moves = negamax(game, 1, 4)
            print(best_moves)
        return random.choice(best_moves)


if __name__ == "__main__":
    def main():
        random.seed(123456789)
        won = 0
        lost = 0
        draw = 0
        for i in range(10):
            # state = OXOState() # uncomment to play OXO
            state = BigGameState()
            move = 0
            while (state.GetMoves() != []):
                if state.playerJustMoved == 1:
                    # m = RandomPlayer(state)
                    m = UCT(rootstate=state, itermax=100, verbose=False)
                else:
                    # m = UCT(rootstate=state, itermax=100, verbose=False)
                    # m = NegamaxPlayer(state)
                    m = HumanPlayer(state)
                    # m = RandomPlayer(state)
                state.DoMove(m)
                move += 1
                print('Game ', i + 1, ', Move ', move, ':\n', state, sep='')
            if state.GetResult(1) == 1.0:
                won += 1
                print("Player 1 wins!")
            elif state.GetResult(1) == 0.0:
                lost += 1
                print("Player 2 wins!")
            else:
                draw += 1
                print("Nobody wins!")
            print('won', won, 'lost', lost, 'draw', draw)

    start_time = time.perf_counter()
    main()
    total_time = time.perf_counter() - start_time
    print('total_time', total_time)