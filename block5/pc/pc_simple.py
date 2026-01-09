import torch
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

###### Load Data and normalize targets

X, y = fetch_openml(name="boston", version=1, as_frame=False, return_X_y=True)

X = StandardScaler().fit_transform(X)
y = y.reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

X_train = torch.tensor(X_train, dtype=torch.float32)
X_test  = torch.tensor(X_test, dtype=torch.float32)

y_mean, y_std = y_train.mean(), y_train.std()
y_test_mean, y_test_std = y_test.mean(), y_test.std()
y_train = torch.tensor((y_train - y_mean) / y_std, dtype=torch.float32)
y_test  = torch.tensor((y_test  - y_test_mean) / y_test_std, dtype=torch.float32)

print("START")
print("Train:", len(y_train), "with mean/std:",y_mean,y_std)
print("Test : ", len(y_test), "with mean/std:",y_test_mean,y_test_std)

###### Initialize Hyperparameter 
torch.manual_seed(0)

learned_variables = []

# early stopping with patience
best_test = float("inf")
patience = 10
wait = 0

D_in = 13
D_hidden = 32
D_out = 1

W1 = torch.randn(D_in, D_hidden) * 0.1
W2 = torch.randn(D_hidden, D_out) * 0.1

n_infer = 50      # inference convergence rate
 
lr_x = 5e-3      # inference rate
lr_w = 1e-4      # weight learning rate 

weight_decay = 1e-3 # L2-Regulation
lambda_h = 1e-2 # Regularize hidden activities NO effect
noise_std = 0.01 # noise during inference
batch_size = 16

def batches(X, y, batch_size):
    for i in range(0, len(X), batch_size):
        yield X[i:i+batch_size], y[i:i+batch_size]

###### Train #######
for epoch in range(300):
    total_loss = 0.0

    for xb, yb in batches(X_train, y_train, batch_size):
        B = xb.shape[0]

        # hidden activities for entire batch
        h = torch.zeros(B, D_hidden, requires_grad=True)    

    #for x, y in zip(X_train, y_train):
    #    x = x.unsqueeze(0)
    #    y = y.unsqueeze(0)
    #
    #    # latent state
    #    h = torch.zeros(1, D_hidden, requires_grad=True)

        # ----- Inference -----
        for _ in range(n_infer):
            pred_h = torch.tanh(xb @ W1)
            pred_y = torch.tanh(h) @ W2

            eps_h = h - pred_h
            eps_y = pred_y - yb

            #energy = (eps_h**2).sum() + (eps_y**2).sum() # original
            # with penalty_ L2-Regulation
            """
            energy = (
                (eps_h**2).sum()
                + (eps_y**2).sum()
                + weight_decay * (W1.norm()**2 + W2.norm()**2)
            )
            """
            energy = (
                (eps_h**2).sum()
                + (eps_y**2).sum()
                + weight_decay * (W1.norm()**2 + W2.norm()**2)
                + lambda_h * (h**2).sum()
            )

            h.grad = None
            energy.backward()

            with torch.no_grad():
                h -= lr_x * h.grad
                h += noise_std * torch.randn_like(h)

        # ----- Learning -----
        with torch.no_grad():
            W2 -= lr_w * torch.tanh(h).T @ eps_y
            W1 -= lr_w * xb.T @ (eps_h * (1 - pred_h**2))

        #total_loss += (eps_y**2).item()
        total_loss += (eps_y**2).mean().item()

    #if epoch % 50 == 0:
    print(f"[PC] Epoch {epoch}, Loss: {total_loss / len(X_train):.5f}")
    
    # ----- Testing -------
    with torch.no_grad():
        h = X_test @ W1
        y_pred = h @ W2
        
        y_pred_denorm = (y_pred+y_test_mean)*y_test_std
        y_test_denorm = (y_test+y_test_mean)*y_test_std

        test_mse = ((y_pred_denorm - y_test_denorm)**2).mean()
        print(f"[PC] Epoch {epoch},  MSE: {test_mse.item()}")

    learnings = {}
    learnings['epoch'] = epoch
    learnings['loss'] = total_loss
    learnings['test'] = test_mse
    learnings['W1'] = W1.clone()
    learnings['W2'] = W2.clone()

    learned_variables.append(learnings)

    # ---- Early Stopping ----
    if test_mse < best_test:
        best_test = test_mse
        best_W1 = W1.clone()
        best_W2 = W2.clone()
        wait = 0
    else:
        wait += 1
        if wait >= patience:
            break
    
print(40*"=")
best_result_loss = sorted([(l['loss'], l) for l in learned_variables])
_, result = best_result_loss[0]
print(result['epoch'])
print(result['loss'])
print(result['test'])
print(40*"=")
best_result_test = sorted([(l['test'], l) for l in learned_variables])
_, result = best_result_test[0]
print(result['epoch'])
print(result['loss'])
print(result['test'])


# problem with overfitting #
""" 
1. boston house prices is a very small dataset
~400 training samples
32 hidden units → ~450 parameters
Very easy to memorize

2. PC aggressively fits training targets
- Inference step forces hidden states to perfectly explain each sample
- Then weights are updated toward that explanation
- This is closer to per-sample memorization than batch SGD

3. No implicit regularization
Backprop has:
- minibatching
- optimizer noise (Adam, momentum)
- early stopping by default
PC loop has:
- deterministic per-sample updates
- no noise
- no penalty on weights or hidden states

--> implement early stopping: implemented
--> Weight decay (L2 regularization). Add a penalty to the energy function
---> add noise during inference


"""

# ------- Use Best W1 and W2
with torch.no_grad():
    for i in range(10):
        h = X_test[i] @ W1
        y_pred = h @ W2
        
        y_pred_denorm = (y_pred+y_test_mean)*y_test_std
        y_test_denorm = (y_test[i]+y_test_mean)*y_test_std

        test_mse = ((y_pred_denorm - y_test_denorm)**2).mean()
        print(f"{y_pred_denorm},{y_test_denorm}, error={test_mse}")
