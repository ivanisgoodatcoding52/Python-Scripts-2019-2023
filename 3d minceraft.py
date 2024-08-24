import pyglet
from pyglet.gl import *

# Constants
WIDTH, HEIGHT = 800, 600
FOV = 65.0

# Cube vertices
vertices = [
    -1, -1, -1,
    -1, 1, -1,
    1, 1, -1,
    1, -1, -1,
    -1, -1, 1,
    -1, 1, 1,
    1, 1, 1,
    1, -1, 1
]

# Cube edges
edges = [
    0, 1, 1, 2, 2, 3, 3, 0,
    4, 5, 5, 6, 6, 7, 7, 4,
    0, 4, 1, 5, 2, 6, 3, 7
]

# Initialize Pyglet window
window = pyglet.window.Window(WIDTH, HEIGHT, caption="Simple 3D Minecraft Clone", resizable=True)
glEnable(GL_DEPTH_TEST)

@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOV, width / float(height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

def draw_cube():
    glBegin(GL_LINES)
    for edge in range(0, len(edges), 2):
        for vertex in range(2):
            index = edges[edge + vertex] * 3
            glVertex3fv(vertices[index:index + 3])
    glEnd()

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 0, -5, 0, 0, 0, 0, 1, 0)
    draw_cube()

def update(dt):
    pass

pyglet.clock.schedule(update)

if __name__ == "__main__":
    pyglet.app.run()
