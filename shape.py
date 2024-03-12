import OpenGL.GL as gl
import numpy as np


# 図形の描画
class Shape:
    # オブジェクトのセットアップ
    #  data: 頂点属性を格納した配列
    def setup_vbo_and_vao(self, data: np.ndarray):
        # 頂点配列オブジェクト
        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        # 頂点バッファオブジェクト
        self.vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, data, gl.GL_STATIC_DRAW)

        # 結合されている頂点バッファオブジェクトを in 変数から参照できるようにする
        gl.glVertexAttribPointer(
            0, data.shape[1], gl.GL_FLOAT, gl.GL_FALSE, 0, gl.GLvoidp(0)
        )
        gl.glEnableVertexAttribArray(0)

    # 頂点配列オブジェクトの結合
    def bind_data(self):
        # 描画する頂点配列オブジェクトを指定する
        gl.glBindVertexArray(self.vao)

    # オブジェクトの削除
    def delete_vbo_and_vao(self):
        # 頂点配列オブジェクトを削除する
        gl.glDeleteVertexArrays(1, self.vao)
        # 頂点バッファオブジェクトを削除する
        gl.glDeleteBuffers(1, self.vbo)

    # コンストラクタ
    #  data: 頂点属性を格納した配列
    def __init__(self, data: np.ndarray) -> None:
        # 頂点情報を保持
        self.data = data

        # vboとvaoを準備
        self.setup_vbo_and_vao(data)

    # デストラクタ
    def __del__(self):
        self.delete_vbo_and_vao()

    # 描画
    def draw(self):
        # 頂点配列オブジェクトを結合する
        self.bind_data()

        # 描画を実行する
        self.execute()

    # 描画の実行
    def execute(self):
        # 折れ線で描画する
        gl.glDrawArrays(gl.GL_LINE_LOOP, 0, self.data.shape[0])
