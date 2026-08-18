from pathlib import Path
import tkinter as tk
from tkinter import ttk

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
WORKSPACE = r"D:\Projects\tjkimeye-staff"


def save(entry: tk.Entry, status: ttk.Label, root: tk.Tk) -> None:
    key = entry.get().strip().strip('"').strip("'")
    if not key:
        status.config(text="키를 붙여 넣은 다음 저장을 누르세요.")
        return
    ENV_PATH.write_text(
        f"CURSOR_API_KEY={key}\nPILAR_WORKSPACE={WORKSPACE}\n",
        encoding="utf-8",
    )
    status.config(text="저장했습니다. 이 창을 닫아도 됩니다.")
    root.after(800, root.destroy)


def main() -> None:
    root = tk.Tk()
    root.title("필라르 — Cursor 키 붙여넣기")
    root.geometry("560x200")
    root.resizable(False, False)
    try:
        root.attributes("-topmost", True)
    except tk.TclError:
        pass

    frame = ttk.Frame(root, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="Cursor 키를 아래 칸에 붙여 넣고 저장을 누르세요.",
    ).pack(anchor="w")

    entry = ttk.Entry(frame, width=64)
    entry.pack(fill="x", pady=12)
    entry.focus_set()

    status = ttk.Label(frame, text="")
    status.pack(anchor="w", pady=(0, 8))

    ttk.Button(
        frame,
        text="저장",
        command=lambda: save(entry, status, root),
    ).pack(anchor="e")

    root.bind("<Return>", lambda _event: save(entry, status, root))
    root.mainloop()


if __name__ == "__main__":
    main()
