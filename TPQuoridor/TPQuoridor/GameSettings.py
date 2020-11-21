import pyglet
import pyglet.image as pyi
import os


SIZE = 600
BOARD_SIZE=10
NUMPLAYERS=3

imgBoard = pyi.load('Media/BoardHQ.png')
imgSlot = pyi.load('Media/SlotHQ.png')

BOARD_BORDER = int(SIZE/15)
BACKGROUND_SCALE = SIZE/imgBoard.width
SLOT_SCALE = BACKGROUND_SCALE*(9/BOARD_SIZE)
JUMP = imgSlot.width*SLOT_SCALE
