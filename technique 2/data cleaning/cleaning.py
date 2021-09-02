# -*- coding: utf-8 -*-
"""cleaning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SltarjZtYy2HWoIPY3pOpXI7n9l5hLdt
"""

from pyspark.sql import SparkSession

from pyspark.sql.types import StructType, IntegerType, StringType, FloatType

from pyspark.sql.functions import col, desc, split, udf, avg

spark=SparkSession.builder.getOrCreate()

#extract ettigimiz 3 dataseti read edip sonrada "ds" isminde union/merge yapiyorum
distance=spark.read.csv('distanceset.csv', header=True) #distance setimizi read yapiyoruz
ds1=spark.read.csv('example/houses500.csv', header=True)
ds2=spark.read.csv('example/houses1000.csv', header=True)
ds3=spark.read.csv('example/houses1500.csv', header=True)
ds=ds1.union(ds2).union(ds3)

#distance 'semt' ve 'mahalle' column isimlerini degistiriyor
distance=distance.withColumnRenamed('Semt', 'Semt1')
distance=distance.withColumnRenamed('Mahalle','Mahalle1')
#joining distance dataset
ds=ds.join(distance, ds.Mahalle==distance.Mahalle1, 'inner')

#print((ds.count(), len(ds.columns)))
#dropping duplicates, ayni ilan no sahip olan ilanlari dropluyor
ds=ds.dropDuplicates(['Ilan no'])
#print((ds.count(), len(ds.columns)))

#ds.repartition(1).write.csv("final.csv", header=True)

#ds = ds.drop('Ilan no')
ds = ds.drop('Son Güncelleme Tarihi')
ds = ds.drop('İlan Durumu')
ds = ds.drop('Konut Şekli')
ds = ds.drop('Krediye Uygunluk')
ds = ds.drop('Yapı Tipi')
ds = ds.drop('Kullanım Durumu')
ds = ds.drop('Tapu Durumu')
ds = ds.drop('Takas')
ds = ds.drop('Semt1')
ds = ds.drop('Mahalle1')
#ds = ds.drop('Öğrenciye / Bekara ')
#ds = ds.drop('Yakıt Tipi')
#ds = ds.drop('Kira Getirisi')
#ds = ds.drop('Depozito')
#ds = ds.drop('Site İçerisinde')

ds=ds.filter(col('Semt') != ('Güdül' and 'Haymana' and 'Kahramankazan'))
ds=ds.filter(col('Semt') != ('Çamlıdere' and 'Çubuk' and 'Evren'))
ds=ds.filter(col('Semt') != ('Akyurt' and 'Ayaş' and 'Beypazarı'))
ds=ds.filter(col('Semt') !=('Kalecik' and 'Kızılcahamam' and 'Nallıhan' and 'Polatlı' and 'Şerehlikoçhisar'))

#print((ds.count(), len(ds.columns)))

#ds.groupby('Fiyat').count().sort(desc('count')).show()

#ds.col('Fiyat')=ds.withColumn('new',ds.select(split(col("Fiyat")," ")))

#Fiyat column icin [fiyat] ve [TL] seklinde "space" ile split edildi
def fiyat(str):
    arr = str.split(" ")
    arr[0]=arr[0].replace(".","")
    return arr[0]
fiyatUDF = udf(lambda z: fiyat(z))
ds=ds.withColumn('Fiyat', fiyatUDF(col('Fiyat')))
ds=ds.filter(col('Fiyat') <= 2500000)
ds=ds.filter(col('Fiyat') >= 50000)

#Brut m2 column icin [nothing], [/], [sayi], [m2] seklinde "space" ile split edildi
def brutm2(str):
    arr = str.split(" ")
    arr[0]=arr[0].replace(",","")
    return arr[0]

brutm2UDF = udf(lambda k: brutm2(k))
#ds=ds.filter(col('Brüt / Net M2') != '/ Belirtilmemiş')
ds=ds.withColumn('Brüt / Net M2', brutm2UDF(col('Brüt / Net M2')))
ds=ds.filter(col('Brüt / Net M2') <= 1000)
ds=ds.filter(col('Brüt / Net M2') >= 50)

