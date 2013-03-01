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


#/*******************************************************************/
#/* Generic game sprite features, game sprites subclass this class. */
#/*******************************************************************/
class GameSprite(pygame.sprite.Sprite):
#  /***************************/
# /* Global class constants. */
#/***************************/
   ANIMATE_COUNT = 2
   DIRECTION_BLOCKED = -1
   DIRECTION_NONE = 0
   DIRECTION_LEFT = 1
   DIRECTION_RIGHT = 2
   DIRECTION_UP = 3
   DIRECTION_DOWN = 4


#/**********************/
#/* Class constructor. */
#/**********************/
   def __init__(self, ImageFile, X, Y):
#  /***************************/
# /* Class member variables. */
#/***************************/
      self.ThisResetLocation = pygame.Rect(X, Y, 0, 0)
      self.ThisLocation = pygame.Rect(X, Y, 0, 0)
      self.ThisImage = []
      self.ThisImageIndex = 0
      self.XSpeed = 0
      self.YSpeed = 0
      self.AnimateCount = 0
      self.CurrentAnimateFrame = 0

#  /************************************************************/
# /* Load sprite images until next image file does not exist. */
#/************************************************************/
      try:
         Count = 0
         while True:
            Filename = "Images/{0}{1}.gif".format(ImageFile, Count)
            self.ThisImage.append(pygame.image.load(Filename))
            Count += 1
      finally:
#  /*********************************************************/
# /* Use the first sprite image as the size of the sprite. */
#/*********************************************************/
         self.ThisLocation.height = self.ThisImage[0].get_height()
         self.ThisLocation.width = self.ThisImage[0].get_width()
         return


#/************************/
#/* Reset sprite object. */
#/************************/
   def Reset(self):
      self.ThisLocation.x = self.ThisResetLocation.x
      self.ThisLocation.y = self.ThisResetLocation.y


#/***********************/
#/* Draw sprite object. */
#/***********************/
   def Draw(self, ThisSurface):
      ThisSurface.blit(self.ThisImage[self.ThisImageIndex], self.ThisLocation)


#/********************************************/
#/* Animate one frame for the sprite object. */
#/********************************************/
   def Move(self, KeysPressed, ThisMap):
      Direction = self.DIRECTION_NONE
      CellSize = ThisMap.GetMapCellSize().width
      OldX = self.ThisLocation.x
      OldY = self.ThisLocation.y

#  /****************/
# /* Move sprite. */
#/****************/
      self.ThisLocation.x += self.XSpeed
      self.ThisLocation.y += self.YSpeed

#   /*************************************************************************/
#  /* If sprite exists left of display, make sprite enter right of display. */
# /* And vice versa.                                                       */
#/*************************************************************************/
      if self.ThisLocation.x < 0:
         self.SetLocation(CellSize * ThisMap.WIDTH - CellSize * 0.25, self.ThisLocation.y)
      elif self.ThisLocation.x > CellSize * ThisMap.WIDTH - CellSize * 0.25:
         self.SetLocation(0, self.ThisLocation.y)

#   /******************************************/
#  /* Change direction when keys pressed.    */
# /* And sprite is aligned with a map cell. */
#/******************************************/
      if self.ThisLocation.x % CellSize == 0 and self.ThisLocation.y % CellSize == 0:
         if KeysPressed[pygame.K_UP]:
            TestLocation = pygame.Rect(self.ThisLocation.x, self.ThisLocation.y - CellSize, 0, 0)
            MapCellType = ThisMap.GetMapCellType(TestLocation)
            if MapCellType not in self.InvalidCells:
               Direction = self.DIRECTION_UP
         elif KeysPressed[pygame.K_DOWN]:
            TestLocation = pygame.Rect(self.ThisLocation.x, self.ThisLocation.y + CellSize, 0, 0)
            MapCellType = ThisMap.GetMapCellType(TestLocation)
            if MapCellType not in self.InvalidCells:
               Direction = self.DIRECTION_DOWN
         elif KeysPressed[pygame.K_LEFT]:
            TestLocation = pygame.Rect(self.ThisLocation.x - CellSize, self.ThisLocation.y, 0, 0)
            MapCellType = ThisMap.GetMapCellType(TestLocation)
            if MapCellType not in self.InvalidCells:
               Direction = self.DIRECTION_LEFT
         elif KeysPressed[pygame.K_RIGHT]:
            TestLocation = pygame.Rect(self.ThisLocation.x + CellSize, self.ThisLocation.y, 0, 0)
            MapCellType = ThisMap.GetMapCellType(TestLocation)
            if MapCellType not in self.InvalidCells:
               Direction = self.DIRECTION_RIGHT

#  /*****************************************/
# /* If moved into wall, go back and stop. */
#/*****************************************/
      MapCellType = ThisMap.GetMapCellType(self.ThisLocation)
      if MapCellType in self.InvalidCells:
         Direction = self.DIRECTION_BLOCKED
         self.SetSpeed(0, 0)
         self.SetLocation(OldX, OldY)

      return Direction


#/***************************************************/
#/* Check for sprite colliding with another sprite. */
#/***************************************************/
   def CheckCollide(self, CheckLocation):
      return self.ThisLocation.colliderect(CheckLocation)


#/**************************************************************************/
#/* Allow other parts of the application to find the current sprite image. */
#/**************************************************************************/
   def GetImageIndex(self):
      return self.ThisImageIndex


#/*************************************************************************/
#/* Allow other parts of the application to set the current sprite image. */
#/*************************************************************************/
   def SetImageIndex(self, NewImageIndex):
      self.ThisImageIndex = NewImageIndex


#/****************************************************************************/
#/* Allow other parts of the application to set the current sprite location. */
#/****************************************************************************/
   def SetLocation(self, X, Y):
      self.ThisLocation.x = X
      self.ThisLocation.y = Y


#/****************************************************************************/
#/* Allow other parts of the application to set the current sprite velocity. */
#/****************************************************************************/
   def SetSpeed(self, NewXSpeed, NewYSpeed):
      self.XSpeed = NewXSpeed
      self.YSpeed = NewYSpeed


#/****************************************************************************/
#/* Allow other parts of the application to get the current sprite location. */
#/****************************************************************************/
   def GetLocation(self):
      return self.ThisLocation


#/*************************************************************************/
#/* Allow other parts of the application to get the current sprite score. */
#/*************************************************************************/
   def GetScore(self):
      return self.Score


#/***************************************************************************/
#/* Allow other parts of the application to reset the current sprite score. */
#/***************************************************************************/
   def ClearScore(self):
      self.Score = 0


#/****************************************************************************/
#/* Allow other parts of the application to add to the current sprite score. */
#/****************************************************************************/
   def AddScore(self, Value):
      self.Score += Value

