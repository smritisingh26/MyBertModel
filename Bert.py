#Importing necessary libraries
import ktrain
import tensorflow as tf
from ktrain import text
import pandas as pd
import numpy as np
import sys
import csv

#To ensure data is loaded without system error
maxInt=sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt=int(maxInt/10)

#Load the dataset into lists
titles=[]
labels=[]
with open("TFdata.csv",'r') as csvfile:
    reader=csv.reader(csvfile,delimiter=',')
    next(reader)
    for row in reader:
        labels.append(row[1])
        title=row[2]
        titles.append(title)

#Having loaded the data into lists, it is divided into training set and a test set.
train_size=int(len(titles)*0.8)
x_train=titles[0:train_size]
y_train=labels[0:train_size]
x_test=titles[train_size:]
y_test=labels[train_size:]

flairs=["Coronavirus","Politics","NonPolitical","AskIndia","BusinessorFinance","PolicyorEconomy","Photography","CAA","ScienceorTechnology","Reddiquette","Entertainment","Sports"]

(x_train,  y_train), (x_test, y_test), preproc = text.texts_from_array(x_train=x_train, y_train=y_train,
                                                                       x_test=x_test, y_test=y_test,
                                                                       class_names=flairs,
                                                                       preprocess_mode='bert',
                                                                       ngram_range=1,
                                                                       maxlen=350,
                                                                       max_features=35000)
model=text.text_classifier('bert', train_data=(x_train, y_train), preproc=preproc)

#Defining the model
learner = ktrain.get_learner(model, train_data=(x_train, y_train),batch_size=5)

#Training the model with 5 epochs and learning rate 0.05
learner.fit(2e-5, 5)

#Testing the model on test set
learner.validate(val_data=(x_test, y_test))

#Saving the model
predictor=ktrain.get_predictor(learner.model, preproc)
predictor.save('flairdetector')
print('*********************************MODEL SAVED***************************************************')

#Saving model to disk
predictor.save('/tmp/my_flairdetector')
print('*********************************MODEL SAVED TO DISK***************************************************')
