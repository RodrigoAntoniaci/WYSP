#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import distance


# In[ ]:


class PlayIt():
    def __init__(self, dataset=None,user_choice=None,metric='euclidean',n_results=20):
        '''
        Initializing the class to calculate distance between games dataset        
        Parameters
        ----------
        dataset : pandas.DataFrame
            Dataset utilized in the analysis
        user_choice: dict
            Dictionary with the user choices 
        metric : str or function, optional
            The distance metric to use. The distance function can
            be 'braycurtis', 'canberra', 'chebyshev', 'cityblock',
            'correlation', 'cosine', 'dice', 'euclidean', 'hamming',
            'jaccard', 'jensenshannon', 'kulsinski', 'mahalanobis', 'matching',
            'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',
            'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'
            
        n_results : Number of similar games you want to see
        
        '''
        self.user_choice = user_choice
        self.dataset = dataset
        self.themes = ['Action', 'Adult','Adventure', 'Baseball', 'Battle', 'Board',
                      'Card','Casino', 'Compilation','Editor', 'Educational', 'Episodic', 'Fighting', 
                      'First-Person', 'Flight','Golf', 'Hardware', 'Hunting', 'Music', 'Other', 'Party', 
                      'Pet', 'Pinball', 'Platformer', 'Productivity', 'Puzzle', 'RPG', 'Racing', 'Shooter',
                      'Simulation','Sports', 'Strategy', 'Trivia', 'Virtual', 'Word', 'Wrestling']

        self.platforms = ['Sony', 'Microsoft','Nintendo','Portable', 'Old_Consoles', 'Mobile', 
                         'PC', 'Others_Plat','Playstation_4', 'Xbox_One','Wii_U']

        self.target_columns = ['old_game', 'critic_high_score'] + self.themes + self.platforms
        
        self.n_results = n_results
        
        self.metric = str(metric)
    
    def handle_result(self,result):
        
        result = result.iloc[-1]
        
        similar_games = result.sort_values()[1:].head(self.n_results)
        
        return self.dataset[['title','release_date','score','score_phrase','editors_choice','all_plat','genre','url']].iloc[similar_games.index]
        
    def calc_dist(self):
        
        calc_dist = pd.DataFrame(distance.squareform(distance.pdist(self.dataset.loc[:, self.target_columns], metric=self.metric)),
                              columns=self.dataset.index, 
                              index=self.dataset.title)
        return calc_dist
    
    def play_it(self):
        '''
        Function to calculate distance between user's input and the rest of the selected dataset
        '''
        new_line = pd.DataFrame.from_dict(self.user_choice)

        self.dataset = self.dataset.append(new_line,ignore_index=True)

        result = self.calc_dist()

        return self.handle_result(result)