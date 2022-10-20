'''BackMan.py
This Backgammon player simply asks the user to decide how
to move.  It can be used either to test another agent in
a competition, or to test the game master itself.

'''
from backgState import *

MAX = 0
MIN = 0
STATES_CREATED = 0
CUTOFFS = 0
AlPHA = True
MAX_PLAY = 3


def move(state, die1, die2):
  w = state.whose_move
  global MAX
  MAX = w
  global MIN
  MIN = 1 - w
  provisional, ans = minimax(state, die1, die2, w, MAX_PLAY, float('-inf'), float('inf'))
  print("I'm playing " + get_color(w))
  print("Tell me which checkers to move, with point numbers, e.g., 19,7")
  print("Use 0 to move from the bar.")
  print("If you want your first (or only) checker to move according")
  print("to the 2nd die, add a 3rd argument R: e.g., 19,7,R to reverse the dice.")
  print("For only 1 checker to move with both dice, give as 2nd argument the point number")
  print("where the checker will be after the move is half done.")
  # ans = input("or enter Q to quit: ")
  return ans
  # return "Q" # quit


def minimax(state, die1, die2, whose_move, play_left, alpha, beta):
  global CUTOFFS
  if play_left == 0:
    return staticEval(state), 'P'
  if whose_move == MAX:
    provisional = float('-inf')
  else:
    provisional = float('inf')
  succ, moves = successors(state, die1, die2, whose_move)
  if succ == []:
    return provisional, 'P'
  else:
    chosen = succ[0]
    for s in succ:
      global STATES_CREATED
      STATES_CREATED += 1
      newVal, command = minimax(s, die1, die2, 1 - whose_move, play_left - 1, alpha, beta)
      if whose_move == MAX and newVal > provisional:
        provisional = newVal
        chosen = s
        if AlPHA:
          alpha = max(alpha, provisional)
          if beta <= alpha:
            CUTOFFS += 1
            break
      elif whose_move == MIN and newVal < provisional:
        provisional = newVal
        chosen = s
        if AlPHA:
          beta = min(beta, provisional)
          if beta <= alpha:
            CUTOFFS += 1
            break
    return provisional, moves[succ.index(chosen)]


def useAlphaBetaPruning(prune=False):
  global AlPHA
  global STATES_CREATED
  if (prune):
    AlPHA = True
  else:
    STATES_CREATED = 0
    AlPHA = 0


def statesAndCutoffsCounts():
  return STATES_CREATED, CUTOFFS


def setMaxPly(maxply=-1):
  global MAX_PLAY
  MAX_PLAY = maxply


def staticEval(state):
  w = state.whose_move
  MAX = w
  MIN = 1 - w
  max_checker = []
  min_checker = []
  points = state.pointLists
  max_sum = 0
  min_sum = 0
  result = 0
  for p in range(len(points)):
    if points[p] != [] and points[p][0] == MAX:
      max_checker.append(p)
  for i in range(len(max_checker)):
    if MAX == 0:
      max_sum += len(points[max_checker[i]]) * max_checker[i]
    if MAX == 1:
      max_sum += (23 - max_checker[i]) * len(points[max_checker[i]])
  if MAX == 0:
    max_off = len(state.white_off)
  else:
    max_off = len(state.red_off)

  for p in range(len(points)):
    if points[p] != [] and points[p][0] == MIN:
      min_checker.append(p)
  for i in range(len(min_checker)):
    if MIN == 0:
      min_sum += len(points[min_checker[i]]) * min_checker[i]
    if MIN == 1:
      min_sum += (23 - min_checker[i]) * len(points[min_checker[i]])
  if MIN == 0:
    min_off = len(state.white_off)
  else:
    min_off = len(state.red_off)
  if bearing_off_allowed(state, w):
    result += max_off * 5000 - min_off * 5000

  result += max_sum * 10 + state.bar.count(MIN) * 100 - state.bar.count(MAX) * 100
  if win_detected(state, MAX):
    result = 100000
  if win_detected(state, MIN):
    result = -100000
  # print(max_off, max_sum, state.bar.count(MIN), state.bar.count(
  # MAX), min_sum, min_off)
  return result


