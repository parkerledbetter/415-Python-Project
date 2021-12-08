# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.q_values = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        return self.q_values[(state, action)]



    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
#First we create a place to store our q values, then we update the list with the state's legal actions,
#and finally evaluate the length of the legal actions and return it.
        qVals = []
        for action in self.getLegalActions(state):
            qVals.append(self.getQValue(state, action))
        if len(self.getLegalActions(state)) == 0:
            return 0.0
        else:
            return max(qVals)


    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
#First we set max_action to None for the terminal state, save the Q value, and evaluate if the value is greater
#than the maximum q value. If so, we update max q value and max action.
        max_action = None
        maxqVal = 0
        for action in self.getLegalActions(state):
            qVal = self.getQValue(state, action)
            if qVal > maxqVal or max_action is None:
                maxqVal = qVal
                max_action = action
        return max_action


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        else:
            return self.computeActionFromQValues(state)


        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
#This portion of the code updates the current q values by using the getqvalue method along with
#the computevaluefromqvalues, similar to what was done on number 5 from our project. Then it was
#just a simple computation that combines the two values to ultimately update our q values.
        self.q_values[(state, action)] = ((1 - self.alpha) * self.getQValue(state, action)) + (
                self.alpha * (reward + self.discount * self.computeValueFromQValues(nextState)))

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
# This portion of our code starts by initiiating q as 0. From that point, we use the method
# 'self.featExtractor.getFeatures' and store the value in 'newFeat' after we pass it state and action.
# After which, we take iterate over newFeat and increment q based on the newFeat multiplied by the
# weights provided of [f]. Finally we return q.
        q = 0
        newFeat = self.featExtractor.getFeatures(state, action)
        for f in newFeat:
            q += newFeat[f] * self.weights[f]
        return q

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
# This portion of our code does the same thing off the start as our code in getQValue did as seen
# above. The main change in this code is to store the difference that is used in our next calculation
# in order to update the weighst of the value we are currently iterating over. This is done by adding
# the current weight plus the diff we gained earlier multiplied by 'self.alpha' and multiplied by
# 'newFeat[f].
        newFeat = self.featExtractor.getFeatures(state, action)

        diff = (reward + (self.discount * self.getValue(nextState))) - self.getQValue(state, action)

        for f in newFeat:
            self.weights[f] = self.weights[f] + (diff * self.alpha * newFeat[f])

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
