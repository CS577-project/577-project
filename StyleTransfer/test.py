# %% [markdown]
# # Style Transfer
# 
# Style Transfer直接利用了VGG-16/VGG-18，没有神经网络需要训练，直接拿一张噪音图开始做梯度下降。优点是任意两张图都可以做风格迁移，缺点就是，每拿两张图，都得train一遍

# %%
import os
from neural_style_transfer import BuildArgParser, BuildOptimizationConfig, neural_style_transfer

# 当前目录
current_directory = os.path.dirname(os.path.abspath(__file__))
#current_directory = os.getcwd()

# %%
default_resource_dir = os.path.join(current_directory, "..", "Images")
content_images_dir = os.path.join(default_resource_dir, 'original')
style_images_dir = os.path.join(default_resource_dir, 'cartoon')

output_img_parent_dir = os.path.join(current_directory, 'styletransfer-output')


# %%
content_weight = 1e5
style_weight = 1e2
tv_weight = 1e2
output_img_dir = os.path.join(output_img_parent_dir, "Args" + str(content_weight) + "_" + str(style_weight) + "_" + str(tv_weight) )

# 创建该目录
is_exist = os.path.exists(output_img_dir)
if not is_exist:
    os.makedirs(output_img_dir)

style_files = os.listdir(style_images_dir)
content_files = os.listdir(content_images_dir)
for content_filename in content_files:
    for style_filename in style_files:
        print(content_filename)
        print(style_filename)
        parser = BuildArgParser()
        custom_args = [
                "--content_weight", str(content_weight),
                "--style_weight", str(style_weight),
                "--tv_weight", str(tv_weight),   
                "--content_img_name", content_filename,
                "--style_img_name", style_filename
            ]        
        args = parser.parse_args(custom_args)
        config = BuildOptimizationConfig(args, content_images_dir, style_images_dir, output_img_dir)
        results_path = neural_style_transfer(config)


# %%



