import tkinter as tk
from tkinter import ttk, font
import time
import random

class HeroTributeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("王贺祥天下无敌致敬程序")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a2e")
        
        # 创建主框架
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建标题
        title_label = ttk.Label(
            self.main_frame, 
            text="王贺祥天下无敌 - 特别致敬程序", 
            font=("Microsoft YaHei", 24, "bold"),
            foreground="#ffcc00",
            background="#1a1a2e"
        )
        title_label.pack(pady=(0, 20))
        
        # 创建分隔线
        separator = ttk.Separator(self.main_frame, orient="horizontal")
        separator.pack(fill=tk.X, pady=10)
        
        # 创建艺术字标签
        self.art_label = ttk.Label(
            self.main_frame, 
            text="", 
            font=("Courier New", 16, "bold"),
            foreground="#00ccff",
            background="#1a1a2e"
        )
        self.art_label.pack(pady=10)
        
        # 创建逐字打印标签
        self.typewriter_label = ttk.Label(
            self.main_frame, 
            text="", 
            font=("Microsoft YaHei", 28, "bold"),
            foreground="#ffffff",
            background="#1a1a2e"
        )
        self.typewriter_label.pack(pady=20)
        
        # 创建彩色文本标签
        self.color_text_frame = ttk.Frame(self.main_frame)
        self.color_text_frame.pack(pady=15)
        
        # 创建边框效果标签
        self.border_frame = ttk.Frame(self.main_frame, relief="solid", borderwidth=3)
        self.border_label = ttk.Label(
            self.border_frame, 
            text="王贺祥天下无敌", 
            font=("Microsoft YaHei", 24, "bold"),
            foreground="#ff3366",
            padding=20
        )
        self.border_label.pack()
        self.border_frame.pack(pady=20)
        
        # 创建附加致敬标签
        poem_frame = ttk.Frame(self.main_frame)
        poem_frame.pack(pady=20)
        
        poem_text = [
            "王者风范显神威",
            "贺喜声中赞英雄",
            "祥瑞之光耀八方",
            "天地为之动容色",
            "下凡英雄独此尊",
            "无敌传说永流传"
        ]
        
        for i, line in enumerate(poem_text):
            label = ttk.Label(
                poem_frame, 
                text=line, 
                font=("KaiTi", 14),
                foreground=["#ff9999", "#99ff99", "#9999ff", "#ffff99", "#ff99ff", "#99ffff"][i]
            )
            label.grid(row=i, column=0, sticky="w", pady=2)
        
        # 创建控制按钮
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        self.start_button = ttk.Button(
            button_frame, 
            text="开始致敬", 
            command=self.start_tribute,
            style="Accent.TButton"
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.reset_button = ttk.Button(
            button_frame, 
            text="重置", 
            command=self.reset,
            style="TButton"
        )
        self.reset_button.pack(side=tk.LEFT, padx=10)
        
        # 设置样式
        self.setup_styles()
        
        # 预加载艺术字
        self.art_text = r"""
        ┌─┐┬  ┬┌─┐┬─┐┬┌─┐┌┬┐
        ├─┤└┐┌┘├┤ ├┬┘│├─┘ │ 
        ┴ ┴ └┘ └─┘┴└─┴┴   ┴ 
        """
    
    def setup_styles(self):
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Microsoft YaHei", 12), foreground="white", background="#4CAF50")
        style.map("Accent.TButton", background=[("active", "#45a049")])
        style.configure("TButton", font=("Microsoft YaHei", 12))
        
        style.configure("TFrame", background="#1a1a2e")
        style.configure("TLabel", background="#1a1a2e")
    
    def start_tribute(self):
        self.start_button.config(state=tk.DISABLED)
        self.show_art()
    
    def reset(self):
        self.art_label.config(text="")
        self.typewriter_label.config(text="")
        self.clear_color_text()
        self.start_button.config(state=tk.NORMAL)
        self.border_frame.config(relief="solid")  # 重置边框样式
    
    def show_art(self):
        # 显示艺术字
        self.art_label.config(text=self.art_text)
        self.root.after(1500, self.typewriter_effect)
    
    def typewriter_effect(self):
        text = "王贺祥天下无敌"
        full_text = ""
        
        def add_char(i=0):
            nonlocal full_text
            if i < len(text):
                full_text += text[i]
                self.typewriter_label.config(text=full_text)
                self.root.after(200, add_char, i+1)
            else:
                self.root.after(500, self.show_color_text)
        
        add_char()
    
    def clear_color_text(self):
        # 清除彩色文本
        for widget in self.color_text_frame.winfo_children():
            widget.destroy()
    
    def show_color_text(self):
        text = "王贺祥天下无敌"
        colors = ['#ff3333', '#ff9933', '#ffff33', '#33ff33', '#33ffff', '#3399ff', '#9933ff']
        
        self.clear_color_text()
        
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            char_label = ttk.Label(
                self.color_text_frame, 
                text=char, 
                font=("Microsoft YaHei", 32, "bold"),
                foreground=color,
                background="#1a1a2e"
            )
            char_label.pack(side=tk.LEFT, padx=5)
        
        # 添加动画效果
        self.animate_border()
    
    def animate_border(self):
        # 边框动画效果
        border_styles = ["raised", "sunken", "ridge", "groove", "solid"]
        colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff"]
        
        def animate(i=0):
            if i < 15:  # 动画持续15步
                style = border_styles[i % len(border_styles)]
                color = colors[i % len(colors)]
                self.border_frame.config(relief=style)
                self.border_label.config(foreground=color)
                self.root.after(150, animate, i+1)
        
        animate()

if __name__ == "__main__":
    root = tk.Tk()
    app = HeroTributeApp(root)
    root.mainloop()