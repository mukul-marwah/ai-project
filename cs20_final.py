import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
import time, random
 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
 
# ── LISTS (Advanced Data Types) ──────────────────────────────────────────────
income_list  = []   # stores income floats
expense_list = []   # stores expense floats
goals_list   = []   # stores {"name": str, "target": float, "saved": float}
grades_list  = []   # stores {"subject": str, "grade": float}
 
 
# ── CLASS: App (page manager) ─────────────────────────────────────────────────
class App:
    """
    Main controller class.
    ATTRIBUTES: window, frames
    Stacks all page frames on top of each other and raises the active one.
    """
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("StudentTrack")
        self.window.geometry("400x420")
        self.window.resizable(False, False)
 
        # Center on screen
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        self.window.geometry(f"400x420+{(sw-400)//2}+{(sh-420)//2}")
 
        self.frames = {}
 
        # DEFINITE LOOP: create and stack all page frames
        for PageClass in (HomePage, BudgetPage, GoalsPage, GradesPage):
            frame = PageClass(self.window, self)
            self.frames[PageClass.NAME] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)  # fill window
 
        self.show("home")
        self.window.mainloop()
 
    def show(self, name):
        # CONDITIONAL: only raise if the page exists
        if name in self.frames:
            self.frames[name].tkraise()
 
 
# ── BASE PAGE ─────────────────────────────────────────────────────────────────
class BasePage(ctk.CTkFrame):
    """Shared layout helpers used by all pages."""
    NAME = "base"
 
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#0f0f1a", corner_radius=0)
        self.app = app
 
    def back_btn(self):
        """Adds a back button that returns to the home page."""
        ctk.CTkButton(
            self, text="← Back", width=90,
            command=lambda: self.app.show("home"),
            fg_color="#1e1e2e", hover_color="#2a2a3e", corner_radius=12
        ).pack(anchor="w", padx=16, pady=(12, 0))
 
    def page_title(self, text):
        """Adds a styled page title label."""
        ctk.CTkLabel(self, text=text, font=("Courier", 20, "bold"), text_color="#7c83fd").pack(pady=(10, 6))
 
 
# ── HOME PAGE ─────────────────────────────────────────────────────────────────
class HomePage(BasePage):
    NAME = "home"
 
    def __init__(self, parent, app):
        super().__init__(parent, app)
 
        ctk.CTkLabel(self, text="📊 StudentTrack", font=("Courier", 26, "bold"), text_color="#7c83fd").pack(pady=(50, 6))
        ctk.CTkLabel(self, text="Your all-in-one student dashboard", font=("Courier", 11), text_color="#555577").pack(pady=(0, 36))
 
        # 3 navigation options — each leads to a different page
        nav_buttons = [
            ("💰  Budget Tracker", "budget", "#166534", "#15803d"),
            ("🎯  Savings Goals",  "goals",  "#1e3a5f", "#1d4ed8"),
            ("📚  Grade Tracker",  "grades", "#3b1f00", "#92400e"),
        ]
 
        # DEFINITE LOOP: build all 3 buttons from the list
        for label, page, fg, hover in nav_buttons:
            ctk.CTkButton(
                self, text=label, width=260, height=48,
                command=lambda p=page: app.show(p),
                fg_color=fg, hover_color=hover,
                corner_radius=16, font=("Courier", 14, "bold")
            ).pack(pady=8)
 
 
