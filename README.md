# TargetDetection

---

### Build

```shell
git clone https://github.com/dddyom/TargetDetection && cd TargetDetection
```

**Creating a virtual environment**

```shell
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python -m pip install --upgrade pip
git clone https://github.com/ultralytics/yolov5.git
```

**Replacing the original detect in yolov5 with our own, modified**

```shell
rm yolov5/detect.py && mv custom_detect.py yolov5/detect.py
```

**Entering launch options**

```shell
nano config.ini
```

### Run

```shell
(source env/bin/activate)
time python main.py
```


