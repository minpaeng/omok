import numpy as np
from omok import OmokState
from util import random_act

DEPTH = 5


def act(state: OmokState):
    if len(state.history) == 0:
        return 9, 9

    prev_stone = state.history[-2:]              # 흑돌, 백돌
    node = (state.game_board, prev_stone)        # 노드 구성 : game_board, 이전 돌, cost

    _, pos = alpha_beta_search(node, DEPTH, float("-inf"), float("inf"), -1)
    print(f"pos: {pos}")

    # v : value, pos : 돌 위치
    x_pos, y_pos = pos[0], pos[1]

    # state에서 생성된 좌표에 돌이 올려져 있는지 여부 체크
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
        return random_act(state)

    return y_pos, x_pos


def alpha_beta_search(node, depth, a, b, player):
    if depth == 0:  # 깊이가 0이면 탐색 종료
        return evaluate(node)

    prev_stone = [node[1][-1]]

    if player == 1:  # 나(흑)의 입장
        stones = get_next_stones(node)
        state = node[0]
        v = float("-inf")

        pos = None
        for stone in stones:
            pos = stone
            child_state = np.copy(state)
            child_state[stone[0]][stone[1]] = 1
            prev_stone.append(stone)
            child_node = (child_state, prev_stone)
            v = max(v, alpha_beta_search(child_node, depth - 1, a, b, -1)[0])
            a = max(a, v)
            if b <= a:
                break

        return v, pos

    elif player == -1:  # 상대(백)의 입장
        state = node[0]
        v = float("inf")
        stones = get_next_stones(node)
        pos = None
        for stone in stones:
            pos = stone
            child_state = np.copy(state)
            child_state[stone[0]][stone[1]] = -1
            prev_stone.append(stone)
            child_node = (child_state, prev_stone)

            v = min(v, alpha_beta_search(child_node, depth - 1, a, b, 1)[0])
            b = min(b, v)

            if b <= a:
                break

        return v, pos


def evaluate2(node):
    # o o o   o 이런식으로 놓인 패턴일 때 빈공간 좌표의 점수를 크게 줘야 함
    # o o o o   이런식으로 놓인 패턴(가로, 세로, 대각선 방향 모두 고려)일 때 빈공간 좌표의 점수를 크게 줘야 함
    state = node[0]
    score = 0
    #
    # for row in range(19):
    #     for col in range(19):
    #         if state[row][col] == 1:
    #             if row

    return score, None


def evaluate(node):
    # o o o   o 이런식으로 놓인 패턴일 때 빈공간 좌표의 점수를 크게 줘야 함
    # o o o o   이런식으로 놓인 패턴(가로, 세로, 대각선 방향 모두 고려)일 때 빈공간 좌표의 점수를 크게 줘야 함
    x_pos, y_pos = node[1][-1]
    # print("pos")
    # print(x_pos, y_pos)

    state = node[0]

    cur_stone = state[x_pos][y_pos]

    x_min = x_pos - 5 if x_pos - 5 > 0 else 0
    x_max = x_pos + 5 if x_pos + 5 < 18 else 18

    y_min = y_pos - 5 if y_pos - 5 > 0 else 0
    y_max = y_pos + 5 if y_pos + 5 < 18 else 18

    score = 1
    for x in range(x_min + 1, x_max + 1):
        for y in range(y_min + 1, y_max + 1):
            if state[x][y] == cur_stone:
                if state[x - 1][y - 1] == state[x][y]:
                    score += 1
                if state[x][y - 1] == state[x][y]:
                    score += 1
                if state[x - 1][y] == state[x][y]:
                    score += 1
    return score, None


def get_next_stones(node):
    """
    내가 최근에 둔 돌, 상대가 최근에 둔 돌 중심으로 -1, +1인 것 모두 고름
    """

    state = node[0]
    next_stones = set()
    cur_stone = node[1]

    avail_stones = np.where(state == 0)
    avail_stones = set([(x, y) for x, y in zip(avail_stones[1], avail_stones[0])])

    # 내가 최근에 둔 돌
    x_min = cur_stone[0][0] - 1 if cur_stone[0][0] - 1 > 0 else 0
    x_max = cur_stone[0][0] + 1 if cur_stone[0][0] + 1 < 18 else 18
    x_pos = np.arange(x_min, x_max + 1)

    y_min = cur_stone[0][1] - 1 if cur_stone[0][1] - 1 > 0 else 0
    y_max = cur_stone[0][1] + 1 if cur_stone[0][1] + 1 < 18 else 18
    y_pos = np.arange(y_min, y_max + 1)

    [next_stones.add((x, y)) for x in x_pos for y in y_pos]

    # 상대가 최근에 둔 돌
    x_min = cur_stone[1][0] - 1 if cur_stone[0][0] - 1 > 0 else 0
    x_max = cur_stone[1][0] + 1 if cur_stone[0][0] + 1 < 18 else 18
    x_pos = np.arange(x_min, x_max + 1)

    y_min = cur_stone[1][1] - 1 if cur_stone[1][1] - 1 > 0 else 0
    y_max = cur_stone[1][1] + 1 if cur_stone[1][1] + 1 < 18 else 18
    y_pos = np.arange(y_min, y_max + 1)

    [next_stones.add((x, y)) for x in x_pos for y in y_pos]

    next_stones = next_stones & avail_stones

    if next_stones == 0:
        print("rand!")
        rand_x, rand_y = random_act(state)
        next_stones.add((rand_x, rand_y))

    return list(next_stones)
