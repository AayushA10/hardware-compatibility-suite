import subprocess
import re
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import psutil
import platform
import time
from datetime import timedelta, datetime
from fpdf import FPDF

class HardwareCompatibilityTestSuite:
    def __init__(self):
        self.devices = {
            'CPUs': [],
            'GPUs': [],
            'Network Cards': []
        }
        self.test_results = []

    def detect_hardware(self, check_cpu=True, check_gpu=True, check_net=True):
        if check_cpu:
            self.devices['CPUs'] = self._detect_cpus()
        if check_gpu:
            self.devices['GPUs'] = self._detect_gpus()
        if check_net:
            self.devices['Network Cards'] = self._detect_network_cards()
        return self.devices

    def _detect_cpus(self):
        try:
            output = subprocess.check_output("sysctl -n machdep.cpu.brand_string", shell=True)
            return [output.decode("utf-8").strip()]
        except Exception as e:
            return [f"CPU detection failed: {str(e)}"]

    def _detect_gpus(self):
        try:
            output = subprocess.check_output("system_profiler SPDisplaysDataType", shell=True)
            gpus = re.findall(r"Chipset Model: (.+)", output.decode("utf-8"))
            return gpus if gpus else ["No GPU detected"]
        except Exception as e:
            return [f"GPU detection failed: {str(e)}"]

    def _detect_network_cards(self):
        try:
            output = subprocess.check_output("networksetup -listallhardwareports", shell=True)
            cards = re.findall(r"Device: (.+)", output.decode("utf-8"))
            return cards if cards else ["No network card detected"]
        except Exception as e:
            return [f"Network card detection failed: {str(e)}"]

    def run_tests(self, check_cpu=True, check_gpu=True, check_net=True, progress_callback=None):
        self.test_results.clear()
        steps = sum([check_cpu * len(self.devices['CPUs']), check_gpu * len(self.devices['GPUs']), check_net * len(self.devices['Network Cards'])]) * 2
        current = 0

        if check_cpu:
            for cpu in self.devices['CPUs']:
                self.test_results.append(self.test_cpu(cpu))
                current += 1
                if progress_callback: progress_callback(current, steps)
                self.test_results.append(self.measure_power_consumption(cpu))
                current += 1
                if progress_callback: progress_callback(current, steps)

        if check_gpu:
            for gpu in self.devices['GPUs']:
                self.test_results.append(self.test_gpu(gpu))
                current += 1
                if progress_callback: progress_callback(current, steps)
                self.test_results.append(self.measure_power_consumption(gpu))
                current += 1
                if progress_callback: progress_callback(current, steps)

        if check_net:
            for net_card in self.devices['Network Cards']:
                self.test_results.append(self.test_network_card(net_card))
                current += 1
                if progress_callback: progress_callback(current, steps)
                self.test_results.append(self.measure_power_consumption(net_card))
                current += 1
                if progress_callback: progress_callback(current, steps)

    def test_cpu(self, cpu):
        try:
            output = subprocess.check_output("sysctl -n hw.ncpu", shell=True)
            cores = output.decode("utf-8").strip()
            return f"Tested CPU: {cpu} — Cores: {cores} — Status: OK"
        except Exception as e:
            return f"Tested CPU: {cpu} — Status: FAILED ({str(e)})"

    def test_gpu(self, gpu):
        try:
            output = subprocess.check_output("system_profiler SPDisplaysDataType", shell=True)
            metal_support = re.findall(r"Metal: (.+)", output.decode("utf-8"))
            status = metal_support[0].strip() if metal_support else "Unknown"
            return f"Tested GPU: {gpu} — Metal Support: {status}"
        except Exception as e:
            return f"Tested GPU: {gpu} — Status: FAILED ({str(e)})"

    def test_network_card(self, net_card):
        try:
            result = subprocess.run(["ping", "-c", "2", "-t", "2", "8.8.8.8"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                return f"Tested Network Card: {net_card} — Ping Success ✅"
            else:
                return f"Tested Network Card: {net_card} — Ping Failed ❌"
        except Exception as e:
            return f"Tested Network Card: {net_card} — Status: FAILED ({str(e)})"

    def measure_power_consumption(self, device):
        return f"Measured power usage of {device} — Simulated: 15W"

    def get_report(self):
        report = "--- Compatibility Report ---\n"
        for line in self.test_results:
            report += line + "\n"
        return report

    def _timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def save_report_txt(self, filepath=None):
        if not filepath:
            filepath = f"report_{self._timestamp()}.txt"
        with open(filepath, "w") as f:
            f.write(self.get_report())

    def save_report_json(self, filepath=None):
        if not filepath:
            filepath = f"report_{self._timestamp()}.json"
        report_data = {
            "Detected Devices": self.devices,
            "Test Results": self.test_results
        }
        with open(filepath, "w") as f:
            json.dump(report_data, f, indent=4)

    def save_report_pdf(self, filepath=None):
        if not filepath:
            filepath = f"report_{self._timestamp()}.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Hardware Compatibility Report", ln=True, align='C')
        pdf.ln(10)
        for line in self.test_results:
            pdf.multi_cell(0, 10, line)
        pdf.output(filepath)

# GUI
root = tk.Tk()
root.title("Hardware Compatibility Tester")
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

style = ttk.Style()
style.theme_use('default')
style.configure("TProgressbar", troughcolor='white', background='blue', thickness=15)

# Tab 1 - Hardware Test
tab1 = tk.Frame(notebook)
notebook.add(tab1, text="Hardware Test")
tk.Label(tab1, text="Hardware Compatibility Test Suite", font=("Helvetica", 16)).pack(pady=10)

cpu_var = tk.BooleanVar(value=True)
gpu_var = tk.BooleanVar(value=True)
net_var = tk.BooleanVar(value=True)

check_frame = tk.Frame(tab1)
check_frame.pack(pady=5)
tk.Checkbutton(check_frame, text="CPU", variable=cpu_var).grid(row=0, column=0, padx=10)
tk.Checkbutton(check_frame, text="GPU", variable=gpu_var).grid(row=0, column=1, padx=10)
tk.Checkbutton(check_frame, text="Network", variable=net_var).grid(row=0, column=2, padx=10)

dark_mode_var = tk.BooleanVar(value=False)
tk.Checkbutton(tab1, text="Dark Mode", variable=dark_mode_var, command=lambda: apply_theme()).pack(pady=5)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(tab1, variable=progress_var, maximum=100)
progress_bar.pack(fill='x', padx=20, pady=5)

output_box = scrolledtext.ScrolledText(tab1, width=100, height=20, font=("Courier", 10))
output_box.pack(padx=10, pady=10)

button_frame = tk.Frame(tab1)
button_frame.pack()
tk.Button(button_frame, text="Run Tests", command=lambda: run_test(), bg="#228B22", fg="white").grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Save as TXT", command=lambda: save_txt(), bg="#007acc", fg="white").grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Save as JSON", command=lambda: save_json(), bg="#ff8c00", fg="white").grid(row=0, column=2, padx=10)
tk.Button(button_frame, text="Save as PDF", command=lambda: save_pdf(), bg="#aa00ff", fg="white").grid(row=0, column=3, padx=10)

# Tab 2 - System Stats
tab2 = tk.Frame(notebook)
notebook.add(tab2, text="System Stats")
tk.Label(tab2, text="System Stats Monitor", font=("Helvetica", 16)).pack(pady=10)
tk.Button(tab2, text="Refresh Stats", command=lambda: refresh_stats(), bg="purple", fg="white").pack(pady=5)
stats_box = scrolledtext.ScrolledText(tab2, width=100, height=20, font=("Courier", 10))
stats_box.pack(padx=10, pady=10)

# Functions
def apply_theme():
    bg = "#1e1e1e" if dark_mode_var.get() else "white"
    fg = "white" if dark_mode_var.get() else "black"
    for widget in [tab1, tab2, check_frame, output_box, stats_box]:
        widget.configure(bg=bg)
    output_box.configure(fg=fg, insertbackground=fg)
    stats_box.configure(fg=fg, insertbackground=fg)

def run_test():
    output_box.delete(1.0, tk.END)
    check_cpu = cpu_var.get()
    check_gpu = gpu_var.get()
    check_net = net_var.get()
    suite = HardwareCompatibilityTestSuite()
    suite.detect_hardware(check_cpu, check_gpu, check_net)

    def update_progress(done, total):
        percent = (done / total) * 100
        progress_var.set(percent)
        root.update_idletasks()

    suite.run_tests(check_cpu, check_gpu, check_net, progress_callback=update_progress)
    output = suite.get_report()
    output_box.insert(tk.END, output)
    progress_var.set(100)
    root.suite = suite

def save_txt():
    try:
        root.suite.save_report_txt()
        messagebox.showinfo("Saved", "Report saved to report.txt")
    except:
        messagebox.showerror("Error", "Run the test first")

def save_json():
    try:
        root.suite.save_report_json()
        messagebox.showinfo("Saved", "Report saved to report.json")
    except:
        messagebox.showerror("Error", "Run the test first")

def save_pdf():
    try:
        root.suite.save_report_pdf()
        messagebox.showinfo("Saved", "Report saved to report.pdf")
    except:
        messagebox.showerror("Error", "Run the test first")

def refresh_stats():
    stats_box.delete(1.0, tk.END)
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    uptime_sec = time.time() - psutil.boot_time()
    uptime = str(timedelta(seconds=int(uptime_sec)))
    stats = f"""
--- System Stats ---
OS: {platform.system()} {platform.release()}
CPU Usage: {cpu_percent}%
RAM Usage: {mem.percent}% ({round(mem.used / (1024**3), 2)} GB used of {round(mem.total / (1024**3), 2)} GB)
Disk Usage: {disk.percent}% ({round(disk.used / (1024**3), 2)} GB used of {round(disk.total / (1024**3), 2)} GB)
Uptime: {uptime}
"""
    stats_box.insert(tk.END, stats)

root.mainloop()
