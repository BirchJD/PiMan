#!/usr/bin/python2

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
import time
import pygame
import Map
import GameSprite
import PiManSprite
import WormSprite


#/***********************************/
#/* Kill the player's current life. */
#/***********************************/
def Die():
   PiMan.Die()
   Worm1.Reset()
   Worm2.Reset()
   Worm3.Reset()
   Worm4.Reset()


#/*********************/
#/* Start a new game. */
#/*********************/
def Reset(HiScore):
   if PiMan.GetScore() > HiScore:
      HiScore = PiMan.GetScore()
   pygame.time.set_timer(EVENT_TIMER, 0)
   Die()
   ThisMap.Reset()
   PiMan.Reset()
   Worm1.Reset()
   Worm2.Reset()
   Worm3.Reset()
   Worm4.Reset()
   pygame.time.set_timer(EVENT_TIMER, 50)
   return HiScore


#/*************************/
#/* Start the next level. */
#/*************************/
def NextLevel():
   pygame.time.set_timer(EVENT_TIMER, 0)
   Worm1.Reset()
   Worm2.Reset()
   Worm3.Reset()
   Worm4.Reset()
   PiMan.SetLocation(9 * MapCellSize.width, 7 * MapCellSize.height)
   ThisMap.NextLevel()
   pygame.time.set_timer(EVENT_TIMER, 50)


#  /*********************/
# /* Define constants. */
#/*********************/
EVENT_TIMER = pygame.USEREVENT + 1

#  /*********************************************************/
# /* Generate a unique set of random numbers for this run. */
#/*********************************************************/
random.seed(time.gmtime())

#  /***************************************/
# /* Initialize application and display. */
#/***************************************/
pygame.init()
pygame.mixer.init()
pygame.font.init()
ThisSurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
ThisVideoInfo = pygame.display.Info()
pygame.mouse.set_visible(False)
SmallFont = pygame.font.Font(None, 25)
LargeFont = pygame.font.Font(None, 100)

#  /********************************************/
# /* Create a surface to use as a background. */
#/********************************************/
Background = ThisSurface.copy()

#  /************************/
# /* Create text objects. */
#/************************/
TextScore = SmallFont.render("SCORE:", True, (0xFF, 0xFF, 0xFF))
TextHiScore = SmallFont.render("HI SCORE:", True, (0xFF, 0xFF, 0xFF))
TextGameOver = LargeFont.render("GAME OVER", True, (0x00, 0x00, 0x00))
TextReady = LargeFont.render("READY!", True, (0x00, 0x00, 0x00))

#  /******************/
# /* Display READY! */
#/******************/
ThisSurface.fill((0xFF, 0xFF, 0x00))
ThisSurface.blit(TextReady, (180, 175))
pygame.display.flip()

#  /*******************************/
# /* Create application objects. */
#/*******************************/
ThisMap = Map.Map(Background)
MapCellSize = ThisMap.GetMapCellSize()

Sprites = []
PiMan = PiManSprite.PiManSprite("PiMan", 9 * MapCellSize.width, 7 * MapCellSize.height)
Sprites.append(PiMan)

Worm1 = WormSprite.WormSprite("Worm", 7 * MapCellSize.width, 6 * MapCellSize.height)
Sprites.append(Worm1)

Worm2 = WormSprite.WormSprite("Worm", 8 * MapCellSize.width, 6 * MapCellSize.height)
Sprites.append(Worm2)

Worm3 = WormSprite.WormSprite("Worm", 10 * MapCellSize.width, 6 * MapCellSize.height)
Sprites.append(Worm3)

Worm4 = WormSprite.WormSprite("Worm", 11 * MapCellSize.width, 6 * MapCellSize.height)
Sprites.append(Worm4)

#  /******************************/
# /* Do application event loop. */
#/******************************/
pygame.time.set_timer(EVENT_TIMER, 50)
HiScore = 0
ExitFlag = False
while ExitFlag == False:
#  /*************************************/
# /* Yeald for other processes to run. */
#/*************************************/
   pygame.time.wait(25)

#  /************************************/
# /* Process application event queue. */
#/************************************/
   for ThisEvent in pygame.event.get():