#odasayisi column icin [sayi1], [sayi2] seklinde " + " ile split edildi
def odasayisi(str):
    arr = str.split(" + ")
    return int(arr[0])+int(arr[1])

odasayisiUDF = udf(lambda k: odasayisi(k))
ds=ds.withColumn('Oda + Salon Sayısı', odasayisiUDF(col('Oda + Salon Sayısı')))
ds=ds.filter(col('Oda + Salon Sayısı') <= 20)

#binayasi column icin sifir bina=0, else icin [sayi], [yasinda] "space" ile split edildi
def binayasi(str):
    if str=="Sıfır Bina":
        return "0"
    else:
        arr = str.split(" ")
        return arr[0]
    
binayasiUDF = udf(lambda k: binayasi(k))
ds=ds.withColumn('Bina Yaşı', binayasiUDF(col('Bina Yaşı')))

#yapidurumu 'sifir' yada 'ikinci el' olarak 2 ye boluyor
def yapidurumu(str):
    if str=='Sıfır' or str=='Yapım Aşamasında':
        return 'Sıfır'
    elif str=='İkinci El':
        return 'İkinci El'
    else:
        return '*'
ds=ds.na.fill('İkinci El', subset=['Yapının Durumu']) #bos olanlar 'Ikinci El' olarak dolduruldu
yapidurumuUDF = udf(lambda k: yapidurumu(k))
ds=ds.withColumn('Yapının Durumu', yapidurumuUDF(col('Yapının Durumu')))
ds=ds.filter(col('Yapının Durumu') != '*') #Sifir, yapim asamasi, ikinci el-den farkli olanlar droplandi

#banyo sayisi bos olanlar droplandi
ds=ds.na.fill('*', subset=['Banyo Sayısı'])
ds=ds.filter(col('Banyo Sayısı') != '*')
ds=ds.filter(col('Banyo Sayısı') != 'Kat Mülkiyeti')
ds=ds.filter(col('Banyo Sayısı') != 'Kat İrtifakı')
ds=ds.filter(col('Banyo Sayısı') <= 6)

#none olan kat sayisi rowlari '*' ile doldurdum sonrada filter ile dropladim
ds=ds.na.fill('*', subset=['Kat Sayısı'])
ds=ds.filter(col('Kat Sayısı') != '*')

#kat sayisi column icin [sayi] ve [katli] seklinde "space" ile split edildi
def katsayisi(str):
    try:
        arr = str.split(" ")
        return arr[0]
    except Exception:
        pass

katsayisiUDF = udf(lambda k: katsayisi(k))
ds=ds.withColumn('Kat Sayısı', katsayisiUDF(col('Kat Sayısı')))

#burada tempds den noneleri dropladim ve avr hesapladim
tempds=ds
tempds=tempds.na.fill('*', subset=['Aidat'])
def tempKatSayi(str):
    try:
        if str.find('TL')!=-1:
            arr=str.split(" ")
            arr[0]=arr[0].replace(',','')
            return arr[0]
        else:
            return '*'
    except Exception:
        pass

tempKatSayiUDF = udf(lambda k: tempKatSayi(k))
tempds=tempds.withColumn('Aidat', tempKatSayiUDF(col('Aidat')))
tempds=tempds.filter(col('Aidat') != '*')

#bu fnc her row icin iterate etmek icin lazim
def toStr(str):
    return str
toStrUDF=udf(lambda k: toStr(k))
tempds=tempds.withColumn('Aidat', toStrUDF(col('Aidat')).cast(IntegerType()))
tempds=tempds.filter(col('Aidat') <= 2500)
tempds=tempds.filter(col('Aidat') >= 20)
#tempds.repartition(1).write.csv("tempds.csv", header=True)
a=tempds.groupBy().avg("Aidat").first()[0]
s=str(int(a))
ds=ds.na.fill(s, subset=['Aidat'])

