import sys
from collections import deque
from heapq import heappop, heappush, heapify

input = sys.stdin.readline

N, M, P, C, D = map(int, input().split())

r_x, r_y = map(int, input().split())

santa_pos = [[0,0] for _ in range(P+1)]
santa_score = [0 for _ in range(P+1)]
santa_sturn = [0 for _ in range(P+1)]
santa_dead = [False for _ in range(P+1)]

for _ in range(P):
    num, x, y = map(int, input().split())
    santa_pos[num][0] = x
    santa_pos[num][1] = y

#루돌프 방향
r_direction = [[-1,0],[-1,1],[0,1],[1,1], [1,0],[1,-1],[0,-1],[-1,-1]]
#산타 방향
s_direction = [[-1,0], [0,1], [1,0],[0,-1]]

def rudolph_move():

    r_s_distance = []

    r_candidate = []

    #가장 가까운 산타 찾기
    for i, [x, y] in enumerate(santa_pos):
        #0번 스킵
        if i == 0:
            continue
        if santa_dead[i]:
            continue
        #산타와의거리
        distance = ((r_x - x) ** 2) + ((r_y - y) ** 2)
        heappush(r_s_distance, [distance, -x, -y, i])
        # r_s_distance.append([distance, -x, -y, i])
    
    # r_s_distance.sort()


    index = r_s_distance[0][3]

    santa_x = santa_pos[index][0]
    santa_y = santa_pos[index][1]
    
    # print("가장가까운산타 ", index, santa_x, santa_y)

    #가장 가까운 방향 찾기
    for i, [dx, dy] in enumerate(r_direction):
        next_x = r_x + dx
        next_y = r_y + dy

        #경계밖체크
        if next_x < 1 or next_x > N or next_y < 1 or next_y > N:
            continue
        distance = ((santa_x - next_x) ** 2) + ((santa_y - next_y) ** 2)
        r_candidate.append([distance, next_x, next_y, i])
    
    r_candidate.sort()
    # print(r_candidate)

    return r_candidate[0][1], r_candidate[0][2], r_candidate[0][3]

def santa_move(s_x, s_y, myself):

    limit = ((r_x - s_x) ** 2) + ((r_y - s_y) ** 2)
    candidate = []

    for i, [dx, dy] in enumerate(s_direction):

        next_x = s_x + dx
        next_y = s_y + dy

        #경계밖이면
        if next_x < 1 or next_x > N or next_y < 1 or next_y > N:
            continue
        
        distance = ((r_x - next_x) ** 2) + ((r_y - next_y) ** 2)

        #거리가 줄어들지 않으면.
        if distance > limit:
            continue
        
        #산타가 존재하면
        if find_santa_index(next_x, next_y, True, myself) != -1:
            continue
        
        candidate.append([distance, i, next_x, next_y])

    candidate.sort()
    # print(candidate)
    # print(candidate)
    #움직일 수 없다면
    if len(candidate) == 0:
        return s_x, s_y, 0
    else:
        return candidate[0][2], candidate[0][3], candidate[0][1]


def find_santa_index(target_x, target_y, santa, myself):

    #산타있는지 체크
    for i, [x, y] in enumerate(santa_pos):
        if i == 0:
            continue
        if santa_dead[i]:
            continue
        if santa:
            if i == myself:
                continue
        
        # print("santalis", x, y,i)

        #충돌이 일어 났다면 스택에 추가
        if (target_x == x) and (target_y == y):
            return i

    return -1

