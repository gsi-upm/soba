from soba.agents.avatar import Avatar

class EmergencyAvatar(Avatar):

	def __init__(self, unique_id, model, initial_pos, color = 'red', initial_state='walking'):
		super().__init__(unique_id, model, initial_pos, color, initial_state)

		self.alive = True
		self.life = 3

	def getExitGate(self):
		if True:
			if self.exitGateStrategy == 'uncrowded':
				self.pos_to_go = self.model.getNearestGate(self)
				self.model.uncrowdedStr.append(self)
			elif self.exitGateStrategy == 'safest':
				self.pos_to_go = self.model.getSafestGate(self)
			elif self.exitGateStrategy == 'nearest':
				self.pos_to_go = self.model.getNearestGate(self)
			elif self.exitGateStrategy == 'lessassigned':
				self.pos_to_go = self.model.getLessAssignedGate()
			else:
				self.pos_to_go = self.model.getNearestGate(self)
		else:
			self.pos_to_go = self.model.getNearestGate(self)
		pathReturn = super().getWay()
		return pathReturn

	def getPosFireFOV():
		others = []
		for pos in self.fov:
			if pos in self.model.FireControl.fireExpansion:
				others.append(pos)
		return others