import datatable as dt
import numpy as np
from scipy.stats import chi2

# データセットの作成
data = [
    {"x": 2, "y": 3, "z": 4},
    {"x": 5, "y": 6, "z": 7},
    {"x": 8, "y": 9, "z": 10},
    # 他のデータ行を追加
]

# datatableフレームの作成
df = dt.Frame(data)

# 平均ベクトルの計算
mean_vector = df.mean().to_numpy()[0]

# 共分散行列の計算
cov_matrix = np.cov(df.to_numpy().T)

# 共分散行列の逆行列の計算
inv_cov_matrix = np.linalg.inv(cov_matrix)

# マハラノビス距離の計算関数
def mahalanobis_distance(x, mean, inv_cov):
    diff = x - mean
    return np.sqrt(np.dot(np.dot(diff, inv_cov), diff.T))

# 各データポイントのマハラノビス距離を計算
distances = np.array([mahalanobis_distance(row, mean_vector, inv_cov_matrix) for row in df.to_numpy()])

# カイ二乗分布の閾値を設定（自由度はデータの次元数）
threshold = chi2.ppf(0.95, df.shape[1])

# 外れ値の判定
outliers = distances > np.sqrt(threshold)

print("マハラノビス距離:", distances)
print("外れ値:", outliers)
