import random

import numpy as np
import torch

from dataloader import train_loader, val_loader
from unet_model import UNet
from loss import BCETverskyLoss


# ============================================================
# Reproducibility
# ============================================================

SEED = 42

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)


# ============================================================
# Device
# ============================================================

device = torch.device("cpu")


print("=" * 60)
print("LandslideAI - Advanced Tversky Training")
print("=" * 60)

print("Device:", device)


# ============================================================
# Model
# ============================================================

model = UNet(
    in_channels=14,
    out_channels=1
).to(device)

print("Model created successfully.")


# ============================================================
# Loss Function
# ============================================================

criterion = BCETverskyLoss(
    bce_weight=0.5,
    tversky_weight=0.5
)

print("Loss: BCE + Tversky")


# ============================================================
# Optimizer
# ============================================================

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=0.0001,
    weight_decay=0.0001
)


# ============================================================
# Training Settings
# ============================================================

epochs = 3

best_val_loss = float("inf")


# ============================================================
# Training Loop
# ============================================================

for epoch in range(epochs):

    print("\n")
    print("=" * 60)
    print(f"Epoch {epoch + 1}/{epochs}")
    print("=" * 60)


    # --------------------------------------------------------
    # Training
    # --------------------------------------------------------

    model.train()

    train_loss = 0.0

    for batch_index, (images, masks) in enumerate(train_loader):

        images = images.to(device)
        masks = masks.to(device)


        # Forward pass
        predictions = model(images)


        # Calculate loss
        loss = criterion(
            predictions,
            masks
        )


        # Clear gradients
        optimizer.zero_grad()


        # Backpropagation
        loss.backward()


        # Update weights
        optimizer.step()


        train_loss += loss.item()


        if (batch_index + 1) % 10 == 0:

            print(
                f"Batch "
                f"[{batch_index + 1}/{len(train_loader)}] "
                f"Loss: {loss.item():.4f}"
            )


    train_loss /= len(train_loader)


    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    model.eval()

    val_loss = 0.0


    with torch.no_grad():

        for images, masks in val_loader:

            images = images.to(device)
            masks = masks.to(device)


            predictions = model(images)


            loss = criterion(
                predictions,
                masks
            )


            val_loss += loss.item()


    val_loss /= len(val_loader)


    # --------------------------------------------------------
    # Epoch Results
    # --------------------------------------------------------

    print("\n")
    print("-" * 60)

    print(
        f"Training Loss   : {train_loss:.4f}"
    )

    print(
        f"Validation Loss : {val_loss:.4f}"
    )

    print("-" * 60)


    # --------------------------------------------------------
    # Save Best Model
    # --------------------------------------------------------

    if val_loss < best_val_loss:

        best_val_loss = val_loss


        torch.save(
            model.state_dict(),
            r"C:\Users\Nishant Dharav\OneDrive\Desktop"
            r"\LandslideAI\models\best_unet.pth"
        )


        print("\n✅ Best model saved successfully!")


# ============================================================
# Training Completed
# ============================================================

print("\n")
print("=" * 60)
print("Advanced Training Completed!")
print("=" * 60)

print(
    f"Best Validation Loss: {best_val_loss:.4f}"
)