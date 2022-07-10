# Digit Draw

This program uses a pretrained MNIST Classification model to predict a user-drawn digit through Flask.

<img src="images/mov.gif">


## Setup

```bash
cd digit-draw

# setup conda env
conda create --name myenv python==3.8
conda activate myenv
conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
pip install -r requirements.txt

# run app
flask run
```
Then, go to http://127.0.0.1:5000.

## Usage
Draw a number and click "predict" to see the prediction!

