# PiMan - Python Game For Raspberry Pi
# Copyright (C) 2013 Jason Birch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see &lt;http://www.gnu.org/licenses/>.


import random
import pygame
import Map
import GameSprite


class WormSprite(GameSprite.GameSprite):
#  /***************************/
# /* Global class constants. */
#/***************************/
   IMG_WORM_RIGHT = 0
   IMG_WORM_DOWN = 1
   IMG_WORM_LEFT = 2
   IMG_WORM_UP = 3
   IMG_HYPER_RIGHT = 4
   IMG_HYPER_DOWN = 5
   IMG_HYPER_LEFT = 6
   IMG_HYPER_UP = 7
   DELAY_START = 50


#/**********************/
#/* Class constructor. */
#/**********************/
   def __init__(self, ImageFile, X, Y):
      GameSprite.GameSprite.__init__(self, ImageFile, X, Y)
#  /***************************/
# /* Class member variables. */
#/***************************/
      self.SpriteMoveFlags = [[] for Index in range(323)]
      self.AnimateFrame = self.IMG_WORM_RIGHT
      self.HyperFlag = False
      self.InvalidCells = (Map.Map.MAP_WALL)
      self.DelayStart = self.DELAY_START


#/************************/
#/* Reset sprite object. */
#/************************/
   def Reset(self):
      GameSprite.GameSprite.Reset(self)
      self.DelayStart = self.DELAY_START
      self.HyperFlag = False


#/********************************************/
#/* Animate one frame for the sprite object. */
#/********************************************/
   def Move(self, KeysPressed, ThisMap):
#   /******************************************************/
#  /* Prevent sprite from moving for a period initially  */
# /* to give player a chance to start a life.           */
#/******************************************************/
      if self.DelayStart > 0:
         self.DelayStart -= 1
      else:
         CellSize = ThisMap.GetMapCellSize().width

#  /**********************************************/
# /* Algorythum for automated moving of sprite. */
#/**********************************************/
         Directions = []

#  /***********************************/
# /* Work out the current direction. */
#/***********************************/
         if self.XSpeed < 0:
            Direction = self.DIRECTION_LEFT
         elif self.XSpeed > 0:
            Direction = self.DIRECTION_RIGHT
         elif self.YSpeed < 0:
            Direction = self.DIRECTION_UP
         elif self.YSpeed > 0:
            Direction = self.DIRECTION_DOWN
         else:
            Direction = self.DIRECTION_NONE

#  /*******************************************************************/
# /* Check which directions are available from the current location. */
#/*******************************************************************/
         TestLocation = pygame.Rect(self.ThisLocation.x - CellSize, self.ThisLocation.y, 0, 0)
         MapCellType = ThisMap.GetMapCellType(TestLocation)
         if MapCellType not in self.InvalidCells:
            Directions.append(self.DIRECTION_LEFT)

         TestLocation = pygame.Rect(self.ThisLocation.x + CellSize, self.ThisLocation.y, 0, 0)
         MapCellType = ThisMap.GetMapCellType(TestLocation)
         if MapCellType not in self.InvalidCells:
            Directions.append(self.DIRECTION_RIGHT)

         TestLocation = pygame.Rect(self.ThisLocation.x, self.ThisLocation.y - CellSize, 0, 0)
         MapCellType = ThisMap.GetMapCellType(TestLocation)
         if MapCellType not in self.InvalidCells:
            Directions.append(self.DIRECTION_UP)

         TestLocation = pygame.Rect(self.ThisLocation.x, self.ThisLocation.y + CellSize, 0, 0)
         MapCellType = ThisMap.GetMapCellType(TestLocation)
         if MapCellType not in self.InvalidCells:
            Directions.append(self.DIRECTION_DOWN)

#   /********************************************/
#  /* If more than one direction is available, */
# /* remove the option to reverse direction.  */
#/********************************************/
         if len(Directions) > 1:
            if Direction == self.DIRECTION_LEFT and self.DIRECTION_RIGHT in Directions:
               Directions.remove(self.DIRECTION_RIGHT)
            elif Direction == self.DIRECTION_RIGHT and self.DIRECTION_LEFT in Directions:
               Directions.remove(self.DIRECTION_LEFT)
            elif Direction == self.DIRECTION_UP and self.DIRECTION_DOWN in Directions:
               Directions.remove(self.DIRECTION_DOWN)
            elif Direction == self.DIRECTION_DOWN and self.DIRECTION_UP in Directions:
               Directions.remove(self.DIRECTION_UP)

