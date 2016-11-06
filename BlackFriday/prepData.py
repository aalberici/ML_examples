# 6.11.2016
# zdroj: https://github.com/SudalaiRajkumar/ML/tree/master/AV_BlackFridayHack

import pandas as pd
import numpy as np
from sklearn.cross_validation import KFold
from sklearn import ensemble
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
import os



def getCountVar(compute_df, count_df, var_name):
	grouped_df = count_df.groupby(var_name)
	count_dict = {}
	for name, group in grouped_df:
		count_dict[name] = group.shape[0]

	count_list = []
	for index, row in compute_df.iterrows():
		name = row[var_name]
		count_list.append(count_dict.get(name, 0))
	return count_list


def getPurchaseVar(compute_df, purchase_df, var_name):
        grouped_df = purchase_df.groupby(var_name)
        min_dict = {}
        max_dict = {}
        mean_dict = {}
        twentyfive_dict = {}
        seventyfive_dict = {}
        for name, group in grouped_df:
                min_dict[name] = min(np.array(group["Purchase"]))
                max_dict[name] = max(np.array(group["Purchase"]))
                mean_dict[name] = np.mean(np.array(group["Purchase"]))
                twentyfive_dict[name] = np.percentile(np.array(group["Purchase"]),25)
                seventyfive_dict[name] = np.percentile(np.array(group["Purchase"]),75)

        min_list = []
        max_list = []
        mean_list = []
        twentyfive_list = []
        seventyfive_list = []
        for index, row in compute_df.iterrows():
                name = row[var_name]
                min_list.append(min_dict.get(name,0))
                max_list.append(max_dict.get(name,0))
                mean_list.append(mean_dict.get(name,0))
                twentyfive_list.append( twentyfive_dict.get(name,0))
                seventyfive_list.append( seventyfive_dict.get(name,0))

        return min_list, max_list, mean_list, twentyfive_list, seventyfive_list


gender_dict = {'F':0, 'M':1}
age_dict = {'0-17':0, '18-25':1, '26-35':2, '36-45':3, '46-50':4, '51-55':5, '55+':6}
city_dict = {'A':0, 'B':1, 'C':2}
stay_dict = {'0':0, '1':1, '2':2, '3':3, '4+':4}


# path with data
parent_parent = os.path.dirname(os.path.dirname(os.getcwd()))
data_path = os.path.join(parent_parent, os.path.join('data_examples', 'BlackFriday'))
train_file = os.path.join(data_path, "train.csv")
test_file = os.path.join(data_path, "test.csv")

train_df = pd.read_csv(train_file)
test_df = pd.read_csv(test_file)
print('train and test shapes', train_df.shape, test_df.shape)

train_df["Gender"] = train_df["Gender"].apply(lambda x: gender_dict[x])
test_df["Gender"] = test_df["Gender"].apply(lambda x: gender_dict[x])

train_df["Age"] = train_df["Age"].apply(lambda x: age_dict[x])
test_df["Age"] = test_df["Age"].apply(lambda x: age_dict[x])

train_df["City_Category"] = train_df["City_Category"].apply(lambda x: city_dict[x])
test_df["City_Category"] = test_df["City_Category"].apply(lambda x: city_dict[x])

train_df["Stay_In_Current_City_Years"] = train_df["Stay_In_Current_City_Years"].apply(lambda x: stay_dict[x])
test_df["Stay_In_Current_City_Years"] = test_df["Stay_In_Current_City_Years"].apply(lambda x: stay_dict[x])


print ("Getting count features..")
train_df["Age_Count"] = getCountVar(train_df, train_df, "Age")
test_df["Age_Count"] = getCountVar(test_df, train_df, "Age")
print ("Age", np.unique(test_df["Age_Count"]))

train_df["Occupation_Count"] = getCountVar(train_df, train_df, "Occupation")
test_df["Occupation_Count"] = getCountVar(test_df, train_df, "Occupation")
print ("Occupation", np.unique(test_df["Occupation_Count"]))

train_df["Product_Category_1_Count"] = getCountVar(train_df, train_df, "Product_Category_1")
test_df["Product_Category_1_Count"] = getCountVar(test_df, train_df, "Product_Category_1")
print ("Cat 1 ",np.unique(test_df["Product_Category_1_Count"]))

train_df["Product_Category_2_Count"] = getCountVar(train_df, train_df, "Product_Category_2")
test_df["Product_Category_2_Count"] = getCountVar(test_df, train_df, "Product_Category_2")
print ("Cat 2 ", np.unique(test_df["Product_Category_2_Count"]))

train_df["Product_Category_3_Count"] = getCountVar(train_df, train_df, "Product_Category_3")
test_df["Product_Category_3_Count"] = getCountVar(test_df, train_df, "Product_Category_3")
print ("Cat 3 ", np.unique(test_df["Product_Category_3_Count"]))

train_df["User_ID_Count"] = getCountVar(train_df, train_df, "User_ID")
test_df["User_ID_Count"] = getCountVar(test_df, train_df, "User_ID")
print ("User id ", np.unique(test_df["User_ID_Count"])[:10])

train_df["Product_ID_Count"] = getCountVar(train_df, train_df, "Product_ID")
test_df["Product_ID_Count"] = getCountVar(test_df, train_df, "Product_ID")
print ("Product id ", np.unique(test_df["Product_ID_Count"])[:10])



train_df.fillna(-999, inplace=True)
test_df.fillna(-999, inplace=True)


print(train_df)
print(test_df)

