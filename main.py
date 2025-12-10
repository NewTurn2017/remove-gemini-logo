#!/usr/bin/env python3
"""
Gemini Logo Remover - 초간단 맥 앱
이미지 드롭하면 바로 로고 제거 (우하단 10%)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False


def remove_logo(image_path: Path, output_path: Path) -> bool:
    """우하단 10% 영역 로고 제거"""
    try:
        image = cv2.imread(str(image_path))
        if image is None:
            return False

        h, w = image.shape[:2]
        x1 = w - int(w * 0.10) - 10
        y1 = h - int(h * 0.10) - 10

        mask = np.zeros((h, w), dtype=np.uint8)
        mask[y1:h, x1:w] = 255

        result = cv2.inpaint(image, mask, 5, cv2.INPAINT_TELEA)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_path), result)
        return True
    except:
        return False


class App(TkinterDnD.Tk if HAS_DND else tk.Tk):
    FORMATS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}

    def __init__(self):
        super().__init__()
        self.title("Gemini Logo Remover")
        self.geometry("400x300")
        self.configure(bg="#1a1a1a")
        self.files = []
        self.processing = False
        self._setup_ui()

    def _setup_ui(self):
        # 드롭존
        self.dropzone = tk.Frame(self, bg="#252525", cursor="hand2")
        self.dropzone.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.label = tk.Label(
            self.dropzone,
            text="🖼️ 이미지를 여기에 드롭\n\n클릭하여 선택",
            bg="#252525", fg="#666",
            font=("SF Pro", 16), justify=tk.CENTER
        )
        self.label.pack(expand=True)

        # 클릭
        self.dropzone.bind("<Button-1>", lambda e: self._select())
        self.label.bind("<Button-1>", lambda e: self._select())

        # 드래그앤드롭
        if HAS_DND:
            self.dropzone.drop_target_register(DND_FILES)
            self.dropzone.dnd_bind("<<Drop>>", self._on_drop)
            self.dropzone.dnd_bind("<<DragEnter>>", lambda e: self.label.config(fg="#4a9eff"))
            self.dropzone.dnd_bind("<<DragLeave>>", lambda e: self.label.config(fg="#666"))

        # 진행바
        self.progress = ttk.Progressbar(self, mode="determinate")
        self.progress.pack(fill=tk.X, padx=20, pady=(0, 20))

    def _on_drop(self, event):
        self.label.config(fg="#666")
        files = self.tk.splitlist(event.data)
        self._process([Path(f) for f in files])

    def _select(self):
        files = filedialog.askopenfilenames(
            filetypes=[("이미지", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff")]
        )
        if files:
            self._process([Path(f) for f in files])

    def _process(self, paths):
        if self.processing:
            return

        # 파일 수집
        files = []
        for p in paths:
            if p.is_dir():
                files.extend(f for f in p.rglob("*") if f.suffix.lower() in self.FORMATS)
            elif p.suffix.lower() in self.FORMATS:
                files.append(p)

        if not files:
            return

        self.processing = True
        self.progress["value"] = 0
        self.progress["maximum"] = len(files)
        self.label.config(text=f"⏳ {len(files)}개 처리 중...", fg="#4a9eff")

        threading.Thread(target=self._batch, args=(files,), daemon=True).start()

    def _batch(self, files):
        success = 0
        with ThreadPoolExecutor(max_workers=4) as ex:
            futures = {
                ex.submit(remove_logo, f, f.parent / f"{f.stem}_clean{f.suffix}"): f
                for f in files
            }
            for future in as_completed(futures):
                if future.result():
                    success += 1
                self.after(0, lambda: self.progress.step(1))

        self.after(0, self._done, success, len(files))

    def _done(self, success, total):
        self.processing = False
        self.label.config(text=f"✅ {success}/{total}개 완료!\n\n드롭하여 계속", fg="#4a9eff")
        if success > 0:
            messagebox.showinfo("완료", f"{success}개 이미지 처리 완료!\n(_clean 접미사로 저장됨)")


def main():
    import sys
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Gemini Logo Remover - 이미지 드롭하면 우하단 로고 제거")
        print("사용법: gemini-logo-remover")
        return
    App().mainloop()


if __name__ == "__main__":
    main()
