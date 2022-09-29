import numpy as np
from omok import OmokState
import random
import copy

DEPTH = 3


def act(state: OmokState):
    if len(state.history) == 0:
        return 9, 9

    # 생성된 좌표에 돌을 놓을 수 있을 때까지 반복?
    while True:
        prev_stone = state.history[-1]  # 백돌
        node = (state.game_board, prev_stone, 0)
        # 노드 구성 :
        #           game_board, 이전 돌, cost

        _, pos = alpha_beta_search(node, DEPTH, float("-inf"), float("inf"), state.turn * -1)  # a-b prunning
        # v : value
        # pos : 돌 위치

        x_pos, y_pos = pos[0], pos[1]

        # state에서 생성된 좌표에 돌이 올려져 있는지 여부 체크
        if state.is_valid_position(x_pos, y_pos):
            break

    return y_pos, x_pos


def alpha_beta_search(node, depth, a, b, player):
    if depth == 0:  # 깊이가 0이면 탐색 종료
        return evaluate(node)

    if player == 1:  # 나(흑)의 입장
        stones = get_next_stones(node)
        state = node[0]
        v = float("-inf")

        pos = None
        for stone in stones:
            pos = stone
            child_state = np.copy(state)  # deep copy
            child_state[stone[0]][stone[1]] = 1  # 상대는 어떻게
            child_node = (child_state, stone, 0)
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
            child_state[stone[0]][stone[1]] = -1  # 백 이라면
            child_node = (child_state, stone, 0)

            v = min(v, alpha_beta_search(child_node, depth - 1, a, b, 1)[0])
            b = min(b, v)

            if b <= a:
                break

        return v, pos


def evaluate(node):
    # o o o   o 이런식으로 놓인 패턴일 때 빈공간 좌표의 점수를 크게 줘야 함
    # o o o o   이런식으로 놓인 패턴(가로, 세로, 대각선 방향 모두 고려)일 때 빈공간 좌표의 점수를 크게 줘야 함
    x_pos, y_pos = node[1]
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
    '''
    0이 아닌걸 고르고
    걔 주변 좌우 상하 대각 -1 ~ +1
    '''

    state = node[0]
    next_stones = set()
    cur_stone = node[1]  # 최근에 상대가 둔 바둑돌 위치

    x_min = cur_stone[0] - 1 if cur_stone[0] - 1 > 0 else 0
    x_max = cur_stone[0] + 1 if cur_stone[0] + 1 < 18 else 18
    x_pos = np.arange(x_min, x_max + 1)

    y_min = cur_stone[1] - 1 if cur_stone[1] - 1 > 0 else 0
    y_max = cur_stone[1] + 1 if cur_stone[1] + 1 < 18 else 18
    y_pos = np.arange(y_min, y_max + 1)

    avail_stones = np.where(state == 0)
    avail_stones = set([(x, y) for x, y in zip(avail_stones[0], avail_stones[1])])

    [next_stones.add((x, y)) for x in x_pos for y in y_pos]

    next_stones = next_stones & avail_stones

    return list(next_stones)

# def act(state: OmokState):
#     sum = 0
#     for i in range(100000000000):  # 강제 timeout
#         sum = i * i
#     # DO something
#
#     while True:
#         # print(state.history)
#
#         # 랜덤 두기
#         y_pos, x_pos = np.random.randint(19), np.random.randint(19)
#
#         # state에서 생성된 좌표에 돌이 올려져 있는지 여부 체크
#         if state.is_valid_position(x_pos, y_pos):
#             break
#
#     return y_pos, x_pos


# class AlphaBetaSearch:
#     def __init__(self):
#         self.minus_inf = -987654321
#         self.plus_inf = 987654321
#         self.x_pos = 0
#         self.y_pos = 0
#
#     def alpha_beta_search(self, state: OmokState):
#         v = self.max_value(state, self.minus_inf, self.plus_inf)
#         # state에서 취할 수 있는 action 집합 중 v를 포함하는 action 리턴하는 코드 작성
#
#         return self.y_pos, self.x_pos
#
#     def max_value(self, state: OmokState, a, b):
#         if state.check_status() == 1:
#             return self.utility(state)
#
#         # 1. state에 대해, 검은 돌을 둘 수 있는 모든 action들을 찾음
#         # 2. actions 중 하나의 action에 대해 min_value를 찾음 - 이 때 알파베타프루닝 적용
#         pass
#
#     def min_value(self, state: OmokState, a, b):
#         # 1. state에 대해, 흰 돌을 둘 수 있는 모든 action들을 찾음
#         # 2. actions 집합의 원소들을 하나하나 탐색하며 utility를 구함 - 가장 작은 값을 계속해서 기록
#         pass
#
#     def utility(self, state: OmokState):
#         # 1. 빈 공간을 모두 흑돌로 채운 후 모든 좌표를 살펴보며 가로, 세로, 대각선 방향으로 오목이 완성되는 수를 카운트
#
#         # 2. 빈 공간을 모두 백돌로 채운 후 모든 좌표를 살펴보며 가로, 세로, 대각선 방향으로 오목이 완성되는 수를 카운트
#
#         # (1. - 2.)를 리턴
#         pass
