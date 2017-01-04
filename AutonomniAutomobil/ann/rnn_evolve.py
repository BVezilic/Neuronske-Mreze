#Author: Nina Marjanovic
#Description: Evolving recurrent neural network for rc car control
#Input: feature vector
#Output: left/right

import pickle

from neat import population, parallel, visualize, nn

from rc_car import car_model

# TODO evaluate genome

num_steps = 100000

def evaluate_genomes(genomes):
    for genome in genomes:
        net = nn.create_feed_forward_phenotype(genome)

        fitnesses = []

        car = car_model.CarModel()

        fitness = 0.0
        for step in range(num_steps):
            #get inputs
            inputs = car.get_distances()
            #get outputs
            outputs = net.serial_activate(inputs)



            print outputs





def main():
    # Load the config file
    pop = population.Population('rnn_config')
    # Create parallel evaluator, 4 threads
    # Evaluate genomes
    pop.run(evaluate_genomes, 1000)

    # Save the winner.
    print('Number of evaluations: {0:d}'.format(pop.total_evaluations))
    winner = pop.statistics.best_genome()
    with open('nn_winner_genome', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)

    # Plot the evolution of the best/average fitness.
    visualize.plot_stats(pop.statistics, ylog=True, filename="nn_fitness.svg")
    # Visualizes speciation
    visualize.plot_species(pop.statistics, filename="nn_speciation.svg")
    # Visualize the best network.
    visualize.draw_net(winner, view=True, filename="nn_winner.gv")
    visualize.draw_net(winner, view=True, filename="nn_winner-enabled.gv", show_disabled=False)
    visualize.draw_net(winner, view=True, filename="nn_winner-enabled-pruned.gv", show_disabled=False,
                       prune_unused=True)

main()

