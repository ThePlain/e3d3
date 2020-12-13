import yagl as gl

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

    @classmethod
    def run(cls):
        gl.clear_color(0.25, 0.25, 0.25, 1)
        gl.clear_depth(1.0)

    @classmethod
    def update(cls):
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT)

    @classmethod
    def clean(cls):
        pass
