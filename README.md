# brortal-kombat
Mortal Kombat-like game written with the arcade library.

![There's supposed to be a gif here](./battlebros.gif)



## Installation
If you already have arcade working, then this should work out of the box. I didn't use any non standard libraries. Or maybe I did. I'm too lazy to look. You'll figure it out, champ.

```
python main.py
```
to run the game.

## Controls
Player 1:
* AWSD + X and C
Player 2:
* arrow keys + O and P

## Using and Adding Assets (sprites, sounds)
Sprite animations were recorded as stop motion with my friends in front of a green screen.

Only one set of animations is provided here, and the sound effects provided are rather minimal.

You can add your own Sprites following the directory structure of the provided one. The game will pick up new sprites automatically.

Animation datastructures are cached between game excutions (pickled and saved to disk). The first time you load a new set of sprite animations it may take a moment.


## Aknowledgements
* William Naaden for the background music
* Nate Bodette for his sprite animations
