import numpy as np
from util import load, build_vocabulary, get_bags_of_sifts
from classifiers import nearest_neighbor_classify, svm_classify
import pickle

#Starter code prepared by Borna Ghotbi, Polina Zablotskaia, and Ariel Shann for Computer Vision
#based on a MATLAB code by James Hays and Sam Birch

#For this assignment, you will need to report performance for sift features on two different classifiers:
# 1) Bag of sift features and nearest neighbor classifier
# 2) Bag of sift features and linear SVM classifier

#For simplicity you can define a "num_train_per_cat" vairable, limiting the number of
#examples per category. num_train_per_cat = 100 for intance.

#Sample images from the training/testing dataset. 
#You can limit number of samples by using the n_sample parameter.

print('Getting paths and labels for all train and test data\n')
train_image_paths, train_labels = load("sift/train")
test_image_paths, test_labels = load("sift/test")
       

''' Step 1: Represent each image with the appropriate feature
 Each function to construct features should return an N x d matrix, where
 N is the number of paths passed to the function and d is the 
 dimensionality of each image representation. See the starter code for
 each function for more details. '''

        
print('Extracting SIFT features\n')
#If you want to avoid recomputing the features while debugging the
#classifiers, you can either 'save' and 'load' the extracted features
#to/from a file.

# Use precomputed models
is_using_saved = not True

VOCAB_SIZE = 1000 # k in KNN for BoW of SIFT images
K_CLASSIFIER = 300 # k in KNN for classifier.
C_PEN_CLASSIFIER = 2 # SVM penality parameter

if(not is_using_saved):
    print("Creating new BoW representation.")
    kmeans = build_vocabulary(train_image_paths, vocab_size=VOCAB_SIZE)
    train_image_feats = get_bags_of_sifts(train_image_paths, kmeans, 'train')
    test_image_feats = get_bags_of_sifts(test_image_paths, kmeans, 'test')

else:
    print("Using saved BoW representation.")
    kmeans = pickle.load(open(f"models/kmeans-vocab-{VOCAB_SIZE}.pkl", "rb"))
    train_image_feats = pickle.load(open(f"models/train-features-{VOCAB_SIZE}.pkl", "rb"))
    test_image_feats = pickle.load(open(f"models/test-features-{VOCAB_SIZE}.pkl", "rb"))


''' Step 2: Classify each test image by training and using the appropriate classifier
 Each function to classify test features will return an N x l cell array,
 where N is the number of test cases and each entry is a string indicating
 the predicted one-hot vector for each test image. See the starter code for each function
 for more details. '''

# == KNN prediction ==
print('Using nearest neighbor classifier to predict test set categories\n')
#: YOU CODE nearest_neighbor_classify function from classifers.py
pred_labels_knn = nearest_neighbor_classify(train_image_feats, train_labels, test_image_feats, K_CLASSIFIER)

# == SVM prediction ==
print('Using support vector machine to predict test set categories\n')
#: YOU CODE svm_classify function from classifers.py
pred_labels_svm = svm_classify(train_image_feats, train_labels, test_image_feats, C_PEN_CLASSIFIER)



print('---Evaluation---\n')
# Step 3: Build a confusion matrix and score the recognition system for 
#         each of the classifiers.
# TODO: In this step you will be doing evaluation. 
# 1) Calculate the total accuracy of your model by counting number
#   of true positives and true negatives over all. 
# 2) Build a Confusion matrix and visualize it. 
#   You will need to convert the one-hot format labels back
#   to their category name format.

# == Compute classification success rate. ==
knn_success = np.sum(test_labels == pred_labels_knn) / len(test_labels)
svm_success = np.sum(test_labels == pred_labels_svm) / len(test_labels)

print(f"KNN success rate: {knn_success}")
print(f"SVM success rate: {svm_success}")



# Interpreting your performance with 100 training examples per category:
#  accuracy  =   0 -> Your code is broken (probably not the classifier's
#                     fault! A classifier would have to be amazing to
#                     perform this badly).
#  accuracy ~= .10 -> Your performance is chance. Something is broken or
#                     you ran the starter code unchanged.
#  accuracy ~= .40 -> Rough performance with bag of SIFT and nearest
#                     neighbor classifier. 
#  accuracy ~= .50 -> You've gotten things roughly correct with bag of
#                     SIFT and a linear SVM classifier.
#  accuracy >= .60 -> You've added in spatial information somehow or you've
#                     added additional, complementary image features. This
#                     represents state of the art in Lazebnik et al 2006.
#  accuracy >= .85 -> You've done extremely well. This is the state of the
#                     art in the 2010 SUN database paper from fusing many 
#                     features. Don't trust this number unless you actually
#                     measure many random splits.
#  accuracy >= .90 -> You used modern deep features trained on much larger
#                     image databases.
#  accuracy >= .96 -> You can beat a human at this task. This isn't a
#                     realistic number. Some accuracy calculation is broken
#                     or your classifier is cheating and seeing the test
#                     labels.
