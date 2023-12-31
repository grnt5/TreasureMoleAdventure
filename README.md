﻿# Treasure Mole Adventure

**Project Background**

This is a game I made for my term project for 15-112 Fundamentals of Programming and Computer Science at CMU in Spring 2022 (Grade: 93.7%). Using the Tkinter graphics library and graph-based algorithms (namely Cellular Automata, Prim's Algorithm, and Breadth First Search), this project is a game where the player must collect treasures in a cave with the help moles they find in the cave, similar to Nintendo's Pikmin series of games. Besides some typo fixes and inclusions of links to important resources, all markdown below and files in the repository remain unchanged since the project's submission.

**About Treasure Mole Adventure**

Treasure Mole Adventure is a top-down 2D adventure and strategy game in which
the player controls an army of moles in a randomly generated cave by throwing
them at objects. Throwing them at enemies (mushrooms) causes them to attack
them and throwing them at dead enemies and treasure makes them carry these
items back to the player's landing site to make more moles and progress
through the game's objective (collecting all the treasure) respectively.

The main objective of the game is to use the moles to collect all the treasure
and defeat enemies to make more moles to carry heavier treasure. If all the
moles die or the player can't make enough moles to carry all the treasure, it's
game over. Try to go for a best time!

**How to run Treasure Mole Adventure**

Download the code as a .zip file and extract it. Then run main.py

**Required libraries**

This program uses the CMU 112 graphics library (an altered version of the Tkinter library), which requires PIL/Pillow and
Requests to work properly.

One can find the CMU 112 graphics library file at the following links:

Current version (As of December 26th, 2023): https://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py

Version used for this project: https://www.kosbie.net/cmu/spring-22/15-112/notes/cmu_112_graphics.py

**Shortcut commands**

For the sake of demonstrating different components of the game, the user can
use the following shortcut commands in gamePlayMode:

0 - Toggles the ability to use shortcuts on and off. They are off by default.

1 - Removes all enemies and pre-existing treasure, replacing such treasure with
one in the player's position and a weight (molesNeeded value) of 1. This
demonstrates the ability for the moles to carry the treasure to the land site
and execute the win condition.

2 - Moves an enemy to the player's position (or makes an enemy in the player's
position if there are no enemies). This demonstrates attacking the enemy,
carrying the dead enemy to the land site when defeated, and the first losing
condition (all the moles are dead)

3 - Changes a treasures weight (molesNeeded value) to 1000, a weight that is
impossible to carry in normal gameplay. This demonstrates the second losing
condition (the player can't make enough moles to carry the treasure).
