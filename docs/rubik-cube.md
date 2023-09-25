# Rubik's cube

The existence of a simple Rubik's cube is common knowledge nowadays.
If someone has been living for ages under a rock, its [Wikipedia page](https://en.wikipedia.org/wiki/Rubik%27s_Cube) has a good description of the cube.
This documentation is oriented onto the code to be used for generating and interacting with the cube.

## Faces orientation

Defining each face of the cube as a 3x3 numpy array, the top-left corner would be at the coordinate [0, 0].
While this sounds logical, the idea gets complicated when it's translated to the 3D world.

The code is defining the coordinates of each face as the user is looking directly to it.
With this definition, let's take the case of following the tile defined by the coordinates [0, 0] from the front face:

- If the cube's left face is rotated once counter-clockwise, the tile ends up at the coordinate [0, 0] from the top-face.
- If the cube's left face is rotated twice counter-clockwise, the tile ends up at the coordinate [2, 2] from the back-face.
- If the cube's left face is rotated twice clockwise, the tile ends up at the coordinate [0, 0] from the back-face.

