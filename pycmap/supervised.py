"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-07-26

Function: Class definitions for supervised ML regression models.
"""


import numpy as np
import pandas as pd
from .common import halt
from .trend import Trend
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn.metrics import mean_squared_error




class Supervised(object):
    """ 
    Abstracts the implementation of a generic supervised machine learning regression model.

    :param dataframe data: dataframe containing the training and test data sets.
    :param str target: target variable name (response function).
    :param str testSize: the proportion of the data set to include in the test split (a float value between 0 to 1).
    """

    def __init__(
                self, 
                data, 
                target,
                testSize,
                ):
        self.data = data
        self.target = target
        self.testSize = testSize
        self.validateInit()

        self.__features = list(self.data.columns)
        self.__features.remove(self.target)
        self.__y = np.array(self.data[self.target])
        self.__X = np.array(self.data[self.__features])
        self.__XTrain, self.__XTest, self.__yTrain, self.__yTest = train_test_split(
                                                                                    self.__X , 
                                                                                    self.__y, 
                                                                                    test_size=self.testSize
                                                                                    )
                                                                                   

    def validateInit(self):
        msg = ''
        if not isinstance(self.data, pd.core.frame.DataFrame): msg += 'data should be a pandas dataframe object. \n'
        if not isinstance(self.target, str): msg += 'target should be string literal. \n'
        if not isinstance(self.testSize, float): msg += 'testSize should be a float value. \n'
        if not self.target in list(self.data.columns): msg += 'target variable not found in the passed dataframe (case sensitive). \n'       
        if len(msg) > 0:        
            halt(msg)    
        return msg


    def split(self):
        """Splites the data set into train and test data sets."""
        return train_test_split(
                               self.__X , 
                               self.__y, 
                               test_size=self.testSize
                               )


    def learn(self):
        """
        Train and score the model using the train and test data sets.        
        """
        self.model.fit(self.XTrain, self.yTrain)
        self.r2 = self.model.score(self.XTest, self.yTest)
        self.pred = self.model.predict(self.XTest)
        self.mse = mean_squared_error(self.yTest, self.pred)


    def report(self):
        """A short log of the trained model performance."""
        print('************************************')
        print('Test size proportion: %.2f' % self.testSize)
        print('XTrain shape: ' + str(self.XTrain.shape))
        print('yTrain shape: ' + str(self.yTrain.shape))
        print('XTest shape: ' + str(self.XTest.shape))
        print('yTest shape: ' + str(self.yTest.shape))
        print('')
        print('Evaluation Results:')
        print('')
        print('\tRoot Mean Squared Error: %.2f' % np.sqrt(self.mse))
        print('\tEvaluation Using split (R^2 on test set): %.4f' % self.r2)
        # print('\tfeature_importances: ', list(zip(self.features, self.model.feature_importances_)) )
        print('************************************')


    @property
    def features(self):
        return self.__features  
    @features.setter
    def features(self, features):
        self.__features = features

    @property
    def X(self):
        return self.__X   
    @X.setter
    def X(self, X):
        self.__X = X        

    @property
    def y(self):
        return self.__y  
    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def XTrain(self):
        return self.__XTrain  
    @XTrain.setter
    def XTrain(self, XTrain):
        self.__XTrain = XTrain        

    @property
    def XTest(self):
        return self.__XTest  
    @XTest.setter
    def XTest(self, XTest):
        self.__XTest = XTest   

    @property
    def yTrain(self):
        return self.__yTrain  
    @yTrain.setter
    def yTrain(self, yTrain):
        self.__yTrain = yTrain           

    @property
    def yTest(self):
        return self.__yTest  
    @yTest.setter
    def yTest(self, yTest):
        self.__yTest = yTest   







class RandomForest(Supervised):
    """
    Instantiates the RandomForestRegressor class from sklearn library.
    More details here: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html


    :param int random_state: random state seed.
    :param int n_estimators : the number of trees in the forest.
    :param int n_jobs : the number of jobs to run in parallel.
    """
    def __init__(
                self,
                data,
                target,
                testSize=0.2,
                random_state=0,
                n_estimators=200,
                n_jobs=-1
                ):
        super().__init__(data, target, testSize)  
        self.random_state = random_state
        self.n_estimators = n_estimators   
        self.n_jobs = n_jobs    


        self.model = RandomForestRegressor(
                                           random_state=self.random_state, 
                                           n_estimators=self.n_estimators, 
                                           n_jobs=self.n_jobs
                                           )  

    def plot_feature_importance(self):
        """
        This method works for forest ensemble models.
        Goes through the trees and sort the features (predictors) by their importance. 
        """
        std = np.std([tree.feature_importances_ for tree in self.model.estimators_], axis=0)
        indices = np.argsort(self.model.feature_importances_)[::-1]
        feature=[]
        for i in range(0, len(indices)):
            feature.append(self.features[indices[i]])
        importance = self.model.feature_importances_[indices]    
        err = std[indices]
        go = Trend(pd.DataFrame({}), self.target).graph_obj()
        go.x = feature
        go.y = importance
        go.yErr = err
        go.title = 'Predictors For ' + self.target
        go.timeSeries = False
        go.ylabel = 'Feature Importance'
        go.render()

         

class ExtraTrees(Supervised):
    """
    Instantiates the ExtraTreesRegressor class from sklearn library.
    More details here: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesRegressor.html 


    :param int random_state: random state seed.
    :param int n_estimators : the number of trees in the forest.
    :param int n_jobs : the number of jobs to run in parallel.
    """
    def __init__(
                self,
                data,
                target,
                testSize=0.2,
                random_state=0,
                n_estimators=200,
                n_jobs=-1
                ):
        super().__init__(data, target, testSize)  
        self.random_state = random_state
        self.n_estimators = n_estimators   
        self.n_jobs = n_jobs    


        self.model = ExtraTreesRegressor(
                                        random_state=self.random_state, 
                                        n_estimators=self.n_estimators, 
                                        n_jobs=self.n_jobs
                                        )  

    def plot_feature_importance(self):
        """
        This method works for forest ensemble models.
        Goes through the trees and sort the features (predictors) by their importance. 
        """
        std = np.std([tree.feature_importances_ for tree in self.model.estimators_], axis=0)
        indices = np.argsort(self.model.feature_importances_)[::-1]
        feature=[]
        for i in range(0, len(indices)):
            feature.append(self.features[indices[i]])
        importance = self.model.feature_importances_[indices]    
        err = std[indices]
        go = Trend(pd.DataFrame({}), self.target).graph_obj()
        go.x = feature
        go.y = importance
        go.yErr = err
        go.title = 'Predictors For ' + self.target
        go.timeSeries = False
        go.ylabel = 'Feature Relative Importance'
        go.render()


class GradientBoost(Supervised):
    """
    Instantiates the GradientBoostingRegressor class from sklearn library.
    More details here: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html

    :param int random_state: random state seed.
    :param int n_estimators : the number of trees in the forest.
    :param float learning_rate : learning rate shrinks the contribution of each tree by learning_rate. There is a trade-off between learning_rate and n_estimators.
    :param int max_depth : maximum depth of the individual regression estimators. The maximum depth limits the number of nodes in the tree. Tune this parameter for best performance; the best value depends on the interaction of the input variables.
    :param str loss : loss function to be optimized. ‘ls’ refers to least squares regression. ‘lad’ (least absolute deviation) is a highly robust loss function solely based on order information of the input variables. ‘huber’ is a combination of the two. ‘quantile’ allows quantile regression (use alpha to specify the quantile).
    """
    def __init__(
                self,
                data,
                target,
                testSize=0.2,
                random_state=0,
                n_estimators=200,
                learning_rate=0.5,
                max_depth=3,
                loss='ls',
                n_jobs=-1
                ):
        super().__init__(data, target, testSize)  
        self.random_state = random_state
        self.n_estimators = n_estimators   
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.loss = loss


        self.model = GradientBoostingRegressor(
                                        random_state=self.random_state, 
                                        n_estimators=self.n_estimators, 
                                        learning_rate=self.learning_rate,
                                        max_depth=self.max_depth,
                                        loss=self.loss
                                        )  



