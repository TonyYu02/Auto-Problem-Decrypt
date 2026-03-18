import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import sys
import os

class ServerManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server 控制面板")
        self.root.geometry("600x400")
        
        self.process = None
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.run_btn = tk.Button(btn_frame, text="运行 (Run)", command=self.start_server, 
                                 width=15, bg=None, fg="black", font=("微软雅黑", 15, "bold"))
        self.run_btn.pack(side=tk.LEFT, padx=20)
        self.stop_btn = tk.Button(btn_frame, text="关闭 (Stop)", command=self.stop_server, 
                                  width=15, bg=None, fg="black", font=("微软雅黑", 15, "bold"), state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=20)

        self.terminal = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="black", fg="#00FF00", font=("Consolas", 10))
        self.terminal.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def log(self, message):
        self.terminal.insert(tk.END, message + "\n")
        self.terminal.see(tk.END)

    def start_server(self):
        if self.process is None or self.process.poll() is not None:
            self.terminal.delete(1.0, tk.END)
            self.log(">>> 正在启动 server.py...")
            
            try:
                self.process = subprocess.Popen(
                    ["python", "server.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                self.run_btn.config(state=tk.DISABLED)
                self.stop_btn.config(state=tk.NORMAL)

                threading.Thread(target=self.read_output, daemon=True).start()
                
            except Exception as e:
                self.log(f"[错误] 启动失败: {e}")

    def stop_server(self):
        if self.process and self.process.poll() is None:
            self.log(">>> 正在发送终止信号 (Ctrl+C)...")
            self.process.terminate() 
            self.process = None
            self.run_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.log(">>> server.py 已关闭。")

    def read_output(self):
        if self.process:
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.root.after(0, self.log, line.strip())
            
            if self.process:
                self.process.stdout.close()
            
            self.root.after(0, self.reset_buttons)

    def reset_buttons(self):
        self.run_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        if self.process and self.process.poll() is not None:
            self.log(f">>> server.py 已退出，返回码: {self.process.poll()}")
            self.process = None

    def on_closing(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerManagerApp(root)
    root.mainloop()