import numpy as np
from omok import OmokState
from util import random_act

DEPTH = 3


def act(state: OmokState):
    if len(state.history) == 0:
        return 9, 9

    prev_stone = state.history[-7:]
    node = (state.game_board, prev_stone)        # 노드 구성 : game_board, 이전 돌, cost

    v, pos = alpha_beta_search(node, DEPTH, float("-inf"), float("inf"), 1, None)
    # v : value, pos : 돌 위치
    x_pos, y_pos = pos[0], pos[1]

    # 이미 돌이 놓여있다면 상하좌우 주변 빈 공간에 놓기
    if not state.is_valid_position(x_pos, y_pos):
        x_min = x_pos - 1 if x_pos - 1 > 0 else 0
        x_max = x_pos + 1 if x_pos + 1 < 18 else 18
        x_pos = np.arange(x_min, x_max + 1)

        y_min = y_pos - 1 if y_pos - 1 > 0 else 0
        y_max = y_pos + 1 if y_pos + 1 < 18 else 18
        y_pos = np.arange(y_min, y_max + 1)

        next_stones = set()
        [next_stones.add((x, y)) for x in x_pos for y in y_pos]

        for x in next_stones:
            if state.is_valid_position(x[0], x[1]):
                return x[1], x[0]
        print("rand!2222")

        # 상하좌우에도 놓여있다면 랜덤으로 놓기
        return random_act(state)

    return y_pos, x_pos


def alpha_beta_search(node, depth, a, b, player, start):
    if depth == 0:  # 깊이가 0이면 탐색 종료
        return evaluate2(node, start)
        # return evaluate(node)

    state = node[0]
    stones = get_next_stones(node)

    if player == 1:  # 나(흑)의 입장
        v = float("-inf")

        pos = stones[0]
        for stone in stones:
            child_state = np.copy(state)
            child_state[stone[1]][stone[0]] = 1
            prev_stone = [node[1][-1], stone]
            child_node = (child_state, prev_stone)
            if depth == 3:
                start = stone
            child_value, child_pos = alpha_beta_search(child_node, depth - 1, a, b, -1, start)
            if v < child_value:
                v = child_value
                pos = child_pos
            a = max(a, v)
            if b <= a:
                break

        return v, pos

    elif player == -1:  # 상대(백)의 입장
        v = float("inf")
        pos = None
        for stone in stones:
            pos = stone
            child_state = np.copy(state)
            child_state[stone[1]][stone[0]] = -1
            prev_stone = [node[1][-1], stone]
            child_node = (child_state, prev_stone)
            if depth == 3:
                start = stone
            child_value, child_pos = alpha_beta_search(child_node, depth - 1, a, b, -1, start)
            if v > child_value:
                v = child_value
                pos = child_pos
            b = min(b, v)

            if b <= a:
                break

        return v, pos


