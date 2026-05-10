from __future__ import annotations

from collections.abc import Sequence

import pygame

from core.constants import COLORS, ROOM_RECT
from core.models import Furniture, Interaction, SceneData, SceneFontBook
from rendering.ui import draw_text


def draw_childhood_background(
    surface: pygame.Surface,
    furniture: Sequence[Furniture],
    fonts: SceneFontBook,
) -> None:
    surface.fill((34, 30, 33))
    _draw_room_shell(surface)
    _draw_floor(surface)
    _draw_wall_details(surface, furniture, fonts)
    _draw_foreground_details(surface)


def _draw_room_shell(surface: pygame.Surface) -> None:
    outer = ROOM_RECT.inflate(28, 28)
    pygame.draw.rect(surface, COLORS["wood_dark"], outer, border_radius=4)
    pygame.draw.rect(surface, COLORS["wall"], ROOM_RECT, border_radius=2)
    pygame.draw.rect(surface, COLORS["ink"], outer, 4, border_radius=4)
    pygame.draw.rect(surface, COLORS["wall_dark"], (ROOM_RECT.x, ROOM_RECT.y, ROOM_RECT.width, 96))
    pygame.draw.rect(surface, COLORS["wood_dark"], (ROOM_RECT.x, ROOM_RECT.y + 94, ROOM_RECT.width, 8))


