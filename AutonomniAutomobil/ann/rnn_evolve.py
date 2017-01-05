#Author: Nina Marjanovic
#Description: Evolving recurrent neural network for rc car control
#Input: feature vector
#Output: left/right

import pickle
import util.csv_reader as reader

from neat import population, visualize, nn, statistics

from rc_car import car_model

input_data = reader.read_inputs("../rc_car/training_data")
output_data = reader.read_outputs("../rc_car/training_data")


def evaluate_genomes(genomes):
    for g in genomes:
        net = nn.create_recurrent_phenotype(g)

        sum_square_error = 0.0
        for inputs, expected in zip(input_data, output_data):
            # Serial activation propagates the inputs through the entire network.

            output = net.activate(inputs)
            sum_square_error += (output[0] - expected[0]) ** 2
            sum_square_error += (output[1] - expected[1]) ** 2
            sum_square_error += (output[2] - expected[2]) ** 2
            sum_square_error/=3

        # When the output matches expected for all inputs, fitness will reach
        # its maximum value of 1.0.
        g.fitness = 1 - sum_square_error



def main():
    # Load the config file
    pop = population.Population('rnn_config')
    # Create parallel evaluator, 4 threads
    # Evaluate genomes
    pop.run(evaluate_genomes, 500)

    print('Number of evaluations: {0}'.format(pop.total_evaluations))

    # Display the most fit genome.
    winner = pop.statistics.best_genome()
    print('\nBest genome:\n{!s}'.format(winner))

    # Verify network output against training data.
    print('\nOutput:')
    winner_net = nn.create_recurrent_phenotype(winner)

    #save winning net
    with open('winner_net', 'wb') as f:
        pickle.dump(winner, f)

    for inputs, expected in zip(input_data, output_data):
        output = winner_net.activate(inputs)
        print("expected {0:1.5f} got {1:1.5f}".format(expected[0], output[0]))
        print("expected {0:1.5f} got {1:1.5f}".format(expected[1], output[1]))
        print("expected {0:1.5f} got {1:1.5f}".format(expected[2], output[2]))

    # Visualize the winner network and plot/log statistics.
    visualize.plot_stats(pop.statistics)
    visualize.plot_species(pop.statistics)
    visualize.draw_net(winner, view=True, filename="car-all.gv")
    visualize.draw_net(winner, view=True, filename="car-enabled.gv", show_disabled=False)
    visualize.draw_net(winner, view=True, filename="car-enabled-pruned.gv", show_disabled=False, prune_unused=True)
    statistics.save_stats(pop.statistics)
    statistics.save_species_count(pop.statistics)
    statistics.save_species_fitness(pop.statistics)


main()
