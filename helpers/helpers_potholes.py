import os
import cv2
import torch
import supervision as sv
from transformers import DetrForObjectDetection, DetrImageProcessor

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
CHECKPOINT = 'facebook/detr-resnet-50'
CONFIDENCE_THRESHOLD = 0.5
BATCH_SIZE = 4
image_processor = DetrImageProcessor.from_pretrained(CHECKPOINT)

id2label = {
    0: 'potholes',
    1: 'pothole'
}

model = DetrForObjectDetection.from_pretrained("D:/Cursuri/ZParticular/LicentaProiectWindows/LicentaProiect/Models/potholes-model-real")
model.to(DEVICE)
model.eval()
box_annotator = sv.BoxAnnotator()


def process_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(os.path.join(output_path, "results_pothole.mp4"), fourcc, fps, (width, height))

    if not out.isOpened():
        print("Error: Could not open VideoWriter.")
        return

    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frames.append(frame)
        if len(frames) == BATCH_SIZE:
            process_and_write_batch(frames, out)
            frames = []

    if frames:
        process_and_write_batch(frames, out)

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def process_and_write_batch(frames, out):
    with torch.no_grad():
        inputs = image_processor(images=frames, return_tensors='pt').to(DEVICE)

        outputs = model(**inputs)
        target_sizes = torch.tensor([frame.shape[:2] for frame in frames]).to(DEVICE)
        results = image_processor.post_process_object_detection(
            outputs=outputs,
            threshold=CONFIDENCE_THRESHOLD,
            target_sizes=target_sizes
        )
    for frame, result in zip(frames, results):
        try:
            detections = sv.Detections.from_transformers(transformers_results=result).with_nms(threshold=0.5)
            labels = [f"{id2label[class_id]} {confidence:.2f}" for _, confidence, class_id, _ in detections]
            annotated_frame = box_annotator.annotate(scene=frame.copy(), detections=detections, labels=labels)
            out.write(annotated_frame)
        except:
            out.write(frame)


def detect_and_annotate_image(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Perform object detection
    with torch.no_grad():
        # Prepare input tensors for the model
        inputs = image_processor(images=image, return_tensors='pt').to(DEVICE)

        # Run object detection model
        outputs = model(**inputs)

        # Post-process object detection results
        target_sizes = torch.tensor([image.shape[:2]]).to(DEVICE)
        results = image_processor.post_process_object_detection(
            outputs=outputs,
            threshold=CONFIDENCE_THRESHOLD,
            target_sizes=target_sizes
        )[0]

    try:

        detections = sv.Detections.from_transformers(transformers_results=results).with_nms(threshold=0.8)

        labels = [f"{id2label[class_id]} {confidence:.2f}" for _, confidence, class_id, _ in detections]
        annotated_frame = box_annotator.annotate(scene=image.copy(), detections=detections, labels=labels)
        return annotated_frame
    except:
        return image

# # Path to your input video file
# video_path = 'C:\\Users\\drval\\Downloads\\potholes_small.mp4'
# # Path to your output video directory
# output_path = 'D:\\Cursuri\\ZParticular\\LicentaProiectWindows\\LicentaProiect\\Results'
#
# # Ensure output directory exists
# if not os.path.exists(output_path):
#     os.makedirs(output_path)
#
# # Process the video
# process_video(video_path, output_path)

# sv.show_frame_in_notebook(detect_and_annotate_image("C:\\Users\\drval\\Desktop\\potholes.jpg"),(16, 16))
