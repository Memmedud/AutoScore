import numpy as np
from sklearn.cluster import KMeans

def make_histogram(cluster):
    numLabels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    hist, _ = np.histogram(cluster.labels_, bins=numLabels)
    hist = hist.astype('float32')
    hist /= hist.sum()
    return hist

def ColorPicker (color):
    lower_red = np.array([100, 0, 0])
    upper_red = np.array([255, 110, 165])
    lower_yellow = np.array([100, 110, 0])
    upper_yellow = np.array([255, 255, 180])
    if np.all(color > lower_red) and np.all(color < upper_red):
        return(1)
    elif np.all(color > lower_yellow) and np.all(color < upper_yellow):
        return(2)
    else:
        return(0) #Not a valid color, remove this "stone"

def FindColor (img, its):
    height, width, _ = np.shape(img)
    image = img.reshape((height * width, 3))
    clusters = KMeans(n_clusters=its)
    clusters.fit(image)
    histogram = make_histogram(clusters)
    combined = zip(histogram, clusters.cluster_centers_)
    combined = sorted(combined, key=lambda x: x[0], reverse=True)
    for index, rows in enumerate(combined):
        rgb = (int(rows[1][2]), int(rows[1][1]), int(rows[1][0]))
        if np.all(rgb > np.array([5, 5, 5])):
            return(ColorPicker(rgb))
