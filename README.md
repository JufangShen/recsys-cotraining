# Building an algorithm that improves recommendations under Co-Training. #
This repository holds the code, the datasets and results for the thesis project:
Building an algorithm that improves recommendations under Co-Training.

This thesis research is under supervision of Professor Paolo Cremonesi and
PhD student Maurizio Ferrari.

## Project organization. ##
The code is organized as follows:
  - Datasets:
  - Implementation:
  - Results:

## Project installation. ##
### Requirements.
  - `Python 3.5+`.
  - `C++` Compiler.
  - On Linux, ensure that you have packages `libc6-dev` and `build-essentials`

### Installation instructions
  1. [On Linux] Install Linux packages: `apt-get install -y libc6-dev build-essentials`.
  2. Install `Miniconda` for `Python 3.5+` [here](https://conda.io/miniconda.html).
  3. Create the virtual environment: `conda create -n cotraining --file requirements.txt`
  4. Activate the virtual environment: `source activate cotraining`.
  5. [Installation and run separately] Install the project: `cd Configuration/ ; sh install.sh ; cd ..`
  6. [Installation and run separately] Run one of the examples:
    * `cd run-examples/ ; sh holdout-cotraining-knn-knn.sh ; cd ..`
    * `cd run-examples/ ; sh holdout-cotraining-knn-funksvd.sh ;cd ..`
    * `cd run-examples/ ; sh holdout-cotraining-mf-mf.sh ; cd ..`

  7. [Installation and run integrated] Run the `run.sh` script: `sh run.sh`

## Results. ##
