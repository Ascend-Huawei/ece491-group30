# Deep Learning Models
The deep learning models provided by Huawei are all pre-trained using the [Caffe](https://caffe.berkeleyvision.org/) framework. These pre-trained models must be converted to Huawei's offline model (.om) format to use. 
- Head Pose Estimation model
- Body Pose Estimation model

## Obtaining Required Models

The head pose estimation model recognizes the head pose of a person in terms of 3 angles: *yaw*, *pitch* and *roll* in an image. The face detection model is used to locate the face region prior to inferring the head pose angles.


1. Face Detection


Download the weights and network files to the models directory.

- Weights: https://c7xcode.obs.cn-north-4.myhuaweicloud.com/models/face_detection/face_detection.caffemodel
- Network: https://c7xcode.obs.cn-north-4.myhuaweicloud.com/models/face_detection/face_detection.prototxt

 Then, run the following command to create the offline model. 

```atc --output_type=FP32 --input_shape="data:1,3,300,300" --weight="face_detection.caffemodel" --input_format=NCHW --output="face_detection" --soc_version=Ascend310 
--framework=0 --save_original_model=false 
--model="face_detection.prototxt"
```

2. Head Pose Estimation

Download the weights and network files to the models directory.

- Weights:
https://obs-model-ascend.obs.cn-east-2.myhuaweicloud.com/head_pose_estimation/head_pose_estimation.caffemodel
- Network: https://raw.githubusercontent.com/Ascend-Huawei/models/master/computer_vision/object_detect/head_pose_estimation/head_pose_estimation.prototxt

Execute the following command from your project directory 'head_pose_estimation/src' to convert the pre-trained model for head pose estimation to offline model (.om) format:

```
atc --output_type=FP32 --input_shape="data:1,3,224,224" --weight="head_pose_estimation.caffemodel" --input_format=NCHW --output="head_pose_estimation"
--soc_version=Ascend310 --framework=0 --save_original_model=false --model="head_pose_estimation.prototxt"
```

## Face Detection and Head Pose Estimation Models
#### Inputs
The input for face detection model are as follows:
- **Input Shape**: [1,300,300, 3]
- **Input Format** : NCHW
- **Input Type**: BGR FLOAT32

The input for the head pose estimation model are as follows:
- **Input Shape**: [1,3, 224, 224]
- **Input Format** : NCHW
- **Input Type**: BGR FLOAT32

#### Outputs
Outputs for the face detection model:

- 2 lists. Only the 2nd list is used.
  - **1st list shape**: [1,8]
  - **2nd list shape**: [1, 100, 8]
- For the second list: **100** represents 100 bounding boxes. **0-8** describe information of each box as below:
  - **0 position**: not used
  - **1 position**: label
  - **2 position**: confidence score
  - **3 position**: top left x coordinate
  - **4 position**: top left y coordinate
  - **5 position**: bottom right x coordinate
  - **6 position**: bottom right y coordinate
  - **7 position**: not used
  
The outputs for the head pose estimation model are as follows:
- List of numpy arrays: 
  - **Array shapes**: (1, 136, 1, 1), (1, 3, 1, 1)
The first list is a set of 136 facial keypoints. The second list in the output containing the 3 values of yaw, pitch, roll angles predicted by the model, which are used to determine head pose based on some preset rules.

Output printed to terminal (sample):
```
Head angles: [array([[9.411621]], dtype=float32), array([[7.91626]], dtype=float32), array([[-1.0116577]], dtype=float32)]
Pose: Head Good posture
```

## Body Pose Estimation
The body pose model is a simplified version for edge computing, based on the model [here](https://github.com/Daniil-Osokin/lightweight-human-pose-estimation.pytorch). It directly outputs the predicted locations of the human body joints. The set of 14 detected joints are shown in the diagram below:

                     12                     0-right shoulder, 1-right elbow, 2-right wrist, 3-left shoulder
                     |                      4-left elbow, 5-left wrist, 6-right hip, 7-right knee, 8-right ankle
                     |                      9-left hip, 10-left knee, 11-left ankle, 12-top of the head, 13-neck
               0-----13-----3
              /     / \      \
             1     /   \      4
            /     /     \      \
           2     6       9      5
                 |       |
                 7       10
                 |       |
                 8       11

    
**Performance:** The inference time of running the model on Atlas 200 DK is about 17 ms per image/frame .  
**Limitation:** The model works well when there is only one persion and with whole body clearly shown in the view.