# ── BUDGET PAGE ───────────────────────────────────────────────────────────────
class BudgetPage(BasePage):
    NAME = "budget"
 
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.back_btn()
        self.page_title("💰 Budget Tracker")
 
        # Income input
        self.inc_entry = ctk.CTkEntry(self, placeholder_text="Income ($)", width=210)
        self.inc_entry.pack(pady=4)
        ctk.CTkButton(self, text="Add Income", width=210, fg_color="#166534", hover_color="#15803d",
                      corner_radius=12, command=self._add_income).pack(pady=4)
 
        ctk.CTkLabel(self, text="", height=8).pack()  # spacer
 
        # Expense input
        self.exp_entry = ctk.CTkEntry(self, placeholder_text="Expense ($)", width=210)
        self.exp_entry.pack(pady=4)
        ctk.CTkButton(self, text="Add Expense", width=210, fg_color="#7f1d1d", hover_color="#991b1b",
                      corner_radius=12, command=self._add_expense).pack(pady=4)
 
        ctk.CTkLabel(self, text="", height=8).pack()  # spacer
 
        ctk.CTkButton(self, text="📋 View Balance", width=210, fg_color="#4169E1", hover_color="#3551B5",
                      corner_radius=12, command=self._show_balance).pack(pady=4)
 
        # Live balance display
        self.bal_label = ctk.CTkLabel(self, text="Balance: $0.00", font=("Courier", 13), text_color="#aaaaaa")
        self.bal_label.pack(pady=8)
 
    def _refresh(self):
        """Update the live balance label after every change."""
        bal = sum(income_list) - sum(expense_list)
        self.bal_label.configure(
            text=f"Balance: ${bal:.2f}",
            text_color="#4ade80" if bal >= 0 else "#f87171"
        )
 
    def _add_income(self):
        try:
            amt = float(self.inc_entry.get())
            if amt <= 0: raise ValueError
            income_list.append(amt)   # append to list (ADVANCED DATA TYPE)
            self.inc_entry.delete(0, "end")
            self._refresh()
            messagebox.showinfo("Added", f"Income ${amt:.2f} added ✓")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive number.")
 
    def _add_expense(self):
        try:
            amt = float(self.exp_entry.get())
            if amt <= 0: raise ValueError
            expense_list.append(amt)
            self.exp_entry.delete(0, "end")
            self._refresh()
            messagebox.showinfo("Added", f"Expense ${amt:.2f} added ✓")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive number.")
 
    def _show_balance(self):
        inc = sum(income_list)
        exp = sum(expense_list)
        bal = inc - exp
 
        # NESTED CONDITIONAL: status depends on balance AND ratio
        if bal > 0 and inc > 0 and (bal / inc) >= 0.2:
            status = "✅ Healthy surplus"
        elif bal > 0:
            status = "🟡 Small surplus"
        elif bal == 0:
            status = "⚖️  Break even"
        else:
            status = "🔴 Over budget"
 
        popup = ctk.CTkToplevel(); popup.title("Balance"); popup.geometry("280x220"); popup.grab_set()
        ctk.CTkLabel(popup, text="Balance Summary", font=("Courier", 15, "bold")).pack(pady=10)
        ctk.CTkLabel(popup, text=f"Income:   ${inc:.2f}", text_color="#4ade80", font=("Courier", 13)).pack(pady=3)
        ctk.CTkLabel(popup, text=f"Expenses: ${exp:.2f}", text_color="#f87171", font=("Courier", 13)).pack(pady=3)
        ctk.CTkLabel(popup, text=f"Balance:  ${bal:.2f}", font=("Courier", 14, "bold")).pack(pady=3)
        ctk.CTkLabel(popup, text=status, font=("Courier", 12), text_color="#7c83fd").pack(pady=3)
        ctk.CTkButton(popup, text="OK", command=popup.destroy,
                      fg_color="#4169E1", hover_color="#3551B5", corner_radius=12).pack(pady=10)
 
 
