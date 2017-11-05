# Based on:
# https://github.com/makeyourownneuralnetwork/makeyourownneuralnetwork

import numpy
import scipy.special


class neuralNetwork:

    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # set number of nodes in each input, hidden, output layer
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes



        # Link weight matricies, weight_input_hidden and weight_hidden_output
        # Weights inside the arrays are w_i_j, where link is form node i to node j in the next layer

        self.weight_input_hidden = (numpy.random.rand(self.hidden_nodes, self.input_nodes) - 0.5)
        self.weight_hidden_output = (numpy.random.rand(self.output_nodes, self.hidden_nodes) - 0.5)

        # More sophisticated weight initialization:
        #self.weight_input_hidden = numpy.random.normal (0.0, pow(self.hidden_nodes, -0.5), (self.hidden_nodes, self.input_nodes))
        #self.weight_hidden_output = numpy.random.normal (0.0, pow(self.output_nodes, -0.5), (self.output_nodes, self.hidden_nodes))

        # learning rate
        self.learning_rate = learning_rate

        # define activation_function, which is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)

        pass

    def train(self, inputs_list, targets_list):
        # Convert inputs list to 2D array:
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T

        # Calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.weight_input_hidden, inputs)
        # Calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        #calculate signals into final output layer
        final_inputs = numpy.dot(self.weight_hidden_output, hidden_outputs)
        #calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        targets = numpy.array(targets_list, ndmin=2).T

        # Error is (target - actual)
        output_errors = targets - final_outputs

        # Hidden layer error is the outout_errors, split by weights, recombined at hidden nodes
        hidden_errors = numpy.dot(self.weight_hidden_output.T, output_errors)

        # Update the weights for the links between the hidden and output layers
        self.weight_hidden_output += self.learning_rate * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)), numpy.transpose(hidden_outputs))

        # Update the weights for the links between the input and hidden layers
        self.weight_input_hidden += self.learning_rate * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), numpy.transpose(inputs))


        pass

    def query(self, inputs_list):
        # Convert inputs list to 2D array:
        inputs = numpy.array(inputs_list, ndmin=2).T

        # Calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.weight_input_hidden, inputs)

        # Calculate the signals into hidden layer
        hidden_inputs = numpy.dot(self.weight_input_hidden, inputs)
        # Calculate the signals emerging from the hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # Calculate signals into final output layer
        final_inputs = numpy.dot(self.weight_hidden_output, hidden_outputs)
        # Calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        return final_outputs

# Input nodes are 52 cards plus the score change of the hand
input_nodes = 52
hidden_nodes = 100
# Output nodes are the 14 possible bids, Nil, and 1 through 13
output_nodes = 14
learning_rate = 0.3

n = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
