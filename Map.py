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


import array
import pygame
import GameSprite


#/*****************************************************/
#/* Class to define the play area of the application. */
#/*****************************************************/
class Map:
#  /***************************/
# /* Global class constants. */
#/***************************/
   WIDTH = 19
   HEIGHT = 13
   MAX_LEVEL = 2
   MAP_WALL = "A"
   MAP_PATH = "B"
   MAP_RASPBERRY = "C"
   MAP_PIP = "D"
   MAP_LAYER_LEFT = "E"
   MAP_LAYER_MIDDLE = "F"
   MAP_LAYER_EXIT = "G"
   MAP_LAYER_RIGHT = "H"


#/**********************/
#/* Class constructor. */
#/**********************/
   def __init__(self, NewBackground):
#  /***************************/
# /* Class member variables. */
#/***************************/
      self.MapCellSize = pygame.Rect(0, 0, 0, 0)
      self.Background = NewBackground
      self.Reset()


#/********************************/
#/* Reset map object to level 1. */
#/********************************/
   def Reset(self):
      self.Level = 1
      self.LevelPipCount = self.LoadLevel(self.Level)


#/******************************/
#/* Load a specific level map. */
#/******************************/
   def LoadLevel(self, Level):
      self.DonePipCount = 0
      PipCount = 0
      self.MapArray = array.array('c')
      self.MapSprites = []

#  /**********************************/
# /* Read specific game level data. */
#/**********************************/
      File = open("Levels/Level_{0}.txt".format(Level), 'r', 0)
      self.MapArray.fromfile(File, (self.WIDTH + 1) * self.HEIGHT)
      File.close()

#  /************************************************/
# /* Create a sprite for each element of the map. */
#/************************************************/
      Count = 0
      SpriteCount = 0
      for MapElement in self.MapArray:
         Y = Count / (self.WIDTH + 1)
         X = (Count % (self.WIDTH + 1))
         if X != self.WIDTH:
            if MapElement == self.MAP_PIP:
               PipCount += 1
            self.MapSprites.append(GameSprite.GameSprite("Map", 0, 0))
            self.MapSprites[SpriteCount].SetImageIndex(ord(MapElement) - ord("A"))
            self.MapCellSize = self.MapSprites[SpriteCount].GetLocation()
            self.MapSprites[SpriteCount].SetLocation(X * self.MapCellSize.width, Y * self.MapCellSize.height)
            SpriteCount += 1
         Count += 1

#   /**********************************************/
#  /* Draw the entire constructed level map onto */
# /* a surface for use as a background.         */
#/**********************************************/
      self.Draw(self.Background)

      return PipCount


#/**********************************************/
#/* Draw the entire constructed level map onto */
#/* a surface for use as a background.         */
#/**********************************************/
   def Draw(self, ThisSurface):
      for Sprite in self.MapSprites:
         Sprite.Draw(ThisSurface)


#/***********************************************************************/
#/* Allow other parts of the application to get the size of a map cell. */
#/***********************************************************************/
   def GetMapCellSize(self):
      return self.MapCellSize


#/***********************************************************************/
#/* Allow other parts of the application to get the type of a map cell. */
#/***********************************************************************/
   def GetMapCellType(self, Location):
#  /*******************************************************/
# /* Align the provided location with an exact map cell. */
#/*******************************************************/
      OffsetX = Location.x % self.MapCellSize.width
      if OffsetX > self.MapCellSize.width / 2:
         OffsetX -= self.MapCellSize.width
      elif OffsetX > 0:
         OffsetX += self.MapCellSize.width / 2

      OffsetY = Location.y % self.MapCellSize.height
      if OffsetY > self.MapCellSize.height / 2:
         OffsetY -= self.MapCellSize.height
      elif OffsetY > 0:
         OffsetY += self.MapCellSize.height / 2

#  /**************************************************************/
# /* Return the type of the map cell with the aligned location. */
#/**************************************************************/
      XIndex = (Location.x + OffsetX) / self.MapCellSize.width
      YIndex = (Location.y + OffsetY) / self.MapCellSize.height
      return self.MapArray[YIndex * (self.WIDTH + 1) + XIndex]


#/***********************************************************************/
#/* Allow other parts of the application to set the type of a map cell. */
#/***********************************************************************/
   def SetMapCellType(self, Location, NewType):
#  /*******************************************************/
# /* Align the provided location with an exact map cell. */
#/*******************************************************/
      OffsetX = Location.x % self.MapCellSize.width
      if OffsetX > self.MapCellSize.width / 2:
         OffsetX -= self.MapCellSize.width
      elif OffsetX > 0:
         OffsetX += self.MapCellSize.width / 2

      OffsetY = Location.y % self.MapCellSize.height
      if OffsetY > self.MapCellSize.height / 2:
         OffsetY -= self.MapCellSize.height
      elif OffsetY > 0:
         OffsetY += self.MapCellSize.height / 2

#   /***********************************************/
#  /* Set the type of the map cell at the aligned */
# /* location with the specified cell type.      */
#/***********************************************/
      XIndex = (Location.x + OffsetX) / self.MapCellSize.width
      YIndex = (Location.y + OffsetY) / self.MapCellSize.height
      Index = YIndex * (self.WIDTH + 1) + XIndex
      if self.MapArray[Index] == self.MAP_PIP:
         self.DonePipCount += 1
      self.MapArray[Index] = NewType
      Index = YIndex * self.WIDTH + XIndex
      self.MapSprites[Index].SetImageIndex(ord(NewType) - ord("A"))
      self.MapSprites[Index].Draw(self.Background)


#   /******************************************************/
#  /* Allow other parts of the application to see if all */
# /* level pips have been consumed.                     */
#/******************************************************/
   def LevelEndCheck(self):
      return (self.DonePipCount == self.LevelPipCount)


#  /*************************************/
# /* Start the next application level. */
#/*************************************/
   def NextLevel(self):
         self.Level += 1
         if self.Level > self.MAX_LEVEL:
            self.Level = 1
         self.LevelPipCount = self.LoadLevel(self.Level)

