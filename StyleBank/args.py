import torch
import os

def ConfigureDevice():
    '''
    这里可以同时支持cuda和mps
    '''
    device = torch.device("cpu")
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
    elif torch.has_mps:
        if not torch.backends.mps.is_available():
            if not torch.backends.mps.is_built():
                print("MPS not available because the current PyTorch install was not "
                    "built with MPS enabled.")
            else:
                print("MPS not available because the current MacOS version is not 12.3+ "
                    "and/or you do not have an MPS-enabled device on this machine.")
        else:
            device = torch.device("mps")
    print("device:" + str(device))
    return device

device = ConfigureDevice()

batch_size = 4
lr = 0.001
T = 2
CONTENT_WEIGHT = 1
STYLE_WEIGHT = 1000000
REG_WEIGHT = 1e-5

continue_training = True

CONTENT_IMG_DIR = 'coco'
STYLE_IMG_DIR = 'style_img'
MODEL_WEIGHT_DIR = 'weights_test'
BANK_WEIGHT_DIR = os.path.join(MODEL_WEIGHT_DIR, 'bank')
BANK_WEIGHT_PATH = os.path.join(BANK_WEIGHT_DIR, '{}.pth')
MODEL_WEIGHT_PATH = os.path.join(MODEL_WEIGHT_DIR, 'model.pth')
ENCODER_WEIGHT_PATH = os.path.join(MODEL_WEIGHT_DIR, 'encoder.pth')
DECODER_WEIGHT_PATH = os.path.join(MODEL_WEIGHT_DIR, 'decoder.pth')
GLOBAL_STEP_PATH = os.path.join(MODEL_WEIGHT_DIR, 'global_step.log')

K = 1000
MAX_ITERATION = 300 * K
ADJUST_LR_ITER = 10 * K
LOG_ITER = 1 * K