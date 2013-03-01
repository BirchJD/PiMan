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


import pygame
import Map
import GameSprite


class PiManSprite(GameSprite.GameSprite):
#  /***************************/
# /* Global class constants. */
#/***************************/
   IMG_PIMAN_RIGHT = 1
   IMG_PIMAN_DOWN = 2
   IMG_PIMAN_LEFT = 3
   IMG_PIMAN_UP = 4
   IMG_PIMAN_SPLAT = 5
   LIVES = 3
   SCORE_PIP = 10
   SCORE_RASPBERRY = 50
   SCORE_HYPER = 100
   HYPER_COUNT = 200
   DIE_COUNT = 25


#/**********************/
#/* Class constructor. */
#/**********************/
   def __init__(self, ImageFile, X, Y):
      GameSprite.GameSprite.__init__(self, ImageFile, X, Y)

#  /*****************************/
# /* Load class sound effects. */
#/*****************************/
      self.SoundPip = pygame.mixer.Sound("Sounds/pip.wav")
      self.SoundSplat = pygame.mixer.Sound("Sounds/splat.wav")
      self.SoundRaspberry = pygame.mixer.Sound("Sounds/raspberry.wav")

#  /***************************/
# /* Class member variables. */
#/***************************/
      self.InvalidCells = (Map.Map.MAP_WALL, Map.Map.MAP_LAYER_LEFT, Map.Map.MAP_LAYER_MIDDLE, Map.Map.MAP_LAYER_EXIT, Map.Map.MAP_LAYER_RIGHT)
      self.Reset()


#/************************/
#/* Reset sprite object. */
#/************************/
   def Reset(self):
      GameSprite.GameSprite.Reset(self)
      self.AnimateFrame = self.IMG_PIMAN_LEFT
      self.AnimateCount = 0
      self.Score = 0
      self.Lives = self.LIVES
      self.HyperCount = 0
      self.DieCount = 0
      GameSprite.GameSprite.SetSpeed(self, 0, 0)


#/********************************************/
#/* If sprite is active, draw sprite object. */
#/********************************************/
   def Draw(self, ThisSurface):
      if self.Lives > 0 or self.DieCount > 0:
         GameSprite.GameSprite.Draw(self, ThisSurface)


#/*************************************************/
#/* Draw sprite object number of lives remaining. */
#/*************************************************/
   def DrawLives(self, ThisSurface, X, Y):
      Location = GameSprite.GameSprite.GetLocation(self)
      for Count in range(0, self.Lives):
         ThisSurface.blit(self.ThisImage[self.IMG_PIMAN_RIGHT], (X, Y))
         X += Location.width * 1.25
      return self.Lives


#/********************************************/
#/* Animate one frame for the sprite object. */
#/********************************************/
   def Move(self, KeysPressed, ThisMap):
#  /******************************************************************/
# /* Show sprite dead for a period of time before resetting sprite. */
#/******************************************************************/
      if self.DieCount > 0:
         self.DieCount -= 1
         if self.DieCount == 0:
            GameSprite.GameSprite.Reset(self)
            self.SetImageIndex(self.IMG_PIMAN_LEFT)
      elif self.Lives > 0:
#  /********************************************************/
# /* Call super class to perform generic sprite movement. */
#/********************************************************/
         CellSize = ThisMap.GetMapCellSize().width
         Direction = GameSprite.GameSprite.Move(self, KeysPressed, ThisMap)

#   /***********************************************/
#  /* If the direction of the sprite has changed, */
# /* change sprite graphic as appropreate.       */
#/***********************************************/
         if Direction == self.DIRECTION_LEFT:
            GameSprite.GameSprite.SetSpeed(self, -CellSize / 4, 0)
            self.AnimateFrame = self.IMG_PIMAN_LEFT
            self.AnimateCount = 0
         elif Direction == self.DIRECTION_RIGHT:
            GameSprite.GameSprite.SetSpeed(self, CellSize / 4, 0)
            self.AnimateFrame = self.IMG_PIMAN_RIGHT
            self.AnimateCount = 0
         elif Direction == self.DIRECTION_UP:
            GameSprite.GameSprite.SetSpeed(self, 0, -CellSize / 4)
            self.AnimateFrame = self.IMG_PIMAN_UP
            self.AnimateCount = 0
         elif Direction == self.DIRECTION_DOWN:
            GameSprite.GameSprite.SetSpeed(self, 0, CellSize / 4)
            self.AnimateFrame = self.IMG_PIMAN_DOWN
            self.AnimateCount = 0

#  /****************************************************************/
# /* When hyper mode is active, decrement the hyper mode counter. */
#/****************************************************************/
         if self.HyperCount > 0:
            self.HyperCount -= 1

#  /*******************/
# /* Animate sprite. */
#/*******************/
         self.AnimateCount -= 1
         if self.AnimateCount < 0:
            self.AnimateCount = self.ANIMATE_COUNT
            if self.CurrentAnimateFrame == 0:
               self.CurrentAnimateFrame = self.AnimateFrame
            else:
               self.CurrentAnimateFrame =  0
            self.SetImageIndex(self.CurrentAnimateFrame)

#   /************************************************************/
#  /* Check the type of map cell the sprite currently occupies */
# /* and react accordingly.                                   */
#/************************************************************/
         MapCellType = ThisMap.GetMapCellType(self.ThisLocation)
         if MapCellType == ThisMap.MAP_PIP:
            self.SoundPip.play()
            self.Score += self.SCORE_PIP
            ThisMap.SetMapCellType(self.ThisLocation, ThisMap.MAP_PATH)
         elif MapCellType == ThisMap.MAP_RASPBERRY:
            self.SoundRaspberry.play()
            self.Score += self.SCORE_RASPBERRY
            ThisMap.SetMapCellType(self.ThisLocation, ThisMap.MAP_PATH)
            self.HyperCount = self.HYPER_COUNT


#/**************************************************************************/
#/* If sprite is currently alive, check for collisions with other sprites. */
#/**************************************************************************/
   def CheckCollide(self, CheckLocation):
      if self.Lives > 0 and self.DieCount == 0:
         return GameSprite.GameSprite.CheckCollide(self, CheckLocation)
      else:
         return False


#/*******************************************/
#/* Allow other parts of the application to */
#/* see the current state of hyper mode.    */
#/*******************************************/
   def GetHyperCount(self):
      return self.HyperCount


#/**********************************************************/
#/* Remove a life from this sprite unless no lives remain. */
#/**********************************************************/
   def Die(self):
      if self.Lives > 0:
         self.SoundSplat.play()
         self.Lives -= 1
         self.DieCount = self.DIE_COUNT
         self.SetImageIndex(self.IMG_PIMAN_SPLAT)

