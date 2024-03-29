import logging

import glfw
import OpenGL.GL as gl

logger = logging.getLogger(__name__)


class Window:
    def __init__(self, width, height, title="Hello!") -> None:
        # window作成
        self.window = self.setup_window(width, height, title)
        # ウィンドウのサイズ
        self.size = [width, height]
        # ワールド座標系に対するデバイス座標系の拡大率
        self.scale = 100.0
        # 図形の正規化デバイス座標系上での位置
        self.location = [0, 0]
        # キーボードの状態
        self.key_status = glfw.RELEASE

        if not self.window:
            logger.error("Can't create GLFW window.")
            return

        # ウィンドウサイズ変更時のコールバック設定
        glfw.set_window_size_callback(self.window, Window.resize)
        # マウスホイール操作時に呼び出す処理の登録
        glfw.set_scroll_callback(self.window, Window.wheel)
        # キーボード操作時に呼び出す処理の登録
        glfw.set_key_callback(self.window, Window.keyboard)

        # このインスタンスの this ポインタを記録しておく
        # (glfwのwindowと、本クラスのインスタンス(self)を関連付ける)
        glfw.set_window_user_pointer(self.window, self)

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
        if self.key_status == glfw.RELEASE:
            glfw.wait_events()
        else:
            glfw.poll_events()

        # キーボードの状態を調べる
        if glfw.get_key(self.window, glfw.KEY_LEFT) != glfw.RELEASE:
            self.location[0] -= 2.0 / self.size[0]
        elif glfw.get_key(self.window, glfw.KEY_RIGHT) != glfw.RELEASE:
            self.location[0] += 2.0 / self.size[0]
        if glfw.get_key(self.window, glfw.KEY_DOWN) != glfw.RELEASE:
            self.location[1] -= 2.0 / self.size[1]
        elif glfw.get_key(self.window, glfw.KEY_UP) != glfw.RELEASE:
            self.location[1] += 2.0 / self.size[1]

        # マウスの左ボタンの状態を調べる
        if glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_1) != glfw.RELEASE:
            # マウスカーソルの位置を取得する
            x, y = glfw.get_cursor_pos(self.window)
            # マウスカーソルの正規化デバイス座標系上での位置を求める
            self.location[0] = x * 2.0 / self.size[0] - 1.0
            self.location[1] = 1.0 - y * 2.0 / self.size[1]
            # logger.info(f"cursor: {x, y} => loc: {self.location}")

        # ウィンドウを閉じる必要がなければ true を返す
        return glfw.window_should_close(self.window) or glfw.get_key(
            self.window, glfw.KEY_ESCAPE
        )

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

        # glfwのwindowに関連付いたインスタンスを取得する
        context: Window = glfw.get_window_user_pointer(window)
        if context:
            context.size[0] = width
            context.size[1] = height

    # マウスホイール操作時の処理
    @staticmethod
    def wheel(window, x, y):
        # glfwのwindowに関連付いたインスタンスを取得する
        context: Window = glfw.get_window_user_pointer(window)
        if context:
            context.scale += y

    # キーボード操作時の処理
    @staticmethod
    def keyboard(window, key, scancode, action, mods):
        # glfwのwindowに関連付いたインスタンスを取得する
        context: Window = glfw.get_window_user_pointer(window)
        if context:
            context.key_status = action
