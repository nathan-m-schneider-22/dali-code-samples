# Pathfinding Algorithms Visualization

After a term in CS1, I was inspired to use the graphics library we used in class to make some of my own projects. After some trials with "3D" graphics, I made this. This interface displays a graph in 3D. You can use the buttons to add and remove vertices, edges, and change algorithms. By clicking on nodes and hovering over the target nodes, you can view a visualization of the search of a path between the start and finish nodes. This interface implements BFS, DFS, Dijkstras, and A* search pathfinding. This relies on Thomas Cormen's CS1 graphics library as a wrapper for pyqt5.

## Implementation
Shortly before I learned what I rotation matrix was, I wrote this code that maintains the position of nodes with spherical coordinates, allowing easy rotation. The nodes are then rendered every frame, (somewhat inefficiently) and displayed to the user. Lags after about 50 spinning nodes. 

## Usage
To run, make sure you have pyqt5 installed (likely through pip), then run main.py. Use the buttons for their displayed functions, and move your mouse to the sides of the screen to spin the model. 