#   /********************************************/
#  /* Randomly select a direction, with a bias */
# /* of continuing in the current direction.  */
#/********************************************/
         if Direction not in Directions:
            Rand = random.randrange(len(Directions))
         else:
            Rand = random.randrange(len(Directions) + 10)

         if Rand < len(Directions):
            if Directions[Rand] == self.DIRECTION_LEFT:
               self.SpriteMoveFlags[pygame.K_LEFT] = True
               self.SpriteMoveFlags[pygame.K_RIGHT] = False
               self.SpriteMoveFlags[pygame.K_UP] = False
               self.SpriteMoveFlags[pygame.K_DOWN] = False
            elif Directions[Rand] == self.DIRECTION_RIGHT:
               self.SpriteMoveFlags[pygame.K_LEFT] = False
               self.SpriteMoveFlags[pygame.K_RIGHT] = True
               self.SpriteMoveFlags[pygame.K_UP] = False
               self.SpriteMoveFlags[pygame.K_DOWN] = False
            elif Directions[Rand] == self.DIRECTION_UP:
               self.SpriteMoveFlags[pygame.K_LEFT] = False
               self.SpriteMoveFlags[pygame.K_RIGHT] = False
               self.SpriteMoveFlags[pygame.K_UP] = True
               self.SpriteMoveFlags[pygame.K_DOWN] = False
            elif Directions[Rand] == self.DIRECTION_DOWN:
               self.SpriteMoveFlags[pygame.K_LEFT] = False
               self.SpriteMoveFlags[pygame.K_RIGHT] = False
               self.SpriteMoveFlags[pygame.K_UP] = False
               self.SpriteMoveFlags[pygame.K_DOWN] = True

#  /********************************************************/
# /* Call super class to perform generic sprite movement. */
#/********************************************************/
         Direction = GameSprite.GameSprite.Move(self, self.SpriteMoveFlags, ThisMap)

#   /***********************************************/
#  /* If the direction of the sprite has changed, */
# /* change sprite graphic as appropreate.       */
#/***********************************************/
         if Direction == self.DIRECTION_LEFT:
            GameSprite.GameSprite.SetSpeed(self, -CellSize / 4, 0)
            if self.HyperFlag:
               self.CurrentAnimateFrame = self.IMG_HYPER_LEFT
            else:
               self.CurrentAnimateFrame = self.IMG_WORM_LEFT
            self.AnimateCount = 0
         elif Direction == self.DIRECTION_RIGHT:
            GameSprite.GameSprite.SetSpeed(self, CellSize / 4, 0)
            if self.HyperFlag:
               self.CurrentAnimateFrame = self.IMG_HYPER_RIGHT
            else:
               self.CurrentAnimateFrame = self.IMG_WORM_RIGHT
            self.AnimateCount = 0
         elif Direction == self.DIRECTION_UP:
            GameSprite.GameSprite.SetSpeed(self, 0, -CellSize / 4)
            if self.HyperFlag:
               self.CurrentAnimateFrame = self.IMG_HYPER_UP
            else:
               self.CurrentAnimateFrame = self.IMG_WORM_UP
            self.AnimateCount = 0
         elif Direction == self.DIRECTION_DOWN:
            GameSprite.GameSprite.SetSpeed(self, 0, CellSize / 4)
            if self.HyperFlag:
               self.CurrentAnimateFrame = self.IMG_HYPER_DOWN
            else:
               self.CurrentAnimateFrame = self.IMG_WORM_DOWN
            self.AnimateCount = 0
         self.SetImageIndex(self.CurrentAnimateFrame)


#/*******************************************/
#/* Allow other parts of the application to */
#/* set the current state of hyper mode.    */
#/*******************************************/
   def SetHyperFlag(self, NewFlag):
      self.HyperFlag = NewFlag


#/*******************************************/
#/* Allow other parts of the application to */
#/* get the current state of hyper mode.    */
#/*******************************************/
   def GetHyperFlag(self):
      return self.HyperFlag

