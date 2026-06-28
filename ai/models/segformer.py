import torch
import torch.nn as nn
from utils.logger import get_logger

logger = get_logger("ai.models.segformer")


class MixFFN(nn.Module):
    """Mix-FFN with depthwise convolution (replaces standard FFN in ViT)."""
    def __init__(self, dim: int, expansion: int = 4):
        super().__init__()
        hidden = dim * expansion
        self.fc1 = nn.Linear(dim, hidden)
        self.dwconv = nn.Conv2d(hidden, hidden, kernel_size=3, padding=1, groups=hidden)
        self.fc2 = nn.Linear(hidden, dim)
        self.act = nn.GELU()

    def forward(self, x: torch.Tensor, h: int, w: int) -> torch.Tensor:
        B, N, C = x.shape
        x = self.fc1(x)
        # Reshape for depthwise conv
        x = x.transpose(1, 2).reshape(B, -1, h, w)
        x = self.act(self.dwconv(x))
        x = x.flatten(2).transpose(1, 2)
        x = self.fc2(x)
        return x


class EfficientSelfAttention(nn.Module):
    """Multi-head self-attention with spatial reduction for efficiency."""
    def __init__(self, dim: int, num_heads: int = 8, sr_ratio: int = 1):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.scale = self.head_dim ** -0.5

        self.q = nn.Linear(dim, dim)
        self.kv = nn.Linear(dim, dim * 2)
        self.proj = nn.Linear(dim, dim)

        # Spatial Reduction
        self.sr_ratio = sr_ratio
        if sr_ratio > 1:
            self.sr = nn.Conv2d(dim, dim, kernel_size=sr_ratio, stride=sr_ratio)
            self.norm = nn.LayerNorm(dim)

    def forward(self, x: torch.Tensor, h: int, w: int) -> torch.Tensor:
        B, N, C = x.shape
        q = self.q(x).reshape(B, N, self.num_heads, self.head_dim).permute(0, 2, 1, 3)

        if self.sr_ratio > 1:
            x_ = x.transpose(1, 2).reshape(B, C, h, w)
            x_ = self.sr(x_).flatten(2).transpose(1, 2)
            x_ = self.norm(x_)
            kv = self.kv(x_).reshape(B, -1, 2, self.num_heads, self.head_dim).permute(2, 0, 3, 1, 4)
        else:
            kv = self.kv(x).reshape(B, -1, 2, self.num_heads, self.head_dim).permute(2, 0, 3, 1, 4)

        k, v = kv[0], kv[1]
        attn = (q @ k.transpose(-2, -1)) * self.scale
        attn = attn.softmax(dim=-1)
        x = (attn @ v).transpose(1, 2).reshape(B, N, C)
        return self.proj(x)


class TransformerBlock(nn.Module):
    """Single SegFormer encoder block."""
    def __init__(self, dim: int, num_heads: int, sr_ratio: int, expansion: int = 4):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.attn = EfficientSelfAttention(dim, num_heads, sr_ratio)
        self.norm2 = nn.LayerNorm(dim)
        self.ffn = MixFFN(dim, expansion)

    def forward(self, x: torch.Tensor, h: int, w: int) -> torch.Tensor:
        x = x + self.attn(self.norm1(x), h, w)
        x = x + self.ffn(self.norm2(x), h, w)
        return x


class OverlapPatchEmbed(nn.Module):
    """Overlapping patch embedding — preserves local continuity, critical for roads."""
    def __init__(self, in_channels: int, embed_dim: int, patch_size: int = 7, stride: int = 4):
        super().__init__()
        self.proj = nn.Conv2d(
            in_channels, embed_dim,
            kernel_size=patch_size, stride=stride, padding=patch_size // 2
        )
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, x: torch.Tensor):
        x = self.proj(x)
        _, _, h, w = x.shape
        x = x.flatten(2).transpose(1, 2)
        x = self.norm(x)
        return x, h, w


