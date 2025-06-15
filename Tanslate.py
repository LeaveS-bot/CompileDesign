import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from collections import deque

class NFAtoDFAConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("NFA to DFA Converter")
        self.root.geometry("800x600")
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
    
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        header = ttk.Label(main_frame, text="NFA to DFA Converter", style="Header.TLabel")
        header.pack(pady=(0, 20))
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="File Selection")
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 输入文件选择
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Input File (NFA):").pack(side=tk.LEFT, padx=(0, 10))
        self.input_entry = ttk.Entry(input_frame, width=50)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="Browse...", command=self.browse_input_file).pack(side=tk.LEFT)
        
        # 输出文件选择
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(output_frame, text="Output File (DFA):").pack(side=tk.LEFT, padx=(0, 10))
        self.output_entry = ttk.Entry(output_frame, width=50)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="Browse...", command=self.browse_output_file).pack(side=tk.LEFT)
        
        # 转换按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        ttk.Button(button_frame, text="Convert NFA to DFA", command=self.convert, style="TButton").pack(pady=10)
        
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
                # 处理空字符串转移（与ε相同）
                if '' in nfa_transitions[state]:
                    for next_state in nfa_transitions[state]['']:
                        if next_state not in closure:
                            closure.add(next_state)
                            stack.append(next_state)
        return closure
    
    def Ia(self, states, symbol, nfa_transitions):
        """Compute transition set for given states and symbol"""
        result = set()
        for state in states:
            # 检查当前状态是否有该符号的转移
            if state in nfa_transitions:
                if symbol in nfa_transitions[state]:
                    result |= set(nfa_transitions[state][symbol])
        return result
    
    def read_nfa_file(self, file_path):
        """Read NFA definition from text file"""
        nfa_info = {
            'states': [],
            'alphabet': [],
            'start': [],
            'accept': [],
            'transitions': {}
        }
        
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # 移除注释和空行
        lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
        
        # 解析每个部分
        section = None
        for line in lines:
            line_lower = line.lower()
            if line_lower.startswith('states:'):
                section = 'states'
                nfa_info['states'] = line.split(':')[1].strip().split()
            elif line_lower.startswith('alphabet:'):
                section = 'alphabet'
                nfa_info['alphabet'] = line.split(':')[1].strip().split()
            elif line_lower.startswith('start state:'):
                section = 'start'
                nfa_info['start'] = line.split(':')[1].strip().split()
            elif line_lower.startswith('accept states:'):
                section = 'accept'
                nfa_info['accept'] = line.split(':')[1].strip().split()
            elif line_lower.startswith('transitions:'):
                section = 'transitions'
            elif section == 'transitions' and line:
                # 支持多种分隔符：空格、逗号、冒号
                if ' ' in line:
                    parts = line.split()
                elif ',' in line:
                    parts = line.split(',')
                elif ':' in line:
                    parts = line.split(':')
                else:
                    continue
                
                # 确保有足够的部分
                if len(parts) < 3:
                    continue
                
                from_state = parts[0].strip()
                symbol = parts[1].strip()
                to_states = [s.strip() for s in parts[2:]]
                
                # 处理空字符串转移
                if symbol == "epsilon" or symbol == "ε" or symbol == "''":
                    symbol = 'ε'
                
                # 初始化转移字典
                if from_state not in nfa_info['transitions']:
                    nfa_info['transitions'][from_state] = {}
                if symbol not in nfa_info['transitions'][from_state]:
                    nfa_info['transitions'][from_state][symbol] = []
                
                nfa_info['transitions'][from_state][symbol].extend(to_states)
        
        return nfa_info
    
    def write_dfa_file(self, dfa_info, file_path):
        """Write DFA definition to text file"""
        with open(file_path, 'w') as f:
            f.write("# DFA generated from NFA conversion\n\n")
            
            # States
            f.write(f"States: {' '.join(str(s) for s in dfa_info['states'])}\n")
            
            # Alphabet
            f.write(f"Alphabet: {' '.join(dfa_info['alphabet'])}\n")
            
            # Start state
            f.write(f"Start state: {dfa_info['start']}\n")
            
            # Accept states
            if dfa_info['accept']:
                f.write(f"Accept states: {' '.join(str(s) for s in dfa_info['accept'])}\n")
            else:
                f.write("Accept states: \n")
            
            # Transitions
            f.write("\nTransitions:\n")
            for (from_state, symbol), to_state in dfa_info['transitions'].items():
                f.write(f"{from_state} {symbol} {to_state}\n")
    
    def nfa_to_dfa(self, nfa_info):
        """Convert NFA to DFA using subset construction"""
        # 过滤出字母表（排除ε）
        alphabet = [char for char in nfa_info['alphabet'] if char != 'ε' and char != '']
        nfa_transitions = nfa_info['transitions']
        
        # 计算初始状态的ε闭包
        start_closure = self.epsilon_closure(nfa_info['start'], nfa_transitions)
        
        # 初始化DFA
        dfa_states = [frozenset(start_closure)]  # DFA状态集合
        dfa_transitions = {}                    # DFA转移函数
        state_queue = deque([frozenset(start_closure)])
        state_index_map = {frozenset(start_closure): 0}  # 状态集合到索引的映射
        next_index = 1
        
        # 记录转换过程
        process_log = []
        process_log.append(f"Initial state: ε-CLOSURE({nfa_info['start']}) = {set(start_closure)}")
        
        while state_queue:
            current_states = state_queue.popleft()
            current_idx = state_index_map[current_states]
            
            for char in alphabet:
                # 计算直接转移
                move_set = self.Ia(current_states, char, nfa_transitions)
                
                # 计算ε闭包
                if move_set:
                    new_state_set = frozenset(self.epsilon_closure(move_set, nfa_transitions))
                else:
                    new_state_set = frozenset()
                
                if not new_state_set:  # 跳过空集
                    continue
                
                # 如果是新状态，添加到DFA
                if new_state_set not in state_index_map:
                    state_index_map[new_state_set] = next_index
                    dfa_states.append(new_state_set)
                    state_queue.append(new_state_set)
                    process_log.append(f"New state discovered: S{next_index} = {set(new_state_set)}")
                    next_index += 1
                
                # 记录转移
                from_idx = state_index_map[current_states]
                to_idx = state_index_map[new_state_set]
                dfa_transitions[(from_idx, char)] = to_idx
                
                process_log.append(f"State S{from_idx} on input '{char}' -> S{to_idx}")
        
        # 确定接受状态（包含NFA任意接受状态的状态）
        accept_states = set()
        for idx, state_set in enumerate(dfa_states):
            if state_set & set(nfa_info['accept']):
                accept_states.add(idx)
        
        # 生成状态报告
        state_report = []
        state_report.append(f"DFA States: {len(dfa_states)}")
        state_report.append(f"Start state: S0")
        if accept_states:
            state_report.append(f"Accept states: {', '.join(f'S{i}' for i in sorted(accept_states))}")
        else:
            state_report.append("Accept states: None")
        state_report.append("\nTransition Table:")
        
        # 添加表头
        header = ["State"] + alphabet
        state_report.append(" | ".join(header))
        state_report.append("-" * (len(header) * 8))
        
        # 添加每个状态的转移
        for idx, state_set in enumerate(dfa_states):
            row = [f"S{idx}"]
            for char in alphabet:
                key = (idx, char)
                if key in dfa_transitions:
                    row.append(f"S{dfa_transitions[key]}")
                else:
                    row.append("--")
            state_report.append(" | ".join(row))
        
        return {
            'states': list(range(len(dfa_states))),
            'alphabet': alphabet,
            'start': 0,
            'accept': sorted(accept_states),
            'transitions': dfa_transitions,
            'process_log': process_log,
            'state_report': state_report
        }
    
    def convert(self):
        if not self.input_file or not os.path.exists(self.input_file):
            messagebox.showerror("Error", "Please select a valid input file")
            return
        
        if not self.output_file:
            messagebox.showerror("Error", "Please select an output file")
            return
        
        try:
            # 读取NFA定义
            self.log(f"Reading NFA file: {self.input_file}")
            nfa_info = self.read_nfa_file(self.input_file)
            
            self.log(f"NFA states: {' '.join(nfa_info['states'])}")
            self.log(f"Alphabet: {' '.join(nfa_info['alphabet'])}")
            self.log(f"Start state: {' '.join(nfa_info['start'])}")
            self.log(f"Accept states: {' '.join(nfa_info['accept'])}")
            
            # 显示NFA转移
            self.log("\nNFA Transitions:")
            for from_state, transitions in nfa_info['transitions'].items():
                for symbol, to_states in transitions.items():
                    self.log(f"  {from_state} --[{symbol}]--> {', '.join(to_states)}")
            
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
            self.log(f"Error: {str(e)}")
            self.log(traceback.format_exc())
            messagebox.showerror("Conversion Error", f"An error occurred during conversion:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NFAtoDFAConverter(root)
    root.mainloop()