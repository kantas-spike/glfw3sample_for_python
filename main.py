import atexit
import logging
import sys

import glfw
import OpenGL.GL as gl


def setup_logger(name):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s",
    )
    logger = logging.getLogger(name)
    return logger


logger = setup_logger("main.py")


def main():
    # GLFW を初期化する
    if not glfw.init():
        logger.error("Can't initialize GLFW")
        return 1

    # プログラム終了時の処理を登録する
    atexit.register(glfw.terminate)

    # OpenGL Version 3.2 Core Profileを選択
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    # ウィンドウを作成する
    window = glfw.create_window(640, 480, "Hello!", None, None)
    if not window:
        logger.error("Can't create GLFW window.")
        return 1

    # 作成したウィンドウを OpenGL の処理対象にする
    glfw.make_context_current(window)

    # pyOpenGLでは、glewは不要のようだ??

    # 作成したウィンドウに対する設定
    glfw.swap_interval(1)

    # 背景色を指定する
    gl.glClearColor(1.0, 1.0, 1.0, 0.0)

    # ウィンドウが開いている間繰り返す
    while glfw.window_should_close(window) == gl.GL_FALSE:
        # ウィンドウを消去する
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        #
        # ここで描画処理を行う
        #

        # カラーバッファを入れ替える
        glfw.swap_buffers(window)

        # イベントを取り出す
        glfw.wait_events()

    return 0


if __name__ == "__main__":
    sys.exit(main())