# ── GOALS PAGE ────────────────────────────────────────────────────────────────
class GoalsPage(BasePage):
    NAME = "goals"
 
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.back_btn()
        self.page_title("🎯 Savings Goals")
 
        self.name_entry   = ctk.CTkEntry(self, placeholder_text="Goal name", width=210)
        self.name_entry.pack(pady=4)
        self.target_entry = ctk.CTkEntry(self, placeholder_text="Target ($)", width=210)
        self.target_entry.pack(pady=4)
 
        ctk.CTkButton(self, text="➕ Add Goal", width=210, fg_color="#1e3a5f", hover_color="#1d4ed8",
                      corner_radius=12, command=self._add_goal).pack(pady=6)
        ctk.CTkButton(self, text="💸 Add Savings to Goal", width=210, fg_color="#0e7490", hover_color="#0c6278",
                      corner_radius=12, command=self._add_savings).pack(pady=4)
        ctk.CTkButton(self, text="📊 View Goals", width=210, fg_color="#4169E1", hover_color="#3551B5",
                      corner_radius=12, command=self._view_goals).pack(pady=4)
 
    def _add_goal(self):
        name = self.name_entry.get().strip()
        try:
            target = float(self.target_entry.get())
            # CONDITIONAL with AND: both fields must pass validation
            if not name or target <= 0: raise ValueError
            goals_list.append({"name": name, "target": target, "saved": 0.0})
            self.name_entry.delete(0, "end"); self.target_entry.delete(0, "end")
            messagebox.showinfo("Added", f'Goal "{name}" — ${target:.2f} ✓')
        except ValueError:
            messagebox.showerror("Error", "Enter a valid name and positive target.")
 
    def _add_savings(self):
        if not goals_list:
            messagebox.showinfo("Goals", "Add a goal first."); return
 
        popup = ctk.CTkToplevel(); popup.title("Add Savings"); popup.geometry("280x200"); popup.grab_set()
        ctk.CTkLabel(popup, text="Which goal?", font=("Courier", 13, "bold")).pack(pady=10)
 
        names    = [g["name"] for g in goals_list]   # list comprehension
        selected = ctk.StringVar(value=names[0])
        ctk.CTkOptionMenu(popup, values=names, variable=selected).pack(pady=4)
 
        amt_entry = ctk.CTkEntry(popup, placeholder_text="Amount ($)", width=180)
        amt_entry.pack(pady=6)
 
        def confirm():
            try:
                amt = float(amt_entry.get())
                if amt <= 0: raise ValueError
                # DEFINITE LOOP: find matching goal by name
                for g in goals_list:
                    if g["name"] == selected.get():
                        g["saved"] += amt
                        done = g["saved"] >= g["target"]
                        messagebox.showinfo("Updated", f'🎉 Goal complete!' if done else f'${amt:.2f} added ✓')
                        break
                popup.destroy()
            except ValueError:
                messagebox.showerror("Error", "Enter a valid amount.")
 
        ctk.CTkButton(popup, text="Confirm", command=confirm,
                      fg_color="#0e7490", hover_color="#0c6278", corner_radius=12).pack(pady=6)
 
    def _view_goals(self):
        if not goals_list:
            messagebox.showinfo("Goals", "No goals yet."); return
 
        popup = ctk.CTkToplevel(); popup.title("Goals"); popup.geometry("300x360"); popup.grab_set()
        ctk.CTkLabel(popup, text="🎯 Your Goals", font=("Courier", 15, "bold")).pack(pady=10)
 
        # DEFINITE LOOP: display each goal
        for g in goals_list:
            pct   = min(g["saved"] / g["target"] * 100, 100)
            color = "#4ade80" if pct >= 100 else "#facc15" if pct >= 50 else "#f87171"
            f = ctk.CTkFrame(popup, corner_radius=8); f.pack(fill="x", padx=12, pady=4)
            ctk.CTkLabel(f, text=f'{g["name"]}  {pct:.0f}%', text_color=color, font=("Courier", 12, "bold")).pack(anchor="w", padx=8, pady=(6,0))
            ctk.CTkLabel(f, text=f'  ${g["saved"]:.2f} / ${g["target"]:.2f}', font=("Courier", 11), text_color="#888").pack(anchor="w", padx=8, pady=(0,6))
 
        ctk.CTkButton(popup, text="Close", command=popup.destroy,
                      fg_color="#4169E1", hover_color="#3551B5", corner_radius=12).pack(pady=10)
 
 
# ── GRADES PAGE ───────────────────────────────────────────────────────────────
class GradesPage(BasePage):
    NAME = "grades"
 
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.back_btn()
        self.page_title("📚 Grade Tracker")
 
        self.sub_entry   = ctk.CTkEntry(self, placeholder_text="Subject", width=210)
        self.sub_entry.pack(pady=4)
        self.grade_entry = ctk.CTkEntry(self, placeholder_text="Grade (0–100)", width=210)
        self.grade_entry.pack(pady=4)
 
        ctk.CTkButton(self, text="➕ Add Grade", width=210, fg_color="#3b1f00", hover_color="#92400e",
                      corner_radius=12, command=self._add_grade).pack(pady=6)
        ctk.CTkButton(self, text="📋 View Report Card", width=210, fg_color="#4169E1", hover_color="#3551B5",
                      corner_radius=12, command=self._view_report).pack(pady=4)
 
    def _letter(self, avg):
        # CONDITIONAL chain: map average to letter grade
        if avg >= 90:   return "A+"
        elif avg >= 80: return "A"
        elif avg >= 70: return "B"
        elif avg >= 60: return "C"
        elif avg >= 50: return "D"
        else:           return "F"
 
    def _add_grade(self):
        sub = self.sub_entry.get().strip()
        try:
            grade = float(self.grade_entry.get())
            # CONDITIONAL with AND
            if not sub or not (0 <= grade <= 100): raise ValueError
            grades_list.append({"subject": sub, "grade": grade})
            self.sub_entry.delete(0, "end"); self.grade_entry.delete(0, "end")
            messagebox.showinfo("Added", f"{sub}: {grade:.1f}% ✓")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid subject and grade (0–100).")
 
    def _view_report(self):
        if not grades_list:
            messagebox.showinfo("Grades", "No grades yet."); return
 
        # Group by subject using a dict
        grouped = {}
        for entry in grades_list:
            s = entry["subject"]
            grouped.setdefault(s, []).append(entry["grade"])
 
        popup = ctk.CTkToplevel(); popup.title("Report Card"); popup.geometry("300x380"); popup.grab_set()
        ctk.CTkLabel(popup, text="📚 Report Card", font=("Courier", 15, "bold")).pack(pady=10)
 
        total, count = 0.0, 0
 
        # DEFINITE LOOP: display each subject row
        for sub, gs in grouped.items():
            avg    = sum(gs) / len(gs)
            letter = self._letter(avg)
            total += avg; count += 1
 
            # NESTED CONDITIONAL: colour based on average AND pass/fail status
            if avg >= 80:
                color = "#4ade80"
            elif avg >= 60 and letter != "F":
                color = "#facc15"
            else:
                color = "#f87171"
 
            f = ctk.CTkFrame(popup, corner_radius=8); f.pack(fill="x", padx=12, pady=4)
            ctk.CTkLabel(f, text=f"{sub}  [{letter}]", text_color=color, font=("Courier", 12, "bold")).pack(anchor="w", padx=8, pady=(6,0))
            ctk.CTkLabel(f, text=f"  Avg: {avg:.1f}%  |  {len(gs)} grade(s)", font=("Courier", 11), text_color="#888").pack(anchor="w", padx=8, pady=(0,6))
 
        if count > 0:
            overall = total / count
            ctk.CTkLabel(popup, text=f"Overall: {overall:.1f}%  [{self._letter(overall)}]",
                         font=("Courier", 13, "bold"), text_color="#7c83fd").pack(pady=6)
 
        ctk.CTkButton(popup, text="Close", command=popup.destroy,
                      fg_color="#4169E1", hover_color="#3551B5", corner_radius=12).pack(pady=6)
 
 
