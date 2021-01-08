import copy
import collections
import warnings

warnings.filterwarnings("ignore")
#check inputs to ensure validity
def InputChecker(n_pegs,disc_weight):
    if not(isinstance(n_pegs, int) and n_pegs >= 3):
        print("ERROR: first input should be an integer greater than 2")
        return False
    if not(isinstance(disc_weight, list)):
        print('ERROR: second input should be a list')
        return False
    for i in disc_weight:
        if not (isinstance(i, int) and i>0):
            print("ERROR: second input list should contain only positive integers")
            return False
    return True

#flatten list
def flatten(nested_list):
    if isinstance(nested_list, collections.Iterable):
        return [j for i in nested_list for j in flatten(i)]
    else:
        return [nested_list]

#state is a 2D array indicating which disks are on which pegs. disks bottom to top, left to right.
def IsGoal(state):
    n_pegs=len(state)
    target=[[] for i in range(n_pegs-1)]
    order=sorted(flatten(state))[::-1]
    target.append(order)
    return state == target

#convert from input to state
def InputToState(n_pegs, disc_weight):
    target = [[] for i in range(n_pegs)]
    target[0] = disc_weight
    return target

#return a list of valid moves
def ComputeNeighbors(state):
    move_list=[]
    n_pegs=len(state)
    for i in range(n_pegs): #choose peg to remove from
        if len(state[i]) != 0: #something to take off the top
            for j in range(n_pegs): #choose peg to add to
                if j == i: #don't add and take off of the same peg
                    continue
                if len(state[j]) == 0 or state[j][-1] > state[i][-1]:
                    to_add = state[i][-1]
                    state_copy=copy.deepcopy(state)
                    state_copy[j].append(to_add)
                    state_copy[i].remove(to_add)
                    move_list.append(state_copy)
    return move_list

#convert nested list to nested tuple
def ListToTuple(lst):
    tup=[]
    for i in lst:
        i=tuple(i)
        tup.append(i)
    tup=tuple(tup)
    return tup

#convert nested tuple to nested list
def TupleToList(tup):
    lst=[]
    for i in tup:
        i=list(i)
        lst.append(i)
    return lst

#convert a state path to a sequence of moves
def StatesToMoves(path):
    seq=[]
    if len(path) < 2:
        return []
    for i in range(len(path)-1):
        two_tuple=[-1,-1]
        for j in range(len(path[i])):
            if len(path[i][j]) > len(path[i+1][j]):
                two_tuple[0]=j #peg you removed from
            if len(path[i][j]) < len(path[i+1][j]):
                two_tuple[1]=j
        two_tuple=tuple(two_tuple)
        seq.append(two_tuple)
        two_tuple=[-1,-1]
    return seq

#take in a converted state
def BFS(state):
    state=ListToTuple(state)
    frontier=[state]
    discovered = set()
    parents={state:None}
    while len(frontier) > 0:
        current_state=frontier.pop(0)
        discovered.add(current_state)
        if IsGoal(TupleToList(current_state)):
            path=[current_state]
            par=parents[current_state]
            while par != None:
                path.append(par)
                par=parents[par]
            return StatesToMoves(path[::-1])
        for neighbor in ComputeNeighbors(TupleToList(current_state)):
            neighbor=ListToTuple(neighbor)
            if neighbor not in discovered and neighbor not in frontier:
                frontier.append(neighbor)
                parents[neighbor]=current_state
    print('not solvable')
    return None


#requested function
def hanoi(n_pegs, disc_weight):
    if InputChecker(n_pegs, disc_weight):
        state=InputToState(n_pegs,disc_weight)
        return BFS(state)
    print("ERROR")
    return None

print(hanoi(3,[5,4,3,2,1]))