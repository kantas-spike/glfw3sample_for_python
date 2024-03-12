import logging
import math

import numpy as np

logger = logging.getLogger(__name__)


# 単位行列を作成する
def identity():
    return np.identity(4)


# (x,y,z)だけ平行移動する変換行列を作成する
def translate(x, y, z):
    t = identity()
    t[0, 3] = x
    t[1, 3] = y
    t[2, 3] = z
    return t


# (x,y,z)倍に拡大縮小する変換行列を作成する
def scale(x, y, z):
    t = identity()
    t[0, 0] = x
    t[1, 1] = y
    t[2, 2] = z
    return t


# (x,y,z)を軸に a 回転する変換行列を作成する
def rotate(a, x, y, z):
    t = identity()
    d = math.sqrt(x * x + y * y + z * z)
    if d > 0.0:
        l = x / d
        m = y / d
        n = z / d
        l2 = l * l
        m2 = m * m
        n2 = n * n
        lm = l * m
        mn = m * n
        nl = n * l
        c = math.cos(a)
        c1 = 1.0 - c
        s = math.sin(a)

        t[0, 0] = (1.0 - l2) * c + l2
        t[1, 0] = lm * c1 + n * s
        t[2, 0] = nl * c1 - m * s
        t[0, 1] = lm * c1 - n * s
        t[1, 1] = (1 - m2) * c + m2
        t[2, 1] = mn * c1 + l * s
        t[0, 2] = nl * c1 + m * s
        t[1, 2] = mn * c1 - l * s
        t[2, 2] = (1.0 - n2) * c + n2

    return t


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)s %(funcName)s %(levelname)s\n %(message)s",
    )
    logging.info(identity())
    logging.info(translate(2, 3, 4))
    logging.info(scale(2, 3, 4))
    logging.info(rotate(math.pi, 2, 3, 4))
    logging.info(identity() @ translate(2, 3, 4))  # @ は内積の演算子
    logging.info(translate(2, 3, 4) @ scale(5, 6, 7))
    logging.info(translate(2, 3, 4) @ scale(5, 6, 7) @ rotate(math.pi, 2, 3, 4))
