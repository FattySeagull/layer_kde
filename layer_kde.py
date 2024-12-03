import sys
import os
import shutil
import glob
import itertools as iter

import datatable as dt
from datatable import f

import numpy as np
from scipy import stats
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import matplotlib.colors
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable

from tkinter import filedialog
from tkinter import messagebox


from nikon_utils import nknmnt as nk
from layer_stats import layer_stats as lys
from myutils import myutils as myu

if __name__ == '__main__':
    # Get command line arguments
    # file = myu.get_inputfile([('monitorファイル','*.csv')]) if len(sys.argv) <= 1 else sys.argv[1]
    alpha = 3.0 if len(sys.argv) <= 2 else float(sys.argv[2])
    
    # Select monitor file
    file = myu.get_inputfile([('monitorファイル','*.csv')])

    # dir_path = myu.get_inputdir()
    # files = glob.glob(dir_path + "/monitor_#*.csv")
    # if len(files) < 1:
    #     sys.exit()

    # dirname = dir_path
    # outdirname = dir_path + "\\outliers"
    # myu.makefolder(outdirname, when_exists='a', sudden_quit=True)

    # for file in files:
    print(f"file path:{file}")

    fname = os.path.basename(file)  # ファイル名を取得
    ftitle = os.path.splitext(os.path.basename(file))[0]    # 拡張子を除いたファイル名を取得

    # Prepare parameters to deal
    nk.inactivateall_monitor_parameters()
    nk.activate_monitor_parameters(
        "Layer", "X", "Y", "Z", "Length", "Width", "SpatterCount", "SpatterTotal", "SpatterMax")
    params = nk.active_monitor_parameters()[4:]
    mnpas = nk.active_monitor_parameters()
    mnpis = nk.inactive_monitor_parameters()
    keys = ["Length", "Width", "SpatterCount", "SpatterTotal", "SpatterMax"]

    # CSVファイルを読み込む
    df = dt.fread(file)
    df = lys.rm_columns(df, mnpis)  # remove deactivated columns
    df = lys.rm_na_row(df, skip_cols = 4)  # remove rows with NA
    #df = df[dt.rowsum(dt.isna(f[4, :])) < len(mnpas) - 4, :]    # Noneを含む行を落とす
    df = df[::100,:]    # 100分の1サンプリング

    
    cx, cy = df[:, dt.mean(f.X)][0, 0], df[:, dt.mean(f.Y)][0, 0]
    df['Radius'] = df[:, dt.math.sqrt((f.X - cx)**2 + (f.Y - cy)**2)]
    df['Aspect Ratio'] = df[:, f.Length / f.Width]
    keys.append('Aspect Ratio')
    #x = df['Aspect Ratio'].to_numpy()
    x = df['Radius'].to_numpy()
    
    for key in keys:
        # サンプルデータの生成
        y = df[key].to_numpy()
        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(x, y, s=2, alpha=0.1)
        plt.axis('equal')
        plt.xlim(0, 7)
        #plt.xlabel('Aspect ratio')
        plt.xlabel('Radius, mm', fontsize=14)
        plt.ylabel(key, fontsize=14)
        plt.title(f"Radius vs {key}", fontsize=16)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.savefig(f"{ftitle}_R_vs_{key}_clustered.png")
        plt.show()


    # for key in keys:
    #     dfstats = df[:, {
    #         'Layer': 0,
    #         'mean': dt.mean(f[key]),
    #         'stdev': dt.sd(f[key]),
    #         'median': dt.median(f[key]),
    #         'min': dt.min(f[key]),
    #         'max': dt.max(f[key]),
    #         'cnt': dt.count(f[key]),
    #         'cnt_in': 0,
    #         'cnt_out': 0,
    #         'r_in': 0.0,
    #         'r_out': 0.0
    #         }]
    #     mu = dfstats[0, f.mean][0,0]
    #     sg = dfstats[0, f.stdev][0,0]
    #     num = dfstats[0, f.cnt][0,0]

    #     # alpha = 3.0
    #     df['Zscore'] = df[:, (f[key] - mu)/sg]
    #     dfi = df[dt.abs(f.Zscore)<=alpha, [f.Layer, f.X, f.Y, f.Z, f[key], f.Zscore]]
    #     dfo = df[dt.abs(f.Zscore)>alpha, [f.Layer, f.X, f.Y, f.Z, f[key], f.Zscore]]

    #     dfstati = dfi[:, {
    #         'mean': dt.mean(f[key]),
    #         'stdev': dt.sd(f[key]),
    #         'median': dt.median(f[key]),
    #         'min': dt.min(f[key]),
    #         'max': dt.max(f[key]),
    #         'cnt_in': dt.count(f[key]),
    #         }, by(f.Layer)]
    #     dfstato = dfo[:, {'cnt_out': dt.count(f[key])}, by(f.Layer)]
    #     dfstato.key = 'Layer'
    #     dfmerg = dfstati[:, :, dt.join(dfstato)]
    #     dfmerg[:, dt.update(cnt = f.cnt_in + f.cnt_out,
    #                     r_in = f.cnt_in / (f.cnt_in + f.cnt_out),
    #                     r_out = f.cnt_out / (f.cnt_in + f.cnt_out))]
    #     dfstats[f.Layer == 0, dt.update(
    #         cnt_in = dfmerg[:, dt.sum(f.cnt_in)],
    #         cnt_out = dfmerg[:, dt.sum(f.cnt_out)])]
    #     dfstats[f.Layer == 0, dt.update(
    #         r_in = f.cnt_in/f.cnt,
    #         r_out = f.cnt_out/f.cnt)]
    #     dfstats.rbind(dfmerg)
    #     dfo.to_csv(f"{outdirname}\{ftitle}_{key}_outlier_inner.csv")
    #     dfstats.to_csv(f"{outdirname}\{ftitle}_{key}_stats_inner.csv")

    #     print(f"{key} fstats:\n{dfstats[:1,:]}")

    #     if dfo.nrows > 0:
    #         data = dfo.to_numpy()
    #         # 可視化
    #         plt.clf()
    #         fig = plt.figure(figsize=(8, 6), layout='tight')
    #         ax = fig.add_subplot(111, projection='3d')
    #         scatter = ax.scatter(data[:, 1], data[:, 2], data[:, 3],  c=data[:, 4],
    #                                 cmap='jet', s=0.5) # Create a scatter plot
    #         cbar = fig.colorbar(scatter, orientation="vertical", pad=0.15, shrink=0.6)
    #         cbar.set_label(f"{key},{nk.mnp[key]['unit']}")  # Set the colorbar label
    #         ax.set_xlabel('x, mm')
    #         ax.set_ylabel('y, mm')
    #         ax.set_zlabel('z, mm')
    #         ax.set_title(f"Outlier by Z-Score Test: {key}")
    #         plt.savefig(f"{outdirname}\{ftitle}_{key}_outlier_inner.png")
    #         #plt.show()
    #         plt.close()

    #         #print("Num of Outliers:", len(data))
    #     else:
    #         #print("No outlier data.")
    #         pass

    print("Finished.")