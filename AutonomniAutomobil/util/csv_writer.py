#Author: Nina Marjanovic


def write_data(f, left_distance, right_distance):
    if left_distance is False:
        left_distance = -1
    if right_distance is False:
        right_distance = -1
    f.write(str(left_distance) + ',' + str(right_distance) + ',1,0,0\n')