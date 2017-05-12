#!/bin/python

import sys
import matplotlib.pyplot as plt


# Convenience functions
def ind_max(x):
  m = max(x)
  return x.index(m)

import random
import math


# Arms to use

class BernoulliArm():
  def __init__(self, p):
    self.p = p

  def draw(self):
    if random.random() > self.p:
      return 0.0
    else:
      return 1.0

class NormalArm():
  def __init__(self, mu, sigma):
    self.mu = mu
    self.sigma = sigma

  def draw(self):
    return random.gauss(self.mu, self.sigma)

#


# Algorithms to use

class WinStay():
  def __init__(self, counts, values):
    self.counts      = counts   # Quantity of times each arm was played
    self.values      = values   # Reward for each arm
    self.last_reward = 0
    return

  def initialize(self, n_arms):
    self.counts = [0 for col in range(n_arms)]
    self.values = [0.0 for col in range(n_arms)]
    return

  def select_arm(self):
     if self.last_reward == 1:
        return self.last_arm
     else:
        n_arm = len(self.counts)
        return random.randint(0, n_arm - 1)

  def update(self, chosen_arm, reward):
    self.last_arm    = chosen_arm
    self.last_reward = reward

    self.counts[chosen_arm] = self.counts[chosen_arm] + 1
    n                       = self.counts[chosen_arm]
    value                   = self.values[chosen_arm]
    new_value               = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
    self.values[chosen_arm] = new_value
    return


class Random():
    def __init__(self, counts, values):
        self.counts      = counts
        self.values      = values
        return

    def initialize(self, n_arms):
        self.counts = [0 for col in range(n_arms)]
        self.values = [0.0 for col in range(n_arms)]
        return

    def select_arm(self):
         n_arm = len(self.counts)
         return random.randint(0, n_arm - 1)

    def update(self, chosen_arm, reward):
        self.counts[chosen_arm] = self.counts[chosen_arm] + 1
        n                       = self.counts[chosen_arm]
        value                   = self.values[chosen_arm]
        new_value               = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.values[chosen_arm] = new_value
        return


class UCB1():
  def __init__(self, counts, values):
    self.counts = counts
    self.values = values
    return

  def initialize(self, n_arms):
    self.counts = [0 for col in range(n_arms)]
    self.values = [0.0 for col in range(n_arms)]
    return

  def select_arm(self):
    n_arms = len(self.counts)
    for arm in range(n_arms):
      if self.counts[arm] == 0:
        return arm

    ucb_values   = [0.0 for arm in range(n_arms)]
    total_counts = sum(self.counts)
    for arm in range(n_arms):
      bonus           = math.sqrt((2 * math.log(total_counts)) / float(self.counts[arm]))
      ucb_values[arm] = self.values[arm] + bonus
    return ind_max(ucb_values)

  def update(self, chosen_arm, reward):
    self.counts[chosen_arm] = self.counts[chosen_arm] + 1
    n                       = self.counts[chosen_arm]

    value                   = self.values[chosen_arm]
    new_value               = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
    self.values[chosen_arm] = new_value
    return


class Biased():
    def __init__(self, counts, values):
        self.counts = counts
        self.values = values
        return

    def initialize(self, n_arms):
        self.counts = [0 for col in range(n_arms)]
        self.values = [0.0 for col in range(n_arms)]
        return

    def select_arm(self):
        return 0

    def update(self, chosen_arm, reward):
        self.counts[chosen_arm] = self.counts[chosen_arm] + 1
        n                       = self.counts[chosen_arm]

        value                   = self.values[chosen_arm]
        new_value               = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.values[chosen_arm] = new_value
        return

#

# def test(algo, arms, num_sims, horizon):
  # chosen_arms        = [0.0 for i in range(num_sims * horizon)]
  # rewards            = [0.0 for i in range(num_sims * horizon)]
  # cumulative_rewards = [0.0 for i in range(num_sims * horizon)]
  # sim_nums           = [0.0 for i in range(num_sims * horizon)]
  # times              = [0.0 for i in range(num_sims * horizon)]

  # for sim in range(num_sims):
    # sim = sim + 1
    # algo.initialize(len(arms))

    # for t in range(horizon):
      # t              +=  1
      # index           = (sim - 1) * horizon + t - 1
      # sim_nums[index] = sim
      # times[index]    = t

      # chosen_arm         = algo.select_arm()
      # chosen_arms[index] = chosen_arm

      # reward         = arms[chosen_arms[index]].draw()
      # rewards[index] = reward

      # if t == 1:
        # cumulative_rewards[index] = reward
      # else:
        # cumulative_rewards[index] = cumulative_rewards[index - 1] + reward

      # algo.update(chosen_arm, reward)

  # return [sim_nums, times, chosen_arms, rewards, cumulative_rewards]



arm1 = BernoulliArm(0.7)
arm2 = BernoulliArm(0.5)
arm3 = BernoulliArm(0.2)
arm4 = BernoulliArm(0.2)
arm5 = BernoulliArm(0.3)

arms = [arm1, arm2, arm3, arm4, arm5]

algo1 = UCB1([], [])
algo2 = WinStay([], [])
algo3 = Random([],[])
algo4 = Biased([],[])

algos = [algo1, algo2, algo3, algo4]
count = 1

def plot(qtd):
    if qtd > 1:
        payoffs = []
        n_arms = len(arms)
        for algo in algos:
            algo.initialize(n_arms)

        # Tempo no cassino
        for t in range(qtd):
            for i in range(0, len(algos)):
                chosen_arm = algos[i].select_arm()
                reward     = arms[chosen_arm].draw()
                algos[i].update(chosen_arm, reward)

        for algo in algos:
            reward = sum([algo.values[n] * algo.counts[n] for n in range(n_arms)])
            payoffs.append(reward)


        # Plot dados
        x    = [1,2,3,4,5]  # 5 bracos
        x_al = [1,2,3,4]    # 4 algoritmos
        plt.subplot(211)

        data = {0:["UCB","bo"], 1:["Vence-fica","ro"], 2:["Aleatorio","go"], 3:["Clarividente","ko"]}
        for i in range(4):
            plt.plot(x, algos[i].counts, data[i][1], label = data[i][0])
            plt.legend()

        plt.xlabel("Braços")
        plt.ylabel("Puxação")

        plt.xticks(range(1,6)) # soh mostra inteiros

        # Mostra payoffs
        plt.subplot(212)
        plt.plot(x_al, payoffs, 'yo')
        plt.legend()

        plt.xticks(range(1,5)) # soh mostra inteiros

        plt.xlabel("Algoritmos")
        plt.ylabel("Ganhos")
        plt.show()

    # num_sims = 1000
    # horizon = 10
    # for algo in algos:
        # results = test(algo, arms, num_sims, horizon)
