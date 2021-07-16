/*************************************************************************/
/* PiMan - Python Game For Raspberry Pi                                  */
/* Copyright (C) 2013 Jason Birch                                        */
/*                                                                       */
/* This program is free software: you can redistribute it and/or modify  */
/* it under the terms of the GNU General Public License as published by  */
/* the Free Software Foundation, either version 3 of the License, or     */
/* (at your option) any later version.                                   */
/*                                                                       */
/* This program is distributed in the hope that it will be useful,       */
/* but WITHOUT ANY WARRANTY; without even the implied warranty of        */
/* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         */
/* GNU General Public License for more details.                          */
/*                                                                       */
/* You should have received a copy of the GNU General Public License     */
/* along with this program.  If not, see <http://www.gnu.org/licenses/>. */
/*************************************************************************/

This Python source code is an example of how to write a game in the Python
scripting language. The scripts use the PyGame libraries which need to be
installed in addition to Python. The target system is the Raspberry Pi
micro computer. Most distributions of Linux already have Python installed
as an example on the Arch Linux distribution install PyGame with the
following command:

`pacman -S pygame`

Run the game by typing the following:
`./PiMan.py`

Or:
`python2 PiMan.py`

Or:
`python PiMan.py`

The purpose of this project, is a first application I have written in 
Python. To become acquainted with Python for a new job which may require
Python experience. The code is being distributed as a starting example
to assist new comers to Pyton coding, to create games and applications 
in Python script.

The application is simple and small. There are five script files:
PiMan.py          - The main application script.
GameSprite.py     - The super class for game sprites. Containing the
                    common code shared by all game sprites.
PiManSprite.py    - The sub class of GameSprite which is the player's
                    character.
WormSprite.py     - The sub class of GameSprite which is the computer's
                    worm characters.
Map.py            - The play area, which can load a series of levels
                    defined in text files.

The application then has three directories of support files:
Levels            - Text files representing the levels of the game.
Images            - Image files for the graphics of the game, 
                    associated with each character and map element.
Sounds            - The sounds associated with each character of the
                    game.

