when making a file, write constatns and all other variables to file
if loading, load all variables from file

after cleaning everything up, removing unnecessary code, etc, I need to do a complete audit of the code, and make sure everything is working as intended
making sure that the return grid is accurate, agent moves as it is supposed to, etc

changing observation space to widthxheightx2, where the first layer is the cell values (nothing, rock, path, agent, exit, etc), and the second layer is how many times the agent has been in that cell.
This might be too much noise for the model though. What I might be able to do instead of the second layer is tack onto the end a flattened array that would consist of a 5x5 (or any size) around the agent with the same values the second layer would have. This would be a lot less noise, and would still give the model the information it needs to learn.

if i change the observation space to be relative to the agent, and not dependent on the size of the dungeon, it would be interesting to see if it can handle a randomized dungeon size each round.

instead of dropping the reward all at the end, move back to giving it some rewards during the round. Giving it a reward of +1 if it moves closer to the exit then it has already been, and a negative reward equal to the amount of times it has previously been in the cell it currently is in. Then, if it succesfully makes it out, give it back a reward equal to how much I've subtracted by it being in the same cell multiple times. This would hopefully teach it that it isn't good to be in the same spot for mutiple turns in a row, but it isn't the worst thing in the world to have to enter a previously entered cell to get to the exit. Or maybe just give that reward more immediately, whenever it gets its next +1 for moving closer to the exit.

what if i gave it its reward categories during each step as a part of the observation. For the time spent, max times in given location, etc. It might be able to better figure out what it is doing wrong, and what it is doing right.
Also adding the current frame number to the observation space.

Finding the optimal path using A\* and then using how long it would hypotheticall take in an optimal case instead of max_frames.
