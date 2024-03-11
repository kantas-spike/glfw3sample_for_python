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


# シェーダオブジェクトのコンパイル結果を表示する
#   shader: シェーダオブジェクト名
#   str: コンパイルエラーが発生した場所を示す文字列
def validate_shader_compiled(shader, name):
    # コンパイル結果を取得する
    status = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
    if status == gl.GL_FALSE:
        logger.error(f"Compile error in {name}")

    # シェーダのコンパイル時のログを取得する
    shader_log = gl.glGetShaderInfoLog(shader)
    if shader_log:
        logger.error(shader_log.decode("utf-8"))

    return status != gl.GL_FALSE


# プログラムオブジェクトのリンク結果を表示する
#    program: プログラムオブジェクト名
def validate_program_linked(program):
    # リンク結果を取得する
    status = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)
    if status == gl.GL_FALSE:
        # シェーダのリンク時のログを取得する
        program_log = gl.glGetProgramInfoLog(program)
        if program_log:
            logger.error(f"program: link error\n{program_log.decode('utf-8')}")

    return status != gl.GL_FALSE


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
        if validate_shader_compiled(vobj, "vertex shader"):
            gl.glAttachShader(program, vobj)
        gl.glDeleteShader(vobj)

    if fsrc:
        # フラグメントシェーダのシェーダオブジェクトを作成する
        fobj = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(fobj, fsrc)
        gl.glCompileShader(fobj)

        # フラグメントシェーダのシェーダオブジェクトをプログラムオブジェクトに組み込む
        if validate_shader_compiled(fobj, "fragment shader"):
            gl.glAttachShader(program, fobj)
        gl.glDeleteShader(fobj)

    # プログラムオブジェクトをリンクする
    gl.glBindAttribLocation(program, 0, "position")
    gl.glBindFragDataLocation(program, 0, "fragment")
    gl.glLinkProgram(program)

    # 作成したプログラムオブジェクトを返す
    if validate_program_linked(program):
        return program

    # プログラムオブジェクトが作成できなければ 0 を返す
    gl.glDeleteProgram(program)
    return 0


# シェーダのソースファイルを読み込む
#   src_path: シェーダのソースファイル
def read_shader_source(src_path):
    with open(src_path) as f:
        return f.read()


# シェーダのソースファイルを読み込んでプログラムオブジェクトを作成する
#   vsrc_path: バーテックスシェーダのソースファイル
#   fsrc_path: フラグメントシェーダのソースファイル
def load_program(vsrc_path, fsrc_path):
    return create_program(read_shader_source(vsrc_path), read_shader_source(fsrc_path))


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

    # プログラムオブジェクトを作成する
    program = load_program("point.vert", "point.frag")

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
