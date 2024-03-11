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


# プログラムオブジェクトを作成する
#   vsrc: バーテックスシェーダのソースプログラムの文字列
#   fsrc: フラグメントシェーダのソースプログラムの文字列
def create_program(vsrc, fsrc):
    # 空のプログラムオブジェクトを作成する
    program = gl.glCreateProgram()

    if vsrc:
        # バーテックスシェーダのシェーダオブジェクトを作成する
        vobj = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(vobj, vsrc)
        gl.glCompileShader(vobj)

        # バーテックスシェーダのシェーダオブジェクトをプログラムオブジェクトに組み込む
        gl.glAttachShader(program, vobj)
        gl.glDeleteShader(vobj)

    if fsrc:
        # フラグメントシェーダのシェーダオブジェクトを作成する
        fobj = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(fobj, fsrc)
        gl.glCompileShader(fobj)

        # フラグメントシェーダのシェーダオブジェクトをプログラムオブジェクトに組み込む
        gl.glAttachShader(program, fobj)
        gl.glDeleteShader(fobj)

    # プログラムオブジェクトをリンクする
    gl.glBindAttribLocation(program, 0, "position")
    gl.glBindFragDataLocation(program, 0, "fragment")
    gl.glLinkProgram(program)

    # 作成したプログラムオブジェクトを返す
    return program


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

    # バーテックスシェーダのソースプログラム
    vsrc = """
#version 150 core
in vec4 position;
void main(void)
{
    gl_Position = position;
}
"""

    fsrc = """
#version 150 core
out vec4 fragment;
void main(void)
{
    fragment = vec4(1.0, 0.0, 0.0, 1.0);
}
"""

    # プログラムオブジェクトを作成する
    program = create_program(vsrc, fsrc)

    # ウィンドウが開いている間繰り返す
    while glfw.window_should_close(window) == gl.GL_FALSE:
        # ウィンドウを消去する
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # シェーダプログラムの使用開始
        gl.glUseProgram(program)

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
