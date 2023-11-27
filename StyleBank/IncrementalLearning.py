# %%
import time
import os

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.datasets as datasets
import image_utils

import args
import utils
from networks import LossNetwork, StyleBankNet

# 当前目录
current_directory = os.path.dirname(os.path.abspath(__file__))
#current_directory = os.getcwd()

default_resource_dir = os.path.join(current_directory, "..", "Images")
content_images_dir = os.path.join(default_resource_dir, 'original')
style_images_dir = os.path.join(default_resource_dir, 'style-images')
model_dir = os.path.join(current_directory, "weights_new")

output_img_parent_dir = os.path.join(current_directory, 'styletransfer-output')

"""********Important*******"""
args.continue_training = False 
args.CONTENT_IMG_DIR = content_images_dir
args.STYLE_IMG_DIR = style_images_dir
args.MODEL_WEIGHT_DIR = model_dir

"""************************"""

device = args.device

# %%
"""
Load Dataset
"""
content_dataset = image_utils.ImageFolder(root_path=args.CONTENT_IMG_DIR, transform=utils.content_img_transform)
content_dataloader = torch.utils.data.DataLoader(content_dataset, batch_size=args.batch_size, shuffle=True, num_workers=4)

style_dataset = image_utils.ImageFolder(root_path=args.STYLE_IMG_DIR, transform=utils.style_img_transform)
style_dataset = torch.cat([img[0].unsqueeze(0) for img in style_dataset], dim=0)
style_dataset = style_dataset.to(device)

# %%
"""
Display content images
"""
for imgs, _ in content_dataloader:
    for i in range(args.batch_size):
        utils.showimg(imgs[i])
    break

# %%
"""
Display style images
"""
for img in style_dataset:
    utils.showimg(img)

# %%
"""
Define Model and Loss Network (vgg16)
"""
# 加载model
model = StyleBankNet(len(style_dataset)).to(device)
# 读取encoder权重
if os.path.exists(args.ENCODER_WEIGHT_PATH):
    model.encoder_net.load_state_dict(torch.load(args.ENCODER_WEIGHT_PATH))
else:
    raise Exception('cannot find encoder weights')

# 读取decoder权重
if os.path.exists(args.DECODER_WEIGHT_PATH):
    model.decoder_net.load_state_dict(torch.load(args.DECODER_WEIGHT_PATH))
else:
    raise Exception('cannot find encoder weights')

if not os.path.exists(args.NEW_BANK_WEIGHT_DIR):
    os.mkdir(args.NEW_BANK_WEIGHT_DIR)

# 只有style bank是train模式，其他部分固定
model.encoder_net.eval()
model.decoder_net.eval()
model.style_bank.train()
# only update the bank
optimizer = optim.Adam(model.style_bank.parameters(), lr=args.lr)
loss_network = LossNetwork().to(device)

# %%
"""
Training
"""

# [0, 1, 2, ..., N]
style_id = list(range(len(style_dataset)))
style_id_idx = 0
style_id_seg = []
# 为batch中每张图分配style id
for i in range(0, len(style_dataset), args.batch_size):
    style_id_seg.append(style_id[i:i+args.batch_size])
    
s_sum = 0 # sum of style loss
c_sum = 0 # sum of content loss
l_sum = 0 # sum of style+content loss
tv_sum = 0 # sum of tv loss

global_step = 0
LOG_ITER = int(args.LOG_ITER)

while global_step <= args.MAX_ITERATION:
    for i, data in enumerate(content_dataloader):
        global_step += 1
        data = data[0].to(device)
        batch_size = data.shape[0]
        
        style_id_idx += 1
        # 得到batch中每张图对应用哪个style id
        sid = utils.get_sid_batch(style_id_seg[style_id_idx % len(style_id_seg)], batch_size)

        optimizer.zero_grad()
        output_image = model(data, sid)
        content_score, style_score = loss_network(output_image, data, style_dataset[sid])
        content_loss = args.CONTENT_WEIGHT * content_score
        style_loss = args.STYLE_WEIGHT * style_score

        diff_i = torch.sum(torch.abs(output_image[:, :, :, 1:] - output_image[:, :, :, :-1]))
        diff_j = torch.sum(torch.abs(output_image[:, :, 1:, :] - output_image[:, :, :-1, :]))
        tv_loss = args.REG_WEIGHT*(diff_i + diff_j)

        total_loss = content_loss + style_loss + tv_loss
        total_loss.backward()
        optimizer.step()

        l_sum += total_loss.item()
        s_sum += style_loss.item()
        c_sum += content_loss.item()
        tv_sum += tv_loss.item()
            
        if global_step % 100 == 0:
            print('.', end='')
            
        if global_step % LOG_ITER == 0:
            print("gs: {} {} {:.6f} {:.6f} {:.6f} {:.6f}".format(global_step / args.K, time.strftime("%H:%M:%S"), l_sum / LOG_ITER, c_sum / LOG_ITER, s_sum / LOG_ITER, tv_sum / LOG_ITER))
            s_sum = 0
            c_sum = 0
            l_sum = 0
            tv_sum = 0

            # save the bank
            for i in range(len(style_dataset)):
                torch.save(model.style_bank[i].state_dict(), args.NEW_BANK_WEIGHT_PATH.format(i))
            
        if global_step % args.ADJUST_LR_ITER == 0:
            lr_step = global_step / args.ADJUST_LR_ITER
            new_lr = utils.adjust_learning_rate(optimizer, lr_step)
            
            print("learning rate decay:", new_lr)

# %%
"""
Testing
"""
for i, data in enumerate(content_dataloader, 0):
    data = data[0].to(device)
    batch_size = data.shape[0]
#     data = data[0].repeat(batch_size, 1, 1, 1)
    for j in range(batch_size):
        utils.showimg(data[j].cpu())
    
    output_image = model(data)
    for j in range(batch_size):
        utils.showimg(output_image[j].cpu().detach())
    output_image = model(data, utils.get_sid_batch(style_id_seg[0], batch_size))
    for j in range(batch_size):
        utils.showimg(output_image[j].cpu().detach())
    break

# %%



