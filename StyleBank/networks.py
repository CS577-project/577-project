from copy import deepcopy
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.modules import Sequential
import torchvision.models as models
from args import ConfigureDevice

device = ConfigureDevice()
# 这里使用vgg16作为pretrained model
vgg16 = models.vgg16(weights="IMAGENET1K_V1").features.to(device).eval()


class ContentLoss(nn.Module):
	'''
	content loss是我们预测出来的图在vgg的feature map和content image在vgg的feature map进行比较
	'''
	def __init__(self):
		super(ContentLoss, self).__init__()
		# we 'detach' the target content from the tree used
		# to dynamically compute the gradient: this is a stated value,
		# not a variable. Otherwise the forward method of the criterion
		# will throw an error.
		# self.target = target
		self.target = None
		self.mode = 'learn'

	def forward(self, input):

		if self.mode == 'loss':
			# loss模式，使用weight计算当前层与target的差异
			self.loss = self.weight * F.mse_loss(input, self.target)
		elif self.mode == 'learn':
			# 训练阶段，把input保存一个副本，存到target里
			self.target = input.detach()
		return input

def gram_matrix(input):
	a, b, c, d = input.size()  # a=batch size(=1)
	# b=number of feature maps
	# (c,d)=dimensions of a f. map (N=c*d)

	# 各个feature map算gram matrix，这里的batch size = 1
	features = input.view(a * b, c * d)  # resise F_XL into \hat F_XL

	G = torch.mm(features, features.t())  # compute the gram product

	# we 'normalize' the values of the gram matrix
	# by dividing by the number of element in each feature maps.
	return G.div(a * b * c * d)

class StyleLoss(nn.Module):
	'''
	style loss是我们预测出来的图在vgg的feature map和content image在vgg的feature map的gram matrix进行比较
	'''
	def __init__(self):
		super(StyleLoss, self).__init__()
		self.targets = []
		# self.target = gram_matrix(target_feature).detach()
		self.mode = 'learn'

	def forward(self, input):
		# 首先计算gram matrix
		G = gram_matrix(input)
		if self.mode == 'loss':
			# 计算loss阶段，当前的gram matirx与target比较
			self.loss = self.weight * F.mse_loss(G, self.target)
		elif self.mode == 'learn':
			# 训练阶段，计算gram matrix，并保存到target上
			self.target = G.detach()
		# 直接把input作为输出
		return input

# create a module to normalize input image so we can easily put it in a
# nn.Sequential
class Normalization(nn.Module):
	def __init__(self):
		super(Normalization, self).__init__()
		# .view the mean and std to make them [C x 1 x 1] so that they can
		# directly work with image Tensor of shape [B x C x H x W].
		# B is batch size. C is number of channels. H is height and W is width.
		mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
		std = torch.tensor([0.229, 0.224, 0.225]).to(device)
		self.mean = torch.tensor(mean).view(-1, 1, 1)
		self.std = torch.tensor(std).view(-1, 1, 1)

	def forward(self, img):
		# normalize img
		return (img - self.mean) / self.std


# desired depth layers to compute style/content losses :
# content layer只取conv 9，权重为1
content_layers = ['conv_9']
content_weight = {
	'conv_9': 1
}
# style layer取4个，权重为1
style_layers = [ 'conv_2', 'conv_4', 'conv_6', 'conv_9']
style_weight = {
	'conv_2': 1,
	'conv_4': 1,
	'conv_6': 1,
	'conv_9': 1,
}

class LossNetwork(nn.Module):

	def __init__(self):
		super(LossNetwork, self).__init__()
		# cnn就是vgg16

		cnn = deepcopy(vgg16)
		normalization = Normalization().to(device)
		# just in order to have an iterable access to or list of content/syle
		# losses
		# 基于vgg，关注content loss和style loss，这个是我们关注的vgg的loss层
		content_losses = []
		style_losses = []

		# assuming that cnn is a nn.Sequential, so we make a new nn.Sequential
		# to put in modules that are supposed to be activated sequentially
		model = nn.Sequential(normalization)

		i = 0  # increment every time we see a conv
		# 首先把所有的layer都扒出来，并用名字记录是第几个conv或者第几个relu等
		for layer in cnn.children():
			if isinstance(layer, nn.Conv2d):
				i += 1
				name = 'conv_{}'.format(i)
			elif isinstance(layer, nn.ReLU):
				name = 'relu_{}'.format(i)
				# The in-place version doesn't play very nicely with the ContentLoss
				# and StyleLoss we insert below. So we replace with out-of-place
				# ones here.
				layer = nn.ReLU(inplace=False)
			elif isinstance(layer, nn.MaxPool2d):
				name = 'pool_{}'.format(i)
			elif isinstance(layer, nn.BatchNorm2d):
				name = 'bn_{}'.format(i)
			else:
				raise RuntimeError('Unrecognized layer: {}'.format(layer.__class__.__name__))
			# 加入所有layer
			model.add_module(name, layer)
			# 如果当前层是我们关注的content layer or style layer，则额外加一层用于计算loss
			if name in content_layers:
				# add content loss:
				# target_feature = model(content_img).detach()
				content_loss = ContentLoss()
				# 这里设置loss的权重
				content_loss.weight = content_weight[name]
				model.add_module("content_loss_{}".format(i), content_loss)
				# 记录content loss的权重
				content_losses.append(content_loss)

			if name in style_layers:
				# add style loss:
				# target_feature = model(style_img).detach()
				style_loss = StyleLoss()
				# style loss的权重
				style_loss.weight = style_weight[name]
				model.add_module("style_loss_{}".format(i), style_loss)
				style_losses.append(style_loss)

		
		# 最后一个content loss or style loss之后的所有层都没用，全删掉
		# now we trim off the layers after the last content and style losses
		for i in range(len(model) - 1, -1, -1):
			if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
				break

		model = model[:(i + 1)]

		self.model = model
		# 记录下style loss层和content loss层
		self.style_losses = style_losses
		self.content_losses = content_losses

	def learn_content(self, input):
		# content loss设为训练模式，记录传入的数据得到的content feature map
		for cl in self.content_losses:
			cl.mode = 'learn'
		# style loss则什么也不做
		for sl in self.style_losses:
			sl.mode = 'nop'
		self.model(input) # feed image to vgg19
	
	def learn_style(self, input):
		# content loss什么也不做
		for cl in self.content_losses:
			cl.mode = 'nop'
		# style loss则设为训练模式，记录传入的input得到的feature map gram matrix
		for sl in self.style_losses: 
			sl.mode = 'learn'
		self.model(input) # feed image to vgg19

	def forward(self, input, content, style):
		'''
		content:(batch_size, 3, w, h)
		style:(batch_size, 3, w, h)
		'''
		# 把content和style的vgg结果，记录到各自的target中
		self.learn_content(content)
		self.learn_style(style)

		# 再设置为loss模式，传入我们预测的input，计算content和style loss
		for cl in self.content_losses:
			cl.mode = 'loss'
		for sl in self.style_losses:
			sl.mode = 'loss'
		self.model(input) # feed image to vgg19

		# 把这两种loss累加起来
		content_loss = 0
		style_loss = 0
		# 累积所有的loss
		for cl in self.content_losses:
			content_loss += cl.loss
		for sl in self.style_losses:
			style_loss += sl.loss
		# 最后返回
		return content_loss, style_loss

