# inference.py
# ------------
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


import itertools
import random
import busters
import game

from util import manhattanDistance, raiseNotDefined


class DiscreteDistribution(dict):
    """
    A DiscreteDistribution models belief distributions and weight distributions
    over a finite set of discrete keys.
    """
    def __getitem__(self, key):
        self.setdefault(key, 0)
        return dict.__getitem__(self, key)

    def copy(self):
        """
        Return a copy of the distribution.
        """
        return DiscreteDistribution(dict.copy(self))

    def argMax(self):
        """
        Return the key with the highest value.
        """
        if len(self.keys()) == 0:
            return None
        all = list(self.items())
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def total(self):
        """
        Return the sum of values for all keys.
        """
        return float(sum(self.values()))

    def normalize(self):
        """
        Normalize the distribution such that the total value of all keys sums
        to 1. The ratio of values for all keys will remain the same. In the case
        where the total value of the distribution is 0, do nothing.

        >>> dist = DiscreteDistribution()
        >>> dist['a'] = 1
        >>> dist['b'] = 2
        >>> dist['c'] = 2
        >>> dist['d'] = 0
        >>> dist.normalize()
        >>> list(sorted(dist.items()))
        [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0)]
        >>> dist['e'] = 4
        >>> list(sorted(dist.items()))
        [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0), ('e', 4)]
        >>> empty = DiscreteDistribution()
        >>> empty.normalize()
        >>> empty
        {}
        """
        "*** YOUR CODE HERE ***"

        total = float(self.total())
        if total == 0: return
        for key in self.keys():
            self[key] = self[key] / total

  

    def sample(self):
        """
        Draw a random sample from the distribution and return the key, weighted
        by the values associated with each key.

        >>> dist = DiscreteDistribution()
        >>> dist['a'] = 1
        >>> dist['b'] = 2
        >>> dist['c'] = 2
        >>> dist['d'] = 0
        >>> N = 100000.0
        >>> samples = [dist.sample() for _ in range(int(N))]
        >>> round(samples.count('a') * 1.0/N, 1)  # proportion of 'a'
        0.2
        >>> round(samples.count('b') * 1.0/N, 1)
        0.4
        >>> round(samples.count('c') * 1.0/N, 1)
        0.4
        >>> round(samples.count('d') * 1.0/N, 1)
        0.0
        """
        "*** YOUR CODE HERE ***"
        if self.total() != 1:
            self.normalize()
        items = sorted(self.items())
        distribution = [i[1] for i in items]
        values = [i[0] for i in items]
        choice = random.random()
        i, total = 0, distribution[0]
        while choice > total:
            i += 1
            total += distribution[i]
        return values[i]



class InferenceModule:
    """
    An inference module tracks a belief distribution over a ghost's location.
    """
    ############################################
    # Useful methods for all inference modules #
    ############################################

    def __init__(self, ghostAgent):
        """
        Set the ghost agent for later access.
        """
        self.ghostAgent = ghostAgent
        self.index = ghostAgent.index
        self.obs = []  # most recent observation position

    def getJailPosition(self):
        return (2 * self.ghostAgent.index - 1, 1)

    def getPositionDistributionHelper(self, gameState, pos, index, agent):
        try:
            jail = self.getJailPosition()
            gameState = self.setGhostPosition(gameState, pos, index + 1)
        except TypeError:
            jail = self.getJailPosition(index)
            gameState = self.setGhostPositions(gameState, pos)
        pacmanPosition = gameState.getPacmanPosition()
        ghostPosition = gameState.getGhostPosition(index + 1)  # The position you set
        dist = DiscreteDistribution()
        if pacmanPosition == ghostPosition:  # The ghost has been caught!
            dist[jail] = 1.0
            return dist
        pacmanSuccessorStates = game.Actions.getLegalNeighbors(pacmanPosition, \
                gameState.getWalls())  # Positions Pacman can move to
        if ghostPosition in pacmanSuccessorStates:  # Ghost could get caught
            mult = 1.0 / float(len(pacmanSuccessorStates))
            dist[jail] = mult
        else:
            mult = 0.0
        actionDist = agent.getDistribution(gameState)
        for action, prob in actionDist.items():
            successorPosition = game.Actions.getSuccessor(ghostPosition, action)
            if successorPosition in pacmanSuccessorStates:  # Ghost could get caught
                denom = float(len(actionDist))
                dist[jail] += prob * (1.0 / denom) * (1.0 - mult)
                dist[successorPosition] = prob * ((denom - 1.0) / denom) * (1.0 - mult)
            else:
                dist[successorPosition] = prob * (1.0 - mult)
        return dist

    def getPositionDistribution(self, gameState, pos, index=None, agent=None):
        """
        Return a distribution over successor positions of the ghost from the
        given gameState. You must first place the ghost in the gameState, using
        setGhostPosition below.
        """
        if index == None:
            index = self.index - 1
        if agent == None:
            agent = self.ghostAgent
        return self.getPositionDistributionHelper(gameState, pos, index, agent)

    def getObservationProb(self, noisyDistance, pacmanPosition, ghostPosition, jailPosition):
        """
        Return the probability P(noisyDistance | pacmanPosition, ghostPosition).
        """
        "*** YOUR CODE HERE ***"
