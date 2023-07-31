import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

phimatrix = pd.read_csv("phimatrix_L6.csv")

for i in range(len(phimatrix)):
    val = phimatrix.iloc[i].values[0:6]
    phi = np.array(phimatrix.iloc[i].values[6:].reshape([8,8]),dtype = float)
    plt.figure(figsize=(20,10))
    sns.heatmap(phi,cmap='magma',annot=True)
    plt.savefig("plots/L{}_Beta{}_Sheet{}.png".format(val[1], val[2], val[4]), format = "png", dpi = 300)