# get successors
def successors(state, die1, die2, whose_move):
  # for each point
  # figure out which piece is allowed to move
  # where it can move to
  # generate legal moves (from+to)
  # new state = successor
  succ = []  # store all the successors states
  moves = []
  first = max(die1, die2)
  second = min(die1, die2)
  move = ''
  move1 = ''
  move2 = ''
  curr_state = bgstate(state)
  points1 = curr_state.pointLists
  check1 = []
  check2 = []
  # alwas move the checker on the bar first
  if any_on_bar(curr_state, whose_move):
    curr1, move1 = handle_move_from_bar(curr_state, whose_move, first)
    # if pass first, pass the entire turn
    if any_on_bar(curr1, whose_move):
      curr2, move2 = handle_move_from_bar(curr1, whose_move, second)
      succ.append(curr2)
      # combie the 2 moved checkers into one command    *P,P,R case?
      move = move1 + ',' + move2
      if move[:1] == "P":
        if move[2:] != "P":
          move = move2 + ',' + move1
          if die1 > die2:
            move += ',R'
          moves.append(move)
          return succ, moves
        else:
          moves.append('P')
          return succ, moves
      else:
        # reverse the move if die1 < die2, since it always choose the greater value first
        if die1 < die2:
          move += ',R'
        moves.append(move)
        return succ, moves
    else:
      # check current locations of all checkers
      for p in range(len(curr1.pointLists)):
        if curr1.pointLists[p] != [] and curr1.pointLists[p][0] == whose_move:
          check1.append(p)
      for i in range(len(check1)):
        starting_point = check1[i] + 1
        curr2, move2 = possible_moves(curr1, starting_point, whose_move, second)
        # add to succesors
        succ.append(curr2)
        # combie the 2 moved checkers into one command
        move = move1 + ',' + move2
        if move[:1] == "P":
          if move[2:] != "P":
            move = move2 + ',' + move1
            if die1 > die2:
              move += ',R'
            moves.append(move)
          else:
            moves.append('P')
        else:
          # reverse the move if die1 < die2, since it always choose the greater value first
          if die1 < die2:
            move += ',R'
          moves.append(move)
      return succ, moves
  else:
    # check current locations of all checkers
    for p in range(len(points1)):
      if points1[p] != [] and points1[p][0] == whose_move:
        check1.append(p)
    # first move
    for i in range(len(check1)):
      starting_point1 = check1[i] + 1
      curr1, move1 = possible_moves(curr_state, starting_point1, whose_move, first)
      # second move
      points2 = curr1.pointLists
      # check current locations of all checkers
      for p in range(len(points2)):
        if points2[p] != [] and points2[p][0] == whose_move:
          check2.append(p)
      for j in range(len(check2)):
        starting_point2 = check2[j] + 1
        curr2, move2 = possible_moves(curr1, starting_point2, whose_move, second)
        # add to succesors
        succ.append(curr2)
        # combie the 2 moved checkers into one command    *P,P,R case?
        move = move1 + ',' + move2
        if move[:1] == "P":
          if move[2:] != "P":
            move = move2 + ',' + move1
            if die1 > die2:
              move += ',R'
            moves.append(move)
          else:
            moves.append('P')
        else:
          # reverse the move if die1 < die2, since it always choose the greater value first
          if die1 < die2:
            move += ',R'
          moves.append(move)
        # Empty check2
      check2 = []
    return succ, moves