class SegFormerEncoder(nn.Module):
    """
    Hierarchical Transformer Encoder (MiT-B2 configuration).
    
    Produces multi-scale feature maps at 1/4, 1/8, 1/16, 1/32 of input resolution.
    """
    def __init__(
        self,
        in_channels: int = 3,
        embed_dims: list = None,
        num_heads: list = None,
        depths: list = None,
        sr_ratios: list = None,
    ):
        super().__init__()
        # MiT-B2 defaults
        if embed_dims is None:
            embed_dims = [64, 128, 320, 512]
        if num_heads is None:
            num_heads = [1, 2, 5, 8]
        if depths is None:
            depths = [3, 4, 6, 3]
        if sr_ratios is None:
            sr_ratios = [8, 4, 2, 1]

        self.num_stages = len(embed_dims)
        self.patch_embeds = nn.ModuleList()
        self.blocks = nn.ModuleList()
        self.norms = nn.ModuleList()

        for i in range(self.num_stages):
            in_ch = in_channels if i == 0 else embed_dims[i - 1]
            patch_size = 7 if i == 0 else 3
            stride = 4 if i == 0 else 2

            self.patch_embeds.append(OverlapPatchEmbed(in_ch, embed_dims[i], patch_size, stride))
            stage_blocks = nn.ModuleList([
                TransformerBlock(embed_dims[i], num_heads[i], sr_ratios[i])
                for _ in range(depths[i])
            ])
            self.blocks.append(stage_blocks)
            self.norms.append(nn.LayerNorm(embed_dims[i]))

    def forward(self, x: torch.Tensor) -> list:
        features = []
        for i in range(self.num_stages):
            x, h, w = self.patch_embeds[i](x)
            for blk in self.blocks[i]:
                x = blk(x, h, w)
            x = self.norms[i](x)
            # Reshape back to spatial
            x = x.transpose(1, 2).reshape(x.shape[0], -1, h, w)
            features.append(x)
        return features


class SegFormerDecoder(nn.Module):
    """
    All-MLP decoder. Unifies multi-scale features into a single prediction.
    """
    def __init__(self, embed_dims: list = None, decoder_dim: int = 256, num_classes: int = 1):
        super().__init__()
        if embed_dims is None:
            embed_dims = [64, 128, 320, 512]

        self.linear_layers = nn.ModuleList([
            nn.Linear(dim, decoder_dim) for dim in embed_dims
        ])
        self.fuse = nn.Sequential(
            nn.Linear(decoder_dim * len(embed_dims), decoder_dim),
            nn.ReLU(inplace=True),
        )
        self.pred = nn.Linear(decoder_dim, num_classes)

    def forward(self, features: list) -> torch.Tensor:
        # Target spatial size = largest feature map (Stage 1)
        B, _, H, W = features[0].shape
        unified = []

        for i, feat in enumerate(features):
            b, c, h, w = feat.shape
            feat = feat.flatten(2).transpose(1, 2)  # (B, h*w, C)
            feat = self.linear_layers[i](feat)       # (B, h*w, decoder_dim)
            feat = feat.transpose(1, 2).reshape(b, -1, h, w)
            # Upsample all to Stage-1 resolution
            feat = nn.functional.interpolate(feat, size=(H, W), mode='bilinear', align_corners=False)
            unified.append(feat)

        # Concatenate and fuse
        x = torch.cat(unified, dim=1)  # (B, decoder_dim*4, H, W)
        x = x.flatten(2).transpose(1, 2)  # (B, H*W, decoder_dim*4)
        x = self.fuse(x)                  # (B, H*W, decoder_dim)
        x = self.pred(x)                  # (B, H*W, num_classes)

        x = x.transpose(1, 2).reshape(B, -1, H, W)
        return x


class SegFormerRoadExtractor(nn.Module):
    """
    Complete SegFormer model for binary road extraction.
    
    Architecture Traceability:
        - Defined in: ai_architecture.md (SegFormer selected over U-Net/SAM)
        - Encoder: MiT-B2 hierarchical transformer
        - Decoder: Lightweight All-MLP
        - Output: Single-channel logits at 1/4 resolution, upsampled to input size
    
    ISRO Alignment:
        FR-02: Global receptive field enables occlusion-robust road prediction.
    """
    def __init__(self, in_channels: int = 3, num_classes: int = 1):
        super().__init__()
        self.encoder = SegFormerEncoder(in_channels=in_channels)
        self.decoder = SegFormerDecoder(num_classes=num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Input tensor (B, 3, H, W), ImageNet-normalized.
        Returns:
            Logits (B, 1, H, W) at input resolution. Apply sigmoid for probabilities.
        """
        input_h, input_w = x.shape[2], x.shape[3]
        features = self.encoder(x)
        logits = self.decoder(features)
        # Upsample to original input resolution
        logits = nn.functional.interpolate(logits, size=(input_h, input_w), mode='bilinear', align_corners=False)
        return logits

    @staticmethod
    def load_pretrained(weights_path: str, device: str = "cpu") -> "SegFormerRoadExtractor":
        """
        Loads a pre-trained checkpoint.
        Gracefully handles missing keys (e.g., decoder trained from scratch).
        """
        model = SegFormerRoadExtractor()
        state_dict = torch.load(weights_path, map_location=device)
        missing, unexpected = model.load_state_dict(state_dict, strict=False)
        if missing:
            logger.warning(f"Missing keys during weight loading: {missing}")
        if unexpected:
            logger.warning(f"Unexpected keys during weight loading: {unexpected}")
        logger.info(f"SegFormer weights loaded from {weights_path}")
        return model.to(device)
