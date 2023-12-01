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

class TrainArgs:
    def __init__(self) -> None:
        self.device = ConfigureDevice()

        self.batch_size = 4
        self.lr = 0.001
        self.T = 2
        self.CONTENT_WEIGHT = 1
        self.STYLE_WEIGHT = 1000000
        self.REG_WEIGHT = 1e-5

        self.continue_training = True

        self.CONTENT_IMG_DIR = 'coco'
        self.STYLE_IMG_DIR = 'style_img'
        self.SetModelWeightDir("weights")
        
        self.SetK(1000)
        
        pass

    def SetModelWeightDir(self, modelweight_dir):
        self.MODEL_WEIGHT_DIR = modelweight_dir
        self.BANK_WEIGHT_DIR = os.path.join(self.MODEL_WEIGHT_DIR, 'bank')
        self.BANK_WEIGHT_PATH = os.path.join(self.BANK_WEIGHT_DIR, '{}.pth')
        
        self.MODEL_WEIGHT_PATH = os.path.join(self.MODEL_WEIGHT_DIR, 'model.pth')
        self.ENCODER_WEIGHT_PATH = os.path.join(self.MODEL_WEIGHT_DIR, 'encoder.pth')
        self.DECODER_WEIGHT_PATH = os.path.join(self.MODEL_WEIGHT_DIR, 'decoder.pth')
        self.GLOBAL_STEP_PATH = os.path.join(self.MODEL_WEIGHT_DIR, 'global_step.log')

        self.SetNewBankWeightDir('new_bank')

    def SetNewBankWeightDir(self, newbankweight_dir):
        '''
        进行增量训练的时候，要指定新的bank weight子目录
        '''
        # 带new字样的，是在incremental learning中，需要继续创建新的bank weights，因此这里可以把目录拆分出来
        self.NEW_BANK_WEIGHT_DIR = os.path.join(self.MODEL_WEIGHT_DIR, newbankweight_dir)
        self.NEW_BANK_WEIGHT_PATH = os.path.join(self.NEW_BANK_WEIGHT_DIR, '{}.pth')

    
    
    def SetK(self, k):
        self.K = k
        self.MAX_ITERATION = 300 * self.K
        self.ADJUST_LR_ITER = 10 * self.K
        self.LOG_ITER = 1 * self.K