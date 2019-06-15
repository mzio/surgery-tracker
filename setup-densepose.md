# Densepose Setup  

As noted in the GitHub, Densepose requires an NVIDA GPU, Linux, Python2, Caffe2, the COCO API, and other Python packages.  

1. Load initial dependencies:  
```
module load python/2.7.13 cuda/8.0.61 cudnn/5.1 gflags glog cmake
```

2. Virtual environment setup (recommended?)  
  1. Load anaconda (although this might have issues with OpenPose): `module labs poldrack anaconda/5.0.0-py36`  
  2. Create python 2 env with (name suggested): `conda create -n env-densepose python=2.7.13`  
  3. Install requirements with `pip install -r requirements.txt` from the cloned densepose directory  
    * This step may lead to a big error with yaml. Not sure if it''s necessary to do anything about this yet  
  4. Load the following modules: `caffe2`, `py-cython/0.27.3_py27`, `py-h5py/2.7.1_py27`  
    * Sherlock h5py and caffe2 have conflicting dependencies (openmpi and cuda)     
    * Can test if caffe2 loaded correctly with 
```  
# Use to detect if Caffe2 build was successful  
python2 -c 'from caffe2.python import core' 2>/dev/null && echo "Success" || echo "Failure"
``` 
and 
```  
# Should return number > 0 to use Detectron  
python2 -c 'from caffe2.python import workspace; print(workspace.NumCudaDevices())'
``` 

3. Install the COCO API (densepose uses this dataset to train)  
```
# COCOAPI=/path/to/clone/cocoapi  (I picked ~/data/cocoapi)  
git clone https://github.com/cocodataset/cocoapi.git $COCOAPI
cd $COCOAPI/PythonAPI
# Install into global site-packages
make install
# Alternatively, if you do not have permissions or prefer
# not to install the COCO API into global site-packages
python2 setup.py install --user
``` 

2. Also load the following modules:  
* py-matplotlib/2.2.2_py27  
* py-numpy/1.14.3_py27  
* opencv (? - maybe not needed) 
* py-cython/0.27.3_py27  
* py-scipy/1.1.0_py27  
* py-h5py/2.7.1_py27  
* caffe2  

Other things can be installed with `pip install -r requirements.txt`  
setuptools
Cython
mock
scipy
h5py
memory_profiler 