def evaluate2(node, start):
    # o o o   o 이런식으로 놓인 패턴일 때 빈공간 좌표의 점수를 크게 줘야 함
    # o o o o   이런식으로 놓인 패턴(가로, 세로, 대각선 방향 모두 고려)일 때 빈공간 좌표의 점수를 크게 줘야 함
    score = 0
    black_cnt = 0
    white_cnt = 0

    state = node[0]

    x_start, y_start = start
    # if state[start[1]][start[0]] == 1:
    #     print("dddddddddddddddddddddddddddddd")

    x_min = start[0] - 4 if start[0] - 4 > 0 else 0
    x_max = start[0] + 4 if start[0] + 4 < 18 else 18

    y_min = start[1] - 4 if start[1] - 4 > 0 else 0
    y_max = start[1] + 4 if start[1] + 4 < 18 else 18

    if y_start + 1 < 19 and y_start - 1 >= 0:
        if state[y_start - 1][x_start] == state[y_start + 1][x_start] == 1:
            black_cnt += 8
    if y_start + 1 < 19 and y_start - 2 >= 0:
        if state[y_start - 2][x_start] == state[y_start - 1][x_start] == state[y_start + 1][x_start] == 1:
            black_cnt += 5
    if y_start + 2 < 19 and y_start - 1 >= 0:
        if state[y_start - 1][x_start] == state[y_start + 1][x_start] == state[y_start + 2][x_start] == 1:
            black_cnt += 5
    if y_start + 1 < 19:
        if state[y_start][x_start] == state[y_start + 1][x_start]:
            black_cnt += 9
    if y_start + 2 < 19:
        if state[y_start][x_start] == state[y_start + 2][x_start]:
            black_cnt += 8
    if y_start + 3 < 19:
        if state[y_start][x_start] == state[y_start + 2][x_start] == state[y_start + 3][x_start]:
            black_cnt += 5
    if y_start + 3 < 19:
        if state[y_start][x_start] == state[y_start + 1][x_start] == state[y_start + 3][x_start]:
            black_cnt += 5
    if y_start - 1 < 19:
        if state[y_start][x_start] == state[y_start + 1][x_start]:
            black_cnt += 9
    if y_start - 2 < 19:
        if state[y_start][x_start] == state[y_start + 1][x_start]:
            black_cnt += 9
    if y_start - 3 < 19:
        if state[y_start][x_start] == state[y_start - 3][x_start]:
            black_cnt += 5
    if y_start - 3 < 19:
        if state[y_start][x_start] == state[y_start - 3][x_start] == state[y_start - 2][x_start]:
            black_cnt += 5
    if y_start - 3 >= 0:
        if state[y_start][x_start] == state[y_start - 3][x_start] == state[y_start - 1][x_start]:
            black_cnt += 5
    if y_start - 2 >= 0:
        if state[y_start][x_start] == state[y_start - 1][x_start] == state[y_start - 2][x_start]:
            black_cnt += 8
    if y_start - 2 >= 0:
        if state[y_start][x_start] == state[y_start - 2][x_start]:
            black_cnt += 8
    if y_start + 3 < 19:
        if state[y_start][x_start] == state[y_start + 1][x_start] == state[y_start + 3][x_start]:
            black_cnt += 5

    if x_start + 1 < 19:
        if state[y_start][x_start] == state[y_start][x_start + 1]:
            black_cnt += 9
    if x_start - 1 < 19:
        if state[y_start][x_start] == state[y_start][x_start - 1]:
            black_cnt += 8
    if x_start + 2 < 19:
        if state[y_start][x_start] == state[y_start][x_start + 1] == state[y_start][x_start + 2]:
            black_cnt += 8
    if x_start - 2 > 0:
        if state[y_start][x_start] == state[y_start][x_start - 1] == state[y_start][x_start - 2]:
            black_cnt += 8
    if x_start + 1 < 19 and x_start - 1 > 0:
        if state[y_start][x_start] == state[y_start][x_start + 1] == state[y_start][x_start - 1]:
            black_cnt += 8
    if x_start + 3 < 19:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] == state[y_start][x_start + 3] == 1:
            black_cnt += 5
    if x_start + 2 < 19 and x_start - 1 > 0:
        if state[y_start][x_start - 1] == state[y_start][x_start + 1] == state[y_start][x_start + 2] == 1:
            black_cnt += 5
    if x_start + 1 < 19 and x_start - 2 > 0:
        if state[y_start][x_start - 2] == state[y_start][x_start - 1] == state[y_start][x_start + 1] == 1:
            black_cnt += 5
    if x_start - 3 > 0:
        if state[y_start][x_start - 1] == state[y_start][x_start - 2] == state[y_start][x_start - 3] == 1:
            black_cnt += 5
    if x_start + 4 < 19:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] \
                == state[y_start][x_start + 3] == state[y_start][x_start + 4] == 1:
            black_cnt += 10
    if x_start + 3 < 19 and x_start - 1 > 0:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] \
                == state[y_start][x_start + 3] == state[y_start][x_start - 1] == 1:
            black_cnt += 10
    if x_start + 2 < 19 and x_start - 2 > 0:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] \
                == state[y_start][x_start - 2] == state[y_start][x_start - 1] == 1:
            black_cnt += 10
    if x_start + 1 < 19 and x_start - 3 > 0:
        if state[y_start][x_start + 1] == state[y_start][x_start - 3] \
                == state[y_start][x_start - 2] == state[y_start][x_start - 1] == 1:
            black_cnt += 10
    if x_start - 4 > 0:
        if state[y_start][x_start - 1] == state[y_start][x_start - 2] \
                == state[y_start][x_start - 3] == state[y_start][x_start - 4] == 1:
            black_cnt += 10

    # 상하좌우대각선 -3, +3로 cost += 검정돌
    looking = state[y_min:y_max + 1, x_min:x_max + 1]
    score += len(np.where(looking == 1)[0]) * 3

    if y_min + 1 < 19:
        if state[y_min][x_min] == state[y_min + 1][x_min]:
            black_cnt = black_cnt + 5
    if y_min + 2 < 19:
        if state[y_min + 1][x_min] == state[y_min + 2][x_min]:
            black_cnt = black_cnt + 5
    if y_min + 3 < 19:
        if state[y_min + 2][x_min] == state[y_min + 3][x_min]:
            black_cnt = black_cnt + 5
    if y_min + 4 < 19:
        if state[y_min + 3][x_min] == state[y_min + 4][x_min]:
            black_cnt = black_cnt + 5
    if y_min + 5 < 19:
        if state[y_min + 4][x_min] == state[y_min + 5][x_min]:
            black_cnt = black_cnt + 5
    if y_min + 6 < 19:
        if state[y_min + 5][x_min] == state[y_min + 6][x_min]:
            black_cnt = black_cnt + 5
    if x_min + 1 < 19:
        if state[y_min][x_min] == state[y_min][x_min + 1]:
            black_cnt = black_cnt + 5
    if x_min + 2 < 19:
        if state[y_min][x_min + 1] == state[y_min][x_min + 2]:
            black_cnt = black_cnt + 5
    if x_min + 3 < 19:
        if state[y_min][x_min + 2] == state[y_min][x_min + 3]:
            black_cnt = black_cnt + 5
    if x_min + 4 < 19:
        if state[y_min][x_min + 3] == state[y_min][x_min + 4]:
            black_cnt = black_cnt + 5
    if x_min + 5 < 19:
        if state[y_min][x_min + 4] == state[y_min][x_min + 5]:
            black_cnt = black_cnt + 5
    if x_min + 6 < 19:
        if state[y_min][x_min + 5] == state[y_min][x_min + 6]:
            black_cnt = black_cnt + 5

    score += (black_cnt + white_cnt)
    return score, None


