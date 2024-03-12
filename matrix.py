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


def look_at(ex, ey, ez, gx, gy, gz, ux, uy, uz):
    # 平行移動の変換行列
    tv = translate(-ex, -ey, -ez)

    # t 軸 = e - g
    tx = ex - gx
    ty = ey - gy
    tz = ez - gz

    # r 軸 = u x t 軸
    rx = uy * tz - uz * ty
    ry = uz * tx - ux * tz
    rz = ux * ty - uy * tx

    # s 軸 = t 軸 x r 軸
    sx = ty * rz - tz * ry
    sy = tz * rx - tx * rz
    sz = tx * ry - ty * rx

    # s 軸の長さのチェック
    s2 = sx * sx + sy * sy + sz * sz
    if s2 == 0.0:
        return tv

    # 回転の変換行列
    rv = identity()

    # r 軸を正規化して配列変数に格納
    r = math.sqrt(rx * rx + ry * ry + rz * rz)
    rv[0, 0] = rx / r
    rv[0, 1] = ry / r
    rv[0, 2] = rz / r
    # s 軸を正規化して配列変数に格納
    s = math.sqrt(s2)
    rv[1, 0] = sx / s
    rv[1, 1] = sy / s
    rv[1, 2] = sz / s
    # t 軸を正規化して配列変数に格納
    t = math.sqrt(tx * tx + ty * ty + tz * tz)
    rv[2, 0] = tx / t
    rv[2, 1] = ty / t
    rv[2, 2] = tz / t

    # 視点の平行移動の変換行列に視線の回転の変換行列を乗じる
    return rv @ tv


# 直交投影変換行列を作成する
def orthogonal(left, right, bottom, top, z_near, z_far):
    dx = right - left
    dy = top - bottom
    dz = z_far - z_near
    if dx != 0.0 and dy != 0.0 and dz != 0.0:
        t = identity()
        t[0, 0] = 2.0 / dx
        t[1, 1] = 2.0 / dy
        t[2, 2] = -2.0 / dz
        t[0, 3] = -(right + left) / dx
        t[1, 3] = -(top + bottom) / dy
        t[2, 3] = -(z_far + z_near) / dz
        return t
    else:
        return np.zeros((4, 4))


# 透視投影変換行列を作成する
def frustum(left, right, bottom, top, z_near, z_far):
    dx = right - left
    dy = top - bottom
    dz = z_far - z_near
    t = np.zeros((4, 4))
    if dx != 0.0 and dy != 0.0 and dz != 0.0:
        t = identity()
        t[0, 0] = 2.0 * z_near / dx
        t[0, 2] = (right + left) / dx
        t[1, 1] = 2.0 * z_near / dy
        t[1, 2] = (top + bottom) / dy
        t[2, 2] = -(z_far + z_near) / dz
        t[2, 3] = -2.0 * z_far * z_near / dz
        t[3, 2] = -1.0

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
    logging.info(np.zeros((4, 4)))
    logging.info(orthogonal(-3.2, 3.2, -2.4, 2.4, 1.0, 10.0))
