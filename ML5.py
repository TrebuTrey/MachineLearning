import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from tqdm import tqdm

REBUILD_DATA = False
TESTING_DATA = True
VAL_PCT = 0.1
BATCH_SIZE = 100
EPOCHS = 1

class DogsVSCats():
    IMG_SIZE = 50
    CATS = "PetImages/Cat"
    DOGS = "PetImages/Dog"
    TESTING = "PetImages/Testing"
    LABELS = {CATS: 0, DOGS: 1} #Creates a list that represents cats as the 1st entry and dogs as the 2nd
    training_data = []
    dogcount = 0
    catcount = 0

    def make_training_data(self):
        for label in self.LABELS:
            for f in tqdm(os.listdir(label)):
                if "jpg" in f: #only tries to download the .jpg files
                    try:
                        path = os.path.join(label, f)
                        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE) #ensures that the pictures coming through are all in grayscale
                        img = cv2.resize(img, (self.IMG_SIZE, self.IMG_SIZE)) #resizes all pictures to pass through the array
                        self.training_data.append([np.array(img), np.eye(2)[self.LABELS[label]]])  # do something like print(np.eye(2)[1]), just makes one_hot 
                        #print(np.eye(2)[self.LABELS[label]])
                    except Exception as e:
                        pass
                        #print(label, f, str(e))
        np.random.shuffle(self.training_data) #shuffling helps the neural network to not get overfit
        np.save("training_data.npy", self.training_data) 
        print('Cats:',dogsvcats.catcount)
        print('Dogs:',dogsvcats.dogcount)

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 5)
        self.conv2 = nn.Conv2d(32, 64, 5)
        self.conv3 = nn.Conv2d(64, 128, 5)

        x = torch.randn(50, 50).view(-1, 1, 50, 50)
        self._to_linear = None
        self.convs(x)
        
        self.fc1 = nn.Linear(self._to_linear , 512)
        self.fc2 = nn.Linear(512, 2)

    def convs(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2,2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2,2))
        x = F.max_pool2d(F.relu(self.conv3(x)), (2,2))

        print(x[0].shape)
        if self._to_linear is None:
            self._to_linear = x[0].shape[0]*x[0].shape[1]*x[0].shape[2]
        return x

    def forward(self,x):
        x = self.convs(x)
        x = x.view(-1, self._to_linear)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)

if REBUILD_DATA: #We only need to build this once unless something changes to the data
    dogsvcats = DogsVSCats()
    dogsvcats.make_training_data()

if TESTING_DATA:

    training_data = np.load("training_data.npy", allow_pickle= True) #look up what allow_pickle means
    # print(len(training_data))
    # print(training_data[0])
    # plt.imshow(training_data[0][0], cmap="gray") #because training_data entries each have two arrays, 
    # #we are asking for the 1st entry of the 1st entry of training_data
    # plt.show()

net = Net()
optimizer = optim.Adam(net.parameters(), lr = 0.001)
loss_function = nn.MSELoss()

X = torch.Tensor([i[0] for i in training_data]).view(-1, 50, 50)
X = X/255.0
y = torch.Tensor([i[1] for i in training_data])

val_size = int(len(X) * VAL_PCT)

train_X = X[: -val_size]
train_y = y[: -val_size]

test_X = X[-val_size:]
test_y = y[-val_size:]

for epoch in range(EPOCHS):
    for i in tqdm(range(0, len(train_X), BATCH_SIZE)):
        # print(i, i+BATCH_SIZE)
        batch_X = train_X[i: i+BATCH_SIZE].view(-1, 1, 50, 50)
        batch_y = train_y[i: i+BATCH_SIZE]

        net.zero_grad()
        outputs = net(batch_X)
        loss = loss_function(outputs, batch_y)
        loss.backward()
        optimizer.step()

print(loss)

correct = 0
total = 0
with torch.no_grad():
    for i in tqdm(range(len(test_X))):
        real_class = torch.argmax(test_y[i])
        net_out = net(test_X[i].view(-1, 1, 50, 50))[0]
        predicted_class = torch.argmax(net_out)
        if predicted_class == real_class:
            correct += 1
        total += 1
    print("Accuracy: ", round(correct/total, 3))