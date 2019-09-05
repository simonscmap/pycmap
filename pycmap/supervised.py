"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-07-26

Function: Class definitions for supervised ML regression models.
"""


import numpy as np
import pandas as pd
from .common import halt
from .trend import Trend
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import sklearn.preprocessing as preproc


class Supervised(object):
    """ 
    Abstracts the implementation of a generic supervised machine learning regression model.

    :param dataframe data: dataframe containing the training and test data sets.
    :param str target: target variable name (response function).
    :param bool standard: if true, feature data set is standardized.
    :param bool feature_interaction: if true, feature-pair interaction terms are added to the feature matrix.
    :param int cv: the number of folds in cross-validation.
    :param str test_size: the proportion of the data set to include in the test split (a float value between 0 to 1).
    """

    def __init__(
                self, 
                data, 
                target,
                standard,
                feature_interaction,
                cv,
                test_size,
                ):
        self.data = data
        self.target = target
        self.standard = standard
        self.feature_interaction = feature_interaction
        self.cv = cv
        self.test_size = test_size
        self.validateInit()
        self.__features = list(self.data.columns)
        self.__features.remove(self.target)
        self.__y = np.array(self.data[self.target])
        self.__X = np.array(self.data[self.__features])
        if self.standard:
            self.__X = preproc.StandardScaler().fit_transform(self.__X)
        if self.feature_interaction:
            if not self.standard: print('Consider standardizing the feature matrix (standard=True).')
            self.__X = preproc.PolynomialFeatures(include_bias=False).fit_transform(self.__X)    
        self.__XTrain, self.__XTest, self.__yTrain, self.__yTest = train_test_split(
                                                                                    self.__X , 
                                                                                    self.__y, 
                                                                                    test_size=self.test_size
                                                                                    )
                                                                                   

    def validateInit(self):
        msg = ''
        if not isinstance(self.data, pd.core.frame.DataFrame): msg += 'data should be a pandas dataframe object. \n'
        if not isinstance(self.target, str): msg += 'target should be string literal. \n'
        if not isinstance(self.cv, int): msg += 'cv should be an integer value. \n'
        if not isinstance(self.test_size, float): msg += 'test_size should be a float value. \n'
        if not self.target in list(self.data.columns): msg += 'target variable not found in the passed dataframe (case sensitive). \n'       
        if len(msg) > 0:        
            halt(msg)    
        return msg


    def split(self):
        """Splites the data set into train and test data sets."""
        return train_test_split(
                               self.__X , 
                               self.__y, 
                               test_size=self.test_size
                               )


    def learn_grid_search(self):
        """
        Train and score the model by an exhaustive search over specified parameter values.        
        """
        params = {
                #  'bootstrap': [True, False],
                #  'max_depth': [80, 90, 100, 110],
                 'max_features': ['auto', 'sqrt', 'log2'],
                #  'min_samples_leaf': [1, 2, 4],
                #  'min_samples_split': [2, 5, 10],
                 'n_estimators': [100, 200, 300]
                 }
        grid = GridSearchCV(estimator=self.model, param_grid=params, cv=self.cv, n_jobs = -1, verbose=2)
        grid.fit(self.XTrain, self.yTrain)
        self.grid = grid
        self.model = grid.best_estimator_
        self.score = grid.best_score_
        self.pred = grid.predict(self.XTest)
        self.mse = mean_squared_error(self.yTest, self.pred)


    def learn(self):
        """
        Train and score the model using the train and test data sets.        
        """
        self.model.fit(self.XTrain, self.yTrain)
        self.score = self.model.score(self.XTest, self.yTest)
        self.pred = self.model.predict(self.XTest)
        self.mse = mean_squared_error(self.yTest, self.pred)



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




class EnsembleTree(Supervised):
    """
    Instantiates the RandomForestRegressor class from sklearn library.
    More details here: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html


    :param int random_state: random state seed.
    :param int n_estimators : the number of trees in the forest.
    :param int/flots/str max_features : the number of features to consider when looking for the best split: 

        If int, then consider max_features features at each split.
        If float, then max_features is a fraction and int(max_features * n_features) features are considered at each split.
        If “auto”, then max_features=n_features (default).
        If “sqrt”, then max_features=sqrt(n_features).
        If “log2”, then max_features=log2(n_features).
        If None, then max_features=n_features.

    :param int max_depth : the maximum depth of the tree (default=None). If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.
    :param int/float min_samples_split : the minimum number of samples required to split an internal node:
  
        If int, then consider min_samples_split as the minimum number (default=2).
        If float, then min_samples_split is a fraction and ceil(min_samples_split * n_samples) are the minimum number of samples for each split.

    :param int n_jobs : the number of jobs to run in parallel.
    """
    def __init__(
                self,
                data,
                target,
                standard,
                feature_interaction,
                cv,
                test_size,
                random_state,
                n_estimators,
                max_features,
                max_depth, 
                min_samples_split,
                n_jobs
                ):
        super().__init__(data, target, standard, feature_interaction, cv, test_size)  
        self.random_state = random_state
        self.n_estimators = n_estimators   
        self.max_features = max_features
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.n_jobs = n_jobs    



    def sorted_feature_importance(self):
        """
        Sortes the features by their importance metric computed by the RanodomForest-based estimator.
        Returns a list of tuples containg the feautr names and their importances, sorted by importance values.
        """
        feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(self.features, self.model.feature_importances_)]
        return sorted(
                     feature_importances, 
                     key = lambda x: x[1], 
                     reverse = True
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


    def report(self):
        """A short log of the trained model performance."""
        print('************************************')
        print('Test size proportion: %.2f' % self.test_size)
        print('XTrain shape: ' + str(self.XTrain.shape))
        print('yTrain shape: ' + str(self.yTrain.shape))
        print('XTest shape: ' + str(self.XTest.shape))
        print('yTest shape: ' + str(self.yTest.shape))

        if hasattr(self, 'grid'):
            print('')
            print('Best Model Parameters:')
            print('')
            print(self.grid.best_params_)

        print('')
        print('Evaluation Results:')
        print('')
        print('\tRoot Mean Squared Error: %.2f' % np.sqrt(self.mse))
        print('\tModel Score: %.4f' % self.score)
        print('')
        print('Feature Importance:')
        print('')
        [print('\t{:20} Importance: {}'.format(*pair)) for pair in self.sorted_feature_importance()]                                    
        print('************************************')



class RandomForest(EnsembleTree):
    """
    Instantiates the RandomForestRegressor class from sklearn library.
    More details here: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
    """
    def __init__(
                self,
                data,
                target,
                standard=False,
                feature_interaction=False,
                cv=10,
                test_size=0.2,
                random_state=0,
                n_estimators=200,
                max_features='auto',
                max_depth=None, 
                min_samples_split=2,
                n_jobs=-1
                ):
        super().__init__(
                        data, 
                        target, 
                        standard,
                        feature_interaction,
                        cv,
                        test_size, 
                        random_state, 
                        n_estimators, 
                        max_features, 
                        max_depth, 
                        min_samples_split, 
                        n_jobs
                        )  

        self.model = RandomForestRegressor(
                                           random_state=self.random_state, 
                                           n_estimators=self.n_estimators, 
                                           max_features=self.max_features,
                                           max_depth=self.max_depth,
                                           min_samples_split=self.min_samples_split,
                                           n_jobs=self.n_jobs
                                           )  



class ExtraTrees(EnsembleTree):
    """
    Instantiates the ExtraTreesRegressor class from sklearn library.
    More details here: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesRegressor.html 
    """
    def __init__(
                self,
                data,
                target,
                standard=False,
                feature_interaction=False,
                cv=10,
                test_size=0.2,
                random_state=0,
                n_estimators=200,
                max_features='auto',
                max_depth=None, 
                min_samples_split=2,
                n_jobs=-1
                ):
        super().__init__(
                        data, 
                        target,
                        standard,
                        feature_interaction, 
                        cv,
                        test_size, 
                        random_state, 
                        n_estimators, 
                        max_features, 
                        max_depth, 
                        min_samples_split, 
                        n_jobs
                        )  

        self.model = ExtraTreesRegressor(
                                        random_state=self.random_state, 
                                        n_estimators=self.n_estimators, 
                                        max_features=self.max_features,
                                        max_depth=self.max_depth,
                                        min_samples_split=self.min_samples_split,
                                        n_jobs=self.n_jobs
                                        )  






        


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
                test_size=0.2,
                random_state=0,
                n_estimators=200,
                learning_rate=0.5,
                max_depth=3,
                loss='ls',
                n_jobs=-1
                ):
        super().__init__(data, target, test_size)  
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