#burada once tempds'den avr aidat buldum, sonra bunlari ds'deki nonelar ile degistirdim
def aidat(str):
        if str.find('TL')!=-1:
            arr=str.split(" ")
            arr[0]=arr[0].replace(',','')
            return arr[0]
        else:
            return s
aidatUDF=udf(lambda k: aidat(k))
ds=ds.withColumn('Aidat', aidatUDF(col('Aidat')))
ds=ds.filter(col('Aidat') <= 2500)
ds=ds.filter(col('Aidat') >= 20)

#isinma tipi "merkezi pay olcer" olanlari "merkezi yaptim", diger(kat kalorifer,soba etc) '*' koyarak droplandi
def isinmatipi(str):
    if str=='Merkezi' or str=='Merkezi (Pay Ölçer)':
        return 'Merkezi'
    elif str=='Kombi':
        return 'Kombi'
    else:
        return '*'
isinmatipiUDF=udf(lambda k: isinmatipi(k))
ds=ds.withColumn('Isınma Tipi', isinmatipiUDF(col('Isınma Tipi')))
ds=ds.filter(col('Isınma Tipi') != '*')
ds=ds.filter(col('Bulunduğu Kat') <= col('Kat Sayısı'))

#bulundugu kat stringe gore sayi assign etme
ds=ds.na.fill('*', subset=['Bulunduğu Kat'])
ds=ds.filter(col('Bulunduğu Kat') != '*')
def bulundugukat(str):
    b='Bahçe Katı' or 'Yüksek Giriş' or 'Giriş Katı' or 'Zemin' or 'Villa' or 'Giriş'
    a='Ara Kat' or 'Asma Kat'
    c='21 ve üzeri' or 'En Üst Kat' or 'Çatı Katı' or 'Teras Katı'
    if str==b:
        return '0'
    elif str==a:
        return '1'
    elif str==c:
        return '21'
    elif str.find('Giriş')!=-1:
        return '0'
    elif str.find('En')!=-1:
        return '21'
    elif str.find('Teras')!=-1:
        return '21'
    elif str.find('Çatı')!=-1:
        return '21'
    elif str.find('Villa')!=-1:
        return '0'
    elif str.find('Kot')!=-1:
        arr=str.split(" ")
        return arr[1]
    elif str.find('Kat')!=-1:
        arr=str.split(" ")
        temp=arr[0].replace('.','')
        return temp
    else:
        return '*'
bulundugukatUDF=udf(lambda k: bulundugukat(k))
ds=ds.withColumn('Bulunduğu Kat', bulundugukatUDF(col('Bulunduğu Kat')))
ds=ds.filter(col('Bulunduğu Kat') != '*')

#string yada int column'lari float ceviriyor
ds=ds.withColumn('Aidat', toStrUDF(col('Aidat')).cast(FloatType()))
ds=ds.withColumn('Oda + Salon Sayısı', toStrUDF(col('Oda + Salon Sayısı')).cast(FloatType()))
ds=ds.withColumn('Brüt / Net M2', toStrUDF(col('Brüt / Net M2')).cast(FloatType()))
ds=ds.withColumn('Bulunduğu Kat', toStrUDF(col('Bulunduğu Kat')).cast(FloatType()))
ds=ds.withColumn('Bina Yaşı', toStrUDF(col('Bina Yaşı')).cast(FloatType()))
ds=ds.withColumn('Kat Sayısı', toStrUDF(col('Kat Sayısı')).cast(FloatType()))
ds=ds.withColumn('Banyo Sayısı', toStrUDF(col('Banyo Sayısı')).cast(FloatType()))
ds=ds.withColumn('Fiyat', toStrUDF(col('Fiyat')).cast(FloatType()))
ds=ds.withColumn('kizilaya mesafe', toStrUDF(col('kizilaya mesafe')).cast(FloatType()))
ds=ds.withColumn('hastane mesafe', toStrUDF(col('hastane mesafe')).cast(FloatType()))

ds.repartition(1).write.csv("final.csv", header=True)

#spark.stop()

ds.count()
