import seaborn as sns
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.float.format", lambda x: "%.2f" % x)

df = sns.load_dataset("diamonds")
df_copy = df

df_copy.head()

#Soru: ListComprehension yapısı kullanarak diamonds verisindeki categoric değişkenlerin isimlerini büyük harfe çeviriniz ve başına CAT ekleyiniz.
#Yöntem1
["CAT_" + col.upper() for col in df_copy.columns if df_copy[col].dtype in ["object", "category", "bool"]]

#Yöntem2
["CAT_" + col.upper() for col in df_copy.columns if df_copy[col].dtype not in ["float", "int", "complex"]]

df_copy.dtypes
# Bütün kategorik değişkenleri category tipinde olduğu için:
#Yöntem3
["CAT_" + col.upper() for col in df_copy.columns if df_copy[col].dtype == "category"]

#Soru: ListComprehension yapısı kullanarak diamonds verisi içerisinde o harfi olmayan değişkenleri alıp sonuna "O" harfi ekleyiniz.
[col + "O" for col in df_copy.columns if "o" not in col]

#Soru: ListCompherension yapısı kullanarak değişkenlerden x,y ve z olmayanları seçip yeni bir dataset' e eşitleyiniz.
df_copy2 = [col for col in df_copy.columns if (col != "x") & (col != "y") & (col != "z")]

#Soru: Her bir değişkendeki boş değerlerin toplamını bulun.
df_copy.isnull().sum()

#Soru: price değişkeninin carat ve cut kırılımında sum count mean değerlerini bulun.
df_copy.groupby(["carat", "cut"]).agg({"price": ["sum", "count", "mean"]}).reset_index().head()

#Soru: carat değişkeninin cut ve color kırılımında sum count mean değerlerini bulun.
df_copy.groupby(["color", "cut"]).agg({"carat": ["sum", "count", "mean"]}).reset_index().head()

#Soru: carat değeri 0.3 ten küçük olanları 0.3 e eşitleyip bunu yeni bir değişkende gösteriniz.
df_copy["carat_kucuk_0.3"] = df_copy["carat"]
#df_copy[df_copy["carat"] < 0.3]["carat_kucuk_0.3"] = 0.3

#Yöntem1
df_copy.loc[df_copy["carat_kucuk_0.3"] < 0.3, "carat_kucuk_0.3"] = 0.3

#Yöntem2
df_copy["carat_kucuk_0.3"].apply(lambda x: 0.3 if x < 0.3 else x)

#Soru: color değeri E olan ama cut değeri Ideal olmayan tüm değerleri getirin.
df_copy.loc[(df["color"] == "E") & (df["cut"] != "Ideal")]

#filtrelenmiş hali
df_copy.loc[(df["color"] == "E") & (df["cut"] != "Ideal"), ["color", "cut"]]

#Soru: her cut değeri için kaç adet veri olduğunu gösteriniz.
df_copy["cut"].value_counts()

#Soru: price değeri 400 den büyük olanları bir başka dataset e atayıp yeni dataset' i price bazında 3 segmente ayırınız.
df_copy3 = df_copy.loc[df["price"] > 400]

pd.qcut(df_copy3.price, q=3, labels=["401_1200", "1201_1900", "1901_2757"])

#Soru: carat değeri bazında bilgileri 4 segmente ayırınız (0.2-0.3    0.3-0.4    0.4-0.5    0.5-5.01) ve bu segmentleri ayrı bir değişken olarak dataset e ekleyiniz.
bins = [0.2, 0.3, 0.4, 0.5, df_copy.carat.max()]
labels = ["0.2-0.3", "0.31-0.4", "0.41-0.5", "0.51-" + str(df_copy.carat.max())]
caret_segments = pd.cut(x=df_copy["carat"], bins=bins, labels=labels)

#df_copy.carat.sort_values()


df_copy.dtypes