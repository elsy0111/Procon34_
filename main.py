import csv

'''
平地　　   : 0 ( Φ )
池        : 1 ( L )
城        : 2 ( C )
先手職人   : 3 (S_A)
後手職人   : 4 (S_B)
先手城壁   : 5 (W_A, A)
後手城壁   : 6 (W_B, B)
'''

def Is_Border(y,x):
    if x == 0 or x == W - 1 or y == 0 or y == H - 1:
        return True
    else:
        return False

def Wall(T):
    if T == "A": # T = 5 => 5
        return 5
    if T == "B": # T = 6 => 6
        return 6

def Enemy_Wall(T):
    if T == "A": # T = 5 => 6
        return 6
    if T == "B": # T = 6 => 5
        return 5

def Is_In_Map(y,x):
    if 0 <= y < H and 0 <= x < W:
        return True
    else:
        return False

Direction = [[0,1],[-1,0],[0,-1],[1,0]] # R U L D

# Is Surrounded => Number of Surrounded Area
def dfs(T,y,x):
    Visited[y][x] = True
    tmp.add((y,x))
    global open
    if Is_Border(y,x):
        open = 1
    for dy,dx in Direction:
        next_y = y + dy
        next_x = x + dx
        if Is_In_Map(next_y,next_x):
            if not Visited[next_y][next_x]:
                if not current_map[next_y][next_x][Wall(T)]:
                    dfs(T,next_y,next_x)
        else:
            continue

def Show_Bool_Arr(arr):
    print()
    print(" \\", end = " ")
    for i in range(H):
        if i < 10:
            print("", end = " ")
        print(i, end = " ")
    print()

    for i in range(H):
        for j in range(W):
            if j == 0:
                if i < 10:
                    print("", end = " ")
                print(i, end = "  ")

            if arr[i][j]:
                print("#",end = "  ") 
            else:
                print(" ",end = "  ") 
                    
        print()
    print()
    return

# Show Array (2Dim H x W)
def Show_Map(arr):
    print("建造物\n")
    print(" \\", end = " ")
    for i in range(H):
        if i < 10:
            print("", end = " ")
        print(i, end = " ")
    print()

    for i in range(H):
        for j in range(W):
            if j == 0:
                if i < 10:
                    print("", end = " ")
                print(i, end = "  ")
            
            # None
            if arr[i][j][0]:
                print(" ", end = "  ")
            # Lake
            elif arr[i][j][1]:
                print("L", end = "  ")
            # Castle
            elif arr[i][j][2]:
                print("C", end = "  ")
            else:
                print(" ", end = "  ")
                
        print()
    print()

    print("職人\n")
    print(" \\", end = " ")
    for i in range(H):
        if i < 10:
            print("", end = " ")
        print(i, end = " ")
    print()

    for i in range(H):
        for j in range(W):
            if j == 0:
                if i < 10:
                    print("", end = " ")
                print(i, end = "  ")
            
            # S_A
            if arr[i][j][3]:
                print("A", end = "  ")
            # S_B
            elif arr[i][j][4]:
                print("B", end = "  ")
            else:
                print(" ", end = "  ")
                
        print()
    print()

    print("壁\n")
    print(" \\", end = " ")
    for i in range(H):
        if i < 10:
            print("", end = " ")
        print(i, end = " ")
    print()

    for i in range(H):
        for j in range(W):
            if j == 0:
                if i < 10:
                    print("", end = " ")
                print(i, end = "  ")
                
            # W_A
            if arr[i][j][5]:
                print("A", end = "  ")
            # W_B
            elif arr[i][j][6]:
                print("B", end = "  ")
            else:
                print(" ", end = "  ")
                
        print()
    print()

    return

# Is Own Wall => True
def Is_Own_Wall(T,y,x): # T \in {"A","B"}
    if T == "A":
        if [y,x] in position_A_wall:
            return True
        else:
            return False
    if T == "B":
        if [y,x] in position_B_wall:
            return True
        else:
            return False

# Is Buildable => True
def Is_Buildable(T,y,x): # T \in {"A","B"}
    return (not Is_Own_Wall(T,y,x)) and Is_Movable(y,x)

# Is Movable => True
def Is_Movable(y,x):
    if [y,x] in (position_castle + position_lake):
        return False
    else:
        return True

def Set2List(Set_):
    k = len(Set_)
    List_ = [[False for _ in range(W)] for _ in range(H)]
    while Set_:
        y,x = Set_.pop()
        List_[y][x] = True
    return List_, k
        
    

# Load Field
filename = 'Field/A11 copy.csv'
f = open(filename, encoding='utf8')
csvreader = list(csv.reader(f))

# Definition H, W
H = len(csvreader)
W = len(csvreader[0])

# 職人
N = 0

# current_map
current_map = [[[0,0,0,0,0,0,0] for _ in range(W)] for _ in range(H)]

# current_position
position_A  = [] # [[y,x],...] (:= [[i,j],...])
position_B  = []

# castle, lake position 
position_castle = []
position_lake = []

# wall position
position_A_wall = []
position_B_wall = []

# String to Integer -> current_map
for i in range(H):
    for j in range(W):
        if csvreader[i][j] in ["a","b"]:
            if csvreader[i][j] == "a":          # S_A
                position_A.append([i,j])
                current_map[i][j][3] = 1
            if csvreader[i][j] == "b":          # S_B
                position_A.append([i,j])
                current_map[i][j][4] = 1 
            N += 1
        else:
            if csvreader[i][j] == "0":          #None
                current_map[i][j][0] = 1
            if csvreader[i][j] == "1":          #Lake
                current_map[i][j][1] = 1
                position_lake.append([i,j])
            if csvreader[i][j] == "2":          #Castle
                current_map[i][j][2] = 1
                position_castle.append([i,j])
            #! Lets say Wall_A = 5
            if csvreader[i][j] == "5":          #Wall_A
                current_map[i][j][5] = 1
                position_A_wall.append([i,j])
            #! Lets say Wall_B = 6
            if csvreader[i][j] == "6":          #Wall_B
                current_map[i][j][6] = 1
                position_B_wall.append([i,j])
                
# Show Current Map
print("\nCurrent Map\n")
Show_Map(current_map)

Filled_set = set()
Visited = [[False for _ in range(W)] for _ in range(H)]

T = "A"
for i in range(H):
    for j in range(W):
        if not Visited[i][j]:
            # Map_{i,j} != W_A
            # W_A = 5
            if not current_map[i][j][Wall(T)]:
                tmp = set()
                open = 0
                dfs(T,i,j)
                if not open:
                    Filled_set = Filled_set | tmp

Filled_A, Wall_pts_A = Set2List(Filled_set)
print("\nA Area\n")
print("Pts :",Wall_pts_A)
Show_Bool_Arr(Filled_A)


Filled_set = set()
Visited = [[False for _ in range(W)] for _ in range(H)]
T = "B"
for i in range(H):
    for j in range(W):
        if not Visited[i][j]:
            # Map_{i,j} != W_B
            # W_B = 6
            if not current_map[i][j][Wall(T)]:
                tmp = set()
                open = 0
                dfs(T,i,j)
                if not open:
                    Filled_set = Filled_set | tmp

Filled_B, Wall_pts_B = Set2List(Filled_set)
print("\nB Area\n")
print("Pts :",Wall_pts_B)
Show_Bool_Arr(Filled_B)

