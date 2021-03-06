#Author: Nina Marjanovic
#Description: RNN - loading, creating, generating output

import pickle

from neat import nn


def load_genome(filename='winner_net'):
    """Loads evolved genome"""
    with open(filename, 'rb') as data:
        return pickle.load(data)


def create_net(genome):
    """Creates rnn based on genome"""
    return nn.create_recurrent_phenotype(genome)
    #return nn.create_feed_forward_phenotype(genome)


def get_output(genome, input_data):
    # type: (object, object) -> object
    """FeedForward through network
    :rtype: object
    """
    net = create_net(genome)
    #return net.serial_activate(input_data)
    return net.activate(input_data)


