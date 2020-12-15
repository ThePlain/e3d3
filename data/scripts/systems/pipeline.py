from OpenGL.GL import *

import e3d3
import e3d3.core
import e3d3.math
import e3d3.events


class Camera(e3d3.core.Component):
    def __init__(self, entity):
        super(Camera, self).__init__(entity)
        self.fov = 80
        self.near = 0.1
        self.far = 500

    def activate(self):
        Pipeline.active_camera = self


class StaticMesh(e3d3.core.Component):
    def __init__(self, entity):
        super(StaticMesh, self).__init__(entity)
        self.mesh = None
        self.material = None

    def on_start(self):
        e3d3.events.subscribe(self, 'pipeline.draw')

    def on_clean(self):
        e3d3.events.remove(self, 'pipeline.draw')


class Pipeline(e3d3.core.System):
    active_camera = None
    framebuffer = None
    layers = dict()
    depth = None
    window = None

    @classmethod
    def run(cls):
        cls.window = e3d3.Window

        cls.framebuffer = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, cls.framebuffer)
        cls.create_framebuffer('position', 0, GL_RGBA16F, GL_FLOAT)
        cls.create_framebuffer('normal', 1, GL_RGBA16F, GL_FLOAT)
        cls.create_framebuffer('color', 2, GL_RGBA, GL_UNSIGNED_BYTE)
        cls.create_framebuffer('specular', 3, GL_RGBA, GL_UNSIGNED_BYTE)

        buffers = [GL_COLOR_ATTACHMENT0 + num for num, _ in cls.layers.values()]
        glDrawBuffers(buffers)

        cls.depth = cls.create_framebuffer(None, -1, GL_DEPTH_COMPONENT32F, GL_FLOAT, content=GL_DEPTH_COMPONENT)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, cls.depth, 0)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError('frame buffer not ready.')

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        glClearColor(0.25, 0.25, 0.25, 1)
        glClearDepth(1.0)

    @classmethod
    def update(cls):
        glBindFramebuffer(GL_FRAMEBUFFER, cls.framebuffer)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # TODO: Data Render Pass
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    @classmethod
    def clean(cls):
        pass

    @classmethod
    def create_framebuffer(cls, name, num, mode, type, content=GL_RGBA):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, mode, cls.window.width, cls.window.height, 0, content, type, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        if name:
            cls.layers[name] = (num, texture)
            return None
        else:
            return texture
