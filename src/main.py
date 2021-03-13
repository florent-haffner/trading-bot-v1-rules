import matplotlib.pyplot as plt
from data_acquisition import getFormattedData


if __name__ == "__main__":
    minute = getFormattedData('BTCEUR', '1')
    print(len(minute))
    minute.plot('timestamp', 'volume')
    plt.show()

    heure = getFormattedData('BTCEUR', '60')
    print(len(heure))
    heure.plot('timestamp', 'volume')
    plt.show()
