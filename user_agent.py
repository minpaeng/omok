import numpy as np
from omok import OmokState
from util import random_act

DEPTH = 3


def act(state: OmokState):
    if len(state.history) == 0:
        return 9, 9

    prev_stone = state.history[-7:]
    node = (state.game_board, prev_stone)        # 노드 구성 : game_board, 이전 돌

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
        # print("random selected.")

        # 상하좌우에도 놓여있다면 랜덤으로 놓기
        return random_act(state)

    return y_pos, x_pos


def alpha_beta_search(node, depth, a, b, player, start):
    if depth == 0:  # 깊이가 0이면 탐색 종료
        return evaluate(node, start)

    state = node[0]
    stones = get_next_stones(node)
    pos = stones[0]

    if player == 1:  # 나(흑)의 입장
        v = float("-inf")

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
                pos = stone
            a = max(a, v)
            if b <= a:
                break

        return v, pos

    elif player == -1:  # 상대(백)의 입장
        v = float("inf")
        pos = None
        for stone in stones:
            child_state = np.copy(state)
            child_state[stone[1]][stone[0]] = -1
            prev_stone = [node[1][-1], stone]
            child_node = (child_state, prev_stone)
            if depth == 3:
                start = stone
            child_value, child_pos = alpha_beta_search(child_node, depth - 1, a, b, 1, start)
            if v > child_value:
                v = child_value
                pos = stone
            b = min(b, v)

            if b <= a:
                break

        return v, pos