def possible_moves(state, starting_point, whose_move, roll):
  curr_state = bgstate(state)
  move = ''
  # move checker
  if whose_move == 0:
    end_point = starting_point + roll
  else:
    end_point = starting_point - roll

  if bearing_off_allowed(state, whose_move):
    if bear_off(curr_state, starting_point, end_point, whose_move):
      curr_state = bear_off(curr_state, starting_point, end_point, whose_move)
      return curr_state, str(starting_point)
    else:
      if end_point < 1 or end_point > 24:
        return curr_state, 'P'
      else:
        target_list = curr_state.pointLists[end_point - 1]
        if target_list != [] and target_list[0] != whose_move and len(target_list) > 1:
          return curr_state, 'P'
        else:
          curr_state.pointLists[starting_point - 1].pop()  # remove last checker form point
          curr_state = hit(curr_state, target_list, end_point)
          curr_state.pointLists[end_point - 1].append(whose_move)
          # copy this state
          # new_state = bgstate(curr_state)
          return curr_state, str(starting_point)
  else:
    if end_point < 1 or end_point > 24:
      return curr_state, 'P'
    else:
      target_list = curr_state.pointLists[end_point - 1]
      if target_list != [] and target_list[0] != whose_move and len(target_list) > 1:
        return curr_state, 'P'
      else:
        curr_state.pointLists[starting_point - 1].pop()  # remove last checker form point
        curr_state = hit(curr_state, target_list, end_point)
        curr_state.pointLists[end_point - 1].append(whose_move)
        # copy this state
        # new_state = bgstate(curr_state)
        return curr_state, str(starting_point)


def any_on_bar(state, who):
  return who in state.bar


def remove_from_bar(new_state, who):
  # removes a white from start of bar list,
  # or a red from the end of the bar list.
  if who == W:
    del new_state.bar[0]
  else:
    new_state.bar.pop()


def handle_move_from_bar(state, who, die):
  # We assume there is a piece of this color available on the bar.
  if who == W:
    target_point = die
  else:
    target_point = 25 - die
  pointList = state.pointLists[target_point - 1]
  if pointList != [] and pointList[0] != who and len(pointList) > 1:
    return state, 'P'
  new_state = bgstate(state)
  new_state = hit(new_state, pointList, target_point)
  remove_from_bar(new_state, who)
  new_state.pointLists[target_point - 1].append(who)
  return new_state, '0'


def hit(new_state, dest_pt_list, dest_pt):
  opponent = 1 - new_state.whose_move
  if len(dest_pt_list) == 1 and dest_pt_list[0] == opponent:
    if opponent == W:
      new_state.bar.insert(W, 0)  # Whites at front of bar
    else:
      new_state.bar.append(R)  # Reds at end of bar
    new_state.pointLists[dest_pt - 1] = []
  return new_state


def bearing_off_allowed(state, who):
  # True provided no checkers of this color on the bar or in
  # first three quadrants.
  if any_on_bar(state, who): return False
  if who == W:
    point_range = range(0, 18)
  else:
    point_range = range(6, 24)
  pl = state.pointLists
  for i in point_range:
    if pl[i] == []: continue
    if pl[i][0] == who: return False
  return True


def bear_off(state, src_pt, dest_pt, who):
  # Return False if 'who' is not allowed to bear off this way.
  # Otherwise, create the new state showing the result of bearing
  # this one checker off, and return the new state.

  # First of all, is bearing off allowed, regardless of the dice roll?
  if not bearing_off_allowed(state, who): return False
  # Direct bear-off, if possible:
  pl = state.pointLists[src_pt - 1]
  if pl == [] or pl[0] != who:
    return False
  # So there is a checker to possibly bear off.
  # If it does not go exactly off, then there must be
  # no pieces of the same color behind it, and dest
  # can only be one further away.
  good = False
  if who == W:
    if dest_pt == 25:
      good = True
    elif dest_pt == 26:
      for point in range(18, src_pt - 1):
        if W in state.pointLists[point]: return False
      good = True
  elif who == R:
    if dest_pt == 0:
      good = True
    elif dest_pt == -1:
      for point in range(src_pt, 6):
        if R in state.pointLists[point]: return False
      good = True
  if not good: return False
  born_off_state = bgstate(state)
  born_off_state.pointLists[src_pt - 1].pop()
  if who == W:
    born_off_state.white_off.append(W)
  else:
    born_off_state.red_off.append(R)
  return born_off_state


def win_detected(state, who):
  if who == W:
    return len(state.white_off) == 15
  else:
    return len(state.red_off) == 15
