import logging

import glfw
import OpenGL.GL as gl

logger = logging.getLogger(__name__)


class Window:
    def __init__(self, width, height, title="Hello!") -> None:
        # window作成
        self.window = self.setup_window(width, height, title)

        if not self.window:
            logger.error("Can't create GLFW window.")
            return

        # ウィンドウサイズ変更時のコールバック設定
        glfw.set_window_size_callback(self.window, Window.resize)

        # ウィンドウサイズの初期設定
        Window.resize(self.window, width, height)

    def __del__(self):
        if self.window:
            glfw.destroy_window(self.window)

    def setup_window(self, width, height, title):
        # windowを作成
        window = glfw.create_window(width, height, title, None, None)
        if not window:
            return None
        # 作成したウィンドウをOpenGLの処理対象にする
        glfw.make_context_current(window)

        # 垂直動機のタイミングを待つ
        glfw.swap_interval(1)

        return window

    # ウィンドウ作成成否
    def has_error(self):
        return not self.window

    # 描画ループ継続判定
    def should_close(self):
        # イベントを取り出す
        glfw.wait_events()
        # ウィンドウを閉じる必要がなければ true を返す
        return glfw.window_should_close(self.window)

    # ダブルバッファリング
    def swap_buffers(self):
        # カラーバッファを入れ替える
        glfw.swap_buffers(self.window)

    # ウィンドウのサイズ変更時の処理
    @staticmethod
    def resize(window, width, height):
        # フレームバッファの大きさを得る
        w, h = glfw.get_framebuffer_size(window)
        # フレームバッファ全体をビューポートにする
        gl.glViewport(0, 0, w, h)
