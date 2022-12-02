import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression as LogRegression
from sklearn import svm
from sklearn.metrics import classification_report

def RandomForest(X_train, y_train, X_test, y_test, test):

    # Create a Gaussian Classifier
    clf = RandomForestClassifier(n_estimators=100)

    # Train the model using the training sets y_pred=clf.predict(X_test)
    clf.fit(X_train,y_train)

    y_pred = clf.predict(X_test)

    # Prediction on the test.csv values
    rf_pred = clf.predict(test)

    # Classification report for model
    report = classification_report(y_test, y_pred)

    return report, rf_pred

def LogisticRegression(X_train, y_train, X_test, y_test, test):

    # Instantiate the model
    logistic_regression = LogRegression()

    # Fit the model using the training data
    logistic_regression.fit(X_train,y_train)

    # Use model to make predictions on test data
    y_pred = logistic_regression.predict(X_test)

    # Prediction on the test.csv values
    log_pred = logistic_regression.predict(test)

    # Classification report for model
    report = classification_report(y_test, y_pred)

    return report, log_pred

def SVM(X_train, y_train, X_test, y_test, test):

    # Create a svm Classifier
    clf = svm.SVC(kernel='linear') # Linear Kernel

    # Train the model using the training sets
    clf.fit(X_train, y_train)

    #Predict the response for test dataset
    y_pred = clf.predict(X_test)

    # Prediction on the test.csv values
    SVM_pred = clf.predict(test)

    # Classification report for model
    report = classification_report(y_test, y_pred)

    return report, SVM_pred


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Reading in the csv files into pandas dataframe
    test = pd.read_csv('titanic_test.csv')
    train = pd.read_csv('titanic_train.csv')

    # Cleaning up data
    # Dropping unnecessary columns
    test = test.drop(["Name", "Ticket", "Cabin"], axis = 1)
    train = train.drop(["Name", "Ticket", "Cabin"], axis = 1)

    # Filling in NaN Values
    test.fillna(test.mean(numeric_only=True).round(1), inplace=True)
    train.fillna(train.mean(numeric_only=True).round(1), inplace=True)
    train["Embarked"] = train["Embarked"].ffill()
    test["Embarked"] = test["Embarked"].ffill()

    # Converting categorical values to numerical values
    train['Sex'].replace(['male', 'female'],[0, 1], inplace=True)
    test['Sex'].replace(['male', 'female'],[0, 1], inplace=True)
    train['Embarked'].replace(['Q', 'S', 'C'],[0, 1, 2], inplace=True)
    test['Embarked'].replace(['Q', 'S', 'C'],[0, 1, 2], inplace=True)

    # Setting up train/test
    X = train[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']]
    y = train['Survived']
    testPred = test[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']]

    # Split the dataset into training (70%) and testing (30%) sets
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)

    # Random Forest
    Rf, RfPred = RandomForest(X_train, y_train, X_test, y_test, testPred)
    # Add to CSV file
    #test['Rf_Pred'] = RfPred
    #test.to_csv('titanic_test.csv', index=False)

    # Linear Regression
    LogReg, LogPred = LogisticRegression(X_train, y_train, X_test, y_test, testPred)
    # Add to CSV file
    #test['LogReg_Pred'] = LogPred
    #test.to_csv('titanic_test.csv', index=False)

    # SVM
    svmReport, svmPred = SVM(X_train, y_train, X_test, y_test, testPred)
    # Add to CSV file
    #test['SVM_Pred'] = svmPred
    #test.to_csv('titanic_test.csv', index=False)

    # Writing to output file
    f = open("output_titanic.txt", "w")
    f.write("Machine Learning Models:\n\n")
    f.write("Random Forest:\n\n")
    f.write(Rf)
    f.write("Linear Regression:\n\n")
    f.write(LogReg)
    f.write("SVM:\n\n")
    f.write(svmReport)
    f.close()