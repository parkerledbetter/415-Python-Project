# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
# This part of our code iterates over the states and creates a counter in order to keep tract of the
# current state. The main part of our code chooses the best action to take. We then get the value of
# the state using the maximum value from the best q-state.
        for i in range(self.iterations):
            states = self.mdp.getStates()
            currCounter = util.Counter()
            for state in states:
                action = self.getAction(state)
                if action is not None:
                    currCounter[state] = self.getQValue(state, action)

            self.values = currCounter

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
# This part of our code is where we implement some of the methods mentioned above to aid in our
# runValueIteration functions working. The states, actions, and transistion states are all recorded
# and stored into various variables in order to compute other portions of problem.s
        total = 0
        transStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)

        for tranStateAndProb in transStatesAndProbs:
            tstate = tranStateAndProb[0]
            prob = tranStateAndProb[1]
            reward = self.mdp.getReward(state, action, tstate)
            value = self.getValue(tstate)
            total += prob * (reward + self.discount * value)

        return total


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
# This portion of our code acts similarly to the above in aiding other functions with the computed
# actions from the values. We start by geting the possible actions from the various states and use
# the information to determine the max value and max action. Depending on the value from those actions,
# we will return max_value equal to the value as it is originally less than and max the max_action equal
# to the new value of action.
        if self.mdp.isTerminal(state):
            return None
        else:
            actions = self.mdp.getPossibleActions(state)
            max_value = self.getQValue(state, actions[0])
            max_action = actions[0]

            for action in actions:
                value = self.getQValue(state, action)
                if max_value <= value:
                    max_value = value
                    max_action = action

            return max_action
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
# This part of our code is something that will be used in implementation later on and throughout the
# remainder of our project. To Start, our code first iterates over all of the states and gets the
# remainder of i % len(states) and stores that as 'currState' in order to see if it isTerminal. If not,
# we create qVals to store the actual Q values that are found in the next part of our code from using
# the computeQValueFromValues function where we pass it currState and an action. Finally, we take the
# maximum of qVals and set it equal to 'self.values[currState].

        for i in range(self.iterations):
            states = self.mdp.getStates()
            currState = states[i % len(states)]

            if not self.mdp.isTerminal(currState):
                qVals = []
                for action in self.mdp.getPossibleActions(currState):
                    q_value = self.computeQValueFromValues(currState, action)
                    qVals.append(q_value)
                self.values[currState] = max(qVals)


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """

    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # This part of our code is similar to the previous runValueIteration programs with a couple of
        # differences being that we need two new variables, 'priority_queue' and 'previous'. We begin
        # by iterating over the states with 'self.mdp.getStates' and check to see if our next condition is not
        # met. For every action, we get the use the 'getPossibleActions' function. The final part of this block
        # of code iterates over every 'nextState' and gets the (state, action) and from there makes the
        # determination on where to add the state to the lists with the previous states already evaluated.
        priority_queue = util.PriorityQueue()
        previous = {}

        for state in self.mdp.getStates():

            if not self.mdp.isTerminal(state):

                for action in self.mdp.getPossibleActions(state):

                    for nextState, x in self.mdp.getTransitionStatesAndProbs(state, action):

                        if nextState in previous:
                            previous[nextState].add(state)

                        else:
                            previous[nextState] = {state}

        # ------------------------------------------------------------------------------------------------------|
        # This code is computing the same 'runValueIteration' function as seen in our previous
        # AsynchronousValueIterationAgent. However, the only difference is made at the last two lines where
        # we take the absolute value of the qVals and subtract the values of [state] in order to get our
        # difference which will be used to update out PriorityQueue.
        for state in self.mdp.getStates():

            if not self.mdp.isTerminal(state):

                qVals = []

                for action in self.mdp.getPossibleActions(state):
                    q_value = self.computeQValueFromValues(state, action)
                    qVals.append(q_value)

                diff = abs(max(qVals) - self.values[state])
                priority_queue.update(state, - diff)

        # ------------------------------------------------------------------------------------------------------|
# This part of our code first starts by evaluating if our priority queue is empty and if not, then
# we create a 'currState' variable that pops our priority queue. The next thing we do is check to see
# whether or not the currState is currently 'isTerminal' where we create qVals to store our values.
# We then continue to iterate over the 'getPossibleActions' of our currState and take the Qvalue and
# append that to a list to take the max similar/identical to what we did previously in our above code.
# Then for every p in previous, we take a look at the qu value and do the same function/code that we
# implemented earlier to get the max qvalue and subtract from values to get the difference. Finally,
# the only change in this problem occurs in the last ling that checks if the diff is greater than
# 'self.theta' where if it is, it updates the priority queue with the p, and -diff.
        for i in range(self.iterations):

            if priority_queue.isEmpty():
                break
            currState = priority_queue.pop()

            if not self.mdp.isTerminal(currState):
                qVals = []

                for action in self.mdp.getPossibleActions(currState):
                    q_value = self.computeQValueFromValues(currState, action)
                    qVals.append(q_value)
                self.values[currState] = max(qVals)
            # ------------------------------------------------------------------------------------------------------|
            for p in previous[currState]:

                if not self.mdp.isTerminal(p):
                    qVals = []
                    for action in self.mdp.getPossibleActions(p):
                        q_value = self.computeQValueFromValues(p, action)
                        qVals.append(q_value)
                    diff = abs(max(qVals) - self.values[p])
                    if diff > self.theta:
                        priority_queue.update(p, -diff)
