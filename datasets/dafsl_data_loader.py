"""
Mnist Data loader, as given in Mnist tutorial
"""
import imageio
import torch
import torchvision.utils as v_utils
from torchvision import datasets, transforms
import PIL
from torch.utils.data import DataLoader, TensorDataset, Dataset
import os

class ReshapeTransform:
    def __init__(self, new_size):
        self.new_size = new_size

    def __call__(self, img):
        return torch.reshape(img, self.new_size)

class DAFSLDataLoader:
    def __init__(self, config):
        """
        :param config:
        """
        self.config = config
        if config.data_mode == "imgs":
            img_root_folder = config.data_folder
            source_domain_list = config.data_domains.split(',')
            src_dataset1 = source_domain_list[0]
            print("Source domains", source_domain_list)
            dafsl_transforms=[transforms.Resize((224,224), interpolation=PIL.Image.BILINEAR),transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406],
                     std=[0.229, 0.224, 0.225])]
            #dafsl_transforms.append(ReshapeTransform((-1,)))
            src_dataset1_train = datasets.ImageFolder(root=os.path.join(img_root_folder, source_domain_list[0], "train"), 
                               transform=transforms.Compose(dafsl_transforms))
            src_dataset1_test = datasets.ImageFolder(root=os.path.join(img_root_folder, source_domain_list[0], "test"), 
                               transform=transforms.Compose(dafsl_transforms))
            self.train_loader = torch.utils.data.DataLoader(src_dataset1_train,batch_size=self.config.batch_size, shuffle=True, num_workers=self.config.data_loader_workers, pin_memory=self.config.pin_memory)
            self.test_loader = torch.utils.data.DataLoader(src_dataset1_test,batch_size=self.config.batch_size, shuffle=True, num_workers=self.config.data_loader_workers, pin_memory=self.config.pin_memory)
        elif config.data_mode == "download":
            raise NotImplementedError("This mode is not implemented YET")
        else:
            raise Exception(
                "Please specify in the json a specified mode in data_mode")


    def plot_samples_per_epoch(self, batch, epoch):
        """
        Plotting the batch images
        :param batch: Tensor of shape (B,C,H,W)
        :param epoch: the number of current epoch
        :return: img_epoch: which will contain the image of this epoch
        """
        img_epoch='{}samples_epoch_{:d}.jpg'.format(self.config.out_dir, epoch)
        v_utils.save_image(batch,
                           img_epoch,
                           nrow=8,
                           padding=2,
                           normalize=True)
        print(img_epoch)
        return imageio.imread(img_epoch)

    def make_gif(self, epochs):
        """
        Make a gif from a multiple images of epochs
        :param epochs: num_epochs till now
        :return:
        """
        gen_image_plots=[]
        for epoch in range(epochs + 1):
            img_epoch='{}samples_epoch_{:d}.png'.format(
                self.config.out_dir, epoch)
            try:
                gen_image_plots.append(imageio.imread(img_epoch))
            except OSError as e:
                pass

        imageio.mimsave(self.config.out_dir +
                        'animation_epochs_{:d}.gif'.format(epochs), gen_image_plots, fps=2)

    def finalize(self):
        pass