#---------------------------------------------------------------------------------------------------
#QUESTION 1 (2 points): Observation Probability 
#For question 1, we start by checking if the ghostPosition is the same as the jail Position. Based
#on the requirements for the problem, if the ghost's position is the jail position like previously
#checed for, then the observation is == to None which we do below and return a probability of '1.0'.
#We finish it off with an else statement to return a probability of zero along with the reading of 
#None returning a probability of zero. Finally, we use the manhattanDistance function to calculate
#the distance between the pacmanPosition and the ghostPosition and return the observation probability
#by passing it the noisy distance, as found before, and the trueDistance. 
        if ghostPosition == jailPosition:
            if noisyDistance == None:
                return 1.0
            else:
                return 0.0
        if noisyDistance == None:
            return 0.0
        trueDistance = manhattanDistance(pacmanPosition, ghostPosition)
        return busters.getObservationProbability(noisyDistance, trueDistance)
#---------------------------------------------------------------------------------------------------
    def setGhostPosition(self, gameState, ghostPosition, index):
        """
        Set the position of the ghost for this inference module to the specified
        position in the supplied gameState.

        Note that calling setGhostPosition does not change the position of the
        ghost in the GameState object used for tracking the true progression of
        the game.  The code in inference.py only ever receives a deep copy of
        the GameState object which is responsible for maintaining game state,
        not a reference to the original object.  Note also that the ghost
        distance observations are stored at the time the GameState object is
        created, so changing the position of the ghost will not affect the
        functioning of observe.
        """
        conf = game.Configuration(ghostPosition, game.Directions.STOP)
        gameState.data.agentStates[index] = game.AgentState(conf, False)
        return gameState

    def setGhostPositions(self, gameState, ghostPositions):
        """
        Sets the position of all ghosts to the values in ghostPositions.
        """
        for index, pos in enumerate(ghostPositions):
            conf = game.Configuration(pos, game.Directions.STOP)
            gameState.data.agentStates[index + 1] = game.AgentState(conf, False)
        return gameState

    def observe(self, gameState):
        """
        Collect the relevant noisy distance observation and pass it along.
        """
        distances = gameState.getNoisyGhostDistances()
        if len(distances) >= self.index:  # Check for missing observations
            obs = distances[self.index - 1]
            self.obs = obs
            self.observeUpdate(obs, gameState)

    def initialize(self, gameState):
        """
        Initialize beliefs to a uniform distribution over all legal positions.
        """
        self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]
        self.allPositions = self.legalPositions + [self.getJailPosition()]
        self.initializeUniformly(gameState)

    ######################################
    # Methods that need to be overridden #
    ######################################

    def initializeUniformly(self, gameState):
        """
        Set the belief state to a uniform prior belief over all positions.
        """
        raise NotImplementedError

    def observeUpdate(self, observation, gameState):
        """
        Update beliefs based on the given distance observation and gameState.
        """
        raise NotImplementedError

    def elapseTime(self, gameState):
        """
        Predict beliefs for the next time step from a gameState.
        """
        raise NotImplementedError

    def getBeliefDistribution(self):
        """
        Return the agent's current belief state, a distribution over ghost
        locations conditioned on all evidence so far.
        """
        raise NotImplementedError


class ExactInference(InferenceModule):
    """
    The exact dynamic inference module should use forward algorithm updates to
    compute the exact belief function at each time step.
    """
    def initializeUniformly(self, gameState):
        """
        Begin with a uniform distribution over legal ghost positions (i.e., not
        including the jail position).
        """
        self.beliefs = DiscreteDistribution()
        for p in self.legalPositions:
            self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observeUpdate(self, observation, gameState):
        """
        Update beliefs based on the distance observation and Pacman's position.

        The observation is the noisy Manhattan distance to the ghost you are
        tracking.

        self.allPositions is a list of the possible ghost positions, including
        the jail position. You should only consider positions that are in
        self.allPositions.

        The update model is not entirely stationary: it may depend on Pacman's
        current position. However, this is not a problem, as Pacman's current
        position is known.
        """
        "*** YOUR CODE HERE ***"
