import glfw

import e3d3
import e3d3.log
import e3d3.core
import e3d3.error
import e3d3.events


logger = e3d3.log.get(__name__)


class WindowError(e3d3.error.CoreError):
    pass


class Window(e3d3.core.System):
    window = None
    display = None
    width = 0
    height = 0

    @classmethod
    def run(cls):
        if not glfw.init():
            e3d3.events.dispatch('app.stop')
            raise WindowError('cant init glfw')

        config = e3d3.data.Config['e3d3.yaml']['window']
        cls.width = config.get('width', 1280)
        cls.height = config.get('height', 720)

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        glfw.window_hint(glfw.DECORATED, not config.get('borderless', False))

        if config.get('full', False):
            cls.display = glfw.get_primary_monitor()

        cls.window = glfw.create_window(
            cls.width, cls.height,
            config.get('label', 'e3d3'),
            cls.display,
            None)

        if not cls.window:
            e3d3.events.dispatch('app.stop')

        glfw.set_key_callback(cls.window, cls.key_callback)

        glfw.make_context_current(cls.window)

        e3d3.events.subscribe(cls.cursor_show, 'window.cursor.show')
        e3d3.events.subscribe(cls.cursor_lock, 'window.cursor.lock')

    @classmethod
    def update(cls):
        glfw.poll_events()
        glfw.swap_buffers(cls.window)

        if glfw.window_should_close(cls.window):
            e3d3.events.dispatch('app.stop')

    @classmethod
    def clean(cls):
        glfw.terminate()

    @classmethod
    def cursor_show(cls, value):
        if value:
            glfw.set_cursor(cls.window, glfw.CURSOR_NORMAL)
        else:
            glfw.set_cursor(cls.window, glfw.CURSOR_HIDDEN)

    @classmethod
    def cursor_lock(cls, value):
        if value:
            glfw.set_input_mode(cls.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        else:
            glfw.set_input_mode(cls.window, glfw.CURSOR, glfw.CURSOR_NORMAL)

    @classmethod
    def key_callback(cls, key, scan, action, mods):
        if action == glfw.PRESS:
            e3d3.events.dispatch('window.key.down', key, scan)
        else:
            e3d3.events.dispatch('window.key.up', key, scan)
