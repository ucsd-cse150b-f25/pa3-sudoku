
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time, random

SIZE = 9
CELL = 52
PAD = 12

PUZZLES = ['530070000600195000098000060800060003400803001700020006060000280000419005000080079',
           '003020600900305001001806400008102900700000008006708200002609500800203009005010300',
           '200080300060070084030500209000105408000000000402706000301007040720040060004010003',
           '000000907000420180000705026100904000050000040000507009920108000034059000507000000',
           '030050040008010500460000012070502080000603000040109030250000098001020600080060020',
'020810740700003100090002805009040087400208003160030200302700060005600008076051090',
'100920000524010000000000070050008102000000000402700090060000000000030945000071006',
'043080250600000000000001094900004070000608000010200003820500000000000005034090710',
'480006902002008001900370060840010200003704100001060049020085007700900600609200018',
'000900002050123400030000160908000000070000090000000205091000050007439020400007000',
'001900003900700160030005007050000009004302600200000070600100030042007006500006800',
'000125400008400000420800000030000095060902010510000060000003049000007200001298000',
'062340750100005600570000040000094800400000006005830000030000091006400007059083260',
'300000000005009000200504000020000700160000058704310600000890100000067080000005437',
'630000000000500008005674000000020000003401020000000345000007004080300902947100080',
'000020040008035000000070602031046970200000000000501203049000730000000010800004000',
'361025900080960010400000057008000471000603000259000800740000005020018060005470329',
'050807020600010090702540006070020301504000908103080070900076205060090003080103040',
'080005000000003457000070809060400903007010500408007020901020000842300000000100080',
'003502900000040000106000305900251008070408030800763001308000104000020000005104800',
'000000000009805100051907420290401065000000000140508093026709580005103600000000000',
'020030090000907000900208005004806500607000208003102900800605007000309000030020050',
'005000006070009020000500107804150000000803000000092805907006000030400010200000600',
'040000050001943600009000300600050002103000506800020007005000200002436700030000040',
'004000000000030002390700080400009001209801307600200008010008053900040000000000800',
'360020089000361000000000000803000602400603007607000108000000000000418000970030014',
'500400060009000800640020000000001008208000501700500000000090084003000600060003002',
'007256400400000005010030060000508000008060200000107000030070090200000004006312700',
'000000000079050180800000007007306800450708096003502700700000005016030420000000000',
'030000080009000500007509200700105008020090030900402001004207100002000800070000090',
'200170603050000100000006079000040700000801000009050000310400000005000060906037002',
'000000080800701040040020030374000900000030000005000321010060050050802006080000000',
'000000085000210009960080100500800016000000000890006007009070052300054000480000000',
'608070502050608070002000300500090006040302050800050003005000200010704090409060701',
'050010040107000602000905000208030501040070020901080406000401000304000709020060010',
'053000790009753400100000002090080010000907000080030070500000003007641200061000940',
'006080300049070250000405000600317004007000800100826009000702000075040190003090600',
'005080700700204005320000084060105040008000500070803010450000091600508007003010600',
'000900800128006400070800060800430007500000009600079008090004010003600284001007000',
'000080000270000054095000810009806400020403060006905100017000620460000038000090000',
'000602000400050001085010620038206710000000000019407350026040530900020007000809000',
'000900002050123400030000160908000000070000090000000205091000050007439020400007000',
'380000000000400785009020300060090000800302009000040070001070500495006000000000092',
'000158000002060800030000040027030510000000000046080790050000080004070100000325000',
'010500200900001000002008030500030007008000500600080004040100700000700006003004050',
'080000040000469000400000007005904600070608030008502100900000005000781000060000010',
'904200007010000000000706500000800090020904060040002000001607000000000030300005702',
'000700800006000031040002000024070000010030080000060290000800070860000500002006000',
'001007090590080001030000080000005800050060020004100000080000030100020079020700400',
'000003017015009008060000000100007000009000200000500004000000020500600340340200000']

DEFAULT_PUZZLE = random.choice(PUZZLES)

class SudokuUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HW2 Sudoku — CSP (Friendlier UI)")

        self.values = [[0]*SIZE for _ in range(SIZE)]
        self.given  = [[False]*SIZE for _ in range(SIZE)]
        self.notes  = [[set() for _ in range(SIZE)] for __ in range(SIZE)]
        self.sel = (0, 0)
        self.original = [[0]*SIZE for _ in range(SIZE)]
        self.status = tk.StringVar(value="Click a cell and type 1–9. Arrow keys move. Shift+digit adds a note. N toggles Note Mode.")
        self.note_mode = tk.BooleanVar(value=False)

        # Solver options
        self.use_mrv = tk.BooleanVar(value=True)
        self.use_lcv = tk.BooleanVar(value=True)
        self.use_fc  = tk.BooleanVar(value=True)
        self.use_ac3 = tk.BooleanVar(value=False)

        self.timer_var = tk.StringVar(value="")
        self.err_cells = set()  # set[(r,c)] with conflicts

        # Top toolbar
        top = ttk.Frame(root, padding=(8,6,8,4)); top.pack(fill="x")
        ttk.Button(top, text="New", command=self.new_game).pack(side='left', padx=2)
        ttk.Button(top, text="Import", command=self.import_dialog).pack(side="left", padx=2)
        ttk.Button(top, text="Export", command=self.export_dialog).pack(side="left", padx=2)
        ttk.Button(top, text="Reset", command=self.reset).pack(side="left", padx=2)
        ttk.Button(top, text="Auto Notes", command=self.auto_notes).pack(side="left", padx=8)
        ttk.Separator(top, orient="vertical").pack(side="left", fill="y", padx=8)
        ttk.Button(top, text="Validate", command=self.validate).pack(side="left", padx=2)
        ttk.Button(top, text="Solve (AI)", command=self.solve).pack(side="left", padx=2)
        ttk.Label(top, textvariable=self.timer_var).pack(side="right")

        # Options
        opts = ttk.Frame(root, padding=(8,0,8,4)); opts.pack(fill="x")
        ttk.Checkbutton(opts, text="Note Mode (N)", variable=self.note_mode).pack(side="left", padx=2)
        ttk.Label(opts, text=" | AI Options: ").pack(side="left")
        ttk.Checkbutton(opts, text="MRV", variable=self.use_mrv).pack(side="left")
        ttk.Checkbutton(opts, text="LCV", variable=self.use_lcv).pack(side="left")
        ttk.Checkbutton(opts, text="Forward Checking", variable=self.use_fc).pack(side="left")
        ttk.Checkbutton(opts, text="AC-3", variable=self.use_ac3).pack(side="left")

        # Canvas grid
        w = h = SIZE*CELL + 1
        self.canvas = tk.Canvas(root, width=w+2*PAD, height=h+2*PAD, bg="white", highlightthickness=0)
        self.canvas.pack(padx=8, pady=6)
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("<Key>", self.on_key)

        # Status bar
        ttk.Label(root, textvariable=self.status, padding=(8,4,8,8)).pack(fill="x")

        # Load default puzzle
        self.load_puzzle(DEFAULT_PUZZLE)
        self.draw()

    # ---------- Model helpers ----------
    def load_puzzle(self, s: str):
        s = "".join(ch for ch in s if ch.isdigit())
        if len(s) != 81:
            messagebox.showerror("Import", "Puzzle must be exactly 81 digits (0 for blank).")
            return
        self.values = [[0]*SIZE for _ in range(SIZE)]
        self.given  = [[False]*SIZE for _ in range(SIZE)]
        self.notes  = [[set() for _ in range(SIZE)] for __ in range(SIZE)]
        k = 0
        for r in range(SIZE):
            for c in range(SIZE):
                v = int(s[k]); k += 1
                self.values[r][c] = v
                if v != 0:
                    self.given[r][c] = True
        # Save original for Reset
        self.original = [row[:] for row in self.values]
        self.compute_conflicts()
        self.status.set("Loaded puzzle. Tip: Shift+digit adds a pencil mark; V validates; S solves.")

    def export_puzzle(self) -> str:
        out = []
        for r in range(SIZE):
            for c in range(SIZE):
                out.append(str(self.values[r][c] or 0))
        return "".join(out)

    def set_cell(self, r, c, v, is_note=False):
        if self.given[r][c] and not is_note:
            return
        if is_note:
            if v == 0:
                self.notes[r][c].clear()
            else:
                if v in self.notes[r][c]:
                    self.notes[r][c].remove(v)
                else:
                    self.notes[r][c].add(v)
        else:
            self.values[r][c] = v
            self.notes[r][c].clear()
        self.compute_conflicts()

    def reset(self):
        self.values = [row[:] for row in self.original]
        self.notes = [[set() for _ in range(SIZE)] for __ in range(SIZE)]
        self.compute_conflicts()
        self.draw()

    def neighbors(self, r, c):
        for cc in range(SIZE):
            yield (r, cc)
        for rr in range(SIZE):
            yield (rr, c)
        br, bc = (r//3)*3, (c//3)*3
        for rr in range(br, br+3):
            for cc in range(bc, bc+3):
                yield (rr, cc)

    def compute_conflicts(self):
        self.err_cells = set()
        # Rows
        for r in range(SIZE):
            seen = {}
            for c in range(SIZE):
                v = self.values[r][c]
                if v:
                    if v in seen:
                        self.err_cells.add((r, c))
                        self.err_cells.add((r, seen[v]))
                    else:
                        seen[v] = c
        # Cols
        for c in range(SIZE):
            seen = {}
            for r in range(SIZE):
                v = self.values[r][c]
                if v:
                    if v in seen:
                        self.err_cells.add((r, c))
                        self.err_cells.add((seen[v], c))
                    else:
                        seen[v] = r
        # Boxes
        for br in range(0, SIZE, 3):
            for bc in range(0, SIZE, 3):
                seen = {}
                for r in range(br, br+3):
                    for c in range(bc, bc+3):
                        v = self.values[r][c]
                        if v:
                            if v in seen:
                                self.err_cells.add((r, c))
                                self.err_cells.add(seen[v])
                            else:
                                seen[v] = (r, c)

    def auto_notes(self):
        # Fill notes with currently legal candidates for blank cells
        for r in range(SIZE):
            for c in range(SIZE):
                if self.values[r][c] == 0:
                    illegal = { self.values[rr][cc] for (rr,cc) in self.neighbors(r,c) if self.values[rr][cc] != 0 }
                    self.notes[r][c] = {d for d in range(1,10) if d not in illegal}
        self.draw()

    # ---------- UI events ----------
    def on_click(self, ev):
        x = ev.x - PAD; y = ev.y - PAD
        if x < 0 or y < 0: return
        c = int(x // CELL); r = int(y // CELL)
        if 0 <= r < SIZE and 0 <= c < SIZE:
            self.sel = (r, c); self.draw()

    def on_key(self, ev):
        r, c = self.sel
        ch = ev.keysym
        # Movement
        if ch in ("Left","h","a"): c = max(0, c-1)
        elif ch in ("Right","l","d"): c = min(SIZE-1, c+1)
        elif ch in ("Up","k","w"): r = max(0, r-1)
        elif ch in ("Down","j","s"): r = min(SIZE-1, r+1)
        elif ch in ("Return", "KP_Enter"):
            pass
        elif ch in ("BackSpace","Delete"):
            self.set_cell(r, c, 0, is_note=False)
        elif ch in [str(i) for i in range(10)] + [f"KP_{i}" for i in range(10)]:
            # Normalize to digit
            digit = None
            if ch.startswith("KP_"):
                digit = int(ch[3:])
            else:
                digit = int(ch)
            if 0 <= digit <= 9:
                is_note = self.note_mode.get() or (ev.state & 0x0001)  # Shift
                if digit == 0:
                    if is_note:
                        self.set_cell(r, c, 0, is_note=True)
                    else:
                        self.set_cell(r, c, 0, is_note=False)
                else:
                    self.set_cell(r, c, digit, is_note=is_note)
        elif ch in ("n","N"):
            self.note_mode.set(not self.note_mode.get())
        elif ch in ("v","V"):
            self.validate()
        elif ch in ("s","S"):
            self.solve()
        else:
            return
        self.sel = (r, c)
        self.draw()

    # ---------- Validate & Solve ----------
    def validate(self):
        self.compute_conflicts()
        if self.err_cells:
            self.status.set(f"Conflicts found in {len(self.err_cells)} cell(s).")
        else:
            # Check completeness
            complete = all(self.values[r][c] != 0 for r in range(SIZE) for c in range(SIZE))
            self.status.set("Looks good!" + (" (Complete ✅)" if complete else " (Incomplete)"))
        self.draw()

    def solve(self):
        try:
            from . import csp as csp
        except Exception as e:
            messagebox.showerror("Import error", f"Could not import solver: {e}")
            return
        # Build grid of '0'/'1'..'9' strings
        grid = [[str(self.values[r][c] or 0) for c in range(SIZE)] for r in range(SIZE)]
        opts = dict(
            use_mrv=self.use_mrv.get(),
            use_lcv=self.use_lcv.get(),
            use_fc=self.use_fc.get(),
            use_ac3=self.use_ac3.get(),
        )
        t0 = time.perf_counter()
        try:
            sol = csp.solve(grid, **opts)
        except NotImplementedError:
            messagebox.showinfo("AI not implemented", "Implement solve() in sudoku/csp.py")
            return
        dt = time.perf_counter() - t0
        if not sol:
            self.status.set("No solution found.")
            return
        # Apply solution (keep original givens marked)
        for r in range(SIZE):
            for c in range(SIZE):
                self.values[r][c] = int(sol[r][c])
        self.compute_conflicts()
        self.draw()
        self.timer_var.set(f"Solved in {dt*1000:.1f} ms")
        self.status.set("Solved. (You can Reset to go back to the original puzzle.)")

    # ---------- Game Generator ---------
    def new_game(self):
        s = random.choice(PUZZLES)
        self.load_puzzle(s)
        self.draw()

    # ---------- Import/Export ----------
    def import_dialog(self):
        s = simpledialog.askstring("Import Puzzle", "Paste 81 digits (0 for blank):", initialvalue=DEFAULT_PUZZLE, parent=self.root)
        if s:
            self.load_puzzle(s)
            self.draw()

    def export_dialog(self):
        s = self.export_puzzle()
        self.root.clipboard_clear()
        self.root.clipboard_append(s)
        self.status.set("Copied current puzzle to clipboard.")

    # ---------- Drawing ----------
    def draw(self):
        cv = self.canvas
        cv.delete("all")
        # Highlights for row/col/box
        rsel, csel = self.sel
        # Highlight row/col
        x0 = PAD; y0 = PAD
        for r in range(SIZE):
            for c in range(SIZE):
                x = x0 + c*CELL; y = y0 + r*CELL
                fill = "white"
                if r == rsel or c == csel:
                    fill = "#f9f6d2"
                br, bc = (r//3), (c//3)
                if (rsel//3)==br and (csel//3)==bc:
                    fill = "#f6f0c0"
                if (r, c) == self.sel:
                    fill = "#e6f2ff"
                cv.create_rectangle(x, y, x+CELL, y+CELL, fill=fill, outline="#cccccc")

        # Heavy grid lines
        for i in range(SIZE+1):
            w = 3 if i%3==0 else 1
            # horizontal
            cv.create_line(PAD, PAD+i*CELL, PAD+SIZE*CELL, PAD+i*CELL, width=w)
            # vertical
            cv.create_line(PAD+i*CELL, PAD, PAD+i*CELL, PAD+SIZE*CELL, width=w)

        # Numbers and notes
        for r in range(SIZE):
            for c in range(SIZE):
                x = PAD + c*CELL; y = PAD + r*CELL
                v = self.values[r][c]
                if v:
                    color = "#000000" if self.given[r][c] else "#1a4a8c"
                    if (r,c) in self.err_cells:
                        color = "#c71f37"
                    cv.create_text(x+CELL//2, y+CELL//2, text=str(v), font=("Helvetica", 20, "bold"), fill=color)
                else:
                    notes = sorted(self.notes[r][c])
                    if notes:
                        # Render as 3x3 small digits
                        for d in notes:
                            rr = (d-1)//3; cc = (d-1)%3
                            nx = x + (cc+0.5)*(CELL/3)
                            ny = y + (rr+0.5)*(CELL/3)
                            cv.create_text(nx, ny, text=str(d), font=("Helvetica", 9), fill="#666666")

def main():
    root = tk.Tk()
    SudokuUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
