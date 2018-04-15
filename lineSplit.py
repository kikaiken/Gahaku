import numpy as np

fs = 100 
k = np.sum(np.array([np.sin(np.pi * ((2 * i + 1) / (2 * fs))) for i in range(fs)]))

def lineSplit_sin(pre_data,data):
    cur_point = np.array(pre_data)
    next_point = np.array(data)
    diff_point = next_point - cur_point
    desired_point = np.empty(3)
    #print(diff_point)

    for n in range(fs):
        split_point = cur_point + diff_point/k * np.sin(np.pi*((2*n + 1)/(2*fs))) 
        #print(split_point)
        cur_point = split_point

        if n == 0:
            desired_point = split_point
            #print(desired_point)
        
        else:
            desired_point = np.vstack((desired_point, split_point))
            #print(desired_point)

    return desired_point.tolist()

def lineSplit_equaly(pre_data, data):
    cur_point = np.array(pre_data)
    next_point = np.array(data)
    diff_point = next_point - cur_point
    desired_point = np.empty(3)
    #print(diff_point)

    for n in range(fs):
        split_point = cur_point + diff_point * (n+1) /fs
        #print(split_point)

        if n == 0:
            desired_point = split_point
            #print(desired_point)
        
        else:
            desired_point = np.vstack((desired_point, split_point))
            #print(desired_point)

    return desired_point.tolist()