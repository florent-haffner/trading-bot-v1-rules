import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from data_acquisition import getFormattedData, splitDataset


if __name__ == "__main__":
    # minute = getFormattedData('BTCEUR', '1')
    # print(len(minute))
    # minute.plot('timestamp', 'volume')
    # plt.show()
    #
    heure = getFormattedData('BTCEUR', '60')
    # print(len(heure))
    # heure.plot('timestamp', 'volume')
    # plt.show()
    #
    print(len(heure))
    train, test = splitDataset(heure, 0.85)
    print(len(train), len(test))


    min_max_scaler = MinMaxScaler()
