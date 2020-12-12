import yagl as gl

import e3d3


class Pipeline(e3d3.core.System):

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
