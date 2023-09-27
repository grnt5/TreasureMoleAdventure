# TreasureMole Adventure

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

This program uses the CMU 112 graphics library, which requires PIL/Pillow and
Requests to work properly.

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
