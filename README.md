Hello CS 4341 A22!

Below is information about using the Referee we are providing for project 2.
_________________________________________________________________________________

# Dependencies and Python Version

This is the referee program for the Ultimate Tic Tac Toe (UTTT) AI for Project 2. 
The details of how your programs need to communicate with the referee are on Canvas.

The referee has two dependencies, `numpy` and `pygame`. Please install these with 
`pip install numpy` and `python3 -m pip install -U pygame --user`. 
If there are issues with installing, please refer to
the official documentation for the libraries.

I can guarantee this program will work for Python 3.9 and up. 
Please check that are you using a valid version of python.
You can check your version with `python --version` and/or `python3 --version`.
You may need to use `python` or `python3` or even `python3.9` 
to properly run the program depending on how your system handled Python and if you are using an IDE.
I will use `python` in the README for simplicity.

___________________________________________________________________

# Running the Referee and Playing the Game

Once python and dependencies are sorted, you can run the referee with 

`python referee.py <Player 1 name> <Player 2 name> --time_limit <time limit>`

The Player 1 and 2 names are *single word names* for each of the agents.
`--time_limit` is an optional argument that allows you to specify the time limit to play (in seconds).
It defaults to 10 seconds. We will use 10 seconds in the competition. 
This argument option is provide to allow easier debugging.

The referee will create the files that it maintains in the same directory that the referee.py file is in.

If you would like to just play the game, run

`python game.py <Player 1 name> <Player 2 name>`

and then you can play using the UI.

You should not need to modify any of the code provided to you. 
You are to write your owm program that can communicate with this referee.

_________________________________________________________________________

# Bugs

Honestly, I fully expect there to be bugs in this code. If you for any reason suspect that 
the referee is not behaving as described in the assignment on Canvas, please let us know in
the `project-2-referee-bugs` channel in Slack. 

## UPDATE TO V2 09/15/2022

The first version of the referee did not produce a *end_game* file like it should.
This version fixes that issue and updates the output messages to match the ones in Canvas.

## UPDATE TO V3 09/20/2022

The previous version of the referee did not filter out invalid initial moves.
This version fixes that issue so the same move cannot be made twice.

## UPDATE TO V4 09/28/2022

The previous version of the referee used 'X' and 'O' in the first four moves
file to indicate player moves; this is confusing because who is 'X' and who is
'O' is randomly chosen and is
not communicated to the players directly. To make communication easier for the
players, the referee now uses the player names in the first_four_moves file.

## UPDATE TO V5 09/30/2022

The clean() function seems to not work well on the previous versions of the referee. 
This update fixes the clean function and modifies the referee to clean up its files when the game is over.

## UPDATE TO V6 09/30/2022

The clean() function has been update _again_ to be cross-platform and work on different python versions.
The default screen size is smaller.
The referee now handles incorrectly formatted moves more gracefully.

## UPDATE TO V7 09/30/2022

The referee now creates both .go files at the end of the game, as described in canvas.

_________________________________________________________________________

That is all! Have fun playing UTTT and finding fun ways to break my code...

Will Babincsak
