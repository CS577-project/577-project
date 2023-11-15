import torch
# 创建一个随机的1x1x4x4的张量
noise = torch.rand(1, 1, 4, 4)
shifted_noise = torch.roll(noise, shifts=1, dims=2)

shifted_noise_mps = torch.cat((noise[:, :, :, -1:], noise[:, :, :, :-1]), dim=2)


# 检查两个结果是否相等
print(shifted_noise, shifted_noise_mps)
print(torch.equal(shifted_noise, shifted_noise_mps))