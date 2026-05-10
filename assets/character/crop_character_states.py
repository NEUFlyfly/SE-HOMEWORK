from __future__ import annotations

from pathlib import Path
from tkinter import BOTH, BOTTOM, HORIZONTAL, LEFT, RIGHT, TOP, X, Y, Canvas, Label, Scrollbar, TclError, Tk, messagebox

from PIL import Image, ImageTk


STATE_NAMES = [
    "main",
    "up-2",
    "up-0",
    "up-1",
    "right-1",
    "right-0",
    "right-2",
    "down-2",
    "down-0",
    "down-1",
    "left-1",
    "left-0",
    "left-2",    

]

DEFAULT_ZOOM = 4
MIN_ZOOM = 1
MAX_ZOOM = 8
STATE_COUNT = len(STATE_NAMES)


class CropWindow:
    def __init__(self, root: Tk, role_name: str, image_path: Path) -> None:
        self.root = root
        self.role_name = role_name
        self.image_path = image_path
        self.output_dir = image_path.parent
        self.image = Image.open(image_path).convert("RGBA")
        self.zoom = DEFAULT_ZOOM
        self.photo: ImageTk.PhotoImage | None = None
        self.image_id: int | None = None
        self.selection_start: tuple[int, int] | None = None
        self.selection_rect: int | None = None
        self.saved_count = 0

        root.title(self._title_text())
        root.geometry(self._initial_geometry())

        self.status = Label(root, anchor="w", justify=LEFT)
        self.status.pack(side=TOP, fill=X)

        self.canvas = Canvas(root, cursor="crosshair", background="#202020")
        self.h_scroll = Scrollbar(root, orient=HORIZONTAL, command=self.canvas.xview)
        self.v_scroll = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.v_scroll.pack(side=RIGHT, fill=Y)
        self.h_scroll.pack(side=BOTTOM, fill=X)

        self._set_zoom(DEFAULT_ZOOM)

        self.canvas.bind("<ButtonPress-1>", self._start_selection)
        self.canvas.bind("<B1-Motion>", self._update_selection)
        self.canvas.bind("<ButtonRelease-1>", self._finish_selection)
        root.bind("<BackSpace>", self._undo_last)
        root.bind("<Delete>", self._undo_last)
        root.bind("+", self._zoom_in)
        root.bind("=", self._zoom_in)
        root.bind("-", self._zoom_out)
        root.bind("0", self._reset_zoom)

        self._maximize_window()
        self._update_status()

    def _initial_geometry(self) -> str:
        width = min(max(self.image.width * self.zoom + 24, 900), 1400)
        height = min(max(self.image.height * self.zoom + 80, 700), 1000)
        return f"{width}x{height}"

    def _title_text(self) -> str:
        return f"{self.role_name} cropper - {self.saved_count}/{STATE_COUNT}"

    def _update_status(self) -> None:
        if self.saved_count < STATE_COUNT:
            next_name = self._output_name(self.saved_count).name
            text = (
                f"拖拽鼠标左键框选第 {self.saved_count + 1}/{STATE_COUNT} 张：{next_name}。"
                f"当前显示 {self.zoom}x，按 + / - 缩放，0 还原，Backspace/Delete 撤销上一张。"
            )
        else:
            text = f"{STATE_COUNT} 张已全部保存。可以关闭窗口，或按 Backspace/Delete 撤销上一张后重选。"
        self.status.configure(text=text)
        self.root.title(self._title_text())

    def _output_name(self, index: int) -> Path:
        return self.output_dir / f"{self.role_name}-{STATE_NAMES[index]}.png"

    def _maximize_window(self) -> None:
        try:
            self.root.state("zoomed")
        except TclError:
            try:
                self.root.attributes("-zoomed", True)
            except TclError:
                self.root.geometry(self._initial_geometry())

    def _set_zoom(self, zoom: int) -> None:
        self.zoom = max(MIN_ZOOM, min(zoom, MAX_ZOOM))
        display_size = (self.image.width * self.zoom, self.image.height * self.zoom)
        display_image = self.image.resize(display_size, Image.Resampling.NEAREST)
        self.photo = ImageTk.PhotoImage(display_image)

        if self.image_id is None:
            self.image_id = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        else:
            self.canvas.itemconfigure(self.image_id, image=self.photo)
        self.canvas.configure(scrollregion=(0, 0, display_size[0], display_size[1]))

        if self.selection_rect is not None:
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None
            self.selection_start = None
        self._update_status()

    def _zoom_in(self, _event=None) -> None:
        self._set_zoom(self.zoom + 1)

    def _zoom_out(self, _event=None) -> None:
        self._set_zoom(self.zoom - 1)

    def _reset_zoom(self, _event=None) -> None:
        self._set_zoom(DEFAULT_ZOOM)

    def _canvas_point(self, event) -> tuple[int, int]:
        x = int(self.canvas.canvasx(event.x))
        y = int(self.canvas.canvasy(event.y))
        return self._clamp_point(x, y)

    def _clamp_point(self, x: int, y: int) -> tuple[int, int]:
        clamped_x = max(0, min(x, self.image.width * self.zoom))
        clamped_y = max(0, min(y, self.image.height * self.zoom))
        return clamped_x, clamped_y

    def _start_selection(self, event) -> None:
        if self.saved_count >= STATE_COUNT:
            return

        self.selection_start = self._canvas_point(event)
        if self.selection_rect is not None:
            self.canvas.delete(self.selection_rect)
        x, y = self.selection_start
        self.selection_rect = self.canvas.create_rectangle(x, y, x, y, outline="#00ff66", width=2)

    def _update_selection(self, event) -> None:
        if self.selection_start is None or self.selection_rect is None:
            return

        x0, y0 = self.selection_start
        x1, y1 = self._canvas_point(event)
        self.canvas.coords(self.selection_rect, x0, y0, x1, y1)

    def _finish_selection(self, event) -> None:
        if self.selection_start is None or self.selection_rect is None:
            return

        x0, y0 = self.selection_start
        x1, y1 = self._canvas_point(event)
        display_left, display_right = sorted((x0, x1))
        display_top, display_bottom = sorted((y0, y1))
        left = display_left // self.zoom
        top = display_top // self.zoom
        right = min(self.image.width, (display_right + self.zoom - 1) // self.zoom)
        bottom = min(self.image.height, (display_bottom + self.zoom - 1) // self.zoom)
        self.selection_start = None

        if right - left <= 1 or bottom - top <= 1:
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None
            self._update_status()
            return

        output_path = self._output_name(self.saved_count)
        self.image.crop((left, top, right, bottom)).save(output_path, "PNG")
        self.saved_count += 1
        self.canvas.delete(self.selection_rect)
        self.selection_rect = None
        self._update_status()

        if self.saved_count == STATE_COUNT:
            messagebox.showinfo("完成", f"{STATE_COUNT} 张人物状态图片已全部保存。")

    def _undo_last(self, _event=None) -> None:
        if self.saved_count == 0:
            return

        self.saved_count -= 1
        last_path = self._output_name(self.saved_count)
        if last_path.exists():
            last_path.unlink()
        self._update_status()


def find_character_image(base_dir: Path, role_name: str) -> Path:
    role_dir = base_dir / role_name
    image_path = role_dir / f"{role_name}.png"
    if not role_dir.is_dir():
        raise FileNotFoundError(f"找不到角色文件夹：{role_dir}")
    if not image_path.is_file():
        raise FileNotFoundError(f"找不到角色原图：{image_path}")
    return image_path


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    role_name = input("请输入角色名：").strip()
    if not role_name:
        print("角色名不能为空。")
        return

    try:
        image_path = find_character_image(base_dir, role_name)
    except FileNotFoundError as exc:
        print(exc)
        return

    root = Tk()
    CropWindow(root, role_name, image_path)
    root.mainloop()


if __name__ == "__main__":
    main()
