# Based on:
# https://github.com/makeyourownneuralnetwork/makeyourownneuralnetwork

import numpy
import scipy.special
import random


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

def train_from_csv():

    data_file = open("bids1.csv", "r")
    data_list = data_file.readlines()
    data_file.close()


    # good_data_list holds successful hands where the team scored more than 5 points
    a = False
    good_data_list = []
    print("LENGTH BEFORE:")
    print(len(data_list))

    for bid in data_list:
        bid_list = bid.split(",")

        if len(bid_list) > 71:
            if bid_list[67] != "scoreChange" and bid_list[67] != "" and bid_list[68] != "":
                scoreChange = int(bid_list[67])
                bagsChange = int(bid_list[68])
                #print(i)
                #print(i < 7)
                #print("\n")
                if scoreChange > 7 and bagsChange < 3:
                    good_data_list.append(bid_list)
    print("LENGTH AFTER:")
    print(len(good_data_list))

    for bid_data in good_data_list:

        useful_values = []
        # Get actual bid:
        # Will be useful_values[0]
        useful_values.append(bid_data[58])

        # Get all cards in hand data
        # Will be useful_values[1:53]
        for i in range(1, 53):
            useful_values.append(bid_data[i])
        #print(useful_values)

        # Normalize all data to 0.01 to 1 scale
        scaled_input = (numpy.asfarray(useful_values[1:53]) / 1.0 * 0.99) + 0.01
        #print(scaled_input)


        # output nodes is 14
        onodes = 14
        targets = numpy.zeros(onodes) + 0.01
        targets[int(useful_values[0])] = 0.99

        #print(targets)

        n.train(scaled_input, targets)
    return "Trained"

def get_bid(input_data):
    input_dataa = (numpy.asfarray(input_data[1:53]) / 1.0 * 0.99) + 0.01
    outputs = n.query(input_dataa)
    bid = 0
    bid_confidence = 0
    for i in range(0, 14):
        print(str(i) + ":\t" + str(outputs[i]))
        if outputs[i] > bid_confidence:
            bid = i
            bid_confidence = outputs[i]

    # Make NN output more fuzzy to generate better data:
    fuzzes = [-4, -3, -3, -2, -2, -2, -1, -1, -1, -1, -4, -3, -3, -2, -2, -2, -1, -1, -1, -1, -4, -3, -3, -2, -2, -2, -1, -1, -1, -1, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    fuzzes_2 = [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3]
    adj = fuzzes[random.randint(0, len(fuzzes) - 1)]
    bid += adj
    if bid < 0:
        bid = fuzzes_2[random.randint(0, len(fuzzes_2) - 1)]

    return bid
