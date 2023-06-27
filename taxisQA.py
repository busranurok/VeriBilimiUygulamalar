import seaborn as sns
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.float.format", lambda x: "%.2f" % x)

df = sns.load_dataset("taxis")
df_copy = df

df_copy.head()

#Soru : ListComprehension yapısı kullanarak taxis verisindeki numeric değişkenlerin isimlerini büyük harfe çeviriniz ve başına NUM  ekleyiniz

["NUM_" + col.upper() for col in df_copy.columns if str(df_copy[col].dtype) not in ["object", "string", "bool"]]

["NUM_" + col.upper() for col in df_copy.columns if df_copy[col].dtype in ["complex", "int", "float"]]

["NUM_" + col.upper() for col in df_copy.columns if df_copy[col].dtype != "O"]


#Soru : ListComprehension yapısı kullanarak taxis verisindeki içerisinde o harfi olmayan değişkenleri alıp sonuna "O" harfi ekleyiniz

df["distance"] # bu bana veri seti döner ama col dediğimde ben column ismini elde ederim!

[col + "O" for col in df_copy.columns if col not in "o"]


#Soru : ListComprehension yapısı kullanarak taxis verisindeki değişkenlerden ["payment","tip"] olmayanları seçin ve yeni bir dataset oluşturun

df[["distance", "tip"]] # Bu banaveri seti döner.

[col for col in df_copy.columns if (col != "payment") & (col != "tip")] # Bu da bana sadece kolon isimlerini döndürür. Ama benden istenen bir df.

df_copy2 = df_copy[[col for col in df_copy.columns if (col != "payment") & (col != "tip")]]


#Soru : her bir değişkendeki boş değerlerin toplamını bulun

df_copy[""]
df_copy.tip

df_copy.isnull().sum()


#Soru : total değişkeninin payment ve passengers kırılımında sum count mean değerlerini bulun

df_copy.groupby(["payment", "passengers"]).agg({"total": ["sum", "count", "mean"]}).reset_index()


#Soru: tip değişkeninin distance ve payment kırılımında sum count mean,median değerlerini bulun

df_copy.groupby(["payment", "distance"]).agg({"tip": ["sum", "count", "mean", "median"]})


#Soru : distance değeri 1 den küçük olanları 1 e eşitleyip bunu yeni bir değişken olarak dataframe e ekleyiniz

df_copy["distance_degeri_1den_kucuk_olanlar"] = df_copy["distance"]

# datasetin içerisinde şu değeri 1 den küçük olanların yine o değerini getir ve 1 e eşitle diyoruz. Eğer virgülden sonraki kısmı yazmazsak bütün değişkenlerin değerlerine 1 ataması yapar.
df_copy.loc[df['distance_degeri_1den_kucuk_olanlar'] < 1,"distance_degeri_1den_kucuk_olanlar"] = 1


#apply değişkendeki her eleman için içerisinde yazılmış olan fonksiyonu gerçekleştiriyor.
df_copy['distance_degeri_1den_kucuk_olanlar'] = df_copy['distance_degeri_1den_kucuk_olanlar'].apply(lambda x: 1 if x < 1 else x)

#Soru : color değeri yellow olan tüm bilgileri getirin 2. işlem olarak: filtreleme yaptıktan sonra sadece color değişkeninin verilerini getir.
#filtrelenmiş halinin tüm bilgileri getiririz
df_copy[df_copy["color"] == "yellow"]

#filtreleme yaptıktan sonra sadece color değişkeninin verilerini getirir
df_copy[df_copy["color"] == "yellow"].color
df_copy[df_copy["color"] == "yellow"]["color"]

df_copy.loc[ df_copy["color"] == "yellow", "color"]

#####
df_copy.loc[(df_copy["color"] == "yellow") & (df_copy["distance"] > 1), "color"]
df_copy.loc[(df_copy["color"] == "yellow") & (df_copy["distance"] > 1), ["color", "distance"]]


#Soru : total değeri 10 dan büyük ve color ı yellow olmayan tüm bilgileri getirin

df_copy.loc[(df["total"] > 10) & (df["color"] != "yellow")]

#pandas.core.series.Series
#type(df["color"])
#df_copy.loc[(df["total"] > 10) & (df["color"] not in "yellow")]

#numpy array' i döndürür
#type(df_copy["color"].values)
#df_copy.loc[(df["total"] > 10) & (df_copy["color"].values.str.contains("yellow")]

#pandas string array' i
type(df_copy.columns)

df_copy.loc[(df["total"] > 10) & (~df_copy["color"].str.contains("yellow"))]


#Soru : her color için verisetinde kaç bilgi olduğunu gösteriniz

df_copy["color"].value_counts()


#Soru : pickup_zone bazında total ve tip değişkenlerinin toplamını gösteriniz

df_copy.groupby("pickup_zone")[["total", "tip"]].sum()

df_copy.groupby("pickup_zone").agg({"total": "sum",
                                    "tip": "sum"})


#Soru : payment bazında total değişkeninin toplam değerini bulup bunu ayrı bir veri setine atayınız ve yeni oluşturulan bu veri setini toplam total değeri bazında büyükten küçüğe doğru sıralayınız

df_copy3 = df_copy.groupby("payment").agg({"total": "sum"})
df_copy3.sort_values("total", ascending=False)


#Soru : passengers değeri 3 ten büyük olan bilgileri pickup_zone bazında kaç tane olduğunu gösteriniz

df_copy.loc[df_copy["passengers"] > 3].groupby("pickup_zone").sum().head()


#Soru : bilgileri total bazında 4 segmente ayırınız. [0-10,10-30,30-50,50-100] ve bu segmentlere görmüş olduğunuz dizideki isimleri verin

bins = [0, 10, 30, 50, 100]
labels = ["0-10", "10-30", "30-50", "50-100"]
df_copy["total_segments"] = pd.cut(x=df_copy["total"], bins=bins, labels=labels)


#Soru : tip verisini pickup_zone ve payment bazında mean değerini bulun. böylelikle Hudson dan binen birinin kredi kartıyla ödeme yapacağı takdirde tahminen ne kadar tip bırakacağını bulabilirsiniz

df_copy.groupby(["payment", "pickup_zone"]).agg({"tip": "mean"})




