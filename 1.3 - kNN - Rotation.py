#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import division # backward compatibility for python2
#from numpy import array
import numpy as np
import pandas as pd
import scipy.special
import operator
import random
#import sys
#library for plotting arrays
from scipy import ndimage
import matplotlib.pyplot as plt
# A particularly interesting backend, provided by IPython, is the inline backend. 
# This is available only for the Jupyter Notebook and the Jupyter QtConsole. 
# It can be invoked as follows: %matplotlib inline
# With this backend, the output of plotting commands is displayed inline 
# within frontends like the Jupyter notebook, directly below the code cell that produced it. 
# The resulting plots are inside this notebook, not an external window.
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# datasets to read
# you can change these when trying out other datasets
train_file = "mnist_train.csv"
test_file = "mnist_test.csv"


# In[3]:


#load the mnist training data CSV file into a list
#train_data_file = open("mnist/mnist_train_100.csv", 'r') # open and read the 100 instances in the text file
train_data_file = open(train_file, 'r')
train_data_list = train_data_file.readlines() # read all lines into memory 
train_data_file.close() 
print("train set size: ", len(train_data_list))

#testing the network
#load the mnist test data CSV file into a list
test_data_file = open(test_file, 'r') # read the file 
test_data_list = test_data_file.readlines()
test_data_file.close()
print("test set size: ", len(test_data_list))


# In[4]:


#Within our class we now need code for each of the components of k-NN.
#First, let's create a method that will measure the distance between two vectors.
def euclidean(instance1, instance2):
        '''
        Calculates euclidean distance between two instances of data
        instance1 will be a List of Float values
        instance2 will be a List of Float values
        length will be an Integer denoting the length of the Lists
        '''
        distance = 0
        for val1, val2 in zip(instance1, instance2):            
            distance += pow((val1 - val2), 2)
        
        distance = pow(distance, 1/2)
             
              
        return 1 / (1+ distance)
    

def manhattan(instance1, instance2):
        '''
        Calculates manhattan distance between two instances of data
        instance1 will be a List of Float values
        instance2 will be a List of Float values
        length will be an Integer denoting the length of the Lists
        '''
        distance = 0
        for val1, val2 in zip(instance1, instance2):
            distance += abs(val1 - val2)      
              
        return 1 / (1+ distance)
    
def dot_product(instance1, instance2):
        '''
        Calculates dot product between two instances 
        instance1 will be a List of Float values
        instance2 will be a List of Float values
        length will be an Integer denoting the length of the Lists
        '''
        return np.dot(instance1, instance2)


# In[5]:


#Finally, we can test to see how many of the test instances we got correct
def accuracy(results):
       correct = 0
       for predict, target in results:
           
           if predict == target:
               correct += 1
       return (correct/float(len(results))) * 100.0


# In[6]:


class kNN:
    """
    Parameters
    X_train, Y_train : list
    these consists of the training set feature values and associated class labels
    k : int
    specify the number of neighbours
    sim : literal
    specify the name of the similarity metric (e.g. manhattan, eucliedean)
    weighted : Boolean
    specify the voting strategy as weighted or not weighted by similarity values
  
    Attributes
    -----------  
    Results : list
      Target and predicted class labels for the test data.    
    """


    def __init__(self, X_train, Y_train, k=3, sim=manhattan, weighted=False):
        self.X_train = X_train
        self.Y_train = Y_train
        
        if k <= len(self.X_train):
            self.k = k # set the k value for neighbourhood size
        else:
            self.k = len(self.X_train) # to ensure the get_neighbours dont crash
    
        self.similarity = sim # specify a sim metric that has been pre-defined e.g. manhattan or euclidean
        
        self.weighted = weighted # boolean to choose between weighted / unweighted majority voting
        
        #store results from testing 
        self.results= []
        
    #With k-NN, we are interested in finding the k number of points with the greatest similarity 
    # to the the query or test instance.
    def get_neighbours(self, test_instance):
        '''
        Locate most similar neighbours 
        X_train will be a containing features (Float) values (i.e. your training data)
        Y_train will be the corresponding class labels for each instance in X_train
        test_instance will be a List of Float values (i.e. a query instance)
        '''
        similarities = [] # collection to store the similarities to be computed

        for train_instance, y in zip(self.X_train, self.Y_train): #for each member of the training set
            sim = self.similarity(test_instance, train_instance) #calculate the similarity to the test instance
            
            similarities.append((y, sim)) #add the actual label of the example and the computed similarity to a collection 
        #print(distances)
        similarities.sort(key = operator.itemgetter(1), reverse = True) #sort the collection by decreasing similarity
        neighbours = [] # holds the k most similar neighbours
        for x in range(self.k): #extract the k top indices of the collection for return
            neighbours.append(similarities[x])

        return neighbours

    # given the neighbours make a prediction
    # the boolean parameter when set to False will use unweighted majority voting; otherwise weighted majority voting
    # weighting can be helpful to break any ties in voting
    def predict(self, neighbours):
        '''
        Summarise a prediction based upon weighted neighbours calculation
        '''
        class_votes = {}
        for x in range(len(neighbours)):
            response = neighbours[x][0]
            if response in class_votes:
                class_votes[response] += (1-self.weighted) + (self.weighted * neighbours[x][1]) #if not weighted simply add 1
                #class_votes[response] += [1, neighbours[x][1]][weighted == True] 
              
            else:
                class_votes[response] = (1-self.weighted) + (self.weighted * neighbours[x][1])
                #class_votes[response] = [1, neighbours[x][1]][weighted == True] 
                
        #print(class_votes)
        sorted_votes = sorted(class_votes, key = lambda k: (class_votes[k], k), reverse = True)
        #print(sorted_votes)
        return sorted_votes[0]
    
    #iterate through all the test data to calculate accuracy
    def test(self, X_test, Y_test):
        self.results = [] # store the predictions returned by kNN

        for test_instance, target_label in zip(X_test, Y_test):
            neighbours = self.get_neighbours(test_instance)
            predict_label = self.predict(neighbours)
            self.results.append([predict_label, target_label])
            #print('> predicted = ', result,', actual = ', test_label)
    


