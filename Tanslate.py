import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from collections import deque

class NFAtoDFAConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("NFA to DFA Converter & Minimizer")
        self.root.geometry("900x700")  # 增加高度以容纳新控件
        self.root.resizable(True, True)
        
        # 设置中文字体支持
        self.font_normal = font.Font(family="Microsoft YaHei", size=10)
        self.font_bold = font.Font(family="Microsoft YaHei", size=14, weight="bold")
        
        # 设置主题
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=self.font_normal)
        self.style.configure("TButton", font=self.font_normal, padding=6)
        self.style.configure("Header.TLabel", font=self.font_bold, foreground="#2c3e50")
        self.style.configure("TEntry", font=self.font_normal)
        self.style.configure("TText", font=("Consolas", 10))
        
        self.create_widgets()
        self.input_file = ""
        self.output_file = ""
        self.min_input_file = ""
        self.min_output_file = ""
    
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        header = ttk.Label(main_frame, text="NFA to DFA Converter & Minimizer", style="Header.TLabel")
        header.pack(pady=(0, 20))
        
        # 文件选择区域 - NFA转DFA
        nfa_frame = ttk.LabelFrame(main_frame, text="NFA to DFA Conversion")
        nfa_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 输入文件选择
        input_frame = ttk.Frame(nfa_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Input File (NFA):").pack(side=tk.LEFT, padx=(0, 10))
        self.input_entry = ttk.Entry(input_frame, width=50)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="Browse...", command=self.browse_input_file).pack(side=tk.LEFT)
        
        # 输出文件选择
        output_frame = ttk.Frame(nfa_frame)
        output_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(output_frame, text="Output File (DFA):").pack(side=tk.LEFT, padx=(0, 10))
        self.output_entry = ttk.Entry(output_frame, width=50)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="Browse...", command=self.browse_output_file).pack(side=tk.LEFT)
        
        # 文件选择区域 - DFA最小化
        min_frame = ttk.LabelFrame(main_frame, text="DFA Minimization")
        min_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 最小化输入文件选择
        min_input_frame = ttk.Frame(min_frame)
        min_input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(min_input_frame, text="Input File (DFA):").pack(side=tk.LEFT, padx=(0, 10))
        self.min_input_entry = ttk.Entry(min_input_frame, width=50)
        self.min_input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(min_input_frame, text="Browse...", command=self.browse_min_input_file).pack(side=tk.LEFT)
        
        # 最小化输出文件选择
        min_output_frame = ttk.Frame(min_frame)
        min_output_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(min_output_frame, text="Output File (Minimized DFA):").pack(side=tk.LEFT, padx=(0, 10))
        self.min_output_entry = ttk.Entry(min_output_frame, width=50)
        self.min_output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(min_output_frame, text="Browse...", command=self.browse_min_output_file).pack(side=tk.LEFT)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        ttk.Button(button_frame, text="Convert NFA to DFA", command=self.convert, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Minimize DFA", command=self.minimize_dfa, style="TButton").pack(side=tk.LEFT, padx=5)
        
        # 状态显示区域
        status_frame = ttk.LabelFrame(main_frame, text="Conversion Status")
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.status_text = tk.Text(status_frame, height=10, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.status_text.config(state=tk.DISABLED)
        self.status_text.config(font=("Consolas", 10))
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
        
        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="Conversion Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_text.config(state=tk.DISABLED)
        self.log_text.config(font=("Consolas", 9))
        
        # 添加滚动条
        scrollbar_log = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar_log.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar_log.set)
        
        # 状态栏
        self.status_bar = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Select NFA Input File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.input_file = file_path
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
            self.log(f"Selected input file: {file_path}")
    
    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Save DFA Output File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            defaultextension=".txt"
        )
        if file_path:
            self.output_file = file_path
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)
            self.log(f"Selected output file: {file_path}")
    
    def browse_min_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Select DFA Input File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.min_input_file = file_path
            self.min_input_entry.delete(0, tk.END)
            self.min_input_entry.insert(0, file_path)
            self.log(f"Selected minimization input file: {file_path}")
    
    def browse_min_output_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Minimized DFA Output File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            defaultextension=".txt"
        )
        if file_path:
            self.min_output_file = file_path
            self.min_output_entry.delete(0, tk.END)
            self.min_output_entry.insert(0, file_path)
            self.log(f"Selected minimization output file: {file_path}")
    
    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.status_bar.config(text=message)
    
    def update_status(self, text):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, text)
        self.status_text.config(state=tk.DISABLED)
    
    def epsilon_closure(self, states, nfa_transitions):
        """Compute epsilon closure for a set of states"""
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            # 检查ε转移
            if state in nfa_transitions:
                # 处理ε转移
                if 'ε' in nfa_transitions[state]:
                    for next_state in nfa_transitions[state]['ε']:
                        if next_state not in closure:
                            closure.add(next_state)
                            stack.append(next_state)
        return closure
    
    def move(self, states, symbol, nfa_transitions):
        """Compute move set for given states and symbol"""
        result = set()
        for state in states:
            # 检查当前状态是否有该符号的转移
            if state in nfa_transitions:
                if symbol in nfa_transitions[state]:
                    result |= set(nfa_transitions[state][symbol])
        return result
    
    def read_nfa_file(self, file_path):
        """Read NFA definition from text file in transition matrix format"""
        nfa_info = {
            'states': [],
            'alphabet': [],
            'start': '',
            'accept': [],
            'transitions': {}
        }
        
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # 移除注释和空行
            lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
            
            if not lines:
                raise ValueError("Empty file")
            
            # 解析状态行
            if not lines[0].startswith("States:"):
                raise ValueError("First line should be States: ...")
            nfa_info['states'] = lines[0].split(':', 1)[1].strip().split()
            
            # 解析字母表行
            if not lines[1].startswith("Alphabet:"):
                raise ValueError("Second line should be Alphabet: ...")
            nfa_info['alphabet'] = lines[1].split(':', 1)[1].strip().split()
            
            # 解析开始状态行
            if not lines[2].startswith("Start state:"):
                raise ValueError("Third line should be Start state: ...")
            nfa_info['start'] = lines[2].split(':', 1)[1].strip()
            
            # 解析接受状态行
            if not lines[3].startswith("Accept states:"):
                raise ValueError("Fourth line should be Accept states: ...")
            nfa_info['accept'] = lines[3].split(':', 1)[1].strip().split()
            
            # 解析转移矩阵
            if not lines[4].startswith("Transitions:"):
                raise ValueError("Fifth line should be Transitions: ...")
            
            # 矩阵头部 - 符号列表
            header = lines[5].split()
            if header[0] != "State":
                raise ValueError("Transition matrix header should start with 'State'")
            
            # 矩阵数据
            for i in range(6, len(lines)):
                parts = lines[i].split()
                if len(parts) != len(header):
                    raise ValueError(f"Invalid transition matrix row: {lines[i]}")
                
                state = parts[0]
                nfa_info['transitions'][state] = {}
                
                for j in range(1, len(parts)):
                    symbol = header[j]
                    if symbol == 'ε':
                        symbol = 'ε'
                    
                    # 解析目标状态
                    targets = parts[j].split(',') if parts[j] != '-' else []
                    
                    if targets:
                        nfa_info['transitions'][state][symbol] = targets
            
            # 验证NFA信息
            if not nfa_info['states']:
                raise ValueError("No states defined in NFA file")
            if not nfa_info['alphabet']:
                raise ValueError("No alphabet defined in NFA file")
            if not nfa_info['start']:
                raise ValueError("No start state defined in NFA file")
            if not nfa_info['accept']:
                self.log("Warning: No accept states defined in NFA file")
        
        except Exception as e:
            raise ValueError(f"Error parsing NFA file: {str(e)}") from e
        
        return nfa_info
    
    def read_dfa_file(self, file_path):
        """Read DFA definition from text file in transition matrix format"""
        dfa_info = {
            'states': [],
            'alphabet': [],
            'start': '',
            'accept': [],
            'transitions': {}
        }
        
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # 移除注释和空行
            lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
            
            if not lines:
                raise ValueError("Empty file")
            
            # 解析状态行
            if not lines[0].startswith("States:"):
                raise ValueError("First line should be States: ...")
            dfa_info['states'] = lines[0].split(':', 1)[1].strip().split()
            
            # 解析字母表行
            if not lines[1].startswith("Alphabet:"):
                raise ValueError("Second line should be Alphabet: ...")
            dfa_info['alphabet'] = lines[1].split(':', 1)[1].strip().split()
            
            # 解析开始状态行
            if not lines[2].startswith("Start state:"):
                raise ValueError("Third line should be Start state: ...")
            dfa_info['start'] = lines[2].split(':', 1)[1].strip()
            
            # 解析接受状态行
            if not lines[3].startswith("Accept states:"):
                raise ValueError("Fourth line should be Accept states: ...")
            dfa_info['accept'] = lines[3].split(':', 1)[1].strip().split()
            
            # 解析转移矩阵
            if not lines[4].startswith("Transitions:"):
                raise ValueError("Fifth line should be Transitions: ...")
            
            # 矩阵头部 - 符号列表
            header = lines[5].split()
            if header[0] != "State":
                raise ValueError("Transition matrix header should start with 'State'")
            
            # 符号列表（不包括"State"）
            symbols = header[1:]
            
            # 矩阵数据
            for i in range(6, len(lines)):
                parts = lines[i].split()
                if len(parts) != len(header):
                    raise ValueError(f"Invalid transition matrix row: {lines[i]}")
                
                state = parts[0]
                
                for j, symbol in enumerate(symbols):
                    target = parts[j+1]
                    if target != '-':
                        dfa_info['transitions'][(state, symbol)] = target
            
            # 验证DFA信息
            if not dfa_info['states']:
                raise ValueError("No states defined in DFA file")
            if not dfa_info['alphabet']:
                raise ValueError("No alphabet defined in DFA file")
            if not dfa_info['start']:
                raise ValueError("No start state defined in DFA file")
            if not dfa_info['accept']:
                self.log("Warning: No accept states defined in DFA file")
        
        except Exception as e:
            raise ValueError(f"Error parsing DFA file: {str(e)}") from e
        
        return dfa_info
    
    def write_dfa_file(self, dfa_info, file_path, minimized=False):
        """Write DFA definition to text file in transition matrix format"""
        try:
            with open(file_path, 'w') as f:
                prefix = "# Minimized DFA\n\n" if minimized else "# DFA generated from NFA conversion\n\n"
                f.write(prefix)
                
                # States
                f.write(f"States: {' '.join(dfa_info['states'])}\n")
                
                # Alphabet
                f.write(f"Alphabet: {' '.join(dfa_info['alphabet'])}\n")
                
                # Start state
                f.write(f"Start state: {dfa_info['start']}\n")
                
                # Accept states
                f.write(f"Accept states: {' '.join(dfa_info['accept'])}\n\n")
                
                # Transition matrix
                f.write("Transitions:\n")
                
                # Matrix header
                header = ["State"] + dfa_info['alphabet']
                f.write(f"{' '.join(header)}\n")
                
                # Matrix rows
                for state in dfa_info['states']:
                    row = [state]
                    
                    for symbol in dfa_info['alphabet']:
                        key = (state, symbol)
                        if key in dfa_info['transitions']:
                            target = dfa_info['transitions'][key]
                            row.append(target)
                        else:
                            row.append("-")
                    
                    f.write(f"{' '.join(row)}\n")
        except Exception as e:
            raise IOError(f"Error writing DFA file: {str(e)}") from e
    
    def nfa_to_dfa(self, nfa_info):
        """Convert NFA to DFA using subset construction"""
        # 过滤出字母表（排除ε）
        alphabet = [char for char in nfa_info['alphabet'] if char != 'ε']
        nfa_transitions = nfa_info['transitions']
        
        # 计算初始状态的ε闭包
        start_closure = self.epsilon_closure([nfa_info['start']], nfa_transitions)
        
        # 初始化DFA
        dfa_states = []                     # DFA状态集合
        dfa_transitions = {}                 # DFA转移函数
        state_queue = deque()                # 待处理状态队列
        state_index_map = {}                 # 状态集合到索引的映射
        
        # 添加初始状态
        dfa_states.append(frozenset(start_closure))
        state_index_map[frozenset(start_closure)] = 0
        state_queue.append(frozenset(start_closure))
        next_index = 1
        
        # 记录转换过程
        process_log = []
        process_log.append(f"Initial state: ε-CLOSURE({nfa_info['start']}) = {set(start_closure)} -> S0")
        
        while state_queue:
            current_states = state_queue.popleft()
            current_idx = state_index_map[current_states]
            
            for char in alphabet:
                # 计算移动集合
                move_set = self.move(current_states, char, nfa_transitions)
                
                # 计算ε闭包
                if move_set:
                    new_state_set = frozenset(self.epsilon_closure(move_set, nfa_transitions))
                else:
                    new_state_set = frozenset()
                
                # 如果新状态不为空
                if new_state_set:
                    # 如果是新状态，添加到DFA
                    if new_state_set not in state_index_map:
                        state_index_map[new_state_set] = next_index
                        dfa_states.append(new_state_set)
                        state_queue.append(new_state_set)
                        process_log.append(f"New state discovered: S{next_index} = {set(new_state_set)}")
                        next_index += 1
                    
                    # 记录转移
                    to_idx = state_index_map[new_state_set]
                    dfa_transitions[(current_idx, char)] = to_idx
                    process_log.append(f"State S{current_idx} on input '{char}' -> S{to_idx}")
                else:
                    process_log.append(f"State S{current_idx} on input '{char}' -> (dead state)")
        
        # 确定接受状态（包含NFA任意接受状态的状态）
        accept_states = set()
        for idx, state_set in enumerate(dfa_states):
            if any(state in nfa_info['accept'] for state in state_set):
                accept_states.add(idx)
        
        # 生成状态报告
        state_report = []
        state_report.append(f"Number of DFA States: {len(dfa_states)}")
        state_report.append(f"Start state: S0")
        if accept_states:
            state_report.append(f"Accept states: {', '.join(f'S{i}' for i in sorted(accept_states))}")
        else:
            state_report.append("Accept states: None")
        state_report.append("\nTransition Matrix:")
        
        # 添加表头
        header = ["State"] + alphabet
        state_report.append(" | ".join(header))
        state_report.append("-" * (len(header) * 8))
        
        # 添加每个状态的转移
        for idx in range(len(dfa_states)):
            row = [f"S{idx}"]
            for char in alphabet:
                key = (idx, char)
                if key in dfa_transitions:
                    row.append(f"S{dfa_transitions[key]}")
                else:
                    row.append("--")
            state_report.append(" | ".join(row))
        
        # 为写入文件准备DFA信息
        dfa_states_str = [f"S{i}" for i in range(len(dfa_states))]
        dfa_accept_str = [f"S{i}" for i in sorted(accept_states)]
        transitions_for_file = {}
        for (state_idx, symbol), target_idx in dfa_transitions.items():
            transitions_for_file[(f"S{state_idx}", symbol)] = f"S{target_idx}"
        
        return {
            'states': dfa_states_str,
            'alphabet': alphabet,
            'start': "S0",
            'accept': dfa_accept_str,
            'transitions': transitions_for_file,
            'process_log': process_log,
            'state_report': state_report
        }
    
    def minimize_dfa(self):
        """Minimize the DFA using Hopcroft's algorithm"""
        if not self.min_input_file or not os.path.exists(self.min_input_file):
            messagebox.showerror("Error", "Please select a valid DFA input file")
            return
        
        if not self.min_output_file:
            messagebox.showerror("Error", "Please select a minimized DFA output file")
            return
        
        try:
            # 重置日志和状态
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state=tk.DISABLED)
            self.update_status("")
            
            # 读取DFA定义
            self.log(f"Reading DFA file: {self.min_input_file}")
            dfa_info = self.read_dfa_file(self.min_input_file)
            
            self.log(f"DFA states: {' '.join(dfa_info['states'])}")
            self.log(f"Alphabet: {' '.join(dfa_info['alphabet'])}")
            self.log(f"Start state: {dfa_info['start']}")
            self.log(f"Accept states: {' '.join(dfa_info['accept'])}")
            
            # 显示DFA转移矩阵
            self.log("\nDFA Transition Matrix:")
            # 表头
            header = ["State"] + dfa_info['alphabet']
            self.log(" | ".join(header))
            self.log("-" * (len(header) * 8))
            
            # 矩阵内容
            for state in dfa_info['states']:
                row = [state]
                for symbol in dfa_info['alphabet']:
                    key = (state, symbol)
                    if key in dfa_info['transitions']:
                        row.append(dfa_info['transitions'][key])
                    else:
                        row.append('-')
                self.log(" | ".join(row))
            
            # 执行最小化
            self.log("\nStarting DFA minimization...")
            minimized_dfa = self.hopcroft_minimization(dfa_info)
            self.log("Minimization completed successfully!")
            
            # 显示最小化后的DFA
            self.log("\nMinimized DFA:")
            self.log(f"States: {' '.join(minimized_dfa['states'])}")
            self.log(f"Start state: {minimized_dfa['start']}")
            self.log(f"Accept states: {' '.join(minimized_dfa['accept'])}")
            
            # 显示转移矩阵
            self.log("\nMinimized Transition Matrix:")
            header = ["State"] + minimized_dfa['alphabet']
            self.log(" | ".join(header))
            self.log("-" * (len(header) * 8))
            
            for state in minimized_dfa['states']:
                row = [state]
                for symbol in minimized_dfa['alphabet']:
                    key = (state, symbol)
                    if key in minimized_dfa['transitions']:
                        row.append(minimized_dfa['transitions'][key])
                    else:
                        row.append('-')
                self.log(" | ".join(row))
            
            # 更新状态显示
            status_report = [
                f"Original DFA States: {len(dfa_info['states'])}",
                f"Minimized DFA States: {len(minimized_dfa['states'])}",
                f"Reduction: {len(dfa_info['states']) - len(minimized_dfa['states'])} states removed",
                "\nMinimized DFA:",
                f"States: {' '.join(minimized_dfa['states'])}",
                f"Alphabet: {' '.join(minimized_dfa['alphabet'])}",
                f"Start state: {minimized_dfa['start']}",
                f"Accept states: {' '.join(minimized_dfa['accept'])}",
                "\nTransition Matrix:"
            ]
            
            # 添加表头
            header = ["State"] + minimized_dfa['alphabet']
            status_report.append(" | ".join(header))
            status_report.append("-" * (len(header) * 8))
            
            # 添加每个状态的转移
            for state in minimized_dfa['states']:
                row = [state]
                for symbol in minimized_dfa['alphabet']:
                    key = (state, symbol)
                    if key in minimized_dfa['transitions']:
                        row.append(minimized_dfa['transitions'][key])
                    else:
                        row.append("--")
                status_report.append(" | ".join(row))
            
            self.update_status("\n".join(status_report))
            
            # 写入输出文件
            self.write_dfa_file(minimized_dfa, self.min_output_file, minimized=True)
            
            self.log(f"\nMinimized DFA saved to: {self.min_output_file}")
            messagebox.showinfo("Success", "DFA minimization completed and saved!")
        
        except Exception as e:
            import traceback
            error_msg = f"Error: {str(e)}"
            self.log(error_msg)
            self.log(traceback.format_exc())
            messagebox.showerror("Minimization Error", f"An error occurred during minimization:\n{error_msg}")
    
    def hopcroft_minimization(self, dfa):
        """Hopcroft's algorithm for DFA minimization"""
        # 步骤1：初始化分区（接受状态和非接受状态）
        accepting = set(dfa['accept'])
        non_accepting = set(dfa['states']) - accepting
        
        # 如果非接受状态为空，则只有接受状态
        partitions = []
        if non_accepting:
            partitions.append(non_accepting)
        if accepting:
            partitions.append(accepting)
        
        # 如果只有一个分区（所有状态都是接受状态或都不是），则无法进一步划分
        if len(partitions) == 1:
            # 所有状态等价
            return self.build_minimized_dfa(dfa, partitions)
        
        # 工作列表初始化
        worklist = deque()
        if len(accepting) <= len(non_accepting):
            worklist.append(accepting)
        else:
            worklist.append(non_accepting)
        
        # 分区映射：每个状态所属的分区
        partition_map = {}
        for state in dfa['states']:
            if state in accepting:
                partition_map[state] = accepting
            else:
                partition_map[state] = non_accepting
        
        # 步骤2：迭代划分
        while worklist:
            a = worklist.popleft()
            
            for symbol in dfa['alphabet']:
                # 查找所有进入A的转移
                x = set()
                for state in dfa['states']:
                    key = (state, symbol)
                    if key in dfa['transitions']:
                        target = dfa['transitions'][key]
                        if target in a:
                            x.add(state)
                
                # 对于每个分区Y，检查是否与X有交集
                new_partitions = []
                for y in partitions:
                    intersect = y & x
                    difference = y - x
                    
                    if intersect and difference:
                        # 将Y划分为两个新分区
                        new_partitions.append(intersect)
                        new_partitions.append(difference)
                        
                        # 更新工作列表
                        if y in worklist:
                            worklist.remove(y)
                            worklist.append(intersect)
                            worklist.append(difference)
                        else:
                            if len(intersect) <= len(difference):
                                worklist.append(intersect)
                            else:
                                worklist.append(difference)
                        
                        # 更新分区映射
                        for state in intersect:
                            partition_map[state] = intersect
                        for state in difference:
                            partition_map[state] = difference
                    else:
                        new_partitions.append(y)
                
                partitions = new_partitions
        
        # 步骤3：构建最小化DFA
        return self.build_minimized_dfa(dfa, partitions)
    
    def build_minimized_dfa(self, dfa, partitions):
        """Build minimized DFA from partitions"""
        # 创建新状态（等价类的代表）
        new_states = []
        partition_rep = {}  # 每个分区的代表状态
        state_to_new = {}   # 原始状态到新状态的映射
        
        for i, part in enumerate(partitions):
            # 选择分区中的第一个状态作为代表
            rep = sorted(part)[0]
            new_state = f"M{i}"
            new_states.append(new_state)
            partition_rep[new_state] = part
            
            # 映射原始状态到新状态
            for state in part:
                state_to_new[state] = new_state
        
        # 确定开始状态
        start_rep = state_to_new[dfa['start']]
        
        # 确定接受状态
        accept_set = set()
        for state in dfa['accept']:
            if state in state_to_new:
                accept_set.add(state_to_new[state])
        
        # 构建转移函数
        new_transitions = {}
        for new_state in new_states:
            # 获取原始代表状态
            orig_rep = next(iter(partition_rep[new_state]))
            
            for symbol in dfa['alphabet']:
                key = (orig_rep, symbol)
                if key in dfa['transitions']:
                    target = dfa['transitions'][key]
                    new_target = state_to_new[target]
                    new_transitions[(new_state, symbol)] = new_target
        
        return {
            'states': new_states,
            'alphabet': dfa['alphabet'],
            'start': start_rep,
            'accept': sorted(accept_set),
            'transitions': new_transitions
        }
    
    def convert(self):
        if not self.input_file or not os.path.exists(self.input_file):
            messagebox.showerror("Error", "Please select a valid input file")
            return
        
        if not self.output_file:
            messagebox.showerror("Error", "Please select an output file")
            return
        
        try:
            # 重置日志和状态
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state=tk.DISABLED)
            self.update_status("")
            
            # 读取NFA定义
            self.log(f"Reading NFA file: {self.input_file}")
            nfa_info = self.read_nfa_file(self.input_file)
            
            self.log(f"NFA states: {' '.join(nfa_info['states'])}")
            self.log(f"Alphabet: {' '.join(nfa_info['alphabet'])}")
            self.log(f"Start state: {nfa_info['start']}")
            self.log(f"Accept states: {' '.join(nfa_info['accept'])}")
            
            # 显示NFA转移矩阵
            self.log("\nNFA Transition Matrix:")
            # 表头
            header = ["State"] + nfa_info['alphabet']
            self.log(" | ".join(header))
            self.log("-" * (len(header) * 8))
            
            # 矩阵内容
            for state in nfa_info['states']:
                row = [state]
                for symbol in nfa_info['alphabet']:
                    if state in nfa_info['transitions'] and symbol in nfa_info['transitions'][state]:
                        row.append(','.join(nfa_info['transitions'][state][symbol]))
                    else:
                        row.append('-')
                self.log(" | ".join(row))
            
            # 执行转换
            self.log("\nStarting NFA to DFA conversion...")
            dfa_info = self.nfa_to_dfa(nfa_info)
            self.log("Conversion completed successfully!")
            
            # 显示转换日志
            self.log("\nConversion process:")
            for entry in dfa_info['process_log']:
                self.log(f"  {entry}")
            
            # 显示状态报告
            self.update_status("\n".join(dfa_info['state_report']))
            
            # 写入输出文件
            self.write_dfa_file(dfa_info, self.output_file)
            
            self.log(f"\nDFA saved to: {self.output_file}")
            messagebox.showinfo("Success", "NFA to DFA conversion completed and saved!")
        
        except Exception as e:
            import traceback
            error_msg = f"Error: {str(e)}"
            self.log(error_msg)
            self.log(traceback.format_exc())
            messagebox.showerror("Conversion Error", f"An error occurred during conversion:\n{error_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NFAtoDFAConverter(root)
    root.mainloop()