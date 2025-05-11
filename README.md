# Final project for Programming II Tag V0.5
# Table of Contents
- [HOW TO INSTALL?](#how-to-install)
    - [NECESSARY FILE TO RUN THE PROGRAM](#necessary-file-to-run-the-program)
- [Files and a brief description of classes it contains](#files-and-a-brief-description-of-classes-it-contains)
    - [game.py](game.py)
    - [monster.py](monster.py)
        - [Monster_TMP](#class-monster_tmp)
    - [player.py](player.py)
        - [Player](#class-player)
    - [item.py](item.py)
        - [Item_TMP](#class-item_tmp)
    - [shop.py](shop.py)
        - [Shop](#class-shop)
    - [ui.py](ui.py)
        - [AllUI](#class-allui)
    - [spritesheet.py](spritesheet.py)
    - [configs.py](configs.py)
    - [sound.py](sound.py)
        -[Sound](#class-sound)
    - [graph.py](graph.py) 
        - [MyApp](#class-myapp)
- [HOW TO PLAY?](#how-to-play)
- [HOW TO INSTALL PYGAME](#how-to-install-pygame)
- [Credit for images and sounds](#credit-for-images-and-sounds)
- [Known Bugs](#known-bugs)
# How to install?
1. Clone or Download the project
2. You **MUST** have pygame library installed
3. In your Git bash or whatever you use, make sure that your directory folder is set to by doing **Slash_Mobs folder** ```cd Slash_mobs```.
4. Once you've confirmed that, you can then type in ```python game.py``` to run the game.

- If the instructions above are too hard, **Install pygame** and you can just click **[game.py](game.py)**
file in the downloaded folder

- NOTE: **DO NOT RUN THIS GAME THROUGH AN IDE**

## Necessary file to run the program.
### Libraries:
- pygame 

# Files and a brief description of classes it contains

## [game.py](game.py)
The main part of the game. You need to run this file in order to run and it also utilizes all the classes in the folder in order to run as well.

## [monster.py](monster.py)
A file containing all mob's skills and their respective behaviour when in ganme.

### Class Monster_TMP
The mother class of all monsters. Basically all the skills animation and their effects are stored in here for child classes to use in the future.

## [player.py](player.py)
A file containg all the player statistics and the player's behavior on screen

### Class Player
Stores every data to transfer to csv along with player's skills and effects. This class also contols how player is limited from walking pass ccertain point on screen (**Border**)

## [item.py](item.py)
Stores all items in game (**Potions, Miscs, Weapons**) and controls how each item can boost/neagte or heal player stats.

### Class Item_TMP
The mother class of all items in the game. This cclass initializes basic variables to be used later in child classes.

## [shop.py](shop.py)
This class handles the SHOP scene and every interactions the player ccan do in this scene.

### Class Shop
Creates the shop/item menus and their respective icons. This class also detects whether the player has already equipped the weapon they're trying to buy. If so, the player won't be able to but it.

## [ui.py](ui.py)
Controls every **UI/Animation** in the game excluding monster and player's.

### Class AllUI
Contains mutiple function to be used in different circumstances such as combat and non-combat scene.

## [spritesheet.py](spritesheet.py)
Extract the image file path from **Class Configs** and send the extracted image back to the class that called it

## [configs.py](configs.py)
Store all settings in game, whether it's **FPS** and **Player's speed** or even **Mob's position** in different circumstances.

## [sound.py](sound.py)
Manages all sound in the game. 

### Class Sound
The class purpose is to only simplify the 4 lines of code into 1 line to add music/sound into the game

## [graph.py](graph.py)
A file contains graph statistics that when it is run, it shows mutiples stats, player can see the trending weapon or even the mob that kills player the most.

### Class MyApp
This class utilized the csv file, chaning into graph visualizations using matplotlib and pandas

# How to play?
- Walk around by using WASD.
- If you see any mobs, walk towards it .
- Info messages will pop up asking you if you to fight this mob or not.
- Press **Space** to start the fight.
- Once the battle starts. Hit any button indicated on screen to start attacking.

# How to install pygame
1. In your IDE, open up your Terminal.
2. Type in this command ```pip install pygame```.
3. Once the installation is done, try this command. 
```
import pygame
print(pygame.__verion__)
```
4. If you're able to run the following code with errors, then you're good to go!
5. If the following method did not work, try ```https://www.pygame.org/wiki/GettingStarted```

# Credit for images and sounds
## BG
 - Hall ```https://www.dreamstime.com/photos-images/background-castle-pixel.html```
 - Plain ```https://www.dreamstime.com/photos-images/background-castle-pixel.html```
 - Shop ```https://images.app.goo.gl/8PaJ3kUi8cSvThpC9```
 - Desert ```https://images.app.goo.gl/wMMxdSSTdaWCYoYD9```
 - Winter ```https://images.app.goo.gl/MefGGkoAiUJZH4Vd7```
 - Cave ```https://www.dreamstime.com/photos-images/background-castle-pixel.html```

## Player
 - Character animation ```https://www.spriters-resource.com/search/?q=final+fantasy&c=-1&o%5B%5D=s&o%5B%5D=ig&o%5B%5D=g```
## Mobs
 - Slime ```https://craftpix.net/freebies/free-slime-mobs-pixel-art-top-down-sprite-pack/```
 - Goblin ```https://nastanliev.itch.io/goblins```
 - Dark Goblin ```https://zneeke.itch.io/goblin-scout-silhouette```
 - Vampires ```https://craftpix.net/freebies/free-vampire-pixel-art-sprite-sheets/```
 - Scorpion ```https://master-blazter.itch.io/scorpion-pixel-art```
 - Worms ```https://nastanliev.itch.io/worms```
 - Minotaurs ```https://craftpix.net/freebies/free-minotaur-sprite-sheet-pixel-art-pack/```

## Effects
 - Fire/Doom/Instincts/Gravity/Half/Demi ```https://ragnapixel.itch.io/particle-fx?download```
 - Thunder ```https://ansimuz.itch.io/gothicvania-magic-pack-9?download```
 - Heal ```https://pimen.itch.io/cutting-and-healing/download/eyJleHBpcmVzIjoxNzQ2OTAyNzEwLCJpZCI6NTcwMTc3fQ%3D%3D.t%2B88i4xy0AhttLSJNB25YfaPvBc%3D```
 - Lock ```https://opengameart.org/content/skull-death-effect-spritesheet```
 - Haste/Greed/Curse ```https://bdragon1727.itch.io/pixel-holy-spell-effect-32x32-pack-3```


## Icons
 - Potions ```https://catballgames.itch.io/800-round-potion-sprites/download/eyJleHBpcmVzIjoxNzQ2ODgxNDk5LCJpZCI6NTEzOTcxfQ%3D%3D.wmRKxxWplc%2BGuxCskYS4sq0hIcU%3D```
 - Weapons ```https://free-game-assets.itch.io/free-melee-weapon-pixel-icons-for-cyberpunk/download/eyJleHBpcmVzIjoxNzQ2ODgxMDQ5LCJpZCI6MjY5Njc5N30%3D.hX9u%2B8xqJ9tMEOHG2SCoYvJ24Wg%3D```
 - Bomb ```https://ansimuz.itch.io/explosion-animations-pack/download/eyJleHBpcmVzIjoxNzQ2OTAyNTQzLCJpZCI6MTMzODMxfQ%3D%3D.hlBFwi6X0rwsD0a%2FUttDM2zOQXM%3D```

## Songs
 - All BG
  ```https://angel-cintado-soundtrack.itch.io/fantasy-town-music```
  
# Known Bugs
- When MINOTAUR2 uses **HASTE**, if the player spam Attack (Z) the Haste effecct will no longer be applied to it, and MINOTAUR2 will lose it's ability to use Haste in that fight

- When you enter Cave scene if you hold **W** key, the player will walk to the right of border which is not intentional by me.