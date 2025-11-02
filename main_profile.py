import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    # choose your yaml file
    model = YOLO(r'C:\python work\ultralytics-yolo11-main-20250205\ultralytics\cfg\models\11\yolo11-RGCSPELAN.yaml')
    model.info(detailed=True)
    try:
        model.profile(imgsz=[640, 640])
    except Exception as e:
        print(e)
        pass
    model.fuse()