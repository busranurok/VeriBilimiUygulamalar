import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
pd.set_option("display.float.format", lambda x: "%.2f" % x)

df = sns.load_dataset("taxis")
df_copy = df

#countploty bool değerleri işlemediği için veri setindeki bool değerler int değerlere döndürülür.
for col in df_copy.columns:
    if df_copy[col].dtype == "bool":
           df_copy[col] = df_copy[col].astype(int)

#Dataset' in genel yapısını inceleme
def check_dataframe(dataframe, head=5):
    print("Head")
    print(dataframe.head(head))
    print("Tail")
    print(dataframe.tail(head))
    print("Shape")
    print(dataframe.shape)
    print("Info")
    print(dataframe.info)
    print("dtype")
    print(dataframe.dtype())
    print("isnull.sum")
    print(dataframe.isnull().sum())
    print("describe")
    print(dataframe.describe().T)


#Kategorik, Nümerik, Kardinal değişkenleri buluyoruz.
def grab_columns_names(dataframe, categoric_treshold=5, cardinal_treshold=20):
    """
    Veri setindeki; kategorik, numerik,ve kategorik gibi gözüküp kardinal olan değişkenlerin isimlerini verir.
    Parameters
    ----------
    dataframe: dataframe
        Deişken isimlerinin alınması istenilen dataframedir.
    categoric_treshold : int, float
        Numerik gibi gözüküp özünde kategorik olan değişkenler için sınıf eşik değeridir.
    cardinal_treshold : int, float
        Kategorik gibi gözüküp özünde kardinal olan değişkenler için sınıf eşik değeridir.
    Returns
    -------
        categoric_columns: list
            Kategorik değişkenler listesidir.
        numeric_columns: list
            Numerik değişkenler listesidir.
        categoric_but_cardinal: list
        Kategorik görünümlü kardinal değişkenler listesidir.

    Notes:
        categoric_columns + numeric_columns + categoric_but_cardinal : toplam değişken sayısı anlamına gelir.
        numeric_but_categoric_columns, categoric_columns' ın içerisindedir

    """
    # Kategorik değişkenleri bulma
    categoric_columns = [col for col in dataframe.columns if str(dataframe[col].dtype) in ["category", "bool", "object"]]
    #Numerik gibi gözüküp kategorik olan değerler
    numeric_but_categoric_columns = [col for col in dataframe.columns if
                                     (dataframe[col].nunique() < categoric_treshold) & (dataframe[col].dtype in ["int", "float"])]
    # categorik değerlerin toplamı
    categoric_columns = categoric_columns + numeric_but_categoric_columns
    #Kategorik gibi gözüken ama eşsiz değeri çok fazla çeşitli olan değişkenleri buluyoruz
    categoric_but_cardinal = [col for col in dataframe.columns if
                              (dataframe[col].nunique() > cardinal_treshold) & (dataframe[col].dtype in ["category", "object"])]
    #kardinal değerlerin de çıkmış kategorik değişkenler
    categoric_columns = [col for col in categoric_columns if col not in categoric_but_cardinal]


    #Nümerik değişkenleri bulma
    numeric_columns = [col for col in dataframe.columns if dataframe[col].dtype in ["int", "float"]]
    numeric_columns = [col for col in numeric_columns if col not in categoric_columns]

    return categoric_columns, numeric_columns, categoric_but_cardinal


categoric_columns, numeric_columns, categoric_but_cardinal = grab_columns_names(df_copy)

print(f"Categorik Columns: {categoric_columns}\n Numeric Columns: {numeric_columns}\n Categoric But Cardinal Columns: {categoric_but_cardinal}")


#Kategorik değişkenlerin özeti
def categoric_summary(dataframe, column_name, plot=False):
    print(pd.DataFrame({column_name: dataframe[column_name].value_counts(),
                        "Ratio": 100 * dataframe[column_name].value_counts() / len(dataframe)}))

    if plot:
        sns.countplot(x=dataframe[column_name], data=dataframe)
        plt.show(block=True)


for col in categoric_columns:
    categoric_summary(dataframe=df_copy, column_name=col, plot=True)


# Nümerik değişkenlerin özeti
def numeric_summary(dataframe, column_name, plot=False):
    quanties = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
    print(dataframe[column_name].describe(quanties).T)

    if plot:
        dataframe[column_name].hist()
        plt.xlabel(column_name)
        plt.title(column_name)
        plt.show(block=True)


for col in numeric_columns:
    numeric_summary(dataframe=df_copy, column_name=col, plot=True)


#Hedef değişken analizi
#Hedef değişkenin kategorik değişkenler ile analizi
def target_summary_with_categoric_columns(dataframe, target, categoric_columns_name):
    print(pd.DataFrame({"TARGET MEAN": dataframe.groupby(categoric_columns_name).agg({target: "mean"})}))


for col in categoric_columns:
    target_summary_with_categoric_columns(dataframe=df_copy, target="tip", categoric_columns_name=col)


#Hedef değişkenin nümerik değişkenler ile analizi
def target_summary_with_numeric_columns(dataframe, target, numeric_columns_name):
    print(pd.DataFrame({"TARGET MEAN": dataframe.groupby(target).agg({numeric_columns_name: "mean"})}))


for col in categoric_columns:
    target_summary_with_numeric_columns(dataframe=df_copy, target="tip", numeric_columns_name=col)