#---------------------------------------------------------------------------------------------------        
#QUESTION 2 (3 points): Exact Inference Observation
#For question 2 we start by initializing distance, pacmanposition, and jail position. Next, 
#we need a for loop that iterates over all positions and gets the probability and distance 
#for each iteration and use the normalize method on the distance we just obtained. From there, we 
#set self.beliefs = to the new normalized distance. 
        dist = DiscreteDistribution()
        pacmanPosition = gameState.getPacmanPosition()
        jailPosition = self.getJailPosition()

        for pos in self.allPositions:
            prob = self.getObservationProb(observation, pacmanPosition, pos, jailPosition) 
            dist[pos] = prob * self.beliefs[pos]
        dist.normalize()
        self.beliefs = dist

#---------------------------------------------------------------------------------------------------
    def elapseTime(self, gameState):
        """
        Predict beliefs in response to a time step passing from the current
        state.

        The transition model is not entirely stationary: it may depend on
        Pacman's current position. However, this is not a problem, as Pacman's
        current position is known.
        """
        "*** YOUR CODE HERE ***"
#---------------------------------------------------------------------------------------------------
#QUESTION 3 (3 points): Exact Inference with Time Elapse
#For question 3, we begin by setting dist equal to the DiscreteDistribution() previously made. 
#From there we look at each old position found in self.allPositions and use the line provided,
#newPostDist = self.getPositionDistribution(gameState, oldPos) in order to obtain the distribution
#over the new positions for the ghost. From there, we set oldProb to the value of self.beleifs at 
#old positions location. Finally, we go through each newPosition in the newposition keys and if found
#then dist[newPos] is updated with the equations oldProb * newPosDist[newPos] and self.beliefs is 
#set equal to dist. 

        dist = DiscreteDistribution()
        for oldPos in self.allPositions:

            newPosDist = self.getPositionDistribution(gameState, oldPos)
            oldProb = self.beliefs[oldPos]

            for newPos in newPosDist.keys():

                dist[newPos] += oldProb * newPosDist[newPos]

        self.beliefs = dist

#---------------------------------------------------------------------------------------------------
    def getBeliefDistribution(self):
        return self.beliefs


class ParticleFilter(InferenceModule):
    """
    A particle filter for approximately tracking a single ghost.
    """
    def __init__(self, ghostAgent, numParticles=300):
        InferenceModule.__init__(self, ghostAgent)
        self.setNumParticles(numParticles)

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles

    def initializeUniformly(self, gameState):
        """
        Initialize a list of particles. Use self.numParticles for the number of
        particles. Use self.legalPositions for the legal board positions where
        a particle could be located. Particles should be evenly (not randomly)
        distributed across positions in order to ensure a uniform prior. Use
        self.particles for the list of particles.
        """
        self.particles = []
        "*** YOUR CODE HERE ***"
#---------------------------------------------------------------------------------------------------
#QUESTION 5 (2 points): Approximate Inference Initialization and Beliefs
#For question 5, we start by creating an empty list which will later be the source of our values
#that are going to be added to it. To start however, we will asign n the value of self.numParticles
#and size equal to the length of self.legal positions. With these two variables, we can now check if
#n is greater than size, then temp will be incremented by self.legalPositions and n will be subtracted
#by size. This is in order to create an evenly distributed spread and not have it just be random, else
#temp will be incremented by the slice of [0:n]. Finally, we set self.particals equal to the value of temp. 
        temp = []
        n = self.numParticles
        size = len(self.legalPositions)
        while n > 0:
            if n > size:
                temp += self.legalPositions
                n -= size
            else:
                temp += self.legalPositions[0:n]
                n = 0
        self.particles = temp
 #---------------------------------------------------------------------------------------------------       

    def observeUpdate(self, observation, gameState):
        """
        Update beliefs based on the distance observation and Pacman's position.

        The observation is the noisy Manhattan distance to the ghost you are
        tracking.

        There is one special case that a correct implementation must handle.
        When all particles receive zero weight, the list of particles should
        be reinitialized by calling initializeUniformly. The total method of
        the DiscreteDistribution may be useful.
        """
        "*** YOUR CODE HERE ***"
