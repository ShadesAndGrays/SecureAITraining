import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def main():
    # import data
    df = pd.read_csv("data/personality_dataset.csv")

    # Clean data
    df = df.dropna()

    # Remap Data
    df['Personality'] = df['Personality'].map({"Introvert" : 1, "Extrovert": 0}) 
    df['Stage_fear'] = df['Stage_fear'].map(lambda p: 1 if p == "Yes" else 0) 
    df['Drained_after_socializing'] = df['Drained_after_socializing'].map(lambda p: 1 if p == "Yes" else 0) 

    # Split Data
    x = df.drop(['Personality'],axis=1)
    y = df['Personality']

    scaler = MinMaxScaler()

    # Convert to numpy array
    x = scaler.fit_transform(x)
    y = y.values

    # Split data
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=42)

    # convert to tensor
    x_train = torch.FloatTensor(x_train)
    x_test = torch.FloatTensor(x_test)
    y_train = torch.LongTensor(y_train)
    y_test = torch.LongTensor(y_test)

    # print(torch.isnan(x_train).any(), torch.isinf(x_train).any())
    # print(torch.isnan(y_train).any(), torch.isinf(y_train).any())
    # print(torch.unique(y_train))  # Should be only 0 and 1
    # print(x)

    # NN network
    class Model(nn.Module):
        def __init__(self,in_features=7, h1=16, h2=16, out_features=1):
            super().__init__()
            self.fc1 = nn.Linear(in_features,h1)
            self.fc2 = nn.Linear(h1,h2)
            self.out = nn.Linear(h2,out_features)
        
        def forward(self,x):
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.out(x)
            return x



    # Training

    torch.manual_seed(42)
    model = Model()

    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(),lr=0.001) 
    losses = []

    epoch = 150
    for i in range(epoch):
        y_pred =  model.forward(x_train)
        loss = criterion(y_pred,y_train.float().unsqueeze(1)) 
        losses.append(loss.detach().numpy())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if i % 10 == 0:
            print(f"Epoch: {i}  Loss: {loss.item()}")
        pass
    # Draw graph
    # plt.xlabel("Epoch")
    # plt.ylabel("Loss")
    # plt.plot(range(epoch),losses)
    # plt.savefig("output.png")

    with torch.no_grad():
        y_eval = model.forward(x_test)
        loss = criterion(y_eval,y_test.float().unsqueeze(1))
        print(loss)



if __name__ == "__main__":
    main()