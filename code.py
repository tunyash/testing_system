::python3
::header
import random
import copy
counter = 0
array = []

def decrypt(i, a):
    return a ^ (7*i + 443)

def encrypt(i, a):
    return a ^ (7*i + 353)

def access(i):
    global counter, array 
    counter = encrypt(3433, decrypt(3433, counter) + 1)
    mylen = len(array)
    assert i - 1 >= 0 and i - 1 < mylen
    return decrypt(i, array[i - 1])

def answer(i, j):
    global ans
    ans = (i, j)
::code
        
def make_step(n, state):
    """
    This solution enumerates all pairs of indices in the array and returns the collision.
    """
    i = state[0]
    j = state[1]
    if i != j and access(i) == access(j):
        answer(i, j)
        return state
    if j < n + 1:
        j += 1
    else:
        j = 1
        i += 1
    state[0] = i
    state[1] = j
    return state

def init(n):
    return [1, 1] + [0] * 8
::footer

n = int(input())
a = list(map(int, input().split()))
ans = None
array = [encrypt(i + 1, x) for i, x in enumerate(a)]
arrays = [array]
origin_arrays = [a]
for _ in range(2):    
    aprime = copy.deepcopy(a)
    random.shuffle(aprime)
    origin_arrays.append(aprime)
    arrays.append([encrypt(i + 1, x) for i, x in enumerate(aprime)])
states = [init(n) for _ in range(len(arrays))]
answers = [None for _ in range(len(arrays))]
counter = encrypt(3433, 0)
for i in range(n * 5):  
    for j in range(len(arrays)):
        if answers[j] is not None:
            continue
        prev_state = None
        new_state = None
        array = arrays[j]
        for _ in range(random.randint(1,3)):
            ans = None
            counter_before = decrypt(3433, counter)
            state_copy = copy.deepcopy(states[j])
            new_state = make_step(n - 1, state_copy)
            counter_after = decrypt(3433, counter)
            assert counter_after >= counter_before
            assert counter_after <= counter_before + 5
            assert len(new_state) == 10
            new_state = list(map(int, new_state))
            assert min(new_state) >= 0 and max(new_state) <= 100 * n * n
            if prev_state is not None:
                for x, y in zip(prev_state, new_state):
                    assert x == y
            prev_state = copy.deepcopy(new_state)
        if ans is not None:
            answers[j] = copy.deepcopy(ans)
        states[j] = copy.deepcopy(new_state)

for j in range(len(arrays)):
    assert(len(answers[j]) == 2)
    if origin_arrays[j][answers[j][0] - 1] != origin_arrays[j][answers[j][1] - 1] or answers[j][0] == answers[j][1]:
        print(-1, -1)
        exit(0)
print(answers[0][0], answers[0][1])