#---------------------------------------------------------------------------------------------------
#Question 6 (3 points): Approximate Inference Observation
#For question 6 we begin by getting pacman's position, jail position, and the distance,
#which is followed by a for loop that iterates over particles. Inside our loop we save the
#obserrvation probability to prob and calculate the distance. If the distance is 0 we have to
#call self.initializeuniformly. Otherwise, our distance needs to be normalized then stored 
#in beliefs. Finally, our for loop iterates over numParticles and gets a new distance sample.
        pacmanPosition = gameState.getPacmanPosition()
        jailPosition = self.getJailPosition()
        dist = DiscreteDistribution()

        for par in self.particles:
            prob = self.getObservationProb(observation, pacmanPosition, par, jailPosition)
            dist[par] += prob
        if dist.total() == 0:
            self.initializeUniformly(gameState)
        else:
            dist.normalize()
            self.beliefs = dist     
            for i in range(self.numParticles):
                pSample = dist.sample()
                self.particles[i] = pSample
 #---------------------------------------------------------------------------------------------------       

    def elapseTime(self, gameState):
        """
        Sample each particle's next state based on its current state and the
        gameState.
        """
        "*** YOUR CODE HERE ***"
#---------------------------------------------------------------------------------------------------
#QUESTION 7 (3 points): Approximate Inference with Time Elapse
#For question 7, we begin by using a for loop to iterate over all values, i, in range of 
#self.numparticles. from there we will set particle equal to the particle in position i and then check
#to see if the particle is in the currState where if so it is set equal to the equivalent of the current
#state particle and taken the sample of. Else, dist is updated with the pacman position and the particle
#and currState of the particle is set equal to dist. Finally, particles[i] is set equal to the previous
#defined dist and taken the sample of once more and stored in self.particles[i].
        currState = {}

        for i in range(self.numParticles):

            particle = self.particles[i]
            if particle in currState:
                self.particles[i] = currState[particle].sample()
            else:
                dist = self.getPositionDistribution(gameState, particle)
                currState[particle] = dist
                self.particles[i] = dist.sample()
        
#---------------------------------------------------------------------------------------------------
    def getBeliefDistribution(self):
        """
        Return the agent's current belief state, a distribution over ghost
        locations conditioned on all evidence and time passage. This method
        essentially converts a list of particles into a belief distribution.
        
        This function should return a normalized distribution.
        """
        "*** YOUR CODE HERE ***"
#---------------------------------------------------------------------------------------------------
#QUESTION 5 (2 points): Approximate Inference Initialization and Beliefs
#For question 5, we start assining dist = DiscreteDistribution(). Next, we use a simple for loop 
# where for every particle in self.particals, dist[par] is incremented by 1 and dist is then 
# normalized and returned.  

        dist = DiscreteDistribution()
        for par in self.particles:
            dist[par] += 1
        dist.normalize()
        return dist
        
#---------------------------------------------------------------------------------------------------

class JointParticleFilter(ParticleFilter):
    """
    JointParticleFilter tracks a joint distribution over tuples of all ghost
    positions.
    """
    def __init__(self, numParticles=600):
        self.setNumParticles(numParticles)

    def initialize(self, gameState, legalPositions):
        """
        Store information about the game, then initialize particles.
        """
        self.numGhosts = gameState.getNumAgents() - 1
        self.ghostAgents = []
        self.legalPositions = legalPositions
        self.initializeUniformly(gameState)

    def initializeUniformly(self, gameState):
        """
        Initialize particles to be consistent with a uniform prior. Particles
        should be evenly distributed across positions in order to ensure a
        uniform prior.
        """
        self.particles = []
        "*** YOUR CODE HERE ***"
#---------------------------------------------------------------------------------------------------
#QUESTION 8 (1 points): Joint Particle Filter Observation
#For question 8, we are using itertools and creating the possible permutations for legalPositions
#based on the number of ghosts that we have. We then shuffle the list of permutations to ensure even
#placement of particles accross the board. From there, a simple while loops analyzes the size compared
#to the number of particles we are presented with and while n is greater than the size, self.particles
#is incremented by the list of permutations and used for part of the cartesian product of possibilites. 

        permutations = list(itertools.product(self.legalPositions, repeat = self.numGhosts))
        random.shuffle(permutations)

        n = self.numParticles
        size = len(permutations)

        while n > size:
            self.particles += permutations
            n -= size
        self.particles += permutations[:n]