def evaluate(node):
    # o o o   o 이런식으로 놓인 패턴일 때 빈공간 좌표의 점수를 크게 줘야 함
    # o o o o   이런식으로 놓인 패턴(가로, 세로, 대각선 방향 모두 고려)일 때 빈공간 좌표의 점수를 크게 줘야 함
    x_pos, y_pos = node[1][0]
    # print("pos")
    # print(x_pos, y_pos)

    state = node[0]
    if state[y_pos][x_pos] == -1:
        x_pos, y_pos = node[1][1]

    cur_stone = state[y_pos][x_pos]

    x_min = x_pos - 5 if x_pos - 5 > 0 else 0
    x_max = x_pos + 5 if x_pos + 5 < 18 else 18

    y_min = y_pos - 5 if y_pos - 5 > 0 else 0
    y_max = y_pos + 5 if y_pos + 5 < 18 else 18

    score = 1
    for y in range(y_min + 1, y_max + 1):
        for x in range(x_min + 1, x_max + 1):
            if state[y][x] == cur_stone:
                if state[y - 1][x - 1] == state[y][x]:
                    score += 1
                if state[y][x - 1] == state[y][x]:
                    score += 1
                if state[y - 1][x] == state[y][x]:
                    score += 1

    print(score)
    return score, None


def get_next_stones(node):
    """
    최근에 놓인 돌들 중심으로 -1, +1인 것
    """

    state = node[0]
    next_stones = set()
    cur_stone = node[1]

    avail_stones = np.where(state == 0)
    avail_stones = set([(x, y) for x, y in zip(avail_stones[1], avail_stones[0])])

    # 최근에 둔 돌
    for i in range(len(node[1])):
        x_min = cur_stone[i][0] - 1 if cur_stone[i][0] - 1 > 0 else 0
        x_max = cur_stone[i][0] + 1 if cur_stone[i][0] + 1 < 18 else 18
        x_pos = np.arange(x_min, x_max + 1)

        y_min = cur_stone[i][1] - 1 if cur_stone[i][1] - 1 > 0 else 0
        y_max = cur_stone[i][1] + 1 if cur_stone[i][1] + 1 < 18 else 18
        y_pos = np.arange(y_min, y_max + 1)

        [next_stones.add((x, y)) for x in x_pos for y in y_pos]

    next_stones = next_stones & avail_stones

    # 아예 비어있다면 랜덤으로 하나 고르기
    if next_stones == 0:
        print("rand!")
        rand_x, rand_y = random_act(state)
        next_stones.add((rand_x, rand_y))

    return list(next_stones)
