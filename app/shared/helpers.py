from PyQt5.QtWidgets import QFileDialog
import matplotlib.pyplot as plt

def plot(data, x, y):
    plt.plot(data[x], data[y])
    plt.xlabel(x)
    plt.ylabel(y)
    plt.savefig('./assets/images/graph.png')
