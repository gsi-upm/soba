from mesa.visualization.ModularVisualization import ModularServer
from mesa.batchrunner import BatchRunner
from model.model import SOBAModel
import datetime as dt

seed = 1000

voting_methods = ['borda_voting', 'pairwise_comparisons_voting',
				  'approval_voting', 'plurality_voting', 
				  'single_transferable_vote', 'range_voting',
				  'exchange_of_weight_voting', 'cumulative_voting'
]

parameters = {"width": 22,
              "height": 22,
              "seed": seed,
              'modelWay': 2
              }


batch = BatchRunner(SOBAModel,
                        fixed_parameters = parameters,
                        #variable_parameters = {"modelWay": range(0, 3)},
                        variable_parameters = {"voting_method": voting_methods},
                        iterations= 1,
                        max_steps = 1000000)


batch.run_all()