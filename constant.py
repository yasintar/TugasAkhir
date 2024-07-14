DEVICEDEBUGCAMERA1   = 'rtsp://admin:L2EB9DF5@192.168.3.29:554/cam/realmonitor?channel=1&subtype=0' #imou_0------cam1
DEVICESTGCAMERA1     = 'rtsp://admin:L2EB9DF5@192.168.3.29:554/cam/realmonitor?channel=1&subtype=0' #imou_0

DEVICEDEBUGCAMERA2   = 'rtsp://admin:L2C1BFD5@192.168.3.30:554/cam/realmonitor?channel=1&subtype=0' #imou_Q------cam2
DEVICESTGCAMERA2     = 'rtsp://admin:L2C1BFD5@192.168.3.30:554/cam/realmonitor?channel=1&subtype=0' #imou_Q

TIME                = 1
IMG_PATH            = './image/'
TIMESLEEPTHREAD     = 0.1
TIMEADAPTCPU        = 20
TIMEADAPTRAM        = 60
TIMEADAPTDISK       = 100

YOLO_SCALE          = 0.00392
YOLO_IMGSIZE        = (416,416)
YOLO_CONFI          = 0.45
YOLO_WEIGHT         = './model/yolov5s.onnx' #changed
YOLO_CFG            = './model/yolov4-tiny.cfg'  #changed

FULL_RESOURCE       = 100
FULL_RESOURCE_DISK  = 75
CONST_CPU           = 60      #Batas usage CPU jika lebih do something
CONST_RAM           = 40      #Batas usage RAM jika lebih do something
CONST_DISK          = 73      #Batas usage Disk jika lebih do something

MAX_RELAY_LIST      = 5
RELAIS_1_GPIO       = 17
