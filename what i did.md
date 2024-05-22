downloaded ubuntu24.04 lts iso

booted into usb

turned off windows drive bitlocker
turned off secure boot
turned off igraphic
set the default storage controller to SATA


installed ubuntu 24.04


installed nvidia proprietary driver 535 
installed python3.11
installed CUDA 12.2
installed cuDNN version ?

wanted to install tensorrt fail yet


cloned into tfodcourse repo

created venv
    python3.11 -m venv tfod
    source tfod/bin/activate

install ipykernel
    pip install ipykernel

install env in ipykernel
    python -m ipykernel install --user --name=tfod

initiated git and did some file managing

installed jupyter 
    pip install jupyter
ERROR : 404 GET /static/notebook/3654.bundle.js : pip install notebook==6.1.5

        Server Information:
        You are using Jupyter notebook.

        The version of the notebook server is: 6.1.5-6702d05
        The server is running on this version of Python:
        Python 3.11.9 (main, Apr 27 2024, 21:16:11) [GCC 13.2.0]

        Current Kernel Information:
        Waiting for kernel to be available...
`


run jupyter note book to validate environment installation
    jupter notebook

image collector app with qt5
    
installed labelimg
    https://github.com/HumanSignal/labelImg
    !cd {LABELIMG_PATH} && make qt5py3
    !cd {LABELIMG_PATH} && python labelImg.py

collecting and labeling images

collecting models
    https://github.com/tensorflow/models
    https://github.com/tensorflow/models/tree/master
    https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md
    

install tensoeflow for gpu
    pip install tensorflow 
    pip install tensorflow[and-cuda]

install tensorflow object detection api
    sudo apt-get install protobuf-compiler
    cd Tensorflow/models/research && protoc object_detection/protos/*.proto --python_out=. && cp object_detection/packages/tf2/setup.py . && python -m pip install . 
    