min_price_list, max_price_list, mean_price_list, twentyfive_price_list, seventyfive_price_list = getPurchaseVar(train_df, train_df, "User_ID")
train_df["User_ID_MinPrice"] = min_price_list
train_df["User_ID_MaxPrice"] = max_price_list
train_df["User_ID_MeanPrice"] = mean_price_list
train_df["User_ID_25PercPrice"] = twentyfive_price_list
train_df["User_ID_75PercPrice"] = seventyfive_price_list
min_price_list, max_price_list, mean_price_list, twentyfive_price_list, seventyfive_price_list = getPurchaseVar(test_df, train_df, "User_ID")
test_df["User_ID_MinPrice"] = min_price_list
test_df["User_ID_MaxPrice"] = max_price_list
test_df["User_ID_MeanPrice"] = mean_price_list
test_df["User_ID_25PercPrice"] = twentyfive_price_list
test_df["User_ID_75PercPrice"] = seventyfive_price_list
#print np.unique(test_df["User_ID_MeanPrice"])[:10]

min_price_list, max_price_list, mean_price_list, twentyfive_price_list, seventyfive_price_list = getPurchaseVar(train_df, train_df, "Product_ID")
train_df["Product_ID_MinPrice"] = min_price_list
train_df["Product_ID_MaxPrice"] = max_price_list
train_df["Product_ID_MeanPrice"] = mean_price_list
train_df["Product_ID_25PercPrice"] = twentyfive_price_list
train_df["Product_ID_75PercPrice"] = seventyfive_price_list
min_price_list, max_price_list, mean_price_list, twentyfive_price_list, seventyfive_price_list = getPurchaseVar(test_df, train_df, "Product_ID")
test_df["Product_ID_MinPrice"] = min_price_list
test_df["Product_ID_MaxPrice"] = max_price_list
test_df["Product_ID_MeanPrice"] = mean_price_list
test_df["Product_ID_25PercPrice"] = twentyfive_price_list
test_df["Product_ID_75PercPrice"] = seventyfive_price_list
#print np.unique(test_df["Product_ID_MeanPrice"])[:10]

min_price_list, max_price_list, mean_price_list, twentyfive_price_list, seventyfive_price_list = getPurchaseVar(train_df, train_df, "Product_Category_1")
train_df["Product_Cat1_MinPrice"] = min_price_list
train_df["Product_Cat1_MaxPrice"] = max_price_list
train_df["Product_Cat1_MeanPrice"] = mean_price_list
train_df["Product_Cat1_25PercPrice"] = twentyfive_price_list
train_df["Product_Cat1_75PercPrice"] = seventyfive_price_list
min_price_list, max_price_list, mean_price_list, twentyfive_price_list, seventyfive_price_list = getPurchaseVar(test_df, train_df, "Product_Category_1")
test_df["Product_Cat1_MinPrice"] = min_price_list
test_df["Product_Cat1_MaxPrice"] = max_price_list
test_df["Product_Cat1_MeanPrice"] = mean_price_list
test_df["Product_Cat1_25PercPrice"] = twentyfive_price_list
test_df["Product_Cat1_75PercPrice"] = seventyfive_price_list
print (np.unique(test_df["Product_Cat1_MeanPrice"])[:10])

min_price_list, max_price_list, mean_price_list, twentyfive_price_list, seventyfive_price_list = getPurchaseVar(train_df, train_df, "Product_Category_2")
train_df["Product_Cat2_MinPrice"] = min_price_list
train_df["Product_Cat2_MaxPrice"] = max_price_list
train_df["Product_Cat2_MeanPrice"] = mean_price_list
train_df["Product_Cat2_25PercPrice"] = twentyfive_price_list
train_df["Product_Cat2_75PercPrice"] = seventyfive_price_list
min_price_list, max_price_list, mean_price_list, twentyfive_price_list, seventyfive_price_list = getPurchaseVar(test_df, train_df, "Product_Category_2")
test_df["Product_Cat2_MinPrice"] = min_price_list
test_df["Product_Cat2_MaxPrice"] = max_price_list
test_df["Product_Cat2_MeanPrice"] = mean_price_list
test_df["Product_Cat2_25PercPrice"] = twentyfive_price_list
test_df["Product_Cat2_75PercPrice"] = seventyfive_price_list
print (np.unique(test_df["Product_Cat2_MeanPrice"])[:10])

min_price_list, max_price_list, mean_price_list, twentyfive_price_list, seventyfive_price_list = getPurchaseVar(train_df, train_df, "Product_Category_3")
train_df["Product_Cat3_MinPrice"] = min_price_list
train_df["Product_Cat3_MaxPrice"] = max_price_list
train_df["Product_Cat3_MeanPrice"] = mean_price_list
train_df["Product_Cat3_25PercPrice"] = twentyfive_price_list
train_df["Product_Cat3_75PercPrice"] = seventyfive_price_list
min_price_list, max_price_list, mean_price_list, twentyfive_price_list, seventyfive_price_list = getPurchaseVar(test_df, train_df, "Product_Category_3")
test_df["Product_Cat3_MinPrice"] = min_price_list
test_df["Product_Cat3_MaxPrice"] = max_price_list
test_df["Product_Cat3_MeanPrice"] = mean_price_list
test_df["Product_Cat3_25PercPrice"] = twentyfive_price_list
test_df["Product_Cat3_75PercPrice"] = seventyfive_price_list
print (np.unique(test_df["Product_Cat3_MeanPrice"])[:10])



train_df.to_csv(os.path.join(data_path, "train_mod.csv"), index=False)
test_df.to_csv(os.path.join(data_path, "test_mod.csv"), index=False)