# import threading
# from datetime import datetime
# import time

# def printit():
#   threading.Timer(5.0, printit).start()
#   print("Hello, World! ", datetime.now())

# printit()
# while True:
#     print("MAIN")
#     time.sleep(2)
  
# import cv2 

# key = cv2. waitKey(1)
# webcam = cv2.VideoCapture(0)
# while True:
#     try:
#         check, frame = webcam.read()
#         print(check) #prints true as long as the webcam is running
#         print(frame) #prints matrix values of each framecd 
#         cv2.imshow("Capturing", frame)
#         key = cv2.waitKey(1)
#         if key == ord('s'): 
#             cv2.imwrite(filename='saved_img.jpg', img=frame)
#             webcam.release()
#             img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
#             img_new = cv2.imshow("Captured Image", img_new)
#             cv2.waitKey(1650)
#             cv2.destroyAllWindows()
#             print("Processing image...")
#             img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
#             print("Converting RGB image to grayscale...")
#             gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
#             print("Converted RGB image to grayscale...")
#             print("Resizing image to 28x28 scale...")
#             img_ = cv2.resize(gray,(28,28))
#             print("Resized...")
#             img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
#             print("Image saved!")
        
#             break
#         elif key == ord('q'):
#             print("Turning off camera.")
#             webcam.release()
#             print("Camera off.")
#             print("Program ended.")
#             cv2.destroyAllWindows()
#             break
        
#     except(KeyboardInterrupt):
#         print("Turning off camera.")
#         webcam.release()
#         print("Camera off.")
#         print("Program ended.")
#         cv2.destroyAllWindows()
#         break

# import cv2 as cv
# from yolo import YOLO

# cap = cv.VideoCapture(0)
# yolo = YOLO(stream=True)
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     cv.imshow('frame', frame)

#     # print("type of frame var -> " + str(type(frame)))
#     # print(frame)

#     detect = yolo.detect(frame)

#     # print(str(detect))

#     c = cv.waitKey(5)
#     if c == 27:
#         break

# cap.release()
# cv.destroyAllWindows()

# import cv2
# cap=cv2.VideoCapture("rtsp://admin:cctv1234@192.168.1.100:554/h264Preview_01_main")

# ret,frame = cap.read()
# while ret:
#     ret,frame = cap.read()
#     cv2.imshow("frame",frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cv2.destroyAllWindows()
# cap.release()

import cv2
import numpy as np
from openvino.inference_engine import IECore
from openvino.inference_engine import IENetwork
from blazeface import BlazeFace


def load_to_IE(model):
    # Loading the Inference Engine API
    ie = IECore()
    # Loading IR files
    net = IENetwork(model=model + ".xml", weights=model + ".bin")
    # Loading the network to the inference engine
    exec_net = ie.load_network(network=net, device_name="CPU")

    return exec_net


def do_inference(exec_net, image):
    input_blob = next(iter(exec_net.inputs))
    return exec_net.infer({input_blob: image})

# load BlazeFace model
blaze_net = load_to_IE("model/blazeface")
# load FaceMesh model
mesh_net = load_to_IE("model/facemesh")

# we need dynamically generated key for fetching output tensor
blaze_outputs = list(blaze_net.outputs.keys())
mesh_outputs = list(mesh_net.outputs.keys())

# to reuse postprocessing from BlazeFace
blazenet = BlazeFace()
blazenet.load_anchors("anchors.npy")


videoCapture = cv2.VideoCapture(0)
while True:
    ret, image = videoCapture.read()
    if not ret:
        break

    # get face detection boxes------------------------------------------------------------------
    # preprocessing
    face_img = cv2.dnn.blobFromImage(image, 1./127.5, (128, 128), (1, 1, 1), True)
    # inference
    output = do_inference(blaze_net, image=face_img)
    # postprocessing
    boxes = output[blaze_outputs[0]]
    confidences = output[blaze_outputs[1]]
    detections = blazenet._tensors_to_detections(boxes, confidences, blazenet.anchors)
    detections = np.squeeze(detections, axis=0)
    # take boxes
    xmin, ymin, face_img = get_crop_face(detections, image)

    # get face mesh ----------------------------------------------------------------------------
    # preprocessing
    mesh_img = cv2.dnn.blobFromImage(face_img, 1./127.5, (192, 192), (1, 1, 1), True)
    #inference
    output = do_inference(mesh_net, image=mesh_img)
    # postprocessing
    detections = output[mesh_outputs[1]].reshape(-1, 3)
    # take mesh
    get_mesh_face(detections, face_img, image, xmin, ymin)

    # show processed image
    cv2.imshow("capture", image)

    if cv2.waitKey(3) & 0xFF == 27:
        break
