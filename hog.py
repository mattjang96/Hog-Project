"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact
from operator import *

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

#Matthew Jang

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1

    """total, k = 0, num_rolls
    while k > 0:
        d = dice()
        if d > 1:
            total, k = total + d, k - 1
        else:
            k -= 1
            return(0)
    return total""" #trial code

    total, k = 0, 1
    pig_out = False
    while k <= num_rolls:
        d = dice()
        if d == 1:
            pig_out = True
        total, k = total + d, k + 1
    if pig_out: #if pig_out == True
        return (0)
    else:
        return total

    # END Question 1

def is_prime(n): 
    if n == 0 or n == 1: #must account for 0 and 1 too (1 is not a prime number)
        return False
    for i in range(2, n): 
        if n % i == 0:
            return False
    return True

def next_prime(n): 
    if is_prime(n+1): #at this point, we already know that n (total for now) is a prime number
        return n + 1
    else:
        return next_prime(n + 1) #used recursion

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2

    if num_rolls == 0:
        total = max(opponent_score // 10, opponent_score % 10) + 1 #Free Bacon Rule
    else: 	
        total = roll_dice(num_rolls, dice)
    if is_prime(total): #Hogtimus Prime Rule
        return next_prime(total) 
    return total

    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    if (score + opponent_score) % 7 == 0: #Hog Wild Rule
        dice = four_sided
    else:
        dice = six_sided
    return dice

    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    if score0 > 100 or score1 > 100: #accounts for score(s) greater than 100
        score0, score1 = score0 % 100, score1 % 100 #(score < 100) % 100 returns itself
    if (score0 % 10) == (score1 // 10) and (score0 // 10) == (score1 % 10):
        return True
    return False #else
    # END Question 4


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who



def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
    # Enforce all the remaining special rules: Piggy Back (check the result of take_turn), Hog wild (call select_dice), and Swine Swap (call is_swap)
    
    def turn_score(current_score, opponent_score, strategy): 
    	strat0 = strategy(current_score, opponent_score)
    	turn_dice = select_dice(current_score, opponent_score)
    	return take_turn(strat0, opponent_score, turn_dice), strat0

    # Main loop
    continue_game = True
    while continue_game:     	
    	if(player == 0):
    		add_score, piggy_back = turn_score(score0, score1, strategy0)
    		if(add_score==0):   #piggy back rule
    			score1 += piggy_back # piggy_back should be an integer (number of dices rolled)
    		score0 += add_score   		
    	else:
    		add_score, piggy_back = turn_score(score1, score0, strategy1)
    		if(add_score==0):   
    			score0 += piggy_back
    		score1 += add_score    	

    	if(is_swap(score0,score1)): #swine swap rule
    		score0, score1 = score1, score0
    	if(score0 >= goal or score1 >= goal):
    		continue_game = False #stop playing if either of the two players' score is greater than 100 (goal)
    	player = other(player) #Return the other player

    return score0, score1

    # END Question 5

  


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy



# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    def average_value(*args): #arbitrary number of arguments called *args
    	sum = 0 
    	k = 0
    	while k < num_samples:
    		sum += fn(*args)
    		k += 1
    	return sum / num_samples
    return average_value
    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    highest_average_score = 0
    best_num_rolls = 0
    k = 10 #max number of rolls is 10
    while k >= 1:
    	x = make_averaged(roll_dice, num_samples)
    	average_dice = x(k, dice)
    	if average_dice >= highest_average_score:
    		highest_average_score = average_dice
    		best_num_rolls = k
    	k = k - 1
    return best_num_rolls


    # END Question 7


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    if take_turn(0, opponent_score) >= margin:
    	return 0
    else: 
    	return num_rolls
    return 5  # Replace this statement
    # END Question 8


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    if_is_swap = take_turn(0, opponent_score)
    if is_swap(if_is_swap + score, opponent_score) and (if_is_swap + score < opponent_score): #checks is_swap and whether or not my score + score is still less than opponent's score
    	return 0 #returns 0 if beneficial (satisfies above if statement)
    else:
    	return num_rolls 
    # END Question 9 

def final_strategy(score, opponent_score): 
    """I used both the bacon_strategy and the swap_strategy 

    """
    # BEGIN Question 1
    margin = 5
    num_rolls = 4
    all_score = opponent_score + score + take_turn(num_rolls, opponent_score, select_dice(score, opponent_score)) 
    if swap_strategy(score, opponent_score, 4) == 0:
        return 0
    if bacon_strategy(score, opponent_score, 5, 4) == 0:
        return 0
    if select_dice == four_sided:
        return 0
    if all_score % 7 == 0:
        return num_rolls
    if abs(opponent_score - score) > 16:
        return 6
    if abs(opponent_score - score) < 20:
        return 3
    if opponent_score > 60:
        return 0
    return num_rolls
    if (swap_strategy(score, opponent_score)) == 0 or (bacon_strategy(score, opponent_score)) == 0:
        return 
    return 2 # Replace this statement
    

    # END Question 10

##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
