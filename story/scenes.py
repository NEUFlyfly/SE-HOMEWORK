from __future__ import annotations

import pygame

from core.models import Furniture, Interaction, SceneData


def childhood_piano_room() -> SceneData:
    piano_rect = pygame.Rect(584, 170, 206, 84)
    window_rect = pygame.Rect(392, 92, 174, 74)
    chair_rect = pygame.Rect(500, 300, 54, 62)
    shelf_rect = pygame.Rect(112, 152, 118, 164)
    table_rect = pygame.Rect(238, 344, 126, 76)
    plant_rect = pygame.Rect(788, 386, 54, 76)
    bed_rect = pygame.Rect(116, 434, 154, 72)

    furniture = (
        Furniture(
            "老钢琴",
            piano_rect,
            "piano",
            Interaction(
                "老钢琴",
                piano_rect.inflate(36, 42),
                "按 Space 弹响老钢琴",
                ("琴键微微泛黄，低音区贴着小明小时候的贴纸。", "你按下一个和弦，房间像被旧时光轻轻照亮。"),
                "第一枚和弦",
            ),
        ),
        Furniture(
            "窗户",
            window_rect,
            "window",
            Interaction(
                "窗户",
                window_rect.inflate(34, 36),
                "按 Space 看向窗外",
                ("窗外是傍晚的梧桐树影。", "风吹进来，谱架上的纸页翻到第一首练习曲。"),
                "梧桐晚风",
            ),
        ),
        Furniture(
            "椅子",
            chair_rect,
            "chair",
            Interaction(
                "椅子",
                chair_rect.inflate(38, 34),
                "按 Space 查看椅子",
                ("小小的木椅被磨得发亮。", "妈妈以前总坐在这里，数着小明练琴的拍子。"),
                "陪练的拍子",
            ),
        ),
        Furniture(
            "书架",
            shelf_rect,
            "shelf",
            Interaction(
                "书架",
                shelf_rect.inflate(28, 28),
                "按 Space 翻看书架",
                ("书架上摆着乐理书、铅笔和一只旧节拍器。", "节拍器停在 60，每一下都像童年的心跳。"),
                "旧节拍器",
            ),
        ),
        Furniture(
            "矮桌",
            table_rect,
            "table",
            Interaction(
                "矮桌",
                table_rect.inflate(32, 30),
                "按 Space 查看矮桌",
                ("桌上放着没写完的五线谱和一杯温牛奶。", "纸角写着：长大以后，要在最大的舞台弹琴。"),
                "未完的五线谱",
            ),
        ),
        Furniture(
            "绿植",
            plant_rect,
            "plant",
            Interaction(
                "绿植",
                plant_rect.inflate(40, 34),
                "按 Space 触碰绿植",
                ("叶片上停着一粒傍晚的金光。", "小明想起每次练琴前，都会先给它浇一点水。"),
                "窗边的小绿意",
            ),
        ),
        Furniture(
            "小床",
            bed_rect,
            "bed",
            Interaction(
                "小床",
                bed_rect.inflate(36, 30),
                "按 Space 整理小床",
                ("被角压着一本贴满星星的练琴本。", "有些夜晚，小明就是抱着旋律睡着的。"),
                "星星练琴本",
            ),
        ),
    )

    return SceneData(
        scene_id="childhood_piano_room",
        title="人生记忆回廊 · 童年 · 老式琴房",
        spawn=(486, 418),
        furniture=furniture,
        initial_dialogue="靠近家具后按 Space 查看童年的记忆。",
    )
