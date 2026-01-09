import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

device = torch.device("mps" if torch.mps.is_available() else "cpu")

# ---------------------- Data ----------------------
batch_size = 128

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_dataset = datasets.MNIST(root="./data", train=True,
                               download=True, transform=transform)
test_dataset = datasets.MNIST(root="./data", train=False,
                              download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader  = DataLoader(test_dataset,  batch_size=256, shuffle=False)

# ---------------------- PCN model ----------------------
class PCN(nn.Module):
    """
    Very simple discriminative predictive coding network:
    - Latent states z1, z2, z3 (output).
    - Iteratively update z1,z2,z3 to minimize cross-entropy at output
      plus quadratic penalties to keep z close to bottom-up predictions.
    - We still learn W with backprop through the inference process.
    """
    def __init__(self, iters=5, eta=0.1):
        super().__init__()
        self.W1 = nn.Linear(28*28, 256)
        self.W2 = nn.Linear(256, 128)
        self.W3 = nn.Linear(128, 10)
        self.iters = iters
        self.eta = eta

    def forward(self, x, y=None):
        """
        If y is provided, do iterative inference (training mode).
        If y is None, do a simple feedforward pass (test mode).
        """
        x = x.view(x.size(0), -1)

        # bottom-up initializations (no grad, just to get shapes)
        with torch.no_grad():
            z1_init = F.relu(self.W1(x))
            z2_init = F.relu(self.W2(z1_init))
            z3_init = self.W3(z2_init)

        if y is None:
            # plain forward for evaluation
            return z3_init

        # make activities LEAF tensors with requires_grad=True
        z1 = z1_init.detach().clone().requires_grad_(True)
        z2 = z2_init.detach().clone().requires_grad_(True)
        z3 = z3_init.detach().clone().requires_grad_(True)

        for _ in range(self.iters):
            # compute energy: CE at output + quadratic prediction errors
            ce = F.cross_entropy(z3, y)
            e1 = 0.5 * (z1 - F.relu(self.W1(x))).pow(2).mean()
            e2 = 0.5 * (z2 - F.relu(self.W2(z1))).pow(2).mean()
            e3 = 0.5 * (z3 - self.W3(z2)).pow(2).mean()
            loss = ce + e1 + e2 + e3

            # zero grads on activities
            if z1.grad is not None:
                z1.grad.zero_()
            if z2.grad is not None:
                z2.grad.zero_()
            if z3.grad is not None:
                z3.grad.zero_()

            # gradients w.r.t. activities only
            loss.backward(retain_graph=True)

            # gradient descent step on activities (no autograd tracking here)
            with torch.no_grad():
                z1 -= self.eta * z1.grad
                z2 -= self.eta * z2.grad
                z3 -= self.eta * z3.grad

        # final loss after inference (no backward here)
        ce = F.cross_entropy(z3, y)
        e1 = 0.5 * (z1 - F.relu(self.W1(x))).pow(2).mean()
        e2 = 0.5 * (z2 - F.relu(self.W2(z1))).pow(2).mean()
        e3 = 0.5 * (z3 - self.W3(z2)).pow(2).mean()
        loss = ce + e1 + e2 + e3

        return z3, loss

model = PCN(iters=3, eta=0.1).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# ---------------------- Training ----------------------
num_epochs = 5

for epoch in range(num_epochs):
    model.train()
    total_loss = 0.0
    total_correct = 0
    total_examples = 0

    for x, y in train_loader:
        x, y = x.to(device), y.to(device)

        optimizer.zero_grad()
        logits, loss = model(x, y)   # PC inference + energy

        loss.backward()              # gradients w.r.t. weights
        optimizer.step()

        total_loss += loss.item() * x.size(0)
        preds = logits.argmax(dim=1)
        total_correct += (preds == y).sum().item()
        total_examples += x.size(0)

    print(f"Epoch {epoch+1}: "
          f"loss={total_loss/total_examples:.4f}, "
          f"acc={100.0*total_correct/total_examples:.2f}%")

# ---------------------- Test ----------------------
model.eval()
correct = 0
total = 0

with torch.no_grad():
    for x, y in test_loader:
        x, y = x.to(device), y.to(device)
        logits = model(x)            # plain forward
        preds = logits.argmax(dim=1)
        correct += (preds == y).sum().item()
        total += x.size(0)

print(f"Test accuracy: {100.0 * correct / total:.2f}%")
