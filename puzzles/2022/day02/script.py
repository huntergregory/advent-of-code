ROCK = 'rock'
PAPER = 'paper'
SCISSOR = 'scissor'

LOSS = 0
DRAW = 3
WIN = 6

hand_scores = {
    ROCK: 1,
    PAPER: 2,
    SCISSOR: 3,
}

opp_conversion = {
    'A': ROCK,
    'B': PAPER,
    'C': SCISSOR,
}

my_conversion = {
    'X': ROCK,
    'Y': PAPER,
    'Z': SCISSOR,
}

win_hands = {
    ROCK: PAPER,
    PAPER: SCISSOR,
    SCISSOR: ROCK,
}

def result_score(opp_hand, my_hand):
    if opp_hand == my_hand:
        return DRAW
    if win_hands[opp_hand] == my_hand:
        return WIN
    return LOSS

def total_score(opp_hand, my_hand):
    return result_score(opp_hand, my_hand) + hand_scores[my_hand]

# part 2 additions
strategies = {
    'X': LOSS,
    'Y': DRAW,
    'Z': WIN,
}

lose_hands = {v:k for k,v in win_hands.items()}

def total_score_with_strategy(opp_hand, strategy):
    # same hand for a DRAW
    my_hand = opp_hand
    if strategy == WIN:
        my_hand = win_hands[opp_hand]
    if strategy == LOSS:
        my_hand = lose_hands[opp_hand]
    return strategy + hand_scores[my_hand]

# solution
sum = 0
with open('input.txt') as f:
    for c, line in enumerate(f.read().splitlines()):
        letters = line.split(' ')
        opp_hand = opp_conversion[letters[0]]

        # part 1
        # my_hand = my_conversion[letters[1]]
        # score = total_score(opp_hand, my_hand)

        # part 2
        score = total_score_with_strategy(opp_hand, strategies[letters[1]])
        
        sum += score
        
print('my total score: {}'.format(sum))
