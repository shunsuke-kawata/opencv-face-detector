import cv2
import glob
import os

ext_list = ['.jpg','.JPG','.jpeg','.JPEG','.png','.PNG']
# カスケード型識別器の読み込み
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
def detect_face(path):
    img = cv2.imread(path)
    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 顔領域の探索
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

    # 複数の顔が検出された場合、最も大きな領域を取得
    largest_face = None
    largest_area = 0
    for (x, y, w, h) in faces:
        area = w * h
        if area > largest_area:
            largest_face = (x, y, w, h)
            largest_area = area

    # 最も大きな領域に対してのみ処理を行う
    if largest_face is not None:
        x, y, w, h = largest_face

        # 顔領域を切り抜いて新しい画像を作成
        face_img = img[y:y + h, x:x + w]

        # 結果を出力
        basename = os.path.basename(path)
        try:
            cv2.imwrite(f"./results/{basename}", face_img)
        except:
            print("failed to detection")

def get_files():
    dir_path = "./"

    files_dir = [f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]
    
    for dir in files_dir:
        if(dir=='.git'):
            continue
        
        files = glob.glob(f"./{dir}/*")
        for filepath in files:
            _,extension = os.path.splitext(filepath)
            if(extension in ext_list):
                detect_face(filepath)
            else:
                print(extension)
            
            
    
    
def main():
    get_files()

if __name__ == '__main__':
    main()