class StyleBankNet(nn.Module):
	def __init__(self, total_style):
		super(StyleBankNet, self).__init__()
		self.total_style = total_style
				
		self.encoder_net = Sequential(
			# 3 -> 32
			# 图像尺寸减半
			nn.Conv2d(3, 32, kernel_size=(9, 9), stride=2, padding=(4, 4), bias=False),
			nn.InstanceNorm2d(32),
			nn.ReLU(inplace=True),
			# 32 -> 64
			# 图像尺寸减半
			nn.Conv2d(32, 64, kernel_size=(3, 3), stride=2, padding=(1, 1), bias=False),
			nn.InstanceNorm2d(64),
			nn.ReLU(inplace=True),
			# 64 -> 128
			nn.Conv2d(64, 128, kernel_size=(3, 3), stride=1, padding=(1, 1), bias=False),
			nn.InstanceNorm2d(128),
			nn.ReLU(inplace=True),
			# encoder的输出有256层
			# 128->256
			nn.Conv2d(128, 256, kernel_size=(3, 3), stride=1, padding=(1, 1), bias=False),
			nn.InstanceNorm2d(256),
			nn.ReLU(inplace=True),
		)
		# decoder的输出还是3通道
		self.decoder_net = Sequential(
			nn.ConvTranspose2d(256, 128, kernel_size=(3, 3), stride=1, padding=(1, 1), bias=False),
			nn.InstanceNorm2d(128),
			nn.ReLU(inplace=True),
			nn.ConvTranspose2d(128, 64, kernel_size=(3, 3), stride=1, padding=(1, 1), bias=False),
			nn.InstanceNorm2d(64),
			nn.ReLU(inplace=True),
			# 图像尺寸翻倍
			nn.ConvTranspose2d(64, 32, kernel_size=(3, 3), stride=2, padding=(1, 1), bias=False),
			nn.InstanceNorm2d(32),
			nn.ReLU(inplace=True),
			# 图像尺寸翻倍
			nn.ConvTranspose2d(32, 3, kernel_size=(9, 9), stride=2, padding=(4, 4), bias=False),
		)
		# style数量为total_style，各个style有自己的sequential，不过style bank不修改feature map尺寸，只是为了调整 style
		self.style_bank = nn.ModuleList([
			Sequential(
				nn.Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False),
				nn.InstanceNorm2d(256),
				nn.ReLU(inplace=True),
				nn.Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False),
				nn.InstanceNorm2d(256),
				nn.ReLU(inplace=True)
			)
			for i in range(total_style)])
		
	def forward(self, X, style_id=None):
		# 进入encoder
		# X:(batch_size, 3, w, h)
		# z:(batch_size, 256, w/4, h/4)
		z = self.encoder_net(X)
		# 遍历各个style，一张图片经过风格变换后，进入decoder
		# style也是同时训练多个，style_id的数量与当前X batch size想同
		if style_id is not None:
			new_z = []
			for idx, i in enumerate(style_id):
				# 一张content image对应一个style bank
				batch_curz = z[idx].view(1, *z[idx].shape)
				# zs:(1, 256, w/4,h/4)
				zs = self.style_bank[i](batch_curz)
				new_z.append(zs)
			# 在batch维度拼接起来，形成一个batch
			# z:(batch_size, 256, w/4,h/4)
			z = torch.cat(new_z, dim=0)
			# z = self.bank_net(z)
		# result(batch_size, 3, w, h)
		result = self.decoder_net(z)
		return result
