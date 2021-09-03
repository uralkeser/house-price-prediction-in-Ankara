


# House Price Prediction in Ankara
In this project we created a system that estimates prices on houses for sale in Ankara and evaluates the factors affecting prices. There are main 3 parts of the project:
Dataset creation (Data mining), Data cleaning and Organizing, and lastly Applying Machine Learning Models for price prediction.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```

## 1. Dataset creation (Data mining)
In this section we extracted data from the real estate website www.hurriyetemlak.com that is quite popular and public domain. Specifically, we extracted dataset of houses for sale, their prices and features such as house area, number of rooms, location etc. 
Two techniques Technique 1 and Technique 2 were adopted for this section. In Technique 1 we used BeautifulSoup and Requests libraries of python for web scraping and Panda library of python was used for Data cleaning part. In Technique 2, however, we used Scrapy library of python for web scraping and PySpark SQL for data cleaning. A dataset of distances from the center, to the nearest hospital and metro was obtained using GoogleMaps library for both techniques. Also, Machine Learning step is same for both techniques. Below you can find information about both techniques and how to run the respective codes. 

### Technique 1
In the file technique 1->dataset creation->scraping This will create a dataset "dataset.csv". 
```bash
python3 dataset_creator.py
``` 

Then, for distance technique 1->dataset creation->distance features This will create a dataset distanceset.csv (Do not forget to obtain your own GoogleMaps key). Thus, datasets were created and ready to data cleaning.
```bash
python3 distance_calculator.py
```


### Technique 2
In the file technique 2->dataset creation->crawling->crawling This will create a json file "links.json".
```bash
scrapy crawl links -o links.json
```
Then, for houses` data technique 2->dataset creation->crawling->crawling This will create a dataset dataset.csv
```bash
scrapy crawl houses -o dataset.csv
```
Let's mention the main differences of Scrapy vs. BeautifulSoup libraries here. 
Scrapy is extremely fast based on crawling algorithm and possible to scrape much larger dataset. But, it is a challenge to able to use and set up the settings correctly. On the other hand, BeautifulSoup is relatively slow since it works on each request. But, it is much easier to adopt than Scrapy. For more check [hexfox.com](https://bit.ly/3pWbTXy).
Distance dataset is same as technique 1. Thus, datasets were created and ready to data cleaning.

## 2. Data cleaning and Organizing
In this section, obtained dataset were cleaned and organized. Specifically, outliers and missing values were handled using different platforms for each techniques. 

### Technique 1
Go to technique 1->dataset cleaning This will create a clean dataset ready for ML application. 
```bash
python3 clean_dataset.py
```

### Technique 2
Go to technique 2->dataset cleaning This will also create a clean dataset ready for ML application. 
```bash
python3 cleaning.py
```
## 3. Machine Learning Models
In this section, we apply the ML models for price prediction using the clean data we processed previously. Install/import libraries such as matplotlib.pyplot and seaborn for plotting the results. Also, we used sklearn library for LinearRegression, Lasso, Ridge, RandomForestRegressor, KNeighborsRegressor, DecisionTreeRegressor, GradientBoostingRegressor, AdaBoostRegressor. Run "mlworks.py" code and you will observe the plots. We discussed the results with plots in "Results.pdf" file.
```bash
python3 mlworks.py
```

## Team

[Osman Ural Keser](https://github.com/uralkeser)

[Lebap Akmyradov](https://github.com/lebapakmyradow)

## License
[MIT](https://choosealicense.com/licenses/mit/)
