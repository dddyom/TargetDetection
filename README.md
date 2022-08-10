# TargetDetection

---

### Build

```shell
git clone https://github.com/dddyom/TargetDetection && cd TargetDetection
```

```shell
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python -m pip install --upgrade pip
git clone https://github.com/ultralytics/yolov5.git
```

```shell
rm yolov5/detect.py && mv custom_detect.py yolov5/detect.py
```

```shell
nano config.ini
```

```shell
time python main.py
```
