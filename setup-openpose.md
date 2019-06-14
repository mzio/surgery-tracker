# OpenPose Sherlock Setup Notes  

The following are notes for loading (and running) OpenPose on a Sherlock remote GPU compute cluster. Do the below and hopefully things will work.  

[Reference for command-line-only configuration](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation.md#cmake-command-line-configuration-ubuntu-only)  

1. Request an interactive node, i.e. `srun -N 1 -c 2 --time=08:00:00 -p gpu --gres=gpu:2 --x11=all --pty bash`  

2. Load dependencies:  
* `module load protobuf python/2.7.13 cuda/8.0.61 cudnn/5.1 opencv system gflags glog cmake` 
* Caffe also has the following dependencies: `leveldb, snappy, boost/1.64.0, hdf5/1.10.0p1, lmdb`
* Keep in mind that if you load other modules, you need to load cmake again so that it recognizes them.  

3. Build openpose:  
  1. (If not done already), clone from openpose (`git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose`)  
  2. Make a new directory `build` and cd to it  
  3. Do `cmake -DBUILD_PYTHON=ON ..`
    * If the above gives an error, manually clone caffe into `3rdparty` at `git clone https://github.com/CMU-Perceptual-Computing-Lab/caffe.git` 
    * Note this is a custom branch of Caffe  
    * Might also need to clone pybind11: `git clone https://github.com/pybind/pybind11.git`   
    * _Edit_: Actually think you should do:
```
cmake -DOpenCV_INCLUDE_DIRS=/home/"${USER}"/softwares/opencv/build/install/include \
  -DOpenCV_LIBS_DIR=/home/"${USER}"/softwares/opencv/build/install/lib -BUILD_PYTHON=ON ..
```
      * _Edit_: Actually not sure. To specify Python though, do `cmake -DBUILD_PYTHON=ON .. ``

4. Actually build then by calling `make 2>&1 | tee make_log.out` (which saves output to a log file)  

Do I need `atlas`? Maybe  
* Possibly build caffe first  

Might a


Alternatively, for Python library, try the following to install `pyopenpose`:  

1. Load dependencies:  
* `module load boost/1.64.0 hdf5/1.10.0p1 eigen`` 
