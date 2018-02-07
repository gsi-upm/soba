from soba.visualization.server import ModularServer
import pandas as pd
from tqdm import tqdm
import collections
import copy
from itertools import product, count
import pandas as pd

"""
In the file bacth.py is implemented the execution in background way:
	Methods: 
		-run: The method that is invoked to execute the simulation as batch way.

"""

class BatchRunner:
	def __init__(self, model_cls, variable_parameters=None, fixed_parameters=None, iterations=1, display_progress=True, ramen=False):
		self.model_cls = model_cls
		self.variable_parameters = self._process_parameters(variable_parameters)
		self.fixed_parameters = fixed_parameters or {}
		self.iterations = iterations
		self.ramen = ramen
		self.display_progress = display_progress

	def run_all(self):
		param_names, param_ranges = zip(*self.variable_parameters.items())
		run_count = count()
		total_iterations = self.iterations
		for param_range in param_ranges:
			total_iterations *= len(param_range)
		with tqdm(total_iterations, disable=not self.display_progress) as pbar:
			for param_values in product(*param_ranges):
				kwargs = dict(zip(param_names, param_values))
				kwargs.update(self.fixed_parameters)
				model = self.model_cls(**kwargs)

				for _ in range(self.iterations):
					self.run_model(model, self.ramen)
					pbar.update()

	def _process_parameters(self, params):
		params = copy.deepcopy(params)
		bad_names = []
		for name, values in params.items():
			if (isinstance(values, str) or
					not hasattr(values, "__iter__")):
				bad_names.append(name)
		if bad_names:
			raise VariableParameterError(bad_names)
		return params

	def run_model(self, model, ramen = False):
		ContinuousModel = ramen
		while model.running:
			model.step()

def run(model, paramsFixed, paramsVariable, iterations, ramen = False):
	"""
	Execute the simulation as batch way.
		Args:
			model: Model that is simulated.
			paramsFixed: Fixed parameters, invariable in different simulations.
			paramsVariable: Parameters that change between different simulations.
			iterations: Number of simulations that will be executed.
	"""
	batch = BatchRunner(model, paramsVariable, paramsFixed, iterations=1, ramen = ramen)
	batch.run_all()

class VariableParameterError(TypeError):
	MESSAGE = ('variable_parameters must map a name to a sequence of values. '
			'These parameters were given with non-sequence values: {}')

	def __init__(self, bad_names):
		self.bad_names = bad_names

	def __str__(self):
		return self.MESSAGE.format(self.bad_names)