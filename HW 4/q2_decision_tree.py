import pandas as pd
from scipy.stats import entropy as ent
import numpy as np

## To Do: Write the entropy(label) function
## Should find the information entropy of dataset (T) with class "label" i.e. Info(T)
def entropy(dataset, label):
    label_list = dataset[label].tolist()
    value,counts = np.unique(label_list, return_counts=True)
    return ent(counts, base=2)

## To Do: Write the information_gain(feature, label) function
## Should find the information gain of "feature"(X) on dataset (T) with class "label" i.e. Gain(X,T)
def information_gain(dataset, feature, label):

    # Calculate original entropy on the target column
    original_entropy = entropy(dataset, label)

    # Find unque values in the split column
    values = dataset[feature].unique()

    # Make two subsets of the data, based on the unique values
    left_split = dataset[dataset[feature] == values[0]]
    right_split = dataset[dataset[feature] == values[1]]

    # Loop through the splits and calculate the subset entropies
    to_subtract = 0
    for subset in [left_split, right_split]:
        prob = (subset.shape[0] / dataset.shape[0]) 
        to_subtract += prob * entropy(subset,label)
    
    # Return information gain
    return original_entropy - to_subtract

## To Do: Fill split(dataset, feature) function
## Should split the dataset on a feature
## Implementing a little differently, returns a dictionary with the information gains
def split(dataset, label):
    columns = ["COLOR", "SIZE", "ACT", "AGE"]

    #Intialize an empty dictionary for information gains
    information_gains = {}

    #Iterate through each column name in our list
    for col in columns:
        #Find the information gain for the column
        info_gain = information_gain(dataset, col, label)
        #Add the information gain to our dictionary using the column name as the ekey                                         
        information_gains[col] = info_gain

    #return the dictionary
    return information_gains

## To Do: Fill find_best_split(dataset, label) function
## Should find the best feature to split the dataset on
## Should return best_feature, best_gain
def find_best_split(dataset, label):
    ## TO DO: Find the best feature to split the dataset
    info_gains = split(dataset,label)
    
    # Get the best fature/value
    best_feature = max(info_gains, key=info_gains.get)
    best_gain = info_gains[best_feature]
    return best_feature, best_gain


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = pd.read_csv('balloons.csv')

    best_feature, best_gain = find_best_split(data, "INFLATED")
    f = open("output_balloons.txt", "w")
    f.write("The Best Feature is {} with a Gain of : {}".format(best_feature, best_gain))
    f.close()