#---------------------------------------------------------------------------------------------------       

    def addGhostAgent(self, agent):
        """
        Each ghost agent is registered separately and stored (in case they are
        different).
        """
        self.ghostAgents.append(agent)

    def getJailPosition(self, i):
        return (2 * i + 1, 1)

    def observe(self, gameState):
        """
        Resample the set of particles using the likelihood of the noisy
        observations.
        """
        observation = gameState.getNoisyGhostDistances()
        self.observeUpdate(observation, gameState)

    def observeUpdate(self, observation, gameState):
        """
        Update beliefs based on the distance observation and Pacman's position.

        The observation is the noisy Manhattan distances to all ghosts you
        are tracking.

        There is one special case that a correct implementation must handle.
        When all particles receive zero weight, the list of particles should
        be reinitialized by calling initializeUniformly. The total method of
        the DiscreteDistribution may be useful.
        """
        "*** YOUR CODE HERE ***"
#--------------------------------------------------------------------------------------------------- 
#Question 9 (3 points): Joint Particle Filter Observation
#For question 9 we start by getting pacmanposition and distance. After that, we need 
#a for loop that iterates through particles and set probability to 1. We also need 
#an additional(nested) for loop iterating over the numGhosts. For each iteration, 
#we pass that to observation and store it in noisyDist. Here, we have to update the 
#probability and distance. Next, we need to update beliefs with the new distance. If
#beliefs.total() == 0, we must Uniformly initialize the gamestate. Else, we normalize 
#beliefs and loop through numParticles getting a new position, storing that position 
#into particles.
        pacmanPosition = gameState.getPacmanPosition()
        dist = DiscreteDistribution()
        for par in self.particles:
            prob = 1
            for i in range(self.numGhosts):
                noisyDist = observation[i]
                prob *= self.getObservationProb(noisyDist, pacmanPosition, par[i], self.getJailPosition(i))
            dist[par] += prob

        self.beliefs = dist
        if self.beliefs.total() == 0:
            self.initializeUniformly(gameState)
        else:
            self.beliefs.normalize()
            for i in range(self.numParticles):
                newPos = self.beliefs.sample()
                self.particles[i] = newPos
#---------------------------------------------------------------------------------------------------       
#QUESTION 10 (3 points): Joint Particle Filter Time Elapse and Full Test
#For question 10, we begin by creating two variables, one being a list and another a dictionary to 
#serve the purpose of storing old ghost positions in. After which, we add every old particle into a 
#new list known as newParticle and advance to the next part of our function. For every gPosition in 
#the range of the number of ghosts, we will check to see if the old particle and position is in ghostDict
#where if not found the sample is added to ghostDict. If else, then the position is then added and stored
#in a new name state where ghostDict[(oldParticle, i)] = newPostDist. From there, we finally take the sample
#of the new position distance and store that in location i of newParticle based on the step of the previous
#ghost in the position before it. 
    def elapseTime(self, gameState):
        """
        Sample each particle's next state based on its current state and the
        gameState.
        """
        newParticles = []
        ghostDict = {}
        for oldParticle in self.particles:
            newParticle = list(oldParticle)  # A list of ghost positions

            # now loop through and update each entry in newParticle...
            "*** YOUR CODE HERE ***"
            prevGhostPositions = list(oldParticle)

            for i in range(self.numGhosts):

                if (oldParticle, i) in ghostDict:
                    newParticle[i] = ghostDict[(oldParticle, i)].sample()
                    
                else:
                    newPosDist = self.getPositionDistribution(gameState, prevGhostPositions, i, self.ghostAgents[i])
                    ghostDict[(oldParticle, i)] = newPosDist
                    newParticle[i] = newPosDist.sample()
            

            """*** END YOUR CODE HERE ***"""
            newParticles.append(tuple(newParticle))
        self.particles = newParticles

#---------------------------------------------------------------------------------------------------
# One JointInference module is shared globally across instances of MarginalInference
jointInference = JointParticleFilter()


class MarginalInference(InferenceModule):
    """
    A wrapper around the JointInference module that returns marginal beliefs
    about ghosts.
    """
    def initializeUniformly(self, gameState):
        """
        Set the belief state to an initial, prior value.
        """
        if self.index == 1:
            jointInference.initialize(gameState, self.legalPositions)
        jointInference.addGhostAgent(self.ghostAgent)

    def observe(self, gameState):
        """
        Update beliefs based on the given distance observation and gameState.
        """
        if self.index == 1:
            jointInference.observe(gameState)

    def elapseTime(self, gameState):
        """
        Predict beliefs for a time step elapsing from a gameState.
        """
        if self.index == 1:
            jointInference.elapseTime(gameState)

    def getBeliefDistribution(self):
        """
        Return the marginal belief over a particular ghost by summing out the
        others.
        """
        jointDistribution = jointInference.getBeliefDistribution()
        dist = DiscreteDistribution()
        for t, prob in jointDistribution.items():
            dist[t[self.index - 1]] += prob
        return dist