#  /******************************************************************/
# /* If ptyhon has posted a QUIT message, flag to exit applicaiton. */
#/******************************************************************/
      if ThisEvent.type == pygame.QUIT:
         ExitFlag = True

#  /*********************************************************/
# /* On timer period perform one frame of the application. */
#/*********************************************************/
      elif ThisEvent.type == EVENT_TIMER:
#  /******************************************************/
# /* Check if level is complete, and start a new level. */
#/******************************************************/
         if ThisMap.LevelEndCheck():
            NextLevel()

#  /****************************************************************/
# /* Check for ESC key press, and exit application when detected. */
#/****************************************************************/
         KeysPressed = pygame.key.get_pressed()
         if KeysPressed[pygame.K_ESCAPE]:
            ExitFlag = True

#  /***********************************************************************/
# /* When raspberry found, put worms in hyper mode for the hyper period. */
#/***********************************************************************/
         HyperCount = PiMan.GetHyperCount()
         if HyperCount == PiMan.HYPER_COUNT:
            Worm1.SetHyperFlag(True)
            Worm2.SetHyperFlag(True)
            Worm3.SetHyperFlag(True)
            Worm4.SetHyperFlag(True)
         elif HyperCount == 1:
            Worm1.SetHyperFlag(False)
            Worm2.SetHyperFlag(False)
            Worm3.SetHyperFlag(False)
            Worm4.SetHyperFlag(False)

#  /*********************************/
# /* Check for sprite collissions. */
#/*********************************/
         if (PiMan.CheckCollide(Worm1.GetLocation())):
            if Worm1.GetHyperFlag():
               Worm1.Reset()
               PiMan.AddScore(PiMan.SCORE_HYPER)
            else:
               Die()
         if (PiMan.CheckCollide(Worm2.GetLocation())):
            if Worm2.GetHyperFlag():
               Worm2.Reset()
               PiMan.AddScore(PiMan.SCORE_HYPER)
            else:
               Die()
         if (PiMan.CheckCollide(Worm3.GetLocation())):
            if Worm3.GetHyperFlag():
               Worm3.Reset()
               PiMan.AddScore(PiMan.SCORE_HYPER)
            else:
               Die()
         if (PiMan.CheckCollide(Worm4.GetLocation())):
            if Worm4.GetHyperFlag():
               Worm4.Reset()
               PiMan.AddScore(PiMan.SCORE_HYPER)
            else:
               Die()

#  /********************/
# /* Draw background. */
#/********************/
         ThisSurface.blit(Background, (0, 0))

#  /*****************************/
# /* Control and draw sprites. */
#/*****************************/
         for Sprite in Sprites:
            Sprite.Move(KeysPressed, ThisMap)
            Sprite.Draw(ThisSurface)

#  /*****************************/
# /* Draw additional graphics. */
#/*****************************/
         ThisSurface.blit(TextScore, (50, 8))
         Text = SmallFont.render(str(PiMan.GetScore()), True, (0xFF, 0xFF, 0xFF))
         ThisSurface.blit(Text, (120, 8))

         ThisSurface.blit(TextHiScore, (230, 8))
         Text = SmallFont.render(str(HiScore), True, (0xFF, 0xFF, 0xFF))
         ThisSurface.blit(Text, (320, 8))

#  /**************************************************************************/
# /* If game ended, display Game Over and check for new game start request. */
#/**************************************************************************/
         if PiMan.DrawLives(ThisSurface, 450, 0) == 0:
            ThisSurface.blit(TextGameOver, (95, 175))

#  /**********************************************************/
# /* Display READY! and start a new game when 1 is pressed. */
#/**********************************************************/
            if KeysPressed[pygame.K_1]:
               ThisSurface.fill((0xFF, 0xFF, 0x00))
               ThisSurface.blit(TextReady, (180, 175))
               pygame.display.flip()
               HiScore = Reset(HiScore)

#  /*******************/
# /* Update display. */
#/*******************/
         pygame.display.flip()


#  /*********************************/
# /* Application clean up and end. */
#/*********************************/
pygame.time.set_timer(EVENT_TIMER, 0)
pygame.mouse.set_visible(True)

