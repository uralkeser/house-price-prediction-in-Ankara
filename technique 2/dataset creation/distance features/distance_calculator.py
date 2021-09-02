#calculate shortest distance between given address and kizilay metro station


import googlemaps
import pandas as pd
from pandas import DataFrame
import time
start=time.time()

def nearestMetro(address, metro):
	distance=gm.distance_matrix(address,metro,mode='walking')
	word=str(distance)
	word=word[word.find('text')+8:word.find('km')]
	return word

gm=googlemaps.Client(key='AIzaSyA1NA3iK-ZZ4u6bJVqZZOr_IFRvobiT8mE')
kizilay = "Kizilay Cankaya/Ankara"
address = pd.read_csv('regions.csv')
hospital = pd.read_csv('hospitals.csv')
hospitalList=hospital.values.tolist()

#iterating over rows of address dataframe
distanceToHospital=[]
min=100
for index, row in address.iterrows():
	temp_address=str(row['Mahalle'])+' '+str(row['Semt'])+' '+'Ankara'
	for a in range(len(hospital)):
		try:
			km=float(nearestMetro(temp_address, hospitalList[a]))
			if km<=min:
				min=km
		except:
			min=100
	distanceToHospital.append(min)
	min=100
df3=DataFrame(distanceToHospital, columns=['hastane mesafe'])
distances=pd.read_csv('distanceset.csv')
frames=[distances,df3]
result=pd.concat(frames, axis=1)
result.to_csv('distanceset.csv', index=False)


#end of timer
end=time.time()
t=(end-start)/60
print(str(t)+' time in min')
