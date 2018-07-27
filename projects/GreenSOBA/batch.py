from mesa.visualization.ModularVisualization import ModularServer
from mesa.batchrunner import BatchRunner
from model.model import SOBAModel
import datetime as dt

seed = 1000

parameters = {"width": 22,
              "height": 22,
              "seed": seed
              }


batch = BatchRunner(SOBAModel,
                        fixed_parameters = parameters,
                        variable_parameters = {"nothing": range(0, 1)},
                        iterations= 1,
                        max_steps = 1000000)


batch.run_all()