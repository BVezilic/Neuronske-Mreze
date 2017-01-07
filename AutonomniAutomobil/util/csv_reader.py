#Author: Nina Marjanovic
#Description: csv reader

import csv


def read_inputs(file_name):
    """Reads input data for rnn"""
    with open(file_name, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        vector = []
        for row in csv_reader:
            vector.append([int(row[0]), int(row[1])])
    csvfile.close()
    return vector


def read_outputs(file_name):
    """Reads output data for rnn"""
    with open(file_name, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        vector = []
        for row in csv_reader:
            vector.append([int(row[2]), int(row[3]), int(row[4])])
    csvfile.close()
    return vector

#test
a = read_inputs('../ann/training_data')
b = read_outputs('../ann/training_data')
print a
print b
