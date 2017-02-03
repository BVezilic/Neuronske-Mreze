#Author: Nina Marjanovic
#Description: Evolving recurrent neural network for rc car control
#Input: feature vector
#Output: forward, left, right

import pickle
import util.csv_reader as reader

from neat import population, nn

input_data = reader.read_inputs("training_data_left")
output_data = reader.read_outputs("training_data_left")


def evaluate_genomes(genomes):
    for g in genomes:
        net = nn.create_recurrent_phenotype(g)
        #net = nn.create_feed_forward_phenotype(g)

        sum_square_error = 0.0
        for inputs, expected in zip(input_data, output_data):
            # Serial activation propagates the inputs through the entire network.

            output = net.activate(inputs)
            #output = net.serial_activate(inputs)
            sum_square_error += (output[0] - expected[0]) ** 2
            sum_square_error += (output[1] - expected[1]) ** 2
            sum_square_error += (output[2] - expected[2]) ** 2
            sum_square_error /= 3.0

        # When the output matches expected for all inputs, fitness will reach
        # its maximum value of 1.0.
        g.fitness = 1 - sum_square_error



def main():
    # Load the config file
    pop = population.Population('rnn_config')
    # Create parallel evaluator, 4 threads
    # Evaluate genomes
    pop.run(evaluate_genomes, 200)

    print('Number of evaluations: {0}'.format(pop.total_evaluations))

    # Display the most fit genome.
    winner = pop.statistics.best_genome()
    print('\nBest genome:\n{!s}'.format(winner))

    # Verify network output against training data.
    print('\nOutput:')
    winner_net = nn.create_recurrent_phenotype(winner)
    #winner_net = nn.create_feed_forward_phenotype(winner)

    #save winning net
    with open('winner_net_left', 'wb') as f:
        pickle.dump(winner, f)

    sum = 0
    count = 0
    for inputs, expected in zip(input_data, output_data):
        #output = winner_net.serial_activate(inputs)
        output = winner_net.activate(inputs)
        print("expected {0:1.5f} got {1:1.5f}".format(expected[0], output[0]))
        print("expected {0:1.5f} got {1:1.5f}".format(expected[1], output[1]))
        print("expected {0:1.5f} got {1:1.5f}".format(expected[2], output[2]))
        count += 3
        if round(expected[0]) == round(output[0]):
            sum += 1

        if round(expected[1]) == round(output[1]):
            sum += 1

        if round(expected[2]) == round(output[2]):
            sum += 1
    print sum
    print count
    print "Precision is:"
    print float(sum)/count

main()
