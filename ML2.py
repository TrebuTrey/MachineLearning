import matplotlib.pyplot as plt
import torch
import torchvision
from torchvision import transforms, datasets

'''Pulling predefinied datasets that are 28x28 handrawn number images'''
train = datasets.MNIST("", train=True, download=True, transform = transforms.Compose([transforms.ToTensor()]))

test = datasets.MNIST("", train=False, download=True, transform = transforms.Compose([transforms.ToTensor()]))

'''Loads in a batch of 10 images at a time to be compiled for training and testing. Shuffle ensures
that data will not overfit the neural network'''
trainset = torch.utils.data.DataLoader(train, batch_size = 10, shuffle = True)
testset = torch.utils.data.DataLoader(test, batch_size = 10, shuffle = True)


for data in trainset:
    # print(data)
    break

'''x will represent a tensor of tensors, y will represent the value stored for the corresponding tensor'''
x, y = data[0][0], data[1][0]
print(y)

'''draws the MNIST file of the number into plt'''
# plt.imshow(data[0][0].view(28,28))
# plt.show()

'''Setting up dict to count total number of instances in the entire dataset'''
total = 0
counter_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

for data in trainset:
    Xs, ys = data
    for y in ys:
        counter_dict[int(y)] += 1
        total += 1

print(counter_dict)

'''Calculates % of each instance. Numbers should be fairly balanced as to optimize the data.'''
for i in counter_dict:
    print(f"{i}: {counter_dict[i]/total*100}")