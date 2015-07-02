# Copyright James Flanagan 2014.
# Provided under the MIT license (see the LICENSE file).

# TODO: add some more comments!

# Now modified to work in jython (java interpeter)
# Sound has been modified - from a sound file to notes mapped from the bits themselves using a music composition library.

# the jythonMusic library is used in this program.
# to run this program, the Java Development Kit, the jythonMusic library and possibly the JEM2 IDE are required.
# the notes here are not a sample on a loop, but are instead calculated using the positions of the bits themselves.
# (only ever 1000th bit is used, as the program is too fast for the notes to otherwise be distinguishable)
# get the jythonMusic library and JEM2 at http://www.cs.cofc.edu/~manaris/jythonmusic/?page_id=23. , and the JDK at http://www.oracle.com/technetwork/java/javase/downloads/index.html

#how to run in java through terminal : http://www.cs.cofc.edu/~manaris/jythonmusic/?page_id=463


#import required modules

from random import randint, randrange  #some random elements are used in this program.
from music import *                    #the jythonMusic library required for music composition.
import console_size                    # console_size is used to find out the size of the window the program is running in.

# Get the size of the console.
if console_size.getCurrentOS() == "Java":
   #currently i cannot find a way to find the CONSOLE_WIDTH in java. Therefore, I have hard-coded the full screen width for macbook pro.
   #(if this is not your terminal width, feel free to change this constant so that it works with your platform.)
         
   CONSOLE_WIDTH = 181
else:
   #in python, the console size can be determined using the console_size module.
   (CONSOLE_WIDTH, CONSOLE_HEIGHT) = console_size.getTerminalSize()

# CONFIGURATION FOR MAPPING NOTES FOR SOUND EFFECT#
# =========================================== #   
BitsPerNote = 1000                                  #constant to control rate of note generation
INSTRUMENT = XYLOPHONE                              #instrument to play notes
SCALE = CHROMATIC_SCALE                             #scale to filter notes to
KEY = C4                                            #key of notes
DURATION = TN/50                                    #duration of each note (TN = thirtysecond note)

def playNote(value, minValue, maxValue, bit):
   """plays a note based on the position of the current bit"""

   #set instrument for channel 0 (the channel we will be using) to INSTRUMENT constant
   Play.setInstrument(INSTRUMENT,0)

   #set the pitch by mapping the range of the terminal window width onto the musical range C3 to C7
   #(the notes are filtered to the constant SCALE, and the key is set to KEY)
   pitch = mapScale(value, minValue, maxValue, C3, C7, SCALE, KEY)

   #base dynamics on whether the bit is a 0 or a 1
   if bit:
      dynamic = randint(65,120)
   else:
      dynamic = randint(10,65)

   #map panning (0 to 127- 0 is left speaker, 127 is right speaker) based on position of bit on terminal width
   pan = mapValue(value, minValue, maxValue, 0, 127)
   #add panning to channel 0 (channel being used)
   Play.setPanning(pan,0)

   #play the note (pitch of note = pitch, play after 0ms, duration = DURATION constant, volume = dynamic, channel =  0)
   Play.note(pitch, 0, DURATION, dynamic, 0)

   
# CONFIGURATION FOR ANIMATION #
# =========================== #

MAX_LENGTH = 10

MAX_CHANGE_EACH_TIME = int(CONSOLE_WIDTH / 5)

#    END OF CONFIGURATION     #
#    --------------------     #


# Used to generate a random bit to display on the screen in the animation.
randbit = lambda: randint(0, 1)
   

      
def generateLines():
    """Generate a random set of column numbers of random length, each of which respresents a line going down the screen. This can be used to create a list of lines to remove from, or add to the screen."""
    lines = set()

    # Generate the number of lines to be chosen, which must be between 1 and MAX_CHANGE_EACH_TIME.
    numToChange = randint(1, MAX_CHANGE_EACH_TIME)

    # Generate the column numbers for the lines.
    for i in range(numToChange):
        lines.add(randrange(CONSOLE_WIDTH))

    return lines


def displayAnimation():
    """Displays the actual animation."""

    lines = set()
    #count bits to stagger note output
    count = 0
    # Loop forever.
    while True:

        #keep the number of lines inside the max change each time.
        if len(lines) > 0 + MAX_CHANGE_EACH_TIME:
            lines -= generateLines()

        if len(lines) < CONSOLE_WIDTH - MAX_CHANGE_EACH_TIME:
            lines |= generateLines()

        linesList = list(lines)

        linesList.sort()

        row = ""           #var to store this row of bits
        for i in range(len(linesList)):
            #increase count
            count += 1

            #find linesList element at this index
            #(currently enumerate is not working for me in jython)
            l = linesList[i]

            #number of spaces to add is the position of the current bit minus the position of the bit before it.
             
            if i == 0:
                numSpacesToAdd = l-1
            else:
                # Have to -1 since one of the columns will have already been used up
                # by the previous line.
                numSpacesToAdd = l - linesList[i-1] - 1

            #add some random bit
            bit = randbit()

            #every 1000th bit, play a note associating with that bit's position on the screen width
            if count >= BitsPerNote:
               playNote(l, 0, CONSOLE_WIDTH, bit)
               #reset count
               count = 0
               
            row += " " * numSpacesToAdd + str(bit)        #add bit to row

        #output this row
        print row



# Begin your hacking adventure!
displayAnimation()
