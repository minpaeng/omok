import numpy as np
from omok import OmokState


def act(state: OmokState):
    # AI 1번 : 흰돌 랜덤 두기
    while True:

        y_pos, x_pos = np.random.randint(19), np.random.randint(19)

        # state에서 생성된 좌표에 돌이 올려져 있는지 여부 체크
        if state.is_valid_position(x_pos, y_pos):
            break

    return y_pos, x_pos
