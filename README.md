# Gess Board Game

This program contains a class named GessGame for playing an abstract board game called Gess. This link has the rules: https://www.chessvariants.com/crossover.dir/gess.html.  Note that when a piece's move causes it to overlap stones, any stones covered by the **footprint** get removed, not just those covered by one of the piece's stones.  It is not legal to make a move that leaves you without a ring.  It's possible for a player to have more than one ring.  A player doesn't lose until they have no remaining rings.

Locations on the board will be specified using columns labeled a-t and rows labeled 1-20, with row 1 being the Black side and row 20 the White side.  The actual board is only columns b-s and rows 2-19.  The center of the piece being moved must stay within those boundaries.  An edge of the piece may go into columns a or t, or rows 1 or 20, but any pieces there are removed at the end of the move.  Black goes first.

GessGame class must includes the following:
* An init method that initializes any data members.
* A method called get_game_state that takes no parameters and returns 'UNFINISHED', 'BLACK_WON' or 'WHITE_WON'.
* A method called resign_game that lets the current player concede the game, giving the other player the win.
* A method called make_move that takes two parameters - strings that represent the center square of the piece being moved and the desired new location of the center square.  For example, make_move('b6', 'e9').  If the indicated move is not legal for the current player, or if the game has already been won, then it should just return False.  Otherwise it should make the indicated move, remove any captured stones, update the game state if necessary, update whose turn it is, and return True.


Here's a very simple example of how the class could be used:
```
game = GessGame()
move_result = game.make_move('m3', 'm6')
game.make_move('e14', 'g14')
state = game.get_game_state()
game.resign_game()
```
