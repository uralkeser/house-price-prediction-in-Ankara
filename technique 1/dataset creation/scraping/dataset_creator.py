import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd


def getTheNumberOfPages():	#get how many pages including house ads
	site ='https://www.hurriyetemlak.com/ankara-satilik?page=1'
	links = bs(rq.get(site).content,"html.parser").find_all('a')
	total_page = 0
	counter = 0

	for link in links:
		if str(link).find('tabindex')!=-1 :
			counter += 1
			if counter == 8:
				total_page = int(str(link)[(str(link).find('>')+1):str(link).rfind('<')]  )
				
	return total_page

def getLinks(total_page): #returns an array of links for house ads

	i = 0
	advert = ['tmp']
	for j in range(1,total_page+1):
		site = 'https://www.hurriyetemlak.com/ankara-satilik?page='+str(j)
		print('page:',j)
		links = bs(rq.get(site).content,"html.parser").find_all('a')
		for link in links:
			if str(link.get('href')).find('ankara')!=-1 :
				temp = str(link.get('href'))
				temp2 = 'https://www.hurriyetemlak.com'+temp
				if advert[i] != temp2:
					advert.append(temp2)
					print(temp2)
					i = i + 1

	return advert

def removeRedundantAdverts(advert): #removes adverts
	
	temp = ''
	advert_range = len(advert)
	k = 0

	while k<advert_range:
		temp = advert[k]
		temp = temp[len(temp)-2:]
		try:
			isinstance(int(temp), int)
		except:
			advert.remove(advert[k])
			advert_range-=1
			k=k-1
		k+=1

	return advert

def getFeatures(advert,features,values): #return houses features and feature values

	links = bs(rq.get(advert).content,"html.parser").find_all('span')

	# to parse data used `009b093a` as a keyword. it changes very often. need to check website`s html to find `<span data-v-009b093a=` like that.

	for link in links:
		if str(link).find('txt') != -1 and str(link).find('Cephe') == -1: #ignores 'Cephe'. they make troubles 
			features.append(str(link)[(str(link).find('>')+1):str(link).rfind('<')]) # to get features' names
		if str(link).find('<span data-v-009b093a=') != -1:
			if str(link).rfind('<span data-v-009b093a=') == str(link).find('<span data-v-009b093a=') and str(link).find('<span data-v-009b093a="">, </span>')==-1 and str(link).find('Batı')==-1 and str(link).find('Doğu')==-1 and str(link).find('Kuzey')==-1 and str(link).find('Güney')==-1 and str(link).find('/sup')==-1:	
				values.append(str(link)[ ( str(link).find('>')+1 ) : str(link).rfind('<') ]) # to get features' values
	return	features,values

def getProvince(advert,features,values): #to get region and neighborhood 
	
	link3 = bs(rq.get(advert).content,"html.parser").find_all('ul',{'class':'short-info-list'}) # get Province value
	province = str(link3).split('</li> <li data-v-009b093a="">')
	
	values.append(province[1].strip())
	values.append(province[2].strip())
	
	features.append('Semt')
	features.append('Mahalle')

	return	features,values	

def getPrice(advert,features,values):
	
	link2 = bs(rq.get(advert).content,"html.parser").find_all('p',{'class':'fontRB fz24 price'}) # get Price value
	values.append( str(link2)[ (str(link2).find('>')+2) : str(link2).rfind('<')-1 ] )
	features.append('Fiyat')

	return	features,values

def createDataset():
	total_page = getTheNumberOfPages()
	advert = getLinks(1) # write how many pages you want	
	advert = removeRedundantAdverts(advert)

	df = pd.DataFrame()

	for j in range(0,len(advert)):
		try:
			print(j,' ',advert[j])
			features = []
			values = []

			features.append('Link')
			values.append(advert[j])

			getFeatures(advert[j],features,values)
			values.remove(values[6])
			getPrice(advert[j],features,values)
			getProvince(advert[j],features,values)

			listvalues = [values]

			try:
				df2 = pd.DataFrame(listvalues,columns=features)
			except:
				values.remove(values[len(values)-2])
				df2 = pd.DataFrame(listvalues,columns=features)

			df = df.append(df2,ignore_index=True)
		except:
			print('hata: ', advert[j])
			
	df.to_csv('dataset.csv',index=False) # write each real estates' features to a csv file

createDataset()