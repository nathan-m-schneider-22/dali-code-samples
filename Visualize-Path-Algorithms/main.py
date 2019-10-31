from interface import *
# This code displays a 3D network of nodes, then naviagtes them using
# different path algorithms, including DFS, BFS, Dijkstra's Algorithm, and
# A* search.
# AS of now the program runs off of Thomas Cormen's graphics library, which I
# am hoping to replace. The main just calls the important functions of the
# Interface class

def main():
    set_clear_color(0, 0, 0)
    clear()
    UI.draw()
    UI.update()


UI = Interface()

start_graphics(main, width=WIDTH, height=HEIGHT, framerate=40, mouse_press=UI.mouse_press, mouse_move=UI.mouse_move)
