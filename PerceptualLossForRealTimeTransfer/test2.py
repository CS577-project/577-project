# %% [markdown]
# # Perceptual Loss For Real Time Transfer

# %% [markdown]
# 该网络与原始版本的Style Transfer的套路是一样的，唯一的不同就是原始版本的style transfer是直接拿vgg-16，从一张噪音图开始，一方面比对content image，另一方面比对style image，不断调整噪音图，从而得到一张融合后的图。而Percept Loss For Real Time Transfer则是增加了一个auto encoder形状的网络，叫做transformation network，进原图出来预测图，这个预测图与原图在内容做比对，与风格图在风格上做比对。在训练的时候，有若干张内容图，只有一张风格图。这样就可以训练transformation network一边顾及到恢复原图，一边顾及到贴近特定的风格。  
# 结果就是，一个transformation network就贴近一张风格图。这样一来，一张新的内容图进来以后，直接就可以推断出风格迁移后的图像。图像质量理论上跟原始版本style transfer不会有啥差异，只不过是可以提前训练好该模型，不像style transfer原始版本，每次都要训练。

# %% [markdown]
# 首先，拿一系列内容图+一张风格图训练一个网络，并保存下来

# %%
from main import build_parser
from train import network_train

# %%
# 训练模式
parser = build_parser()
#parser.Namespace()
custom_args = [
    "--train-flag", "True",
    "--train-content", "../Images/original",
    "--train-style", "../Images/style-images/candy.jpg"
]
args = parser.parse_args(custom_args)
print(args)

transform_network = network_train(args)

# %%