# ── PIL LOADING ANIMATION ─────────────────────────────────────────────────────
def show_loading():
    """
    Spinning gradient arc animation using PIL.
    INDEFINITE LOOP: loader.after() keeps calling frame() until time expires.
    DEFINITE LOOP: 60 arc segments drawn per frame to create gradient effect.
    """
    loader = tk.Tk()
    loader.title("Loading")
    loader.geometry("340x340")
    loader.configure(bg="#0f0f1a")
    loader.resizable(False, False)
    sw = loader.winfo_screenwidth(); sh = loader.winfo_screenheight()
    loader.geometry(f"340x340+{(sw-340)//2}+{(sh-340)//2}")
 
    canvas = tk.Canvas(loader, width=340, height=340, bg="#0f0f1a", highlightthickness=0)
    canvas.pack()
    tk.Label(loader, text="StudentTrack", bg="#0f0f1a", fg="#7c83fd", font=("Courier", 17, "bold")).place(relx=0.5, rely=0.2, anchor="center")
    msg_lbl = tk.Label(loader, text="Loading...", bg="#0f0f1a", fg="#555577", font=("Courier", 10))
    msg_lbl.place(relx=0.5, rely=0.82, anchor="center")
 
    messages = ["Initializing...", "Loading modules...", "Almost ready..."]
    img_ref  = [None]
    angle    = [0]
    start    = time.time()
    duration = random.randint(3, 5)
    CX = CY  = 170; R = 75
 
    def frame():
        elapsed = time.time() - start
 
        # INDEFINITE LOOP: keep animating until duration expires
        if elapsed >= duration:
            loader.destroy(); return
 
        # Cycle loading message
        idx = min(int(elapsed / (duration / len(messages))), len(messages) - 1)
        msg_lbl.config(text=messages[idx])
 
        img = Image.new("RGBA", (340, 340), (15, 15, 26, 255))
        d   = ImageDraw.Draw(img)
        d.ellipse([CX-R, CY-R, CX+R, CY+R], outline=(50, 50, 80, 255), width=13)
 
        # DEFINITE LOOP: draw gradient arc in 60 small segments
        for i in range(60):
            if i >= 45: break          # 45/60 * 360 = 270° arc span
            t  = i / 60
            rc = int(124 * (1 - t))    # red channel fades out
            gc = int(131 + t * 79)     # green channel rises
            bc = 255
            d.arc([CX-R, CY-R, CX+R, CY+R],
                  start=angle[0] + i * 6,
                  end=angle[0] + (i + 1) * 6,
                  fill=(rc, gc, bc, 255), width=13)
 
        photo = ImageTk.PhotoImage(img)
        img_ref[0] = photo              # prevent garbage collection
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=photo)
 
        angle[0] = (angle[0] + 7) % 360   # rotate 7° per frame
        loader.after(30, frame)            # schedule next frame (~33 fps)
 
    frame()
    loader.mainloop()
 
 
# ── ENTRY POINT ───────────────────────────────────────────────────────────────
show_loading()
App()
