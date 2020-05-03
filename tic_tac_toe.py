from copy import copy
from random import choice

class tic_tac_toe:
    # 0 - free box | 1 - AI Piece | 2 - Player 1 Piece
    def __init__(self, state=[0, 0, 0, 0, 0, 0, 0, 0, 0]):
        self.state = state
        self.player2index = {"AI": 1, "human": 2}
        self.index2player = {1: "AI", 2: "human"}
        self.state2symbol = {0: "?", 1: "X", 2: "O"}

    def actions(self, state):
        return [i for i in range(9) if state[i]==0]

    def result(self, state):
        # return 0 if values are not all equal, else return the value
        def check_equals(values):
            not_equals = [item for item in values if item != values[0]]
            return values[0] if len(not_equals) == 0 else 0

        #indices of conditions
        horizontal_conditions = [[x+i for x in [0, 1, 2]] for i in [0, 3, 6]]
        vertical_conditions = [[x+i for x in [0, 3, 6]] for i in [0, 1, 2]]
        diagonal_conditions = [[0, 4, 8], [2, 4, 6]]
        conditions = horizontal_conditions + vertical_conditions + diagonal_conditions

        for condition in conditions:
            values = [state[index] for index in condition]
            result = check_equals(values)
            if result in self.index2player.keys():
                return self.index2player[result]

        return 'undecided' if 0 in state else 'draw'

    def display(self, state):
        symbols = [self.state2symbol[value] for value in state]
        for row in [0, 3, 6]:
            print(f"{symbols[row]}|{symbols[row+1]}|{symbols[row+2]}")
        print()

    def play(self, state, position, player):
        assert state[position] == 0
        newState = copy(state)
        newState[position] = self.player2index[player]
        return newState

def pure_monte_carlo_search(game, state, num_playouts=1000):
    loss_score = {move: float('-inf') for move in game.actions(state)}

    for ai_move in game.actions(state):
        hypothetical_state = game.play(state, ai_move, 'AI')

        # For each move, simulate a number of playouts
        for human_move in game.actions(hypothetical_state):
            loss = 0
            for i in range(num_playouts):
                if game.result(hypothetical_state) == 'undecided':
                    hypothetical_state = game.play(hypothetical_state, human_move, "human")
                player = "AI"

                while (game.result(hypothetical_state) == 'undecided'):
                    action = choice(game.actions(hypothetical_state))
                    hypothetical_state = game.play(hypothetical_state, action, player)
                    player = 'human' if player == "AI" else 'AI'

                if game.result(hypothetical_state) == 'human':
                    loss += 3
                if game.result(hypothetical_state) == 'AI':
                    loss -= 2

                hypothetical_state = game.play(state, ai_move, 'AI') # Reset state

            if loss > loss_score[ai_move]:  # Record the highest loss score out of the possible human moves.
                loss_score[ai_move] = loss

    best_action = min(loss_score, key=loss_score.get) # Choose the move that minmizes the loss score
    return best_action

#https://www.101computing.net/ascii-bot-challenge/
def intro_message():
    print("Welcome to Skynet Tic-Tac-Toe")
    print("         +-+      +")
    print("           | +-+  |   +-+")
    print("     +-+   |   |  |   |    +--+")
    print("       |   |   |  |   |    |")
    print("       |   |   |  |   |    |")
    print("   +---+---+---+--+---+----+----+")
    print("   |                            |")
    print("   |   +-------+     +-------+  |")
    print("+--+   |       |     |       |  +--+")
    print("|  |   |       |     |       |  |  |")
    print("|  |   |    +--+     |    +--+  |  |")
    print("+--+   |    |--|     |    |--|  +--+")
    print("   |   +-------+     +-------+  |")
    print("   |             +-+            |")
    print("   |             | |            |")
    print("   |             +-+            |")
    print("   |  +--+               +--+   |")
    print("   |    +-----------------+     |")
    print("   |                            |")
    print("   +----------------------------+")
    print("")

    print("Hint: enter index value according to this chart")
    for row in [0, 3, 6]:
        print(f"{row}|{row+1}|{row+2}")
    print("")

def play_a_new_game():
    game = tic_tac_toe([0 for i in range(9)])
    intro_message()

    human_first = input("Human player first? [y/n] ")
    player = 'human' if human_first == 'y' else 'AI'

    while(game.result(game.state) == "undecided"):
        game.display(game.state)
        actions = game.actions(game.state)

        if player == 'human':   #Wait for human input
            while True:
                move = int(input('Enter your move: '))
                if move in actions:
                    break
        else:   # Monte Carlo Search with min max search elements
            print("AI's move")
            move = pure_monte_carlo_search(game, game.state, NUM_PLAYOUTS)

        game.state = game.play(game.state, move, player)
        player = 'human' if player == "AI" else 'AI'

    game.display(game.state)
    if game.result(game.state) == 'draw':
        print("It's a draw")
    else:
        print(f"{game.result(game.state)} wins!")

if __name__ == '__main__':
    NUM_PLAYOUTS = 600
    play_a_new_game()
