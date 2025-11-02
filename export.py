import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

# onnx onnxsim onnxruntime onnxruntime-gpu

# 导出参数官方详解链接：https://docs.ultralytics.com/modes/export/#usage-examples

if __name__ == '__main__':
    model = YOLO(R'C:\python work\ultralytics-yolo11-main-bushu\runs\train\yolo11-Rephgnetv2-CA-HSFPN-DY-ladh-private date-bushu\weights\best.pt')
    model.export(format='onnx', simplify=True)