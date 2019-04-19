from unittest import TestCase
import unittest
from pyunitreport import HTMLTestRunner
import json
from copy import deepcopy
import itertools


#### Social Choice Class ####


class SocialChoice:

	def __init__(self):

		self.step = 0
		self.voting_history = []
		self.step_record = {
			'votes':{},
			'satisfaction':{},
			'voting_result':{}
		}
		self.negotiation_weights = {}

	def save_results(self, services, voting_result, satisfaction):

		self.step_record['votes'] = services
		self.step_record['voting_result'] = voting_result
		self.step_record['satisfaction'] = satisfaction


	def increase_step(self):

		self.voting_history.append(self.step_record)
		self.step += 1


	def restart_steps(self):
		
		self.voting_history = []
		self.step = 0

	def voting_method(self, preferences, voting_method):
		method = getattr(self, voting_method)
		result = method(preferences)
		return result

	# Voting Operation Methods #


	def sum_preferences_votes(self, preferences):

		summed_preferences = {}
		for user, configurations in deepcopy(preferences).items():
			if not summed_preferences:
				summed_preferences = configurations
				continue
			for configuration, value in configurations.items():
				summed_preferences[configuration] += value
		return summed_preferences


	def sort_configurations(self, configurations):

		sorted_configurations_with_values = sorted(configurations.items(), key=lambda kv: kv[1], reverse=True)
		sorted_configurations = []
		for configuration in sorted_configurations_with_values:
			sorted_configurations.append(configuration[0])
		return sorted_configurations



	def sum_configuration_votes(self, configurations):

		summed_configurations = 0
		for configuration, value in deepcopy(configurations).items():
			summed_configurations += value
		return summed_configurations


	def count_number_keys(self, dictionary):

		number_keys = len(dictionary.keys())
		return number_keys


	def obtain_maximum_value(self, dictionary):

		maximum_key = False
		maximum_value = -1000
		for key, value in dictionary.items():
			if value > maximum_value:
				maximum_value = value
				maximum_key = key
		return maximum_key


	def compare_values_two_keys(self, dictionary, key1, key2):

		key = key1 if dictionary[key1] > dictionary[key2] else key2
		return key

	def get_threshold(self, preferences, threshold):

		return (threshold * len(preferences.keys()))/100

	def remove_option(self, preferences, option):
		new_preferences = deepcopy(preferences)
		for user, configuration in new_preferences.items():
			del new_preferences[user][option]
		return new_preferences

	def transfer_vote(self, preferences, vote):

		new_preferences = deepcopy(preferences)
		for user, configuration in preferences.items():
			sort_configurations = self.sort_configurations(configuration)
			if len(sort_configurations) > sort_configurations.index(vote)+1:
				vote_to_increase = sort_configurations[sort_configurations.index(vote)+1]
				new_preferences[user][vote_to_increase] += new_preferences[user][vote]
			del new_preferences[user][vote]
		return new_preferences

	def filter_preferences_maximum_voting_value(self, preferences, maximum_voting_value = 10):

		filtered_preferences = deepcopy(preferences)
		for user, configurations in filtered_preferences.items():
			for configuration, value in configurations.items():
				if abs(value) > maximum_voting_value:
					if value > 0:
						filtered_preferences[user][configuration] = maximum_voting_value
					else:
						filtered_preferences[user][configuration] = - maximum_voting_value
		return filtered_preferences


	def filter_preferences_maximum_total_votes(self, preferences, maximum_total_votes = 20):

		filtered_preferences = deepcopy(preferences)
		for user, configurations in deepcopy(preferences).items():
			summed_votes = 0
			for configuration, value in configurations.items():
				if summed_votes > 20:
					filtered_preferences[user][configuration] = 0
					continue
				summed_votes += abs(value)
				if summed_votes > maximum_total_votes:
					if value > 0:
						filtered_preferences[user][configuration] = maximum_total_votes - (summed_votes - abs(value))
					else:
						filtered_preferences[user][configuration] = -(maximum_total_votes - (summed_votes - abs(value)))
		return filtered_preferences


	def eval_user_is_winner(self, user, service, step = False):

		step = step if step else (self.step-1)
		winning_configuration = self.voting_history[step]['voting_result'][service]
		user_votes = self.voting_history[step]['votes'][service][user]
		result = self.obtain_maximum_value(user_votes) == winning_configuration[0]
		return result


	# Voting Weighting Methods #


	def greater_preferences(self, preferences):

		weighted_preferences = deepcopy(preferences)
		for user, configurations in deepcopy(preferences).items():
			greater_preference_name = False
			greater_preference_value = -1000
			for configuration, value in configurations.items():
				if value > greater_preference_value:
					greater_preference_value = value
					greater_preference_name = configuration
				weighted_preferences[user][configuration] = 0
			weighted_preferences[user][greater_preference_name] = 1
		return weighted_preferences


	def greater_preferences_multiple(self, preferences):

		weighted_preferences = deepcopy(preferences)
		for user, configurations in deepcopy(preferences).items():
			greater_preference_value = -1000
			for configuration, value in configurations.items():
				if value > greater_preference_value:
					greater_preference_value = value
			greater_preference_names = []
			for configuration, value in configurations.items():
				if value == greater_preference_value:
					greater_preference_value = value
					greater_preference_names.append(configuration)
				weighted_preferences[user][configuration] = 0
			number_of_configurations = len(greater_preference_names)
			for configuration in greater_preference_names:
				weighted_preferences[user][configuration] = 1/number_of_configurations
		return weighted_preferences


	def binary_preferences(self, preferences):

		binary_preferences = deepcopy(preferences)
		for user, configurations in deepcopy(preferences).items():
			for configuration, value in configurations.items():
				if value:
					binary_preferences[user][configuration] = 1
		return binary_preferences


	def descending_preferences(self, preferences):

		descending_preferences = deepcopy(preferences)
		for user, configurations in deepcopy(preferences).items():
			sorted_configurations = self.sort_configurations(configurations)
			n = len(sorted_configurations) - 1
			for configuration in sorted_configurations:
				descending_preferences[user][configuration] = n
				n -= 1
		return descending_preferences


	def normalized_preferences(self, preferences):

		normalized_preferences = deepcopy(preferences)
		for user, configurations in deepcopy(preferences).items():
			summed_configuration_values = self.sum_configuration_votes(configurations)
			for configuration, value in configurations.items():
				normalized_preferences[user][configuration] = value/summed_configuration_values
		return normalized_preferences


	def match_pair_configuration_values(self, preferences):
		services = list(next(iter(deepcopy(preferences).values())))
		combinations = list(itertools.combinations(services, 2))
		matched_pairs_configuration = dict.fromkeys(next(iter(deepcopy(preferences).values())), 0)
		for pair in combinations:
			k1, k2 = pair
			for user, configurations in preferences.items():
				winner_key = self.compare_values_two_keys(configurations, k1, k2)
				matched_pairs_configuration[winner_key] += 1
		return matched_pairs_configuration



	def get_negotiation_weights(self, preferences, winner_configuration):
		
		negotiation_weights_favorite = 0
		negotiation_weights_reminder = 0
		for user, configurations in preferences.items():
			weight = self.negotiation_weights.get(user) if self.negotiation_weights.get(user) else 0
			if self.obtain_maximum_value(configurations) == winner_configuration:
				negotiation_weights_favorite += weight
			else:
				negotiation_weights_reminder += weight
		return (negotiation_weights_favorite, negotiation_weights_reminder)



	def update_negotiation_weights(self, preferences, winner_configuration, value):

		control_value = value
		for user, configurations in preferences.items():
			if control_value > 0:
				control_value -= 1
				if self.obtain_maximum_value(configurations) == winner_configuration:
					self.negotiation_weights[user] = self.negotiation_weights[user] - 1 if self.negotiation_weights.get(user) else -1
				else:
					self.negotiation_weights[user] = self.negotiation_weights[user] + 1 if self.negotiation_weights.get(user) else 1



	def count_losers(self, preferences, winner_configuration):
		
		number_loser = 0
		for user, configurations in preferences.items():
			if not self.obtain_maximum_value(configurations) == winner_configuration:
				number_loser +=1
		return number_loser



	# Social Choice Methods #

	def borda_voting(self, preferences):

		descending_preferences = self.descending_preferences(preferences)
		summed_preferences_votes = self.sum_preferences_votes(descending_preferences)
		sort_configurations = self.sort_configurations(summed_preferences_votes)
		return sort_configurations


	def pairwise_comparisons_voting(self, preferences):

		descending_preferences = self.descending_preferences(preferences)
		matched_pairs_configuration = self.match_pair_configuration_values(descending_preferences)
		sort_configurations = self.sort_configurations(matched_pairs_configuration)
		return sort_configurations


	def plurality_voting_votes(self, preferences):

		greater_preferences = self.greater_preferences(preferences)
		summed_preferences_votes = self.sum_preferences_votes(greater_preferences)
		sort_configurations = self.sort_configurations(summed_preferences_votes)
		return (summed_preferences_votes, sort_configurations)


	def plurality_voting(self, preferences):

		summed_preferences_votes, sort_configurations = self.plurality_voting_votes(preferences)
		return sort_configurations


	def approval_voting(self, preferences):

		binary_preferences = self.binary_preferences(preferences)
		summed_preferences_votes = self.sum_preferences_votes(binary_preferences)
		sort_configurations = self.sort_configurations(summed_preferences_votes)
		return sort_configurations


	def single_transferable_vote(self, preferences, threshold = 50):

		new_preferences = self.greater_preferences(deepcopy(preferences))
		threshold = self.get_threshold(preferences, threshold)
		plurality_voting, sort_configurations = self.plurality_voting_votes(new_preferences)
		while threshold >= plurality_voting[sort_configurations[0]]:
			new_preferences = self.transfer_vote(new_preferences, sort_configurations[-1])
			plurality_voting, sort_configurations = self.plurality_voting_votes(new_preferences)
		return sort_configurations


	def range_voting_votes(self, preferences):

		summed_preferences_votes = self.sum_preferences_votes(preferences)
		sort_configurations = self.sort_configurations(summed_preferences_votes)
		return (summed_preferences_votes, sort_configurations)


	def range_voting(self, preferences):

		summed_preferences_votes, sort_configurations = self.range_voting_votes(preferences)
		return sort_configurations


	def exchange_of_weight_voting(self, preferences):

		summed_preferences_votes, sort_configurations = self.range_voting_votes(deepcopy(preferences))
		negotiation_weights_favorite, negotiation_weights_reminder = self.get_negotiation_weights(preferences, sort_configurations[0])
		if(negotiation_weights_reminder > negotiation_weights_favorite):
			new_preferences = self.remove_option(preferences, sort_configurations[0])
			summed_preferences_votes, sort_configurations = self.range_voting_votes(new_preferences)
		weight = self.count_losers(preferences, sort_configurations[0])
		self.update_negotiation_weights(preferences, sort_configurations[0], weight)
		return sort_configurations


	def cumulative_voting(self, preferences, maximum_votes = 15):

		filter_preferences_maximum_total_votes = self.filter_preferences_maximum_total_votes(preferences, maximum_votes)
		summed_preferences_votes = self.sum_preferences_votes(filter_preferences_maximum_total_votes)
		sort_configurations = self.sort_configurations(summed_preferences_votes)
		return sort_configurations



	# User Satisfaction Measurement Methods #


	def service_users_satisfaction(self, preferences, winner_configuration):

		service_users_satisfaction = {}
		for user, configurations in preferences.items():
			service_users_satisfaction[user] = configurations[winner_configuration]
		return service_users_satisfaction


	def total_service_satisfaction(self, service_users_satisfaction):

		total_service_satisfaction = 0
		for user, satisfaction in service_users_satisfaction.items():
			total_service_satisfaction += satisfaction
		return total_service_satisfaction


	def average_service_satisfaction(self, service_users_satisfaction):

		total_service_satisfaction = self.total_service_satisfaction(service_users_satisfaction)
		number_users = self.count_number_keys(service_users_satisfaction)
		average_service_satisfaction = total_service_satisfaction/number_users
		return average_service_satisfaction


	def normalized_service_satisfaction(self, service_users_satisfaction, maximum_voting_value = 10):

		average_service_satisfaction = self.average_service_satisfaction(service_users_satisfaction)
		normalized_service_satisfaction = average_service_satisfaction/maximum_voting_value
		return normalized_service_satisfaction

	'''
	def winning_configurations(self, services, methods):

		winning_configurations = {}
		for service_name, preferences in services.items():
			method = methods
			if isinstance(methods, dict):
				method = methods[service_name]
			func = getattr(self, method)
			sort_winning_configurations = func(preferences)
			winning_configurations[service_name] = sort_winning_configurations

		return winning_configurations


	def services_satisfaction_values(self, services, winning_configurations):

		services_satisfaction_values = {}
		for service_name, preferences in deepcopy(services).items():
			services_satisfaction_values[service_name] = {}

			service_users_satisfaction = self.service_users_satisfaction(preferences, winning_configurations[service_name][0])
			services_satisfaction_values[service_name]['service_users_satisfaction'] = service_users_satisfaction

			total_service_satisfaction = self.total_service_satisfaction(service_users_satisfaction)
			services_satisfaction_values[service_name]['total_service_satisfaction'] = total_service_satisfaction

			average_service_satisfaction = self.average_service_satisfaction(service_users_satisfaction)
			services_satisfaction_values[service_name]['average_service_satisfaction'] = average_service_satisfaction

			normalized_service_satisfaction = self.normalized_service_satisfaction(service_users_satisfaction)
			services_satisfaction_values[service_name]['normalized_service_satisfaction'] = normalized_service_satisfaction
		
		return services_satisfaction_values


	def global_services_satisfaction_values(self, services_satisfaction_values):
		
		global_services_satisfaction_values = {}
		global_total_satisfaction_value = 0
		global_average_satisfaction_value = 0

		for service_name, satisfaction_values in deepcopy(services_satisfaction_values).items():
			global_total_satisfaction_value += satisfaction_values["total_service_satisfaction"]
		
		global_services_satisfaction_values['global_total_satisfaction_value'] = global_total_satisfaction_value
		global_services_satisfaction_values['global_average_satisfaction_value'] = global_total_satisfaction_value/self.count_number_keys(services_satisfaction_values)

		return global_services_satisfaction_values


	def satisfaction_values(self, services, winning_configurations):

		services_satisfaction_values = self.services_satisfaction_values(services, winning_configurations)
		global_services_satisfaction_values = self.global_services_satisfaction_values(services_satisfaction_values)
		services_satisfaction_values['global'] = global_services_satisfaction_values

		return services_satisfaction_values

	def accumulated_services_satisfaction(self, first_step = 0, last_step = False):

		step = last_step if last_step else (self.step-1)
		accumulated_record = {}
		accumulated_record['global'] = {}
		voting_history = deepcopy(self.voting_history)
		number_steps = last_step - first_step

		for service, values in voting_history[first_step]:
			if service == 'global':
				accumulated_record[service] = {"accumulated_total_global_satisfaction_value": values["global_total_satisfaction_value"]}
				continue
			accumulated_record[service] = {"accumulated_total_service_satisfaction": values["total_service_satisfaction"]}
			accumulated_record[service] = {"accumulated_normalized_service_satisfaction": values["normalized_service_satisfaction"]}

		for step in range(first_step+1, last_step):
			for service, values in voting_history[step]:
				if service == 'global':
					accumulated_record[service] += service["global_total_satisfaction_value"]
					continue
				accumulated_record[service] += service["total_service_satisfaction"]

		for service, values in accumulated_record:
			if service == 'global':
				service["accumulated_global_average_satisfaction_value"] = service["accumulated_total_global_satisfaction_value"]/number_steps
				continue
			service["accumulated_average_service_satisfaction"] = service["accumulated_total_service_satisfaction"]/number_steps
			service["accumulated_average_normalized_service_satisfaction"] = service["accumulated_normalized_service_satisfaction"]/number_steps

		return accumulated_record


	def total_time_users_unsatisfied(self, first_step = 0, last_step = False):

		last_step = last_step if last_step else (self.step-1)
		total_time_users_unsatisfied = deepcopy(self.voting_history[first_step]['votes'])
		voting_history = deepcopy(self.voting_history)

		total_time_users_unsatisfied['global'] = total_time_users_unsatisfied[next(iter(total_time_users_unsatisfied))]

		for service, users in total_time_users_unsatisfied.items():
			for user, configuration in users.items():
				total_time_users_unsatisfied[service][user] = 0

		for step in range(first_step, last_step):
			for service, users in self.voting_history[step]['votes'].items():
				for user, value in users.items():
					if not self.eval_user_is_winner(user, service, step = step) and not service == 'global':
						total_time_users_unsatisfied[service][user] += 1

		return total_time_users_unsatisfied

	'''


	def run_social_choice(self, services, methods):

		winning_configurations = self.winning_configurations(services, methods)
		satisfaction_values = self.satisfaction_values(services, winning_configurations)
		self.save_results(services, winning_configurations, satisfaction_values)
		return self.step_record





if __name__ == '__main__':
	
	services = {
		's1':{
			'u1':{
				'c1': 8,
				'c2': 5,
				'c3': 3
			},
			'u2':{
				'c1': 3,
				'c2': 8,
				'c3': 5
			},
			'u3':{
				'c1': 2,
				'c2': 4,
				'c3': 9
			},
			'u3':{
				'c1': 7,
				'c2': 2,
				'c3': 5
			}
		},
		's2':{
			'u1':{
				'c1': 3,
				'c2': 7,
				'c3': 4
			},
			'u2':{
				'c1': 3,
				'c2': 7,
				'c3': 2
			},
			'u3':{
				'c1': 9,
				'c2': 3,
				'c3': 2
			},
			'u3':{
				'c1': 1,
				'c2': 4,
				'c3': 9
			}
		}
	}

	sc = SocialChoice()

	methods = {'s1':'plurality_voting', 's2':'plurality_voting'}

	#methods = 'plurality_voting'

	result = sc.run_social_choice(services, methods)

   
	print(json.dumps(result, sort_keys=True, indent=4))
