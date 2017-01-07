#Author: Nina Marjanovic
#Descrioption: CSV Writer


def write_data(f, left_distance, right_distance, front, left, right):
    """Writes training data to csv file"""
    if left_distance is False:
        left_distance = -1
    if right_distance is False:
        right_distance = -1
    f.write(str(left_distance) + ',' + str(right_distance) + ',' + str(front) +
            ',' + str(left) + ',' + str(right) + '\n')
