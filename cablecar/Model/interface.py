"""
This is the interface the player uses to make their moves and communicate
with the engine.   Nothing in this file should be modified by you.

Author: Adam Oest (amo9149@rit.edu)
"""

class PlayerMove(object):
	"""
		The player uses this class to communicate information about their
		next move to the engine.  The engine uses this class internally
		to verify the player's move and update the board display.
    """
	__slots__ = ('playerId','position','tileName','rotation')
	
	def __init__(self, playerId, position, tileName, rotation):
		"""
		Initialize the object.
		
		playerId: the id for this player, 0-5
		position: tuple (row,column)
		tileName: a-i
		rotation: 0-3
		tileId: used by the engine only (when playing back from history)
		"""
		
		self.playerId = playerId
		self.position = position
		self.tileName = tileName
		self.rotation = rotation

	def __str__(self):
		"""Return a string representation of this object"""
	
		return "PlayerMove:\n\tplayerId: %s\n\tposition: %s\n\ttileName: %s\n\trotation: %s" \
				% (self.playerId, self.position, self.tileName, self.rotation)
	