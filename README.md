# Image Segmenter

Group 5 proudly presents their image editing application with an included image segmenter
giving users the option to segment images using different algorithms.

### Setup instructions

#### Create virtual environment and install dependencies

Using `venv`:

```sh
python -m venv venv
source ./venv/bin/activate # Unix
./venv/bin/Activate.ps1    # Windows
pip install -r requirements.txt
```

Using `conda`:

```sh
conda create -n group-5
conda activate group-5
conda install --file conda.txt
```

#### Run the application

```
python src/main.py
```
