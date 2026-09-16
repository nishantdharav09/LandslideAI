import torch
import torch.nn as nn


class TverskyLoss(nn.Module):

    def __init__(
        self,
        alpha=0.3,
        beta=0.7,
        smooth=1e-6
    ):
        super().__init__()

        self.alpha = alpha
        self.beta = beta
        self.smooth = smooth

    def forward(self, predictions, targets):

        predictions = torch.sigmoid(predictions)

        predictions = predictions.view(-1)
        targets = targets.view(-1)

        true_positive = (predictions * targets).sum()

        false_positive = (
            predictions * (1 - targets)
        ).sum()

        false_negative = (
            (1 - predictions) * targets
        ).sum()

        tversky = (
            true_positive + self.smooth
        ) / (
            true_positive
            + self.alpha * false_positive
            + self.beta * false_negative
            + self.smooth
        )

        return 1.0 - tversky


class BCETverskyLoss(nn.Module):

    def __init__(
        self,
        bce_weight=0.5,
        tversky_weight=0.5
    ):
        super().__init__()

        self.bce_weight = bce_weight
        self.tversky_weight = tversky_weight

        self.bce = nn.BCEWithLogitsLoss()

        self.tversky = TverskyLoss(
            alpha=0.3,
            beta=0.7
        )

    def forward(self, predictions, targets):

        bce_loss = self.bce(
            predictions,
            targets
        )

        tversky_loss = self.tversky(
            predictions,
            targets
        )

        total_loss = (
            self.bce_weight * bce_loss
            + self.tversky_weight * tversky_loss
        )

        return total_loss