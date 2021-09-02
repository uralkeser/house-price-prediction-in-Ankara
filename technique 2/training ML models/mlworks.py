import math
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


def removeColumn(ds,name): # to remove a cloumn given by parameter and return new dataframe, removed column list
    dropedColumn = list(ds[name])
    ds = ds.drop([name], axis=1)
    return ds, dropedColumn

def dataTransforming():
    dataset = pd.read_csv('ds.csv')
    dataset, ids = removeColumn(dataset,'İlan no')

    y = dataset['Fiyat']
    X = dataset.drop('Fiyat', axis=1)

    X = pd.get_dummies(X, columns = ["Yapının Durumu", "Eşya Durumu", "Isınma Tipi"])
    X = pd.get_dummies(X, columns = ["Semt"])

    columns = X.columns
    columns = list(columns)
    
    scaler1 = StandardScaler()
    scaler1.fit(X)
    X = scaler1.transform(X)
    
    
    X = pd.DataFrame(X)
    for col, realcol in zip(X.columns, columns) :
        X = X.rename(columns={col: realcol})

    return X, y, ids

def trainModel(model, X, y):
    errors = []
    kf = KFold(n_splits=10, shuffle = True, random_state = 8)

    for train_index, test_index in kf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        MAE = mean_absolute_error(y_test, y_pred)
        errors.append(MAE)

    return errors

def getResults(X,y):
    models_reg = [LinearRegression(), Lasso(), Ridge(), KNeighborsRegressor(), DecisionTreeRegressor(),
          GradientBoostingRegressor(warm_start='True',n_estimators=50), RandomForestRegressor(warm_start='True'), AdaBoostRegressor(n_estimators=50)]

    for model in models_reg:
        errors = trainModel(model, X ,y)
        print(type(model).__name__)
        print("%.2f\n" %np.mean(errors))
        #print(model)
        # VisualizePrediction(model, X, y)
        VisualizeCoefficient(model, X)

def VisualizeCoefficient(model, X):
    try:
        coefs = pd.Series(model.coef_, index = X.columns)
        print(type(model).__name__ , str(sum(coefs != 0)) , " features and eliminated the other " +  str(sum(coefs == 0)) + " features")
        imp_coefs = pd.concat([coefs.sort_values().head(12),coefs.sort_values().tail(13)])
        imp_coefs.plot(kind = "barh")
        title = 'Coefficients in the ' + type(model).__name__ 
        plt.title(title)
        plt.show()
    except:
        print('there is no coefficient')
    
    try:
        coefs = pd.Series(model.feature_importances_, index = X.columns)
        imp_coefs = pd.concat([coefs.sort_values().head(12),coefs.sort_values().tail(13)])
        imp_coefs.plot(kind = "barh")
        title = 'Importance in the ' + type(model).__name__ 
        plt.title(title)
        plt.show()    
    except:
        print('there is no importance')
    
def VisualizePrediction(model, X, y):
    # print(type(model).__name__)
    predicted = cross_val_predict(model, X, y, cv=10)
    fig, ax = plt.subplots()
    ax.scatter(y, predicted, edgecolors=(0, 0, 0))
    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
    ax.set_xlabel('Real')
    ax.set_ylabel('Predicted')
    title = type(model).__name__ 
    plt.title(title)
    plt.show()      

def VisualizeCorrelationsAll(X):
    corr = X.corr()
    sns.heatmap(corr,cmap="YlGnBu")
    plt.show()        
        
def VisualizeCorrelationsOnebyOne(X,y):
    for col in X.columns:
        plt.scatter(X[col], y, c= 'red')
        plt.title("Outliers")
        plt.xlabel(col)
        plt.ylabel("Fiyat")
        plt.show()

def showPricePLot(y):
    sns.distplot(np.log(y))
    plt.show()

def showLogPredictions(X,y,links):
    predicted = cross_val_predict(RandomForestRegressor(warm_start='True'), X, np.log(y), cv=10)
    lst = []
    for i in predicted:
        lst.append(round(math.exp(i)))
    d = {'real':list(y), 'predicted':lst}
    pred = pd.DataFrame(data=d)
    pred['fark'] = pred['real'] - pred['predicted']
    pred['linkler'] = links
    #print(pred)
    pred.to_csv('sonuclar_log.csv',index=False)

def showPredictions(X,y,links):
    predicted = cross_val_predict(RandomForestRegressor(warm_start='True'), X, y, cv=10)
    lst = []
    for i in predicted:
        lst.append(int(round(i)))
    d = {'real':list(y), 'predicted':lst}
    pred = pd.DataFrame(data=d)
    pred['fark'] = pred['real'] - pred['predicted']
    pred['linkler'] = links
    #print(pred)
    pred.to_csv('sonuclar.csv',index=False)  

x, y, ids = dataTransforming()
getResults(x,y)
# VisualizeCorrelationsOnebyOne(x,y)
# VisualizeCorrelationsAll(x)
    
