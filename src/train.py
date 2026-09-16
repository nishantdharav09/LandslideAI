import os

import torch
from torch.optim import AdamW

from dataloader import train_loader, val_loader
from unet_model import UNet
from loss import BCEDiceLoss


# --------------------------------------------------
# Device
# --------------------------------------------------

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Using Device:", device)


# --------------------------------------------------
# Model
# --------------------------------------------------

model = UNet(
    in_channels=14,
    out_channels=1
).to(device)


# --------------------------------------------------
# Loss
# --------------------------------------------------

criterion = BCEDiceLoss(
    bce_weight=0.5,
    dice_weight=0.5
)


# --------------------------------------------------
# Optimizer
# --------------------------------------------------

optimizer = AdamW(
    model.parameters(),
    lr=1e-4,
    weight_decay=1e-4
)


# --------------------------------------------------
# Training settings
# --------------------------------------------------

epochs = 5

best_val_loss = float("inf")

os.makedirs(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop\LandslideAI\models",
    exist_ok=True
)


# --------------------------------------------------
# Training Loop
# --------------------------------------------------

for epoch in range(epochs):

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

        # Clear previous gradients
        optimizer.zero_grad()

        # Backpropagation
        loss.backward()

        # Update model weights
        optimizer.step()

        train_loss += loss.item()

        if (batch_index + 1) % 50 == 0:

            print(
                f"Epoch [{epoch + 1}/{epochs}] "
                f"Batch [{batch_index + 1}/{len(train_loader)}] "
                f"Loss: {loss.item():.4f}"
            )

    train_loss /= len(train_loader)


    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

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


    print("\n" + "=" * 60)
    print(
        f"Epoch {epoch + 1}/{epochs} Completed"
    )
    print(
        f"Training Loss   : {train_loss:.4f}"
    )
    print(
        f"Validation Loss : {val_loss:.4f}"
    )
    print("=" * 60)


    # --------------------------------------------------
    # Save best model
    # --------------------------------------------------

    if val_loss < best_val_loss:

        best_val_loss = val_loss

        model_path = (
            r"C:\Users\Nishant Dharav"
            r"\OneDrive\Desktop\LandslideAI"
            r"\models\best_unet.pth"
        )

        torch.save(
            model.state_dict(),
            model_path
        )

        print(
            f"✅ Best model saved: {model_path}"
        )


print("\nTraining Completed!")