def _draw_floor(surface: pygame.Surface) -> None:
    floor = pygame.Rect(ROOM_RECT.x, ROOM_RECT.y + 102, ROOM_RECT.width - 40, ROOM_RECT.height - 122)
    pygame.draw.rect(surface, COLORS["floor_a"], floor)
    tile = 32
    for y in range(floor.y, floor.bottom, tile):
        for x in range(floor.x, floor.right, tile):
            color = COLORS["floor_b"] if (x // tile + y // tile) % 2 else COLORS["floor_a"]
            pygame.draw.rect(surface, color, (x, y, tile, tile))
            pygame.draw.rect(surface, (178, 127, 78), (x, y, tile, tile), 1)

    rug = pygame.Rect(366, 326, 218, 118)
    pygame.draw.rect(surface, COLORS["red_dark"], rug, border_radius=4)
    pygame.draw.rect(surface, COLORS["red"], rug.inflate(-12, -12), border_radius=4)
    pygame.draw.rect(surface, COLORS["gold"], rug.inflate(-30, -30), 4, border_radius=4)
    for x in range(rug.x + 26, rug.right - 20, 22):
        pygame.draw.circle(surface, COLORS["cream"], (x, rug.centery), 3)


def _draw_wall_details(surface: pygame.Surface, furniture: Sequence[Furniture], fonts: SceneFontBook) -> None:
    pygame.draw.rect(surface, COLORS["wood_light"], (122, 94, 78, 42), border_radius=2)
    pygame.draw.rect(surface, COLORS["ink"], (122, 94, 78, 42), 3, border_radius=2)
    draw_text(surface, "练琴日程", (126, 95), fonts.small, COLORS["paper"])
    draw_text(surface, "1  2  3  4", (126, 110), fonts.small, (231, 205, 162))

    window = next((item for item in furniture if item.kind == "window"), None)
    if window is None:
        return

    frame = window.rect
    pygame.draw.rect(surface, COLORS["wood_dark"], frame.inflate(10, 10), border_radius=3)
    pygame.draw.rect(surface, COLORS["glass"], frame, border_radius=2)
    pygame.draw.circle(surface, (249, 199, 112), (frame.x + 26, frame.y + 20), 12)
    pygame.draw.line(surface, COLORS["glass_light"], (frame.x + 10, frame.y + 12), (frame.x + 76, frame.y + 12), 4)
    pygame.draw.line(surface, COLORS["glass_light"], (frame.x + 94, frame.y + 12), (frame.x + 164, frame.y + 12), 4)
    pygame.draw.line(surface, COLORS["wood_dark"], frame.midtop, frame.midbottom, 5)
    pygame.draw.line(surface, COLORS["wood_dark"], frame.midleft, frame.midright, 5)
    pygame.draw.rect(surface, COLORS["ink"], frame.inflate(10, 10), 3, border_radius=3)


def _draw_foreground_details(surface: pygame.Surface) -> None:
    pygame.draw.rect(surface, COLORS["wood_dark"], (ROOM_RECT.centerx - 44, ROOM_RECT.bottom - 28, 88, 24))
    pygame.draw.rect(surface, COLORS["gold"], (ROOM_RECT.centerx - 10, ROOM_RECT.bottom - 22, 20, 8), border_radius=2)


def childhood_piano_room() -> SceneData:
    piano_rect = pygame.Rect(584, 170, 206, 84)
    window_rect = pygame.Rect(392, 92, 174, 74)
    cabinet_rect = pygame.Rect(112, 148, 118, 116)
    fridge_rect = pygame.Rect(242, 138, 64, 128)
    microwave_rect = pygame.Rect(322, 186, 44, 36)
    desk_rect = pygame.Rect(400, 288, 146, 142)
    chair_rect = pygame.Rect(260, 304, 54, 82)
    clean_desk_rect = pygame.Rect(620, 276, 142, 54)
    bed_rect = pygame.Rect(100, 300, 150, 190)
    sofa_rect = pygame.Rect(660,370, 148, 92)
    little_table_rect = pygame.Rect(809, 180, 58, 76)

    furniture = (
        Furniture(
            "老钢琴",
            piano_rect,
            "piano",
            Interaction(
                "老钢琴",
                piano_rect.inflate(36, 42),
                "按 Space 轻触琴键",
                ("琴盖下睡着一排月光，指尖落下时，童年的尘埃都变得温柔。", "有一枚和弦没有散去，它一直替你记着回家的方向。"),
                "未散的和弦",
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
                ("窗玻璃收着一小片黄昏，梧桐叶在里面慢慢漂远。", "那阵风翻过谱页，也翻过你还不懂离别的年纪。"),
                "窗里的黄昏",
            ),
        ),
        Furniture(
            "旧木柜",
            cabinet_rect,
            "cabinet",
            Interaction(
                "旧木柜",
                cabinet_rect.inflate(28, 28),
                "按 Space 打开木柜",
                ("柜门轻轻一响，像替旧日子咳去一层薄薄的灰。", "里面藏着泛黄的贴纸和半截铅笔，都是练习曲旁边开出的花。"),
                "柜中的小花",
            ),
        ),
        Furniture(
            "小冰箱",
            fridge_rect,
            "fridge",
            Interaction(
                "小冰箱",
                fridge_rect.inflate(30, 26),
                "按 Space 打开冰箱",
                ("冰箱轻轻嗡鸣，像夏夜躲在角落里的一只小兽。", "里面的牛奶还带着凉意，等你练完最后一遍音阶。"),
                "夏夜牛奶",
            ),
        ),
        Furniture(
            "微波炉",
            microwave_rect,
            "microwave",
            Interaction(
                "微波炉",
                microwave_rect.inflate(30, 28),
                "按 Space 查看微波炉",
                ("小小的屏幕暗着，玻璃门里收着一圈没有转完的暖光。", "有些等待很短，却足够把一杯牛奶变成安慰。"),
                "旋转的暖光",
            ),
        ),
        Furniture(
            "写字桌",
            desk_rect,
            "desk",
            Interaction(
                "写字桌",
                desk_rect.inflate(32, 32),
                "按 Space 查看写字桌",
                ("摊开的本子像一片小小舞台，铅笔和橡皮都安静候场。", "你曾在这里把错音圈起来，也把明天写得闪闪发亮。"),
                "发亮的明天",
            ),
        ),
        Furniture(
            "紫椅子",
            chair_rect,
            "chair",
            Interaction(
                "紫椅子",
                chair_rect.inflate(38, 34),
                "按 Space 坐上椅子",
                ("紫色椅面像一朵安静的花，等过许多个放学后的傍晚。", "你仿佛又听见有人在身后轻轻数拍：一、二、三、别急。"),
                "温柔的拍子",
            ),
        ),
        Furniture(
            "长矮桌",
            clean_desk_rect,
            "clean_desk",
            Interaction(
                "长矮桌",
                clean_desk_rect.inflate(32, 30),
                "按 Space 查看矮桌",
                ("桌面被擦得发亮，像刚铺好的一段沉默旋律。", "那些没有说出口的鼓励，曾一件件摆在这里等你发现。"),
                "沉默的旋律",
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
                ("枕头像两朵白云停在床头，紫色被面盛着还没醒来的梦。", "有些旋律不是练会的，是在夜里悄悄陪你长大的。"),
                "枕边的旋律",
            ),
        ),
        Furniture(
            "红沙发",
            sofa_rect,
            "sofa",
            Interaction(
                "红沙发",
                sofa_rect.inflate(34, 30),
                "按 Space 靠近沙发",
                ("红沙发把午后的光抱得很满，像一段可以坐下来的安宁。", "你曾窝在这里听大人聊天，偷偷把旋律藏进心里。"),
                "午后的安宁",
            ),
        ),
        Furniture(
            "小圆桌",
            little_table_rect,
            "little_table",
            Interaction(
                "小圆桌",
                little_table_rect.inflate(40, 34),
                "按 Space 查看小圆桌",
                ("小圆桌托着一枚安静的红，像把掌心里的春天放在这里。", "你想起每次练琴前，总要先整理好那些细小却郑重的仪式。"),
                "掌心的春天",
            ),
        ),
    )

    return SceneData(
        scene_id="childhood_piano_room",
        title="人生记忆回廊 · 童年 · 老式琴房",
        spawn=(492, 404),
        furniture=furniture,
        draw_background=draw_childhood_background,
        initial_dialogue="靠近家具后按 Space 查看童年的记忆。",
    )
