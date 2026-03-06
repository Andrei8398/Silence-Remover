import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import threading
import os

class SilenceRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spartacus Silence Remover")
        self.root.geometry("550x550")

        frame_in = ttk.LabelFrame(root, text="1. Select Input Audio File", padding="10")
        frame_in.pack(fill=tk.X, padx=10, pady=5)
        
        self.input_var = tk.StringVar()
        ttk.Entry(frame_in, textvariable=self.input_var, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(frame_in, text="📂 Browse File", command=self.browse_input).pack(side=tk.RIGHT)

        frame_out = ttk.LabelFrame(root, text="2. Select Destination", padding="10")
        frame_out.pack(fill=tk.X, padx=10, pady=5)
        
        self.output_var = tk.StringVar()
        ttk.Entry(frame_out, textvariable=self.output_var, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(frame_out, text="💾 Save As...", command=self.browse_output).pack(side=tk.RIGHT)

        frame_opts = ttk.LabelFrame(root, text="3. Trim Options", padding="10")
        frame_opts.pack(fill=tk.X, padx=10, pady=5)

        self.trim_start_var = tk.BooleanVar(value=True)
        self.chk_start = ttk.Checkbutton(frame_opts, text="✂️ Remove silence from the BEGINNING", variable=self.trim_start_var)
        self.chk_start.pack(anchor=tk.W, pady=5)

        self.trim_end_var = tk.BooleanVar(value=True)
        self.chk_end = ttk.Checkbutton(frame_opts, text="✂️ Remove silence from the END", variable=self.trim_end_var)
        self.chk_end.pack(anchor=tk.W, pady=5)

        self.btn_convert = ttk.Button(root, text="⚡ CLEAN AUDIO", command=self.start_processing)
        self.btn_convert.pack(pady=15, ipadx=10, ipady=10)

        self.log_area = scrolledtext.ScrolledText(root, width=50, height=10, state='disabled', font=("Consolas", 9), background="black", foreground="lightgreen")
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def browse_input(self):
        filename = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio files", "*.wav *.mp3 *.flac *.ogg *.m4a *.wma"), ("All files", "*.*")])
        if filename:
            self.input_var.set(filename)
            base, ext = os.path.splitext(filename)
            self.output_var.set(f"{base}_cleaned{ext}")

    def browse_output(self):
        infile = self.input_var.get()
        if not infile:
            messagebox.showwarning("Warning", "Please select an Input file first so I know what extension to use!")
            return
            
        _, ext = os.path.splitext(infile)
        filename = filedialog.asksaveasfilename(title="Save As", defaultextension=ext, filetypes=[("Audio File", f"*{ext}"), ("All Files", "*.*")])
        if filename:
            self.output_var.set(filename)

    def log(self, message):
        self.root.after(0, self._append_log, message)

    def _append_log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def start_processing(self):
        infile = self.input_var.get()
        outfile = self.output_var.get()
        trim_start = self.trim_start_var.get()
        trim_end = self.trim_end_var.get()
        
        if not infile or not outfile:
            messagebox.showerror("Error", "Please select both Input and Output files!")
            return

        if not trim_start and not trim_end:
            messagebox.showerror("Error", "You must select at least one trimming option (Beginning or End)!")
            return

        if not os.path.exists("ffmpeg.exe"):
            messagebox.showerror("Critical Error", "I cannot find 'ffmpeg.exe'! Please put it in the same folder as this app.")
            return

        self.btn_convert.config(state='disabled')
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')
        
        threading.Thread(target=self.run_ffmpeg, args=(infile, outfile, trim_start, trim_end), daemon=True).start()

    def run_ffmpeg(self, infile, outfile, trim_start, trim_end):
        try:
            self.log("[*] Analyzing audio and preparing filters...")
            
            cmd = ["ffmpeg.exe", "-y", "-i", infile]
            filters = []
            
            if trim_start:
                filters.append("silenceremove=start_periods=1:start_threshold=-50dB")
            
            if trim_end:
                filters.append("areverse")
                filters.append("silenceremove=start_periods=1:start_threshold=-50dB")
                filters.append("areverse")
            
            if filters:
                cmd.extend(["-af", ",".join(filters)])
            
            cmd.extend(["-b:a", "320k"])
            cmd.append(outfile)
            
            self.log(f"[*] Executing FFmpeg magic...\n")
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            for line in iter(process.stdout.readline, ''):
                clean_line = line.strip()
                if "size=" in clean_line or "time=" in clean_line:
                    self.log(clean_line)

            process.wait()

            if process.returncode == 0:
                self.log("\n[+] MISSION ACCOMPLISHED! Silence has been banished.")
                self.root.after(0, lambda: messagebox.showinfo("Success", "Audio cleaned successfully!"))
            else:
                self.log("\n[-] MISSION FAILED. FFmpeg encountered an error.")

        except Exception as e:
            self.log(f"\n[-] ERROR:\n{e}")
        finally:
            self.root.after(0, lambda: self.btn_convert.config(state='normal'))

if __name__ == "__main__":
    root = tk.Tk()
    app = SilenceRemoverApp(root)
    root.mainloop()
