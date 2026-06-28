import csv
from pathlib import Path
from typing import Dict
from utils.logger import get_logger

logger = get_logger("ai.training.logger")

try:
    from torch.utils.tensorboard import SummaryWriter
    TENSORBOARD_AVAILABLE = True
except ImportError:
    TENSORBOARD_AVAILABLE = False
    logger.warning("TensorBoard not available. Logging to CSV only.")


class TrainingLogger:
    """
    Records training and validation history to both structured CSV and TensorBoard.
    Ensures Kaggle compatibility by writing clear log artifacts.
    """
    def __init__(self, log_dir: Path | str):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.csv_path = self.log_dir / "training_history.csv"
        self.tb_writer = SummaryWriter(log_dir=str(self.log_dir / "tensorboard")) if TENSORBOARD_AVAILABLE else None
        
        # Initialize CSV header if file doesn't exist
        if not self.csv_path.exists():
            with open(self.csv_path, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "epoch", "phase", "loss_total", "loss_bce", "loss_dice", "loss_cldice",
                    "iou", "dice", "precision", "recall", "f1", "connectivity_ratio", "lr"
                ])
                
    def log_epoch(self, epoch: int, phase: str, losses: Dict[str, float], metrics: Dict[str, float], lr: float):
        """
        Logs metrics for a single epoch and phase ('train' or 'val').
        """
        # CSV Logging
        with open(self.csv_path, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                epoch,
                phase,
                f"{losses.get('total', 0.0):.4f}",
                f"{losses.get('bce', 0.0):.4f}",
                f"{losses.get('dice', 0.0):.4f}",
                f"{losses.get('cldice', 0.0):.4f}",
                f"{metrics.get('iou', 0.0):.4f}",
                f"{metrics.get('dice', 0.0):.4f}",
                f"{metrics.get('precision', 0.0):.4f}",
                f"{metrics.get('recall', 0.0):.4f}",
                f"{metrics.get('f1', 0.0):.4f}",
                f"{metrics.get('connectivity_ratio', 0.0):.4f}",
                f"{lr:.6e}"
            ])
            
        # TensorBoard Logging
        if self.tb_writer is not None:
            for k, v in losses.items():
                self.tb_writer.add_scalar(f"Loss/{phase}/{k}", v, epoch)
            for k, v in metrics.items():
                self.tb_writer.add_scalar(f"Metrics/{phase}/{k}", v, epoch)
            if phase == "train":
                self.tb_writer.add_scalar("Hyperparameters/learning_rate", lr, epoch)
            self.tb_writer.flush()
            
        logger.info(
            f"[{phase.upper()}] Epoch {epoch} | Loss: {losses.get('total', 0.0):.4f} "
            f"(BCE: {losses.get('bce', 0.0):.4f}, Dice: {losses.get('dice', 0.0):.4f}, clDice: {losses.get('cldice', 0.0):.4f}) | "
            f"IoU: {metrics.get('iou', 0.0):.4f} | ConnRatio: {metrics.get('connectivity_ratio', 0.0):.4f}"
        )
        
    def close(self):
        if self.tb_writer is not None:
            self.tb_writer.close()