def 충돌(santa_index, r_dir_i):
    q = deque()
    q.append(santa_index)

    #처음밀리는지 확인
    isFirst = True

    while q:
        i = q.popleft()

        tmp = 0
        if isFirst:
            tmp = C
        else:
            tmp = 1

        next_x = santa_pos[i][0] + tmp * r_direction[r_dir_i][0]
        next_y = santa_pos[i][1] + tmp * r_direction[r_dir_i][1]

        #산타 점수 갱신
        if isFirst:
            santa_score[i] += C

        #밖으로 튕겨나가면
        if next_x < 1 or next_x > N or next_y < 1 or next_y > N:
            santa_dead[i] = True
            continue

        #산타 좌표 갱신
        santa_pos[i][0] = next_x
        santa_pos[i][1] = next_y

        #아직 판에 존재하면 스턴 셋팅
        if isFirst:
            santa_sturn[i] = 2

        next_i = find_santa_index(next_x, next_y, True, i)

        #다음칸에 산타가 있다면
        if next_i != -1:
            q.append(next_i)
            isFirst = False


#M 번 턴동안 
for k in range(M):
    
    # print("----------------", k)
    #루돌프 이동
    r_next_x, r_next_y, r_dir_i = rudolph_move()

    santa_index = find_santa_index(r_next_x, r_next_y, False, 0)


    # print("santa", santa_index)
    #루돌프 -> 산타 충돌 로직
    if santa_index != -1:
        충돌(santa_index, r_dir_i)

    #루돌프 좌표 갱신
    r_x = r_next_x
    r_y = r_next_y

    #산타 차례
    for i, [x,y] in enumerate(santa_pos):
        if i == 0:
            continue
        #죽었으면 패스
        if santa_dead[i]:
            continue
        #기절했으면 1개빼고 패스
        if santa_sturn[i] != 0:
            continue
        
        #산타이동
        # print("santa_move ", i)
        s_x, s_y, s_d = santa_move(x, y, i)

        santa_pos[i][0] = s_x
        santa_pos[i][1] = s_y

        # print("r_x, r_y", r_x, r_y)
        # print("s_x, s_y", s_x, s_y, s_d)
        #이동한 곳이 루돌프면
        if (r_x == s_x) and (r_y == s_y):
            
            q = deque()
            q.append(i)
            isFirst = True

            while q:
                index = q.popleft()

                # print("----------index--------", index)

                tmp = 0
                
                #연쇄충돌설정
                if isFirst:
                    tmp = D
                else:
                    tmp = 1

                
                #진행방향 반대 설정
                current_dir = 0

                if s_d == 0:
                    current_dir = 2
                elif s_d == 1:
                    current_dir = 3
                elif s_d == 2:
                    current_dir = 0
                elif s_d == 3:
                    current_dir = 1

                next_x = santa_pos[index][0] + tmp * s_direction[current_dir][0]
                next_y = santa_pos[index][1] + tmp * s_direction[current_dir][1]

                #산타 점수 갱신
                if isFirst:
                    santa_score[index] += D

                #밖으로 튕겨나가면
                if next_x < 1 or next_x > N or next_y < 1 or next_y > N:
                    santa_dead[index] = True
                    continue

                #산타 좌표 갱신
                santa_pos[index][0] = next_x
                santa_pos[index][1] = next_y

                #아직 판에 존재하면 스턴 셋팅
                if isFirst:
                    santa_sturn[index] = 2

                # print("next_x, next_y", next_x, next_y)
                next_i = find_santa_index(next_x, next_y, True, index)

                # print("-----next-----", next_i)
                #다음칸에 산타가 있다면
                if next_i != -1:
                    q.append(next_i)
                    isFirst = False            
        # print("santa_move", i, s_x, s_y)


    # print(x, y)

    count = 0
    #살아있으면 1점추가
    for i in range(1, P+1):
        if santa_dead[i] == False:
            santa_score[i] += 1
        else:
            count += 1
    
    #산타다죽었으면게임종료
    if count == P:
        break
    #sturn 1개 줄이기
    for i in range(1, P+1):
        if santa_sturn[i] != 0:
            santa_sturn[i] -= 1
    # print(r_x, r_y)
    # print(santa_dead)
    # print(santa_score)
    # print(santa_pos)
    # print(santa_sturn)

    # if k == 3:
    #     break

# print(r_x, r_y)
# print(santa_dead)
# print(santa_score)
# print(santa_pos)
# print(santa_sturn)

for i in range(1, P + 1):
    print(santa_score[i], end=" ")