# In[7]:



def rotate_image_anticlockwise(inputs, degree):
  
    ## create rotated variations
    # rotated anticlockwise by x degrees
    inputs_plusx_img = scipy.ndimage.interpolation.rotate(inputs.reshape(28,28), degree, cval=0.01, order=1, reshape=False)
    new_inputs1 = inputs_plusx_img.reshape(784)
    return new_inputs1

def rotate_image_clockwise(inputs, degree):
  
    # rotated clockwise by x degrees
    inputs_minusx_img = scipy.ndimage.interpolation.rotate(inputs.reshape(28,28), -degree, cval=0.01, order=1, reshape=False)
    new_inputs1 = inputs_minusx_img.reshape(784)
    
    return (new_inputs1)


# In[8]:


def rotate_preprocess_data(Xy, degree):
    X=[]
    y=[]
    for instance in Xy:
        # split the record by the ',' commas
        all_values = instance.split(',')
        # scale and shift the inputs
        inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        # create the target output values (all 0.01, except the desired label which is 0.99)
        # all_values[0] is the target label for this record
        targets=all_values[0]
        if len(X) % 2 == 0:
            X.insert(len(X), rotate_image_anticlockwise(inputs,degree))
            y.insert(len(y), targets)
        else:
            X.insert(len(X), rotate_image_clockwise(inputs,degree))
            y.insert(len(y), targets)
    pass
    return(X,y)
pass

def preprocess_data(Xy):
    X=[]
    y=[]
    for instance in Xy:
        # split the record by the ',' commas
        all_values = instance.split(',')
        # scale and shift the inputs
        inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        # all_values[0] is the target label for this record
        targets=all_values[0]
        X.insert(len(X), inputs)
        #print(len(y), targets)
        y.insert(len(y), targets)
    pass
    return(X,y)
pass


# In[9]:


np.random.seed(4)
mini_training_data = np.random.choice(train_data_list, 500, replace=False)
degreeArray = [5,10,60,90,120]
X_test, Y_test = preprocess_data(test_data_list[:100])

accuracies = []
knn_list = []
for i in range(len(degreeArray)):
    X_train, Y_train = rotate_preprocess_data(mini_training_data[:100], degreeArray[i])
    knn = kNN(X_train, Y_train, 3, manhattan, True)
    knn_list.append(knn)
pass
print(knn_list)
for knn in knn_list:
    knn.test(X_test, Y_test)
    accuracies.append(accuracy(knn.results))
pass
   
print(accuracies)


# In[11]:


N = len(degreeArray) # this is the number of results we want to plot pn the x-axis
ind = np.arange(N) 

performance1 = accuracies[0]
performance2 = accuracies[1]

width = 0.35 # width of the bar      
plt.bar(ind, performance1, width, label='Unweighted')
plt.bar(ind + width, performance2, width, label='Weighted')

plt.ylabel('Accuracy')
plt.xlabel('Rotation Degrees')
plt.title('kNN performance with increasing')

plt.xticks(ind + width / 2, degreeArray)
plt.legend(loc='lower right')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




