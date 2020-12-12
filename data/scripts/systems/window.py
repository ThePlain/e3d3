import glfw

import e3d3
import e3d3.log
import e3d3.core
import e3d3.error
import e3d3.events


logger = e3d3.log.get(__name__)


MAP = {
    glfw.KEY_ESCAPE: 'KeyEscape',
    glfw.KEY_GRAVE_ACCENT: 'KeyGrave',
    glfw.KEY_TAB: 'KeyTab',
    glfw.KEY_CAPS_LOCK: 'KeyCapsLock',
    glfw.KEY_LEFT_SHIFT: 'KeyShiftLeft',
    glfw.KEY_LEFT_CONTROL: 'KeyCtrlLeft',
    glfw.KEY_LEFT_ALT: 'KeyAltLeft',

    glfw.KEY_BACKSPACE: '',

    glfw.KEY_F1:    'KeyF1',
    glfw.KEY_F2:    'KeyF2',
    glfw.KEY_F3:    'KeyF3',
    glfw.KEY_F4:    'KeyF4',
    glfw.KEY_F5:    'KeyF5',
    glfw.KEY_F6:    'KeyF6',
    glfw.KEY_F7:    'KeyF7',
    glfw.KEY_F8:    'KeyF8',
    glfw.KEY_F9:    'KeyF9',
    glfw.KEY_F10:   'KeyF10',
    glfw.KEY_F11:   'KeyF11',
    glfw.KEY_F12:   'KeyF12',

    glfw.KEY_Q: 'KeyQ',
    glfw.KEY_W: 'KeyW',
    glfw.KEY_E: 'KeyE',
    glfw.KEY_R: 'KeyR',
    glfw.KEY_T: 'KeyT',
    glfw.KEY_Y: 'KeyY',
    glfw.KEY_U: 'KeyU',
    glfw.KEY_I: 'KeyI',
    glfw.KEY_O: 'KeyO',
    glfw.KEY_P: 'KeyP',
    glfw.KEY_A: 'KeyA',
    glfw.KEY_S: 'KeyS',
    glfw.KEY_D: 'KeyD',
    glfw.KEY_F: 'KeyF',
    glfw.KEY_G: 'KeyG',
    glfw.KEY_H: 'KeyH',
    glfw.KEY_J: 'KeyJ',
    glfw.KEY_K: 'KeyK',
    glfw.KEY_L: 'KeyL',
    glfw.KEY_Z: 'KeyZ',
    glfw.KEY_X: 'KeyX',
    glfw.KEY_C: 'KeyC',
    glfw.KEY_V: 'KeyV',
    glfw.KEY_B: 'KeyB',
    glfw.KEY_N: 'KeyN',
    glfw.KEY_M: 'KeyM',
}


class WindowError(e3d3.error.CoreError):
    pass


class Window(e3d3.core.System):
    window = None
    display = None

    @classmethod
    def run(cls):
        if not glfw.init():
            e3d3.events.dispatch('app.stop')
            raise WindowError('cant init glfw')

        config = e3d3.data.Config['e3d3.yaml']['window']

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        glfw.window_hint(glfw.DECORATED, not config.get('borderless', False))

        if config.get('full', False):
            cls.display = glfw.get_primary_monitor()

        cls.window = glfw.create_window(
            config.get('width', 1280),
            config.get('height', 720),
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
        name = MAP.get(key)
        if not name:
            return

        if action == glfw.PRESS:
            e3d3.events.dispatch('window.key.down', name, scan)
        else:
            e3d3.events.dispatch('window.key.up', name, scan)
