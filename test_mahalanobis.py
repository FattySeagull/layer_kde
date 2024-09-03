import numpy as np
from scipy.stats import chi2

# データセットの例
data = np.array([
    [2, 3, 4],
    [5, 6, 7],
    [8, 9, 10],
    [11, 12, 13],
    [30, 21, 32],
    [33, 24, 35],
    [7, 8, 9]
    # 他のデータポイント
])

# 平均ベクトルの計算
mean_vector = np.mean(data, axis=0)

# 共分散行列の計算
cov_matrix = np.cov(data, rowvar=False)

# 共分散行列の逆行列の計算
inv_cov_matrix = np.linalg.inv(cov_matrix)

# マハラノビス距離の計算関数
def mahalanobis_distance(x, mean, inv_cov):
    diff = x - mean
    return np.sqrt(np.dot(np.dot(diff, inv_cov), diff.T))

# 各データポイントのマハラノビス距離を計算
distances = np.array([mahalanobis_distance(x, mean_vector, inv_cov_matrix) for x in data])

# カイ二乗分布の閾値を設定（自由度はデータの次元数）
threshold = chi2.ppf(0.95, df=data.shape[1])

# 外れ値の判定
outliers = distances > np.sqrt(threshold)

print("マハラノビス距離:", distances)
print("外れ値:", outliers)
