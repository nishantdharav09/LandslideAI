import torch

from loss import DiceLoss, BCEDiceLoss


# Dummy prediction and target
predictions = torch.randn(2, 1, 128, 128)

targets = torch.randint(
    0,
    2,
    (2, 1, 128, 128)
).float()


# Test Dice Loss
dice_loss = DiceLoss()
dice_value = dice_loss(predictions, targets)

# Test combined BCE + Dice Loss
combined_loss = BCEDiceLoss()
combined_value = combined_loss(predictions, targets)


print("Dice Loss:", dice_value.item())
print("BCE + Dice Loss:", combined_value.item())