def evaluate(node, start):
    score = 0
    state = node[0]
    x_start, y_start = start

    # 공격 점수
    if x_start + 1 < 19:
        if state[y_start][x_start] == state[y_start][x_start + 1]:
            score += 10
            if x_start + 2 < 19 and state[y_start][x_start + 2] != -1:
                score += 100
    if x_start - 1 >= 0:
        if state[y_start][x_start] == state[y_start][x_start - 1]:
            score += 10
            if x_start - 2 >= 0 and state[y_start][x_start - 2] != -1:
                score += 10
    if x_start + 2 < 19:
        if state[y_start][x_start] == state[y_start][x_start + 1] == state[y_start][x_start + 2]:
            score += 100
            if x_start + 3 < 19 and state[y_start][x_start + 3] != -1:
                score += 100
            if y_start + 2 < 19 and state[y_start + 1][x_start] == state[y_start + 2][x_start]:
                score += 100
            if y_start - 2 < 19 and state[y_start - 1][x_start] == state[y_start - 2][x_start]:
                score += 100
    if x_start - 2 >= 0:
        if state[y_start][x_start] == state[y_start][x_start - 1] == state[y_start][x_start - 2]:
            score += 100
            if x_start - 3 >= 0 and state[y_start][x_start - 3] != -1:
                score += 100
            if y_start + 2 < 19 and state[y_start + 1][x_start] == state[y_start + 2][x_start]:
                score += 100
            if y_start - 2 < 19 and state[y_start - 1][x_start] == state[y_start - 2][x_start]:
                score += 100
    if x_start + 1 < 19 and x_start - 1 >= 0:
        if state[y_start][x_start] == state[y_start][x_start + 1] == state[y_start][x_start - 1]:
            score += 100
            if x_start + 2 < 19 and state[y_start][x_start + 2] != -1:
                score += 100
            if x_start - 2 >= 0 and state[y_start][x_start - 2] != -1:
                score += 100
    if x_start + 3 < 19:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] == state[y_start][x_start + 3] == 1:
            if x_start + 4 < 19 and state[y_start][x_start + 4] != -1:
                score += 300
    if x_start + 2 < 19 and x_start - 1 >= 0:
        if state[y_start][x_start - 1] == state[y_start][x_start + 1] == state[y_start][x_start + 2] == 1:
            if x_start + 3 < 19 and state[y_start][x_start + 3] != -1:
                score += 300
            if x_start - 2 >= 0 and state[y_start][x_start - 2] != -1:
                score += 300
    if x_start + 1 < 19 and x_start - 2 >= 0:
        if state[y_start][x_start - 2] == state[y_start][x_start - 1] == state[y_start][x_start + 1] == 1:
            if x_start + 2 < 19 and state[y_start][x_start + 2] != -1:
                score += 300
            if x_start - 3 >= 0 and state[y_start][x_start - 3] != -1:
                score += 300
    if x_start - 3 >= 0:
        if state[y_start][x_start - 1] == state[y_start][x_start - 2] == state[y_start][x_start - 3] == 1:
            if x_start - 4 >= 0 and state[y_start][x_start - 4] != -1:
                score += 300
    if x_start + 4 < 19:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] \
                == state[y_start][x_start + 3] == state[y_start][x_start + 4] == 1:
            score += 50000
    if x_start + 3 < 19 and x_start - 1 >= 0:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] \
                == state[y_start][x_start + 3] == state[y_start][x_start - 1] == 1:
            score += 50000
    if x_start + 2 < 19 and x_start - 2 >= 0:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] \
                == state[y_start][x_start - 2] == state[y_start][x_start - 1] == 1:
            score += 50000
    if x_start + 1 < 19 and x_start - 3 >= 0:
        if state[y_start][x_start + 1] == state[y_start][x_start - 3] \
                == state[y_start][x_start - 2] == state[y_start][x_start - 1] == 1:
            score += 50000
    if x_start - 4 >= 0:
        if state[y_start][x_start - 1] == state[y_start][x_start - 2] \
                == state[y_start][x_start - 3] == state[y_start][x_start - 4] == 1:
            score += 50000

    if y_start + 1 < 19:
        if state[y_start][x_start] == state[y_start + 1][x_start]:
            score += 10
    if y_start - 1 >= 0:
        if state[y_start][x_start] == state[y_start - 1][x_start]:
            score += 10
    if y_start + 2 < 19:
        if state[y_start][x_start] == state[y_start + 1][x_start] == state[y_start + 2][x_start]:
            score += 100
    if y_start - 2 >= 0:
        if state[y_start][x_start] == state[y_start - 1][x_start] == state[y_start - 2][x_start]:
            score += 100
    if y_start + 1 < 19 and y_start - 1 >= 0:
        if state[y_start][x_start] == state[y_start + 1][x_start] == state[y_start - 1][x_start]:
            score += 100
    if y_start + 3 < 19:
        if state[y_start + 1][x_start] == state[y_start + 2][x_start] == state[y_start + 3][x_start] == 1:
            if y_start + 4 < 19 and state[y_start + 4][x_start] != -1:
                score += 300
    if y_start + 2 < 19 and y_start - 1 >= 0:
        if state[y_start - 1][x_start] == state[y_start + 1][x_start] == state[y_start + 2][x_start] == 1:
            if y_start + 3 < 19 and state[y_start + 3][x_start] != -1:
                score += 300
            if y_start - 2 >= 0 and state[y_start - 2][x_start] != -1:
                score += 300
    if y_start + 1 < 19 and y_start - 2 >= 0:
        if state[y_start - 2][x_start] == state[y_start - 1][x_start] == state[y_start + 1][x_start] == 1:
            if y_start + 2 < 19 and state[y_start + 2][x_start] != -1:
                score += 300
            if y_start - 3 >= 0 and state[y_start - 3][x_start] != -1:
                score += 300
    if y_start - 3 >= 0:
        if state[y_start - 1][x_start] == state[y_start - 2][x_start] == state[y_start - 3][x_start] == 1:
            if y_start - 4 >= 0 and state[y_start - 4][x_start] != -1:
                score += 300
    if y_start + 4 < 19:
        if state[y_start + 1][x_start] == state[y_start + 2][x_start] \
                == state[y_start + 3][x_start] == state[y_start + 4][x_start] == 1:
            score += 50000
    if y_start + 3 < 19 and y_start - 1 > 0:
        if state[y_start + 1][x_start] == state[y_start + 2][x_start] \
                == state[y_start + 3][x_start] == state[y_start - 1][x_start] == 1:
            score += 50000
    if y_start + 2 < 19 and y_start - 2 > 0:
        if state[y_start + 1][x_start] == state[y_start + 2][x_start] \
                == state[y_start - 1][x_start] == state[y_start - 2][x_start] == 1:
            score += 50000
    if y_start + 1 < 19 and y_start - 3 > 0:
        if state[y_start + 1][x_start] == state[y_start - 3][x_start] \
                == state[y_start - 2][x_start] == state[y_start - 1][x_start] == 1:
            score += 50000
    if y_start - 4 >= 0:
        if state[y_start - 1][x_start] == state[y_start - 2][x_start] \
                == state[y_start - 3][x_start] == state[y_start - 4][x_start] == 1:
            score += 50000

    if x_start + 1 < 19 and y_start + 1 < 19:
        if state[y_start + 1][x_start + 1] == 1:
            score += 10
    if x_start - 1 >= 0 and y_start + 1 < 19:
        if state[y_start + 1][x_start - 1] == 1:
            score += 10
    if x_start - 1 >= 0 and y_start - 1 >= 0:
        if state[y_start - 1][x_start - 1] == 1:
            score += 10
    if x_start + 1 < 19 and y_start - 1 >= 0:
        if state[y_start - 1][x_start + 1] == 1:
            score += 10
    if x_start + 2 < 19 and y_start + 2 < 19:
        if state[y_start + 1][x_start + 1] == state[y_start + 2][x_start + 2] == 1:
            score += 100
    if x_start - 2 >= 0 and y_start + 2 < 19:
        if state[y_start + 1][x_start - 1] == state[y_start + 2][x_start - 2] == 1:
            score += 100
    if x_start - 2 >= 0 and y_start - 2 >= 0:
        if state[y_start - 1][x_start - 1] == state[y_start - 2][x_start - 2] == 1:
            score += 100
    if x_start + 2 < 19 and y_start - 2 >= 0:
        if state[y_start - 1][x_start + 1] == state[y_start - 2][x_start + 2] == 1:
            score += 100
    if x_start + 1 < 19 and y_start + 1 < 19 and x_start - 1 >= 0 and y_start - 1 >= 0:
        if state[y_start + 1][x_start + 1] == state[y_start - 1][x_start - 1] == 1:
            score += 100
    if (x_start - 1 >= 0 and y_start + 1 < 19) and (x_start + 1 < 19 and y_start - 1 >= 0):
        if state[y_start + 1][x_start - 1] == state[y_start - 1][x_start + 1] == 1:
            score += 100
    if x_start + 3 < 19 and y_start + 3 < 19:
        if state[y_start + 1][x_start + 1] == state[y_start + 2][x_start + 2] == state[y_start + 3][x_start + 3] == 1:
            score += 300
    if x_start - 3 >= 0 and y_start + 3 < 19:
        if state[y_start + 1][x_start - 1] == state[y_start + 2][x_start - 2] == state[y_start + 3][x_start - 3] == 1:
            score += 300
    if x_start - 3 >= 0 and y_start - 3 >= 0:
        if state[y_start - 1][x_start - 1] == state[y_start - 2][x_start - 2] == state[y_start - 3][x_start - 3] == 1:
            score += 300
    if x_start + 3 < 19 and y_start - 3 >= 0:
        if state[y_start - 1][x_start + 1] == state[y_start - 2][x_start + 2] == state[y_start - 3][x_start + 3] == 1:
            score += 300
    if x_start + 4 < 19 and y_start - 4 >= 0:
        if state[y_start - 1][x_start + 1] == state[y_start - 2][x_start + 2] == \
                state[y_start - 3][x_start + 3] == state[y_start - 4][x_start + 4] == 1:
            score += 50000
    if x_start + 4 < 19 and y_start + 4 < 19:
        if state[y_start + 1][x_start + 1] == state[y_start + 2][x_start + 2] == \
                state[y_start + 3][x_start + 3] == state[y_start + 4][x_start + 4] == 1:
            score += 50000
    if x_start - 4 >= 0 and y_start + 4 < 19:
        if state[y_start + 1][x_start - 1] == state[y_start + 2][x_start - 2] == \
                state[y_start + 3][x_start - 3] == state[y_start + 4][x_start - 4] == 1:
            score += 50000
    if x_start - 4 >= 0 and y_start - 4 >= 0:
        if state[y_start - 1][x_start - 1] == state[y_start - 2][x_start - 2] == \
                state[y_start - 3][x_start - 3] == state[y_start - 4][x_start - 4] == 1:
            score += 50000
    if x_start - 3 >= 0 and y_start - 3 >= 0 and x_start + 1 < 19 and y_start + 1 < 19:
        if state[y_start - 1][x_start - 1] == state[y_start - 2][x_start - 2] == \
                state[y_start - 3][x_start - 3] == state[y_start + 1][x_start + 1] == 1:
            score += 50000
    if x_start - 2 >= 0 and y_start - 2 >= 0 and x_start + 2 < 19 and y_start + 2 < 19:
        if state[y_start - 2][x_start - 2] == state[y_start - 1][x_start - 1] == \
                state[y_start + 1][x_start + 1] == state[y_start + 2][x_start + 2] == 1:
            score += 50000
    if x_start + 2 < 19 and y_start - 2 >= 0 and x_start - 2 >= 0 and y_start + 2 < 19:
        if state[y_start + 2][x_start - 2] == state[y_start + 1][x_start - 1] == \
                state[y_start - 1][x_start + 1] == state[y_start - 2][x_start + 2] == 1:
            score += 50000

    # 흰 돌 견제 점수 - 검정보다 우선순위를 높게 둬야 함
    if x_start + 3 < 19:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] == state[y_start][x_start + 3] == -1:
            if x_start + 4 < 19 and state[y_start][x_start + 4] != 1:
                score += 3000
    if x_start + 2 < 19 and x_start - 1 > 0:
        if state[y_start][x_start - 1] == state[y_start][x_start + 1] == state[y_start][x_start + 2] == -1:
            if x_start + 3 < 19 and state[y_start][x_start + 3] != 1:
                score += 3000
            if x_start - 2 >= 0 and state[y_start][x_start - 2] != 1:
                score += 3000
    if x_start + 1 < 19 and x_start - 2 > 0:
        if state[y_start][x_start - 2] == state[y_start][x_start - 1] == state[y_start][x_start + 1] == -1:
            if x_start + 2 < 19 and state[y_start][x_start + 2] != 1:
                score += 3000
            if x_start - 3 >= 0 and state[y_start][x_start - 3] != 1:
                score += 3000
    if x_start - 3 >= 0:
        if state[y_start][x_start - 1] == state[y_start][x_start - 2] == state[y_start][x_start - 3] == -1:
            if x_start - 4 >= 0 and state[y_start][x_start - 4] != 1:
                score += 3000
    if x_start + 4 < 19:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] \
                == state[y_start][x_start + 3] == state[y_start][x_start + 4] == -1:
            score += 10000
    if x_start + 3 < 19 and x_start - 1 > 0:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] \
                == state[y_start][x_start + 3] == state[y_start][x_start - 1] == -1:
            score += 10000
    if x_start + 2 < 19 and x_start - 2 > 0:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] \
                == state[y_start][x_start - 2] == state[y_start][x_start - 1] == -1:
            score += 10000
    if x_start + 1 < 19 and x_start - 3 > 0:
        if state[y_start][x_start + 1] == state[y_start][x_start - 3] \
                == state[y_start][x_start - 2] == state[y_start][x_start - 1] == -1:
            score += 10000
    if x_start - 4 >= 0:
        if state[y_start][x_start - 1] == state[y_start][x_start - 2] \
                == state[y_start][x_start - 3] == state[y_start][x_start - 4] == -1:
            score += 10000

    if y_start + 3 < 19:
        if state[y_start + 1][x_start] == state[y_start + 2][x_start] == state[y_start + 3][x_start] == -1:
            if y_start + 4 < 19 and state[y_start + 4][x_start] != 1:
                score += 3000
    if y_start + 2 < 19 and y_start - 1 > 0:
        if state[y_start - 1][x_start] == state[y_start + 1][x_start] == state[y_start + 2][x_start] == -1:
            if y_start + 3 < 19 and state[y_start + 3][x_start] != 1:
                score += 3000
            if y_start - 2 >= 0 and state[y_start - 2][x_start] != 1:
                score += 3000
    if y_start + 1 < 19 and y_start - 2 > 0:
        if state[y_start - 2][x_start] == state[y_start - 1][x_start] == state[y_start + 1][x_start] == -1:
            if y_start + 2 < 19 and state[y_start + 2][x_start] != 1:
                score += 3000
            if y_start - 3 >= 0 and state[y_start - 3][x_start] != 1:
                score += 3000
    if y_start - 3 >= 0:
        if state[y_start - 1][x_start] == state[y_start - 2][x_start] == state[y_start - 3][x_start] == -1:
            if y_start - 4 < 19 and state[y_start - 4][x_start] != 1:
                score += 3000
    if y_start + 4 < 19:
        if state[y_start + 1][x_start] == state[y_start + 2][x_start] \
                == state[y_start + 3][x_start] == state[y_start + 4][x_start] == -1:
            score += 10000
    if y_start + 3 < 19 and y_start - 1 > 0:
        if state[y_start + 1][x_start] == state[y_start + 2][x_start] \
                == state[y_start + 3][x_start] == state[y_start - 1][x_start] == -1:
            score += 10000
    if y_start + 2 < 19 and y_start - 2 > 0:
        if state[y_start + 1][x_start] == state[y_start + 2][x_start] \
                == state[y_start - 1][x_start] == state[y_start - 2][x_start] == -1:
            score += 10000
    if y_start + 1 < 19 and y_start - 3 > 0:
        if state[y_start + 1][x_start] == state[y_start - 3][x_start] \
                == state[y_start - 2][x_start] == state[y_start - 1][x_start] == -1:
            score += 10000
    if y_start - 4 >= 0:
        if state[y_start - 1][x_start] == state[y_start - 2][x_start] \
                == state[y_start - 3][x_start] == state[y_start - 4][x_start] == -1:
            score += 10000

    # 무조건 이기는 경우? 방어
    if y_start + 3 < 19 and x_start + 2 < 19:
        if state[y_start + 1][x_start] == state[y_start + 2][x_start] == state[y_start][x_start + 1] == -1\
                and state[y_start + 3][x_start] == state[y_start][x_start + 2] != 1:
            score += 1000
    if y_start - 3 >= 0 and x_start + 2 < 19:
        if state[y_start - 1][x_start] == state[y_start - 2][x_start] == state[y_start][x_start + 1] == -1 \
                and state[y_start - 3][x_start] == state[y_start][x_start + 2] != 1:
            score += 1000
    if y_start + 3 < 19 and x_start - 2 >= 0:
        if state[y_start + 1][x_start] == state[y_start + 2][x_start] == state[y_start][x_start - 1] == -1\
                and state[y_start + 3][x_start] == state[y_start][x_start - 2] != 1:
            score += 1000
    if y_start - 3 >= 0 and x_start - 2 >= 0:
        if state[y_start - 1][x_start] == state[y_start - 2][x_start] == state[y_start][x_start - 1] == -1\
                and state[y_start - 3][x_start] == state[y_start][x_start - 2] != 1:
            score += 1000
    if y_start + 2 < 19 and x_start + 3 < 19:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] == state[y_start + 1][x_start] == -1 \
                and state[y_start + 2][x_start] == state[y_start][x_start + 3] == -1:
            score += 1000
    if y_start + 2 < 19 and x_start - 3 >= 0:
        if state[y_start][x_start - 1] == state[y_start][x_start - 2] == state[y_start + 1][x_start] == -1\
                and state[y_start + 2][x_start] == state[y_start][x_start - 3] != 1:
            score += 1000
    if y_start - 2 >= 0 and x_start + 3 < 19:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] == state[y_start - 1][x_start] == -1\
                and state[y_start - 2][x_start] == state[y_start][x_start + 3] == -1:
            score += 1000
    if y_start - 2 >= 0 and x_start - 3 >= 0:
        if state[y_start][x_start - 1] == state[y_start][x_start - 2] == state[y_start - 1][x_start] == -1\
                and state[y_start - 2][x_start] == state[y_start][x_start - 3] != 1:
            score += 1000

    if y_start + 2 < 19 and x_start + 2 < 19:
        if state[y_start + 1][x_start] == state[y_start + 2][x_start] == \
                state[y_start + 1][x_start + 1] == state[y_start + 2][x_start + 2] == -1:
            if y_start + 3 < 19 and state[y_start + 3][x_start] != 1:
                score += 5000
    if y_start + 2 < 19 and x_start - 2 >= 0:
        if state[y_start + 1][x_start] == state[y_start + 2][x_start] == \
                state[y_start + 1][x_start - 1] == state[y_start + 2][x_start - 2] == -1:
            if y_start + 3 < 19 and state[y_start + 3][x_start] != 1:
                score += 5000
    if y_start - 2 >= 0 and x_start + 2 < 19:
        if state[y_start - 1][x_start] == state[y_start - 2][x_start] == \
                state[y_start - 1][x_start + 1] == state[y_start - 2][x_start + 2] == -1:
            if y_start - 3 >= 0 and state[y_start - 3][x_start] != 1:
                score += 5000
    if y_start - 2 >= 0 and x_start - 2 >= 0:
        if state[y_start - 1][x_start] == state[y_start - 2][x_start] == \
                state[y_start - 1][x_start - 1] == state[y_start - 2][x_start - 2] == -1:
            if y_start - 3 >= 0 and state[y_start - 3][x_start] != 1:
                score += 5000
    if y_start + 2 < 19 and x_start + 2 < 19:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] == \
                state[y_start + 1][x_start + 1] == state[y_start + 2][x_start + 2] == -1:
            if x_start + 3 < 19 and state[y_start][x_start + 3] != 1:
                score += 5000
    if y_start + 2 < 19 and x_start - 2 >= 0:
        if state[y_start][x_start - 1] == state[y_start][x_start - 2] == \
                state[y_start + 1][x_start - 1] == state[y_start + 2][x_start - 2] == -1:
            if x_start - 3 >= 0 and state[y_start][x_start - 3] != 1:
                score += 5000
    if y_start - 2 >= 0 and x_start + 2 < 19:
        if state[y_start][x_start + 1] == state[y_start][x_start + 2] == \
                state[y_start - 1][x_start + 1] == state[y_start - 2][x_start + 2] == -1:
            if x_start + 3 < 19 and state[y_start][x_start + 3] != 1:
                score += 5000
    if y_start - 2 >= 0 and x_start - 2 >= 0:
        if state[y_start][x_start - 1] == state[y_start][x_start - 2] == \
                state[y_start - 1][x_start - 1] == state[y_start - 2][x_start - 2] == -1:
            if x_start - 3 >= 0 and state[y_start][x_start - 3] != 1:
                score += 5000

    # 대각선 방어
    if x_start + 4 < 19 and y_start + 4 < 19:
        if state[y_start + 1][x_start + 1] == state[y_start + 2][x_start + 2] == state[y_start + 3][x_start + 3] == -1\
                and state[y_start + 4][x_start + 4] != 1:
            score += 3000
    if x_start - 4 >= 0 and y_start - 4 >= 0:
        if state[y_start - 1][x_start - 1] == state[y_start - 2][x_start - 2] == state[y_start - 3][x_start - 3] == -1\
                and state[y_start - 4][x_start - 4] != 1:
            score += 3000
    if x_start + 3 < 19 and y_start + 3 < 19 and x_start - 1 >= 0 and y_start - 1 >= 0:
        if state[y_start - 1][x_start - 1] == state[y_start + 1][x_start + 1] == state[y_start + 2][x_start + 2] == -1\
                and state[y_start + 3][x_start + 3] != 1:
            score += 3000
    if x_start + 2 < 19 and y_start + 2 < 19 and x_start - 2 >= 0 and y_start - 2 >= 0:
        if state[y_start - 1][x_start - 1] == state[y_start + 1][x_start + 1] == state[y_start + 2][x_start + 2] == -1\
                and state[y_start - 2][x_start - 2] != 1:
            score += 3000
    if x_start + 2 < 19 and y_start + 2 < 19 and x_start - 2 >= 0 and y_start - 2 >= 0:
        if state[y_start - 2][x_start - 2] == state[y_start - 1][x_start - 1] == state[y_start + 1][x_start + 1] == -1\
                and state[y_start + 2][x_start + 2] != 1:
            score += 3000
    if x_start + 1 < 19 and y_start + 1 < 19 and x_start - 3 >= 0 and y_start - 3 >= 0:
        if state[y_start - 2][x_start - 2] == state[y_start - 1][x_start - 1] == state[y_start + 1][x_start + 1] == -1\
                and state[y_start - 3][x_start - 3] != 1:
            score += 3000
    if x_start - 3 >= 0 and y_start + 3 < 19 and x_start + 1 < 19 and y_start - 1 >= 0:
        if state[y_start - 1][x_start + 1] == state[y_start + 1][x_start - 1] == state[y_start + 2][x_start - 2] == -1\
                and state[y_start + 3][x_start - 3] != 1:
            score += 3000
    if x_start - 2 >= 0 and y_start + 2 < 19 and x_start + 2 < 19 and y_start - 2 >= 0:
        if state[y_start + 1][x_start - 1] == state[y_start - 1][x_start + 1] == state[y_start - 2][x_start + 2] == -1\
                and state[y_start + 2][x_start - 2] != 1:
            score += 3000
        if state[y_start - 1][x_start + 1] == state[y_start + 1][x_start - 1] == state[y_start + 2][x_start - 2] == -1\
                and state[y_start - 2][x_start + 2] != 1:
            score += 3000
    if x_start - 1 >= 0 and y_start + 1 < 19 and x_start + 3 < 19 and y_start - 3 >= 0:
        if state[y_start - 2][x_start + 2] == state[y_start - 1][x_start + 1] == state[y_start + 1][x_start - 1] == -1\
                and state[y_start - 3][x_start + 3] != 1:
            score += 3000

    if x_start + 4 < 19 and y_start + 4 < 19:
        if state[y_start + 1][x_start + 1] == state[y_start + 2][x_start + 2] == \
                state[y_start + 3][x_start + 3] == state[y_start + 4][x_start + 4] == -1:
            score += 5000
    if x_start - 4 >= 0 and y_start - 4 >= 0:
        if state[y_start - 1][x_start - 1] == state[y_start - 2][x_start - 2] == \
                state[y_start - 3][x_start - 3] == state[y_start - 4][x_start - 4] == -1:
            score += 5000
    if x_start - 4 >= 0 and y_start + 4 < 19:
        if state[y_start + 1][x_start - 1] == state[y_start + 2][x_start - 2] == \
                state[y_start + 3][x_start - 3] == state[y_start + 4][x_start - 4] == -1:
            score += 5000
    if x_start + 4 < 19 and y_start - 4 >= 0:
        if state[y_start - 1][x_start + 1] == state[y_start - 2][x_start + 2] == \
                state[y_start - 3][x_start + 3] == state[y_start - 4][x_start + 4] == -1:
            score += 5000
    if x_start + 2 < 19 and y_start + 2 < 19 and x_start - 2 >= 0 and y_start - 2 >= 0:
        if state[y_start - 2][x_start - 2] == state[y_start - 1][x_start - 1] == \
                state[y_start + 1][x_start + 1] == state[y_start + 2][x_start + 2] == -1:
            if x_start + 3 < 19 and y_start + 3 < 19 and state[y_start + 3][x_start + 3] != 1:
                score += 5000
            if x_start - 3 >= 0 and y_start - 3 >= 0 and state[y_start - 3][x_start - 3] != 1:
                score += 5000
    if x_start - 2 >= 0 and y_start + 2 < 19 and x_start + 2 < 19 and y_start - 2 >= 0:
        if state[y_start + 2][x_start - 2] == state[y_start + 1][x_start - 1] == \
                state[y_start - 1][x_start + 1] == state[y_start - 2][x_start + 2] == -1:
            if x_start - 3 >= 0 and y_start + 3 < 19 and state[y_start + 3][x_start - 3] != 1:
                score += 5000
            if x_start + 3 < 19 and y_start - 3 >= 0 and state[y_start - 3][x_start + 3] != 1:
                score += 5000
    if x_start - 4 >= 0 and y_start + 4 < 19:
        if state[y_start + 1][x_start - 1] == state[y_start + 2][x_start - 2] == state[y_start + 3][x_start - 3] == -1\
                and state[y_start + 4][x_start - 4] != 1:
            score += 3000
    if x_start - 4 >= 0 and y_start - 4 >= 0:
        if state[y_start - 1][x_start - 1] == state[y_start - 2][x_start - 2] == state[y_start - 3][x_start - 3] == -1\
                and state[y_start - 4][x_start - 4] != 1:
            score += 3000
    if x_start + 4 < 19 and y_start - 4 >= 0:
        if state[y_start - 1][x_start + 1] == state[y_start - 2][x_start + 2] == state[y_start - 3][x_start + 3] == -1\
                and state[y_start - 4][x_start + 4] != 1:
            score += 3000
    if x_start + 4 < 19 and y_start - 4 >= 0 and x_start - 1 >= 0 and y_start + 1 < 19:
        if state[y_start + 1][x_start - 1] == state[y_start - 1][x_start + 1] \
                == state[y_start - 2][x_start + 2] == state[y_start - 3][x_start + 3] == -1\
                and state[y_start - 4][x_start + 4] != 1:
            score += 3000
    if x_start - 4 >= 0 and y_start + 4 < 19:
        if state[y_start + 1][x_start - 1] == state[y_start + 2][x_start - 2] == state[y_start + 3][x_start - 3] == -1\
                and state[y_start + 4][x_start - 4] != 1:
            score += 3000
    if x_start - 4 >= 0 and y_start + 4 < 19 and x_start + 1 < 19 and y_start - 1 >= 0:
        if state[y_start - 1][x_start + 1] == state[y_start + 1][x_start - 1] \
                == state[y_start + 2][x_start - 2] == state[y_start + 3][x_start - 3] == -1\
                and state[y_start + 4][x_start - 4] != 1:
            score += 3000

    return score, None


