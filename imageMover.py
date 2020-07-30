import cv2
import glob
import shutil
import os
import numpy as np

#画像のサイズは200pxで統一
size = (200, 200)  

name = []   #ファイル名
data = []   #ファイルのデータ
coordinates = []    #クリック時の座標

#移動先のフォルダを作成。LとRがそれぞれ左クリックと右クリックに対応。
os.makedirs('./L', exist_ok=True)
os.makedirs('./R', exist_ok=True)

#ファイルの読み込み
for file in glob.glob('*.bmp'):
    img = cv2.imread(file)
    img = cv2.resize(img, size) 
    name.append(file) 
    data.append(img)

#マウスクリック時に実行される関数
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        coordinates[0:3] = [x, y, 'L']
    if event == cv2.EVENT_RBUTTONDOWN:
        coordinates[0:3] = [x, y, 'R']

#画像の枚数
hasWindow = len(data)

#画像の残り枚数が1枚以上の場合に実行
while hasWindow > 0:
    img = cv2.hconcat(data[:5])

    while(1):
        cv2.imshow('img', img)
        cv2.setMouseCallback("img", click_event) #クリック時
        
        #クリック時の座標を取得し、対応する画像を移動
        if len(coordinates) != 0:
            n = coordinates[0]//200
            shutil.move(name[n], coordinates[2]+'/'+name[n])
            print(F'フォルダ {coordinates[2]} に {name[n]} を移動しました')
            data.pop(n)
            name.pop(n)
            coordinates = []
            hasWindow -= 1 #画像の残り枚数を更新
            break
        
        #座標を初期化
        coordinates = []    

        #キー入力があるか
        key = cv2.waitKey(100) & 0xff

        #キーボードかｘが押されたらウィンドウを閉じる
        if key != 255 or cv2.getWindowProperty('img', cv2.WND_PROP_AUTOSIZE) == -1:
            cv2.destroyAllWindows()
            exit()