import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import transforms, datasets

class Net(nn.Module):
    def __init__(self):
        '''super.init will run any parent class initialization procedures, which we are receiving from nn.Module'''
        super().__init__()
        self.fc1 = nn.Linear(784, 64) 
        '''fc = fully connected. 784 is 28x28, our input of the image, 64 is our number of hidden layers'''
        self.fc2 = nn.Linear(64, 64)
        '''layer 2 must accept the number of outputs from its predecessor'''
        self.fc3 = nn.Linear(64, 64)
        self.fc4 = nn.Linear(64, 10)
        '''The reason layer 4 only outputs 10 is because we have 10 classes'''

    '''Most neural networks are feed-forward, which means data passes from one neuron layer to the next.
    This must be defined by some function we call forward()'''
    def forward(self, x):
        '''F.relu is our activation function that will do calculations on the input. relu is short for rectified linear'''
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        '''softmax is used when you are looking to define the test as a single class among multiple classes'''
        return F.log_softmax(x, dim=1)

'''Pulling predefinied datasets that are 28x28 handrawn number images'''
train = datasets.MNIST("", train=True, download=True, transform = transforms.Compose([transforms.ToTensor()]))

test = datasets.MNIST("", train=False, download=True, transform = transforms.Compose([transforms.ToTensor()]))

'''Loads in a batch of 10 images at a time to be compiled for training and testing. Shuffle ensures
that data will not overfit the neural network'''
trainset = torch.utils.data.DataLoader(train, batch_size = 10, shuffle = True)
testset = torch.utils.data.DataLoader(test, batch_size = 10, shuffle = True)

net = Net()
# print(net)

X = torch.rand((28, 28))
'''-1 tells the network to not throw an error for dimension issues and that it will be a data of unknown dimension'''
X = X.view(-1, 28*28)

output = net(X)

# print(output)

'''lr is learning rate, or the amount of change the network can make to itself between generations as it continues to learn'''
optimizer = optim.Adam(net.parameters(), lr = 0.001)
EPOCHS = 3

for epoch in range(EPOCHS):
    for data in trainset:
        '''data is a batch of featuresets and Labels. featureset is the array that makes up the handdrawn picture, and y is the
        label associated in the training set with each picture'''
        X, y = data
        net.zero_grad()
        output = net(X.view(-1, 28*28))
        loss = F.nll_loss(output, y)
        loss.backward()
        optimizer.step()
    # print(loss)

correct = 0
total = 0

with torch.no_grad():
    for data in trainset:
        X, y = data
        output = net(X.view(-1, 784))
        for idx,i in enumerate(output):
            if torch.argmax(i) == y[idx]:
                correct += 1
            total += 1
print("Accuracy: ", round(correct/total, 3))

plt.imshow(X[0].view(28, 28))
fig1 = plt.savefig("number_guess.png")
print(torch.argmax(net(X[0].view(-1, 784))[0]))