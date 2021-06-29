#-*- coding : utf-8-*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation

from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import classification_report, confusion_matrix

from tensorflow.keras.models import load_model
import joblib


def train(filename, test_percentage, hidden_nums, activate_func, optimizer_func, ep, batch):
    raw_data = pd.read_csv(filename, encoding='utf-8')
    raw_data = raw_data.iloc[:, 2:]

    features = raw_data.iloc[:, :-1]
    target = raw_data.iloc[:, -1]

    scaler_1 = StandardScaler()
    scaler_1.fit(features)
    features_scaled = scaler_1.transform(features)

    target = np.array(target).reshape(-1, 1)
    scaler_2 = StandardScaler()
    scaler_2.fit(target)
    target_scaled = scaler_2.transform(target)

    joblib.dump(scaler_1, "./model/scalerFeature.pkl")
    joblib.dump(scaler_2, "./model/scalerTarget.pkl")

    train_nums = raw_data.shape[1] * (1-test_percentage)
    train_nums = int(train_nums)
    x_train, x_test = features_scaled[:train_nums], features_scaled[train_nums:]
    y_train, y_test = target_scaled[:train_nums], target_scaled[train_nums:]

    model = Sequential()
    model.add(Dense(hidden_nums, input_dim=14))
    model.add(Activation(activate_func))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer=optimizer_func)
    model.fit(x_train, y_train, epochs=ep, batch_size=batch)

    model.save("./model/ann_model.h5")

    y_pre = model.predict(x_test)

    y_pre_inv = scaler_2.inverse_transform(y_pre)
    y_test_inv = scaler_2.inverse_transform(y_test)

    plt.figure(figsize=(20, 15))
    plt.plot(range(1, len(y_test_inv) + 1), y_test_inv, color='black', linestyle='-', linewidth=0.8, label='real')
    plt.plot(range(1, len(y_pre_inv) + 1), y_pre_inv, color='red', linestyle='-', linewidth=0.8, label='prediction')
    plt.title('temp prediction')
    plt.legend()
    plt.show()

    mse = mean_squared_error(y_test_inv, y_pre_inv)
    r2 = r2_score(y_test_inv, y_pre_inv)
    print(mse)
    print(r2)

    return mse, r2


def run(filename):
    scaler_1 = joblib.load("./model/scalerFeature.pkl")
    model = load_model("./model/ann_model.h5")
    scaler_2 = joblib.load("./model/scalerTarget.pkl")

    raw_data = pd.read_csv(filename, encoding='utf-8')
    features = raw_data.iloc[-51:-1, 2:]
    features_scaled = scaler_1.transform(features)
    yhat = model.predict(features_scaled)
    y_pre_inv = scaler_2.inverse_transform(yhat)

    plt.ion()
    plt.figure(figsize=(20, 15))
    plt.title('returnTemp Predict')

    for i in range(2000):
        if i == 1999:
            i = 1
            plt.clf()

        raw_data = pd.read_csv(filename, encoding='utf-8')

        features = raw_data.iloc[-51:-1, 2:]
        features_scaled = scaler_1.transform(features)

        yhat = model.predict(features_scaled)
        y_pre_inv = scaler_2.inverse_transform(yhat)

        plt.cla()
        plt.plot(range(1, len(y_pre_inv) + 1), y_pre_inv, color='red', linestyle='-', linewidth=0.8, label='prediction')
        plt.pause(10)

        print('冷却水回水温度为：%f' %(y_pre_inv[-1]))

    # plt.close()

    # return 0