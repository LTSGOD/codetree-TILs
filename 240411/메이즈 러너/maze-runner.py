import sys

input = sys.stdin.readline

def calculate_move(current_x, current_y):
    
    global count
    candidate = []

    #출구까리 최단거리
    limit = abs(e_x - current_x) + abs(e_y - current_y)
    
    #방향체크
    for i, [dx, dy] in enumerate(direction):
        next_x = current_x + dx
        next_y = current_y + dy

        #범위 넘어가면
        if next_x < 1 or next_x > N or next_y  < 1 or next_y > N:
            continue
        
        #벽이면 pass
        if board[next_x][next_y]:
            continue
        
        current_distance = abs(e_x - next_x) + abs(e_y - next_y)

        #더 작아지면 추가
        if current_distance < limit:
            candidate.append([i, next_x, next_y])

    #움직일수 없다면
    if len(candidate) == 0:
        return current_x, current_y
    else:
        count += 1
        return candidate[0][1], candidate[0][2]

N, M, K = map(int, input().split())

board = [[0 for _ in range(N + 1)]]
exit = [False for _ in range(M)]
pos = []
global e_x, e_y
global count
e_x, e_y = 0,0
count = 0



for _ in range(N):
    board.append([0] + list(map(int, input().split())))

for _ in range(M):
    pos.append(list(map(int, input().split())))

e_x, e_y = map(int, input().split())

direction = [[-1,0], [1,0], [0, -1], [0, 1]]

def calculate_retangle():
    
    #직사각형 좌상단, 길이
    candidate = []

    #참가자마다좌표 구하기
    for i in range(M):

        if exit[i]:
            continue

        l_x = 0
        l_y = 0

        x = pos[i][0]
        y = pos[i][1]

        #한변의길이
        r_len = max(abs(e_y - y), abs(e_x - x)) + 1
        
        #r좌표가더큰것이 밑바닥으로 붙음.
        if e_x < x:
            l_x = x - r_len + 1

        else:
            l_x = e_x - r_len + 1
        
        #x범위넘어가면
        if l_x < 1:
            l_x = 1

        #y좌표가 더 큰것이 오른쪽으로 붙음.

        if e_y < y:
            l_y = y - r_len + 1
        else:
            l_y = e_y - r_len + 1
        
        #예외 범위 넘어가면
        if l_y < 1:
            l_y = 1
        candidate.append([r_len, l_x, l_y])

    candidate.sort()
    # print("rec candida/te ", candidate)

    return candidate[0][1], candidate[0][2], candidate[0][0]

def rotate(x, y, length):
    global e_x, e_y

    #출구 로테이트
    next_e_x = (e_y - y + 1)
    next_e_y = r_len + 1 - (e_x - x + 1)

    e_x = next_e_x + x -1
    e_y = next_e_y + y - 1

    #참가자 좌표 로테이트
    for p_num in range(M):
        if exit[p_num]:
            continue
        #참가자가 범위안에 있으면
        if x <= pos[p_num][0] and x+ length -1 >= pos[p_num][0] and y <= pos[p_num][1] and y + length -1 >= pos[p_num][1]:
            
            #좌표 보정
            p_x = pos[p_num][0] - x + 1
            p_y = pos[p_num][1] - y + 1

            #90도회전
            next_p_x = p_y
            next_p_y = r_len + 1 - p_x

            #저장
            pos[p_num][0] = next_p_x + x - 1
            pos[p_num][1] = next_p_y + y - 1

    임시사각형 = [[0 for _ in range(r_len + 1)] for _ in range(r_len + 1)]

    #임시사각형에 로테이트
    for i in range(x, x+length):
        for j in range(y, y+length):

            #좌표보정
            tmp_x = i - x + 1
            tmp_y = j - y + 1

            rotate_x = r_len + 1 - tmp_y
            rotate_y = tmp_x

            임시사각형[tmp_x][tmp_y] = board[rotate_x + x - 1][rotate_y + y - 1]

            #벽내구도 감소
            if 임시사각형[tmp_x][tmp_y]:
                임시사각형[tmp_x][tmp_y]-= 1

    #임시사각형에 board반영

    for i in range(x, x + length):
        for j in range(y, y+length):
            board[i][j] = 임시사각형[i -x + 1][j - y + 1]


#초마다 시작
for i in range(1, K + 1):
    # print("--------", i, "------------")
    
    #참가자 움직이기
    for num in range(M):
        
        #탈출했으면
        if exit[num]:
            continue
        p_x = pos[num][0]
        p_y = pos[num][1]

        #다음좌표 계산
        next_x, next_y = calculate_move(p_x, p_y)

        #이동
        pos[num][0] = next_x
        pos[num][1] = next_y

        #탈출구라면
        if (pos[num][0] == e_x) and (pos[num][1] == e_y):
            exit[num] = True

    #다 탈출하면
    for i in range(M):
        if not exit[i]:
            break
    else:
        break

    #가장작은정사각형 계산
    r_x, r_y, r_len = calculate_retangle()

    rotate(r_x, r_y, r_len)

print(count)
print(e_x, e_y)