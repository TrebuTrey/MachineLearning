import torch
import torch.nn as nn
import torch.nn.functional as F

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


net = Net()
# print(net)

X = torch.rand((28, 28))
'''-1 tells the network to not throw an error for dimension issues and that it will be a data of unknown dimension'''
X = X.view(-1, 28*28)

output = net(X)

print(output)