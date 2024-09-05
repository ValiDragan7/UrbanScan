# UrbanScan

UrbanScan is an application dedicated to improving urban infrastructure and the environment through advanced visualization technology and artificial intelligence like Vision Transformers. The project integrates two essential functionalities for modern cities:

## Features

### For both potholes and waste detection
- **Detection on Images**
- **Detection on Videos**

## Technology
UrbanScan leverages the DEtection TRansformer (DETR) model, a state-of-the-art object detection framework developed by Facebook AI Research. In addition to using the pre-trained DETR model, we have customized it to better suit our specific needs for pothole and waste detection.


## Characteristics
- **User Interface**: Simple and intuitive interface for uploading and analyzing images and videos.
- **Visualization and Saving**: Options to view and save processed images.
- **Theme Modes**: Supports switching the application theme between "Light" and "Dark" for a personalized experience.

For training and evaluation, the project utilized the following datasets:

- **[TACO Dataset](https://github.com/pedropro/TACO)**: A large-scale dataset for trash detection.
- **[Pothole Detection Computer Vision Project](https://universe.roboflow.com/imacs-pothole-detection-wo8mu/pothole-detection-irkz9)**: A dataset specifically created for detecting potholes, including various types of road conditions and pothole appearances.

## Installation

Clone the repository:
```bash
git clone https://github.com/ValiDragan7/UrbanScan.git
```
## Install the models:
The models are too large to be added to github.
Install the .rar file from the link below and extract it in the "UrbanScan" folder
```
https://drive.google.com/drive/folders/14JhGs4lDD_eUWh9sEuxgj1kAGCz2N4ng?usp=sharing
```

## Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage
```bash
python Start.py
```
