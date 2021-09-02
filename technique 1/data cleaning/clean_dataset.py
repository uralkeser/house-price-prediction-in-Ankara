import pandas as pd

def dropRedundantColumns(ds):
	ds = ds.drop(['İlan no'], axis=1)
	ds = ds.drop(['Son Güncelleme Tarihi'], axis=1)
	ds = ds.drop(['İlan Durumu'], axis=1)
	ds = ds.drop(['Konut Şekli'], axis=1)
	ds = ds.drop(['Krediye Uygunluk'], axis=1)
	ds = ds.drop(['Yapı Tipi'], axis=1)
	ds = ds.drop(['Kullanım Durumu'], axis=1)
	ds = ds.drop(['Tapu Durumu'], axis=1)
	ds = ds.drop(['Takas'], axis=1)
	ds = ds.drop(['Öğrenciye / Bekara '], axis=1)
	ds = ds.drop(['Yakıt Tipi'], axis=1)
	ds = ds.drop(['Kira Getirisi'], axis=1)
	ds = ds.drop(['Depozito'], axis=1)
	ds = ds.drop(['Site İçerisinde'], axis=1)
	return ds

def CleanDataset():
	dataset = pd.read_csv('dataset.csv')#if your file name is difrent change here
	dataset = dropRedundantColumns(dataset)

	dataset = dataset.loc[ dataset['Semt'] != 'Akyurt' ]
	dataset = dataset.loc[ dataset['Semt'] != 'Ayaş' ]
	dataset = dataset.loc[ dataset['Semt'] != 'Beypazarı' ]
	dataset = dataset.loc[ dataset['Semt'] != 'Çamlıdere' ]
	dataset = dataset.loc[ dataset['Semt'] != 'Çubuk' ]
	dataset = dataset.loc[ dataset['Semt'] != 'Evren' ]	
	dataset = dataset.loc[ dataset['Semt'] != 'Güdül' ]	
	dataset = dataset.loc[ dataset['Semt'] != 'Haymana' ]
	dataset = dataset.loc[ dataset['Semt'] != 'Kahramankazan' ]	
	dataset = dataset.loc[ dataset['Semt'] != 'Kalecik' ]	
	dataset = dataset.loc[ dataset['Semt'] != 'Kızılcahamam' ]	
	dataset = dataset.loc[ dataset['Semt'] != 'Nallıhan' ]	
	dataset = dataset.loc[ dataset['Semt'] != 'Polatlı' ]
	dataset = dataset.loc[ dataset['Semt'] != 'Şerehlikoçhisar' ]	

	def OdaSayisi(x):
		a = str(x).replace(' ', '')
		b = int(a[0:a.find('+')]) + int(a[a.find('+'):])
		return b

	#Oda + Salon Sayısı
	dataset['Oda + Salon Sayısı'] = dataset['Oda + Salon Sayısı'].apply(lambda x: OdaSayisi(x) )
	dataset = dataset.loc[ dataset['Oda + Salon Sayısı'] <= 10 ]
	
	#Brüt / Net M2
	dataset['Brüt / Net M2'] = dataset['Brüt / Net M2'].apply(lambda x: str(x)[str(x).find('/')+2:] )
	dataset['Brüt / Net M2'] = dataset['Brüt / Net M2'].apply(lambda x: str(x)[0:str(x).find('m2')-1] )
	dataset = dataset.loc[ dataset['Brüt / Net M2'] != 'Belirtilmem' ]
	dataset['Brüt / Net M2'] = dataset['Brüt / Net M2'].apply(lambda x: int(x.replace(',', '')) )
	dataset = dataset.loc[ dataset['Brüt / Net M2'] >= 50 ]
	dataset = dataset.loc[ dataset['Brüt / Net M2'] <= 350 ]

	#Bina Yaşı
	dataset['Bina Yaşı'] = dataset['Bina Yaşı'].apply(lambda x: str(x)[0:str(x).find('Yaşında')-1] if str(x).find('Yaşında')!=-1 else x )
	dataset['Bina Yaşı'] = dataset['Bina Yaşı'].apply(lambda x: 0 if str(x).find('Sıfır')!=-1 else x)
	dataset['Bina Yaşı'] = dataset['Bina Yaşı'].apply(lambda x: int(x) )
	dataset = dataset.loc[ dataset['Bina Yaşı'] <= 100 ]
	
	#Fiyat
	dataset['Fiyat'] = dataset['Fiyat'].apply(lambda x: str(x)[0:str(x).find('TL')-1] if str(x).find('TL')!=-1 else x )
	dataset['Fiyat'] = dataset['Fiyat'].apply(lambda x: int(x.replace(',', '')) )
	dataset = dataset.loc[ dataset['Fiyat'] <= 2260000 ]
	dataset = dataset.loc[ dataset['Fiyat'] >= 50000 ]
	dataset = dataset.sort_values(by=['Fiyat','Mahalle'])
		
	#Bulunduğu Kat
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: str(x)[0:str(x).find('. Kat')] if str(x).find('. Kat')!=-1 else x )	
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: '-'+(str(x)[(str(x).find('Kot')+4):]) if str(x).find('Kot')!=-1 else x )
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: 0 if str(x).find('Bahçe Katı')!=-1 else x )
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: 0 if str(x).find('Yüksek Giriş')!=-1 else x )
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: 0 if str(x).find('Giriş Katı')!=-1 else x )
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: 0 if str(x).find('Zemin')!=-1 else x )
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: -2 if str(x).find('Bodrum')!=-1 else x )
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: 21 if str(x).find('21 ve üzeri')!=-1 else x )
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: None if str(x).find('Üst')!=-1 else x )
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: None if str(x).find('Teras')!=-1 else x )
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: None if str(x).find('Çatı Katı')!=-1 else x )
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: 0 if str(x).find('Villa Katı')!=-1 else x )
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: 1 if str(x).find('Ara Kat')!=-1 else x )
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: 1 if str(x).find('Asma Kat')!=-1 else x )
	dataset.dropna(subset = ['Bulunduğu Kat'], inplace=True)
	dataset['Bulunduğu Kat'] = dataset['Bulunduğu Kat'].apply(lambda x: int(x) )
	
	#Yapının Durumu
	dataset = dataset[ dataset['Yapının Durumu'] != 'Yapım Aşamasında']
	dataset['Yapının Durumu'].fillna('İkinci El', inplace = True)
	
	#Isınma Tipi ve Aidat 
	dataset['Aidat'] = dataset['Aidat'].apply(lambda x: str(x)[0:str(x).find('TL')-1] if str(x).find('TL')!=-1 else x )
	dataset['Aidat'] = dataset['Aidat'].apply(lambda x: int(str(x).replace(',', '')) if str(x).find(',')!=-1 else x)
	dataset['Isınma Tipi'] = dataset['Isınma Tipi'].apply(lambda x: str(x)[0:str(x).find('(Pay Ölçer)')-1] if str(x).find('(Pay Ölçer)')!=-1 else x )
	
	df1 = dataset.loc[ dataset['Isınma Tipi'] == 'Kombi' ]
	#df1['Aidat'].fillna(method = 'bfill', inplace=True)
	
	df2 = dataset.loc[ dataset['Isınma Tipi'] == 'Merkezi' ]
	#df2['Aidat'].fillna(method = 'bfill', inplace=True)
	
	dataset = pd.concat([df1, df2],ignore_index=True)
	#dataset['Aidat'].fillna(method = 'ffill', inplace=True)
	dataset.dropna(subset = ['Aidat'], inplace=True)
	dataset['Aidat'] = dataset['Aidat'].apply(lambda x: int(x) )
	
	dataset = dataset.loc[ dataset['Aidat'] <= 1000  ]
	dataset = dataset.loc[ dataset['Aidat'] >= 20  ]
	
	
	#Banyo Sayısı
	dataset = dataset.loc[ dataset['Banyo Sayısı'] <= 6 ]
	
	#Kat Sayısı
	dataset['Kat Sayısı'] = dataset['Kat Sayısı'].apply(lambda x: str(x)[0:str(x).find('Katlı')-1] if str(x).find('Katlı')!=-1 else x )
	dataset = dataset.sort_values(by=['Bulunduğu Kat'])
	#dataset['Kat Sayısı'].fillna(method = 'bfill', inplace=True)
	dataset.dropna(subset = ['Kat Sayısı'], inplace=True)	
	dataset.dropna(axis=1, how='any')
	dataset['Kat Sayısı'] = dataset['Kat Sayısı'].apply(lambda x: int(x) )
	dataset = dataset[dataset['Bulunduğu Kat'] <= dataset['Kat Sayısı']]

	dataset.to_csv('cleandataset.csv',index=False)

def mapDistanceFeatures():
	dataset = pd.read_csv('cleandataset.csv')
	distanceset = pd.read_csv('distanceset.csv')
	finalset = pd.merge(dataset,distanceset,on=['Semt','Mahalle'],how='left')
	#finalset = finalset.drop(['Semt'], axis=1)
	finalset = finalset.drop(['Mahalle'], axis=1)
	finalset.dropna(subset = ["kizilaya mesafe"], inplace=True)
	finalset.dropna(subset = ["hastane mesafe"], inplace=True)
	finalset.to_csv('mappedset.csv',index=False)

CleanDataset()
mapDistanceFeatures()