def get_next_stones(node):
    # 최근에 놓인 돌들을 중심으로 -2, +2인 위치 선택(3으로하면 timeout되는 경우가 종종 있음..)
    state = node[0]
    next_stones = set()
    cur_stone = node[1]

    avail_stones = np.where(state == 0)
    avail_stones = set([(x, y) for x, y in zip(avail_stones[1], avail_stones[0])])

    # 최근에 둔 돌
    for i in range(len(node[1])):
        x_min = cur_stone[i][0] - 2 if cur_stone[i][0] - 2 > 0 else 0
        x_max = cur_stone[i][0] + 2 if cur_stone[i][0] + 2 < 18 else 18
        x_pos = np.arange(x_min, x_max + 1)

        y_min = cur_stone[i][1] - 2 if cur_stone[i][1] - 2 > 0 else 0
        y_max = cur_stone[i][1] + 2 if cur_stone[i][1] + 2 < 18 else 18
        y_pos = np.arange(y_min, y_max + 1)

        [next_stones.add((x, y)) for x in x_pos for y in y_pos]

    next_stones = next_stones & avail_stones

    # 아예 비어있다면 랜덤으로 하나 고르기
    if next_stones == 0:
        # print("random selected.")
        rand_x, rand_y = random_act(state)
        next_stones.add((rand_x, rand_y))

    return list(next_stones)
