#Author: Nina Marjanovic
#csv reader

import csv


def read_inputs(file_name):
    with open(file_name, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        vector = []
        for row in csv_reader:
            vector.append([int(row[0]), int(row[1])])
    csvfile.close()
    return vector


def read_outputs(file_name):
    with open(file_name, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        vector = []
        for row in csv_reader:
            vector.append([int(row[2]), int(row[3]), int(row[4])])
    csvfile.close()
    return vector

#test
a = read_inputs('../rc_car/training_data')
b = read_outputs('../rc_car/training_data')
print a
print b
