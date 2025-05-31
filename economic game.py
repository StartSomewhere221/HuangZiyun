import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import math

# 设置中文字体
try:
    plt.rcParams["font.family"] = ["SimSun", "DejaVu Sans"]
except:
    plt.rcParams["font.family"] = ["DejaVu Sans"]
plt.rcParams['axes.unicode_minus'] = False


class EconomicSimulationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("公共经济学模拟游戏")

        # 设置保守的窗口尺寸，确保在大多数屏幕上都能正常显示
        window_width = 1400
        window_height = 900

        # 先设置基本几何，然后获取屏幕信息
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.update_idletasks()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 如果窗口太大，调整为屏幕的85%
        if window_width > screen_width * 0.9:
            window_width = int(screen_width * 0.85)
        if window_height > screen_height * 0.9:
            window_height = int(screen_height * 0.85)

        # 设置安全的位置，确保窗口标题栏可见且能拖动
        x = max(10, min(100, (screen_width - window_width) // 4))
        y = max(10, min(50, (screen_height - window_height) // 4))

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(True, True)
        self.root.minsize(1200, 700)  # 设置最小尺寸

        # 新的配色方案
        self.colors = {
            'bg_primary': '#FBF6F0',  # 新的底色
            'bg_secondary': '#F7EFE8',  # 浅杏色背景
            'bg_accent': '#F2E3D4',  # 强调背景
            'text_primary': '#3E2723',  # 深棕色文字
            'text_secondary': '#5D4037',  # 中等棕色文字
            'accent': '#C35107',  # 橘色强调
            'accent_light': '#AF5E0C',  # 浅橘色
            'success': '#4CAF50',  # 成功绿
            'warning': '#FF9800',  # 警告橙
            'danger': '#F44336',  # 危险红
            'chart_colors': ['#FF8C42', '#FF6B35', '#F7931E', '#FFB366', '#E8751A', '#D2691E']
        }

        self.root.configure(bg=self.colors['bg_primary'])

        # 字体设置：统一为四号(14pt)，宋体
        self.fonts = {
            'title': ("SimSun", 25, "bold"),  # 四号字体，加粗
            'header': ("SimSun", 23, "bold"),  # 四号字体，加粗
            'normal': ("SimSun", 20),  # 四号字体，正常
            'small': ("SimSun", 20),  # 四号字体
            'tiny': ("SimSun", 20)  # 四号字体
        }

        # 游戏状态初始化
        self.turn = 1
        self.max_turns = 12
        self.budget = 100
        self.max_budget = 100

        # 经济指标初始化
        self.economic_data = {
            "GDP增长率": 2.5,
            "失业率": 6.0,
            "通胀率": 2.0,
            "财政赤字率": 3.0,
            "基尼系数": 0.45,
            "碳排放指数": 100.0,
            "社会福利指数": 65.0,
            "创新指数": 60.0,
            "教育水平": 70.0,
            "健康指数": 75.0
        }

        # 数据历史记录
        self.data_history = {key: [value] for key, value in self.economic_data.items()}
        self.budget_history = [self.budget]

        # 政策系统
        self.selected_policies = []
        self.policy_cooldowns = {}
        self.random_events = []

        # 目标系统
        self.objectives = {
            "📈 经济发展": {"target": "GDP增长率 ≥ 4.0%", "completed": False},
            "👥 社会稳定": {"target": "失业率 ≤ 4.0%", "completed": False},
            "🌱 环境保护": {"target": "碳排放指数 ≤ 70", "completed": False},
            "⚖️ 社会公平": {"target": "基尼系数 ≤ 0.35", "completed": False}
        }

        # 显示游戏说明
        self.show_game_instructions()

        # 创建UI
        self.setup_styles()
        self.create_widgets()
        self.initialize_policies()
        self.update_display()

    def show_game_instructions(self):
        """显示游戏说明 - 150mm x 100mm"""
        instructions = """🎯 游戏目标
作为国家领导人，您需要通过制定政策来管理国家经济，实现以下目标：
• 📈 经济发展：GDP增长率达到4.0%以上
• 👥 社会稳定：失业率控制在4.0%以下  
• 🌱 环境保护：碳排放指数降至70以下
• ⚖️ 社会公平：基尼系数降至0.35以下

🎮 游戏规则
• 总共12个回合，每回合可以实施多项政策
• 每回合开始时获得30点政策预算，最多储存100点
• 每项政策都有实施成本和冷却时间
• 部分政策需要满足特定前置条件才能实施
• 随机事件会影响经济指标，需要灵活应对

🏆 胜利条件
• 完成4个目标中的3个即可获胜
• 避免经济崩溃、财政危机等严重后果

💡 策略提示
• 平衡短期效益与长期发展
• 注意政策间的相互影响
• 合理管理政策预算
• 关注各项指标的变化趋势

祝您游戏愉快！🎉"""

        # 创建自定义说明窗口 - 150mm x 100mm
        instruction_window = tk.Toplevel(self.root)
        instruction_window.title("游戏说明")
        instruction_window.configure(bg=self.colors['bg_primary'])

        # 设置说明窗口尺寸为固定大小
        window_width = 600
        window_height = 1000

        # 设置基本几何，然后获取屏幕信息
        instruction_window.geometry(f"{window_width}x{window_height}")
        instruction_window.update_idletasks()

        screen_width = instruction_window.winfo_screenwidth()
        screen_height = instruction_window.winfo_screenheight()

        # 设置说明窗口位置，偏向屏幕中央但留出安全边距
        x = max(50, min(200, (screen_width - window_width) // 3))
        y = max(50, min(100, (screen_height - window_height) // 3))

        instruction_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        instruction_window.resizable(True, True)

        # 设置模态
        instruction_window.transient(self.root)
        instruction_window.grab_set()

        # 标题
        title_label = tk.Label(instruction_window,
                               text="🎮 公共经济学模拟游戏",
                               font=self.fonts['title'],
                               fg=self.colors['accent'],
                               bg=self.colors['bg_primary'])
        title_label.pack(pady=10)

        # 说明文本框
        text_frame = tk.Frame(instruction_window, bg=self.colors['bg_secondary'], relief='ridge', bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(text_frame,
                              wrap=tk.WORD,
                              font=self.fonts['normal'],
                              fg=self.colors['text_primary'],
                              bg=self.colors['bg_secondary'],
                              yscrollcommand=scrollbar.set,
                              padx=10,
                              pady=10,
                              border=0,
                              highlightthickness=0)
        text_widget.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.insert(tk.END, instructions)
        text_widget.configure(state=tk.DISABLED)

        # 开始游戏按钮
        start_button = tk.Button(instruction_window,
                                 text="🚀 开始游戏",
                                 font=self.fonts['header'],
                                 fg='white',
                                 bg=self.colors['accent'],
                                 activebackground=self.colors['accent_light'],
                                 border=0,
                                 padx=20,
                                 pady=5,
                                 command=instruction_window.destroy)
        start_button.pack(pady=10)

    def setup_styles(self):
        """设置样式"""
        style = ttk.Style()
        style.theme_use('clam')

        # 配置各种组件样式
        style.configure("Title.TLabel",
                        foreground=self.colors['text_primary'],
                        background=self.colors['bg_primary'],
                        font=self.fonts['title'])

        style.configure("Header.TLabel",
                        foreground=self.colors['text_primary'],
                        background=self.colors['bg_secondary'],
                        font=self.fonts['header'])

        style.configure("Modern.TFrame",
                        background=self.colors['bg_secondary'],
                        relief='ridge',
                        borderwidth=2)

        style.configure("Accent.TFrame",
                        background=self.colors['bg_accent'],
                        relief='ridge',
                        borderwidth=2)

        style.configure("Modern.TLabelframe",
                        background=self.colors['bg_secondary'],
                        foreground=self.colors['accent'],
                        borderwidth=2,
                        relief='groove',
                        labelanchor='n')

        style.configure("Modern.TLabelframe.Label",
                        foreground=self.colors['accent'],
                        background=self.colors['bg_secondary'],
                        font=self.fonts['header'])

    def create_widgets(self):
        """创建主界面"""
        # 顶部标题栏
        self.create_header()

        # 主要内容区 - 使用grid布局来精确控制比例
        self.main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # 配置grid权重：左侧1，右侧2（即1/3和2/3的比例）
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=2)
        self.main_container.grid_rowconfigure(0, weight=1)

        # 左侧面板 - 政策和状态，占据1/3宽度
        self.left_panel = tk.Frame(self.main_container, bg=self.colors['bg_primary'])
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.create_status_panel()
        self.create_policy_panel()

        # 右侧面板 - 图表和目标，占据2/3宽度
        self.right_panel = tk.Frame(self.main_container, bg=self.colors['bg_primary'])
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self.create_objectives_panel()
        self.create_charts_panel()

        # 底部控制栏
        self.create_control_panel()

    def create_header(self):
        """创建顶部标题栏"""
        header = tk.Frame(self.root, bg=self.colors['bg_accent'], relief='ridge', bd=3)
        header.pack(fill=tk.X, padx=10, pady=10)

        # 游戏标题
        title_frame = tk.Frame(header, bg=self.colors['bg_accent'])
        title_frame.pack(side=tk.LEFT, pady=15, padx=20)

        title = tk.Label(title_frame,
                         text="🏛️ 公共经济学模拟游戏",
                         font=self.fonts['title'],
                         fg=self.colors['accent'],
                         bg=self.colors['bg_accent'])
        title.pack()

        # 回合和预算信息
        info_frame = tk.Frame(header, bg=self.colors['bg_accent'])
        info_frame.pack(side=tk.RIGHT, pady=15, padx=20)

        self.turn_label = tk.Label(info_frame,
                                   text=f"📅 第 {self.turn} 回合 / {self.max_turns}",
                                   font=self.fonts['header'],
                                   fg=self.colors['text_primary'],
                                   bg=self.colors['bg_accent'])
        self.turn_label.pack(anchor="e", pady=(0, 5))

        self.budget_label = tk.Label(info_frame,
                                     text=f"💰 政策预算: {self.budget} 点",
                                     font=self.fonts['header'],
                                     fg=self.colors['accent'],
                                     bg=self.colors['bg_accent'])
        self.budget_label.pack(anchor="e")

    def create_status_panel(self):
        """创建经济状态面板"""
        status_frame = tk.LabelFrame(self.left_panel,
                                     text="📊 经济指标",
                                     font=self.fonts['header'],
                                     fg=self.colors['accent'],
                                     bg=self.colors['bg_secondary'],
                                     relief='ridge',
                                     bd=2)
        status_frame.pack(fill=tk.X, pady=(0, 10))

        # 指标图标映射
        indicator_icons = {
            "GDP增长率": "📈",
            "失业率": "👥",
            "通胀率": "💹",
            "财政赤字率": "💸",
            "基尼系数": "⚖️",
            "碳排放指数": "🌡️",
            "社会福利指数": "🏥",
            "创新指数": "💡",
            "教育水平": "🎓",
            "健康指数": "❤️"
        }

        # 创建指标网格 - 改为5行2列以减少高度
        self.indicator_labels = {}
        indicators = list(self.economic_data.keys())

        for i, indicator in enumerate(indicators):
            row = i // 2
            col = i % 2

            frame = tk.Frame(status_frame, bg=self.colors['bg_secondary'])
            frame.grid(row=row, column=col, sticky="ew", padx=10, pady=4)
            status_frame.columnconfigure(col, weight=1)

            # 指标图标和名称
            icon = indicator_icons.get(indicator, "📊")
            name_label = tk.Label(frame,
                                  text=f"{icon} {indicator}:",
                                  font=self.fonts['normal'],
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg_secondary'])
            name_label.pack(side=tk.LEFT)

            # 指标值
            value_label = tk.Label(frame,
                                   text="",
                                   font=self.fonts['normal'],
                                   fg=self.colors['text_primary'],
                                   bg=self.colors['bg_secondary'])
            value_label.pack(side=tk.RIGHT)

            self.indicator_labels[indicator] = value_label

    def create_policy_panel(self):
        """创建政策选择面板 - 填满剩余空间"""
        policy_frame = tk.LabelFrame(self.left_panel,
                                     text="🎯 政策选项",
                                     font=self.fonts['header'],
                                     fg=self.colors['accent'],
                                     bg=self.colors['bg_secondary'],
                                     relief='ridge',
                                     bd=2)
        # 让政策面板占据剩余的所有空间
        policy_frame.pack(fill=tk.BOTH, expand=True)

        # 创建滚动区域，填满整个policy_frame
        canvas = tk.Canvas(policy_frame,
                           bg=self.colors['bg_secondary'],
                           highlightthickness=0)
        scrollbar = tk.Scrollbar(policy_frame, orient="vertical", command=canvas.yview)
        self.policy_scrollable = tk.Frame(canvas, bg=self.colors['bg_secondary'])

        canvas.create_window((0, 0), window=self.policy_scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.policy_scrollable.bind("<Configure>", on_frame_configure)
        canvas.bind("<MouseWheel>", on_mousewheel)

        # 让canvas和scrollbar填满policy_frame
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

    def create_objectives_panel(self):
        """创建目标面板"""
        obj_frame = tk.LabelFrame(self.right_panel,
                                  text="🏆 游戏目标",
                                  font=self.fonts['header'],
                                  fg=self.colors['accent'],
                                  bg=self.colors['bg_secondary'],
                                  relief='ridge',
                                  bd=2)
        obj_frame.pack(fill=tk.X, pady=(0, 10))

        self.objective_labels = {}
        for i, (name, obj) in enumerate(self.objectives.items()):
            frame = tk.Frame(obj_frame, bg=self.colors['bg_secondary'])
            frame.pack(fill=tk.X, pady=8, padx=15)

            # 目标名称
            name_label = tk.Label(frame,
                                  text=f"{name}: {obj['target']}",
                                  font=self.fonts['normal'],
                                  fg=self.colors['text_primary'],
                                  bg=self.colors['bg_secondary'])
            name_label.pack(side=tk.LEFT)

            # 完成状态
            completion_label = tk.Label(frame,
                                        text="❌",
                                        font=self.fonts['normal'],
                                        bg=self.colors['bg_secondary'])
            completion_label.pack(side=tk.RIGHT)

            self.objective_labels[name] = completion_label

    def create_charts_panel(self):
        """创建图表面板"""
        chart_frame = tk.LabelFrame(self.right_panel,
                                    text="📈 经济趋势图",
                                    font=self.fonts['header'],
                                    fg=self.colors['accent'],
                                    bg=self.colors['bg_secondary'],
                                    relief='ridge',
                                    bd=2)
        chart_frame.pack(fill=tk.BOTH, expand=True)

        # 创建matplotlib图表
        self.fig, self.axes = plt.subplots(2, 2, figsize=(10, 8), dpi=80)
        self.fig.patch.set_facecolor(self.colors['bg_secondary'])

        # 设置子图样式
        chart_indicators = [
            ["GDP增长率", "失业率"],
            ["基尼系数", "碳排放指数"]
        ]

        for i, row in enumerate(chart_indicators):
            for j, indicator in enumerate(row):
                ax = self.axes[i, j]
                ax.set_facecolor(self.colors['bg_accent'])
                # 设置所有文字元素为20pt
                ax.tick_params(colors=self.colors['text_secondary'], labelsize=20)
                ax.set_title(indicator, color=self.colors['text_primary'],
                             fontsize=20, fontweight='bold', pad=15)
                # 设置坐标轴标签字体大小
                ax.set_xlabel('回合', fontsize=20, color=self.colors['text_secondary'])
                ax.set_ylabel('数值', fontsize=20, color=self.colors['text_secondary'])
                for spine in ax.spines.values():
                    spine.set_color(self.colors['text_secondary'])

        plt.tight_layout(pad=2.0)

        # 嵌入到tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_control_panel(self):
        """创建底部控制面板"""
        control = tk.Frame(self.root, bg=self.colors['bg_primary'])
        control.pack(fill=tk.X, padx=10, pady=(0, 10))

        # 创建按钮框架
        button_frame = tk.Frame(control, bg=self.colors['bg_accent'], relief='ridge', bd=2)
        button_frame.pack(fill=tk.X, pady=5)

        # 左侧按钮
        left_buttons = tk.Frame(button_frame, bg=self.colors['bg_accent'])
        left_buttons.pack(side=tk.LEFT, pady=10, padx=15)

        self.reset_btn = tk.Button(left_buttons,
                                   text="🔄 重新开始",
                                   font=self.fonts['normal'],
                                   fg='white',
                                   bg=self.colors['danger'],
                                   activebackground='#d32f2f',
                                   border=0,
                                   padx=20,
                                   pady=8,
                                   command=self.reset_game)
        self.reset_btn.pack(side=tk.LEFT)

        # 右侧按钮
        right_buttons = tk.Frame(button_frame, bg=self.colors['bg_accent'])
        right_buttons.pack(side=tk.RIGHT, pady=10, padx=15)

        self.next_turn_btn = tk.Button(right_buttons,
                                       text="⏭️ 下一回合",
                                       font=self.fonts['normal'],
                                       fg='white',
                                       bg=self.colors['warning'],
                                       activebackground='#f57c00',
                                       border=0,
                                       padx=20,
                                       pady=8,
                                       state=tk.DISABLED,
                                       command=self.next_turn)
        self.next_turn_btn.pack(side=tk.RIGHT, padx=(10, 0))

        self.apply_btn = tk.Button(right_buttons,
                                   text="✅ 实施政策",
                                   font=self.fonts['normal'],
                                   fg='white',
                                   bg=self.colors['success'],
                                   activebackground='#388e3c',
                                   border=0,
                                   padx=20,
                                   pady=8,
                                   command=self.apply_policies)
        self.apply_btn.pack(side=tk.RIGHT, padx=(10, 0))

    def initialize_policies(self):
        """初始化政策系统"""
        self.policies = [
            {
                "name": "💰 减税政策",
                "cost": 15,
                "cooldown": 2,
                "description": "降低个人和企业税率，刺激经济增长，但会增加财政赤字。",
                "effects": {
                    "GDP增长率": 0.8,
                    "失业率": -0.3,
                    "财政赤字率": 1.2,
                    "基尼系数": 0.02
                },
                "requirements": {"财政赤字率": 8.0}
            },
            {
                "name": "🏗️ 基础设施投资",
                "cost": 20,
                "cooldown": 1,
                "description": "大规模基础设施建设，创造就业，促进长期增长。",
                "effects": {
                    "GDP增长率": 0.6,
                    "失业率": -0.8,
                    "财政赤字率": 1.5,
                    "创新指数": 2.0,
                    "碳排放指数": 3.0
                }
            },
            {
                "name": "🎓 教育改革",
                "cost": 18,
                "cooldown": 3,
                "description": "增加教育投入，提高人力资本质量。",
                "effects": {
                    "GDP增长率": 0.4,
                    "教育水平": 5.0,
                    "创新指数": 3.0,
                    "基尼系数": -0.03,
                    "财政赤字率": 0.8
                }
            },
            {
                "name": "🌱 绿色能源补贴",
                "cost": 22,
                "cooldown": 2,
                "description": "支持可再生能源发展，减少碳排放。",
                "effects": {
                    "碳排放指数": -8.0,
                    "GDP增长率": 0.3,
                    "失业率": -0.2,
                    "财政赤字率": 1.0,
                    "创新指数": 2.5
                }
            },
            {
                "name": "🏥 社会保障扩展",
                "cost": 25,
                "cooldown": 2,
                "description": "扩大社会保障覆盖面，提高社会福利。",
                "effects": {
                    "社会福利指数": 8.0,
                    "基尼系数": -0.05,
                    "失业率": -0.3,
                    "财政赤字率": 2.0,
                    "GDP增长率": -0.1
                }
            },
            {
                "name": "💡 创新激励计划",
                "cost": 16,
                "cooldown": 1,
                "description": "支持研发创新，提高科技竞争力。",
                "effects": {
                    "创新指数": 6.0,
                    "GDP增长率": 0.5,
                    "教育水平": 2.0,
                    "碳排放指数": -2.0,
                    "财政赤字率": 0.6
                }
            },
            {
                "name": "❤️ 医疗改革",
                "cost": 20,
                "cooldown": 3,
                "description": "改善医疗体系，提高公共健康水平。",
                "effects": {
                    "健康指数": 8.0,
                    "社会福利指数": 4.0,
                    "基尼系数": -0.02,
                    "财政赤字率": 1.2
                }
            },
            {
                "name": "👷 劳动市场改革",
                "cost": 12,
                "cooldown": 2,
                "description": "提高劳动市场灵活性，促进就业。",
                "effects": {
                    "失业率": -1.0,
                    "GDP增长率": 0.4,
                    "基尼系数": 0.01,
                    "社会福利指数": -1.0
                }
            },
            {
                "name": "🌍 环境监管加强",
                "cost": 14,
                "cooldown": 1,
                "description": "加强环境保护，但可能影响经济增长。",
                "effects": {
                    "碳排放指数": -5.0,
                    "健康指数": 3.0,
                    "GDP增长率": -0.2,
                    "创新指数": 1.0
                }
            },
            {
                "name": "💹 货币宽松政策",
                "cost": 10,
                "cooldown": 1,
                "description": "降低利率，刺激投资和消费。",
                "effects": {
                    "GDP增长率": 0.6,
                    "失业率": -0.4,
                    "通胀率": 0.5,
                    "财政赤字率": -0.3
                },
                "requirements": {"通胀率": 4.0}
            }
        ]

        self.create_policy_widgets()

    def create_policy_widgets(self):
        """创建政策选择控件"""
        # 清除现有控件
        for widget in self.policy_scrollable.winfo_children():
            widget.destroy()

        self.policy_vars = []

        for i, policy in enumerate(self.policies):
            # 检查冷却时间
            is_available = self.policy_cooldowns.get(policy['name'], 0) <= 0
            can_afford = self.budget >= policy['cost']

            # 创建政策框架 - 横向填满左侧页面
            policy_frame = tk.Frame(self.policy_scrollable,
                                    bg=self.colors['bg_accent'],
                                    relief='ridge',
                                    bd=2)
            policy_frame.pack(fill=tk.BOTH, pady=3, padx=3)

            # 政策主信息框架 - 填满整个policy_frame
            main_frame = tk.Frame(policy_frame, bg=self.colors['bg_accent'])
            main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

            # 复选框和标题
            var = tk.BooleanVar()
            self.policy_vars.append(var)

            # 自定义复选框样式
            def create_checkbox(parent, variable, enabled=True):
                checkbox_frame = tk.Frame(parent, bg=self.colors['bg_accent'])

                def toggle_checkbox():
                    if enabled:
                        variable.set(not variable.get())
                        update_checkbox_display()

                def update_checkbox_display():
                    if variable.get():
                        checkbox_label.config(text="☑️", fg=self.colors['success'])
                    else:
                        checkbox_label.config(text="☐", fg=self.colors['text_secondary'])

                checkbox_label = tk.Label(checkbox_frame,
                                          text="☐",
                                          font=self.fonts['normal'],
                                          fg=self.colors['text_secondary'] if enabled else self.colors[
                                              'text_secondary'],
                                          bg=self.colors['bg_accent'],
                                          cursor="hand2" if enabled else "")
                checkbox_label.pack()

                if enabled:
                    checkbox_label.bind("<Button-1>", lambda e: toggle_checkbox())

                # 绑定变量变化事件
                variable.trace_add('write', lambda *args: update_checkbox_display())

                return checkbox_frame

            checkbox = create_checkbox(main_frame, var, is_available and can_afford)
            checkbox.pack(side=tk.LEFT, padx=(0, 12))

            # 政策名称和状态
            title_frame = tk.Frame(main_frame, bg=self.colors['bg_accent'])
            title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

            name_text = policy['name']
            if not is_available:
                cooldown_left = self.policy_cooldowns.get(policy['name'], 0)
                name_text += f" (冷却中: {cooldown_left} 回合)"

            name_label = tk.Label(title_frame,
                                  text=name_text,
                                  font=self.fonts['normal'],
                                  fg=self.colors['text_primary'] if is_available and can_afford
                                  else self.colors['text_secondary'],
                                  bg=self.colors['bg_accent'])
            name_label.pack(side=tk.LEFT)

            # 成本显示
            cost_color = self.colors['accent'] if can_afford else self.colors['danger']
            cost_label = tk.Label(main_frame,
                                  text=f"💰 {policy['cost']}",
                                  font=self.fonts['normal'],
                                  fg=cost_color,
                                  bg=self.colors['bg_accent'])
            cost_label.pack(side=tk.RIGHT)

            # 政策描述 - 调整wraplength以适应1/3的页面宽度
            desc_label = tk.Label(policy_frame,
                                  text=policy['description'],
                                  font=self.fonts['normal'],
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg_accent'],
                                  wraplength=1000,  # 适应1/3页面宽度
                                  justify=tk.LEFT)
            desc_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

    def apply_policies(self):
        """应用选中的政策"""
        selected_indices = [i for i, var in enumerate(self.policy_vars) if var.get()]

        if not selected_indices:
            messagebox.showwarning("⚠️ 警告", "请至少选择一项政策。")
            return

        total_cost = sum(self.policies[i]['cost'] for i in selected_indices)

        if total_cost > self.budget:
            messagebox.showwarning("💸 预算不足",
                                   f"选中政策总成本 {total_cost} 超过可用预算 {self.budget}。")
            return

        # 检查政策要求
        for i in selected_indices:
            policy = self.policies[i]
            if 'requirements' in policy:
                for indicator, max_value in policy['requirements'].items():
                    if self.economic_data[indicator] > max_value:
                        messagebox.showwarning("❌ 条件不满足",
                                               f"政策 '{policy['name']}' 要求 {indicator} 不超过 {max_value}，"
                                               f"当前值为 {self.economic_data[indicator]:.1f}。")
                        return

        # 应用政策效果
        self.selected_policies = [self.policies[i] for i in selected_indices]
        self.budget -= total_cost

        for policy in self.selected_policies:
            # 设置冷却时间
            self.policy_cooldowns[policy['name']] = policy['cooldown']

            # 应用效果
            for indicator, effect in policy['effects'].items():
                if indicator in self.economic_data:
                    # 添加一些随机性
                    random_factor = 1.0 + random.uniform(-0.1, 0.1)
                    actual_effect = effect * random_factor
                    self.economic_data[indicator] += actual_effect

        # 触发随机事件
        self.trigger_random_events()

        # 更新显示
        self.update_display()

        # 更新按钮状态
        self.apply_btn.configure(state=tk.DISABLED)
        self.next_turn_btn.configure(state=tk.NORMAL)

        # 检查游戏结束条件
        self.check_game_end()

    def trigger_random_events(self):
        """触发随机事件"""
        if random.random() < 0.3:  # 30%概率发生随机事件
            events = [
                {
                    "name": "🌍 全球经济衰退",
                    "description": "全球经济形势恶化，影响本国经济。",
                    "effects": {"GDP增长率": -0.5, "失业率": 0.3, "财政赤字率": 0.5}
                },
                {
                    "name": "🚀 技术突破",
                    "description": "重大技术突破促进经济发展。",
                    "effects": {"GDP增长率": 0.4, "创新指数": 3.0, "碳排放指数": -2.0}
                },
                {
                    "name": "🌪️ 自然灾害",
                    "description": "自然灾害造成经济损失。",
                    "effects": {"GDP增长率": -0.3, "财政赤字率": 0.8, "健康指数": -2.0}
                },
                {
                    "name": "🤝 国际贸易协定",
                    "description": "签署有利的国际贸易协定。",
                    "effects": {"GDP增长率": 0.3, "失业率": -0.2}
                }
            ]

            event = random.choice(events)
            self.random_events.append(event)

            # 应用事件效果
            for indicator, effect in event['effects'].items():
                if indicator in self.economic_data:
                    self.economic_data[indicator] += effect

            messagebox.showinfo("🎲 随机事件", f"{event['name']}\n\n{event['description']}")

    def next_turn(self):
        """进入下一回合"""
        self.turn += 1

        # 恢复预算
        self.budget = min(self.max_budget, self.budget + 30)

        # 减少政策冷却时间
        for policy_name in list(self.policy_cooldowns.keys()):
            self.policy_cooldowns[policy_name] -= 1
            if self.policy_cooldowns[policy_name] <= 0:
                del self.policy_cooldowns[policy_name]

        # 自然变化（经济的内在动态）
        self.apply_natural_changes()

        # 记录历史数据
        for key, value in self.economic_data.items():
            self.data_history[key].append(value)
        self.budget_history.append(self.budget)

        # 更新显示
        self.update_display()
        self.create_policy_widgets()

        # 重置按钮状态
        self.apply_btn.configure(state=tk.NORMAL)
        self.next_turn_btn.configure(state=tk.DISABLED)

        # 检查游戏结束
        if self.turn > self.max_turns:
            self.end_game()

    def apply_natural_changes(self):
        """应用自然经济变化"""
        # GDP增长率向长期趋势回归
        target_gdp_growth = 2.5
        self.economic_data["GDP增长率"] += (target_gdp_growth - self.economic_data["GDP增长率"]) * 0.1

        # 失业率受GDP增长影响
        if self.economic_data["GDP增长率"] > 3.0:
            self.economic_data["失业率"] -= 0.1
        elif self.economic_data["GDP增长率"] < 1.0:
            self.economic_data["失业率"] += 0.2

        # 通胀率小幅波动
        self.economic_data["通胀率"] += random.uniform(-0.2, 0.2)

        # 添加一些随机噪声
        for key in self.economic_data:
            noise = random.uniform(-0.05, 0.05)
            self.economic_data[key] += noise

        # 确保数值在合理范围内
        self.clamp_values()

    def clamp_values(self):
        """限制数值在合理范围内"""
        ranges = {
            "GDP增长率": (-5.0, 10.0),
            "失业率": (0.0, 25.0),
            "通胀率": (-2.0, 15.0),
            "财政赤字率": (-5.0, 20.0),
            "基尼系数": (0.2, 0.8),
            "碳排放指数": (0.0, 200.0),
            "社会福利指数": (0.0, 100.0),
            "创新指数": (0.0, 100.0),
            "教育水平": (0.0, 100.0),
            "健康指数": (0.0, 100.0)
        }

        for key, (min_val, max_val) in ranges.items():
            if key in self.economic_data:
                self.economic_data[key] = max(min_val, min(max_val, self.economic_data[key]))

    def update_display(self):
        """更新所有显示元素"""
        # 更新回合和预算显示
        self.turn_label.configure(text=f"📅 第 {self.turn} 回合 / {self.max_turns}")
        self.budget_label.configure(text=f"💰 政策预算: {self.budget} 点")

        # 更新经济指标
        for indicator, label in self.indicator_labels.items():
            value = self.economic_data[indicator]
            if indicator in ["基尼系数"]:
                text = f"{value:.3f}"
            else:
                text = f"{value:.1f}"

            # 根据指标好坏设置颜色
            if self.is_indicator_good(indicator, value):
                color = self.colors['success']
            elif self.is_indicator_bad(indicator, value):
                color = self.colors['danger']
            else:
                color = self.colors['warning']

            label.configure(text=text, fg=color)

        # 更新目标完成状态
        self.update_objectives()

        # 更新图表
        self.update_charts()

    def is_indicator_good(self, indicator, value):
        """判断指标是否良好"""
        good_ranges = {
            "GDP增长率": value >= 3.0,
            "失业率": value <= 4.0,
            "通胀率": 1.0 <= value <= 3.0,
            "财政赤字率": value <= 3.0,
            "基尼系数": value <= 0.35,
            "碳排放指数": value <= 70.0,
            "社会福利指数": value >= 80.0,
            "创新指数": value >= 80.0,
            "教育水平": value >= 85.0,
            "健康指数": value >= 85.0
        }
        return good_ranges.get(indicator, False)

    def is_indicator_bad(self, indicator, value):
        """判断指标是否糟糕"""
        bad_ranges = {
            "GDP增长率": value <= 0.0,
            "失业率": value >= 10.0,
            "通胀率": value >= 5.0 or value <= -1.0,
            "财政赤字率": value >= 8.0,
            "基尼系数": value >= 0.6,
            "碳排放指数": value >= 150.0,
            "社会福利指数": value <= 40.0,
            "创新指数": value <= 30.0,
            "教育水平": value <= 40.0,
            "健康指数": value <= 40.0
        }
        return bad_ranges.get(indicator, False)

    def update_objectives(self):
        """更新目标完成状态"""
        objectives_check = {
            "📈 经济发展": self.economic_data["GDP增长率"] >= 4.0,
            "👥 社会稳定": self.economic_data["失业率"] <= 4.0,
            "🌱 环境保护": self.economic_data["碳排放指数"] <= 70,
            "⚖️ 社会公平": self.economic_data["基尼系数"] <= 0.35
        }

        for name, completed in objectives_check.items():
            self.objectives[name]["completed"] = completed
            status = "✅" if completed else "❌"
            self.objective_labels[name].configure(text=status)

    def update_charts(self):
        """更新图表显示"""
        if len(self.data_history["GDP增长率"]) < 2:
            return

        x = range(len(self.data_history["GDP增长率"]))

        # 清除所有子图
        for ax in self.axes.flat:
            ax.clear()
            ax.set_facecolor(self.colors['bg_accent'])

        # 绘制各个指标
        indicators_to_plot = [
            ["GDP增长率", "失业率"],
            ["基尼系数", "碳排放指数"]
        ]

        colors = self.colors['chart_colors']

        for i, row in enumerate(indicators_to_plot):
            for j, indicator in enumerate(row):
                ax = self.axes[i, j]
                data = self.data_history[indicator]

                # 绘制线图
                line_color = colors[i * 2 + j % len(colors)]
                ax.plot(x, data, color=line_color, linewidth=3, marker='o', markersize=6)

                # 设置标题和样式 - 所有文字都是20pt
                ax.set_title(indicator, color=self.colors['text_primary'],
                             fontsize=20, fontweight='bold', pad=15)
                ax.tick_params(colors=self.colors['text_secondary'], labelsize=20)
                # 设置坐标轴标签字体大小为20pt
                ax.set_xlabel('回合', fontsize=20, color=self.colors['text_secondary'])
                ax.set_ylabel('数值', fontsize=20, color=self.colors['text_secondary'])
                ax.grid(True, alpha=0.3, color=self.colors['text_secondary'])

                # 设置边框颜色
                for spine in ax.spines.values():
                    spine.set_color(self.colors['text_secondary'])

                # 添加目标线（如果有的话）
                if indicator == "GDP增长率":
                    ax.axhline(y=4.0, color=self.colors['success'], linestyle='--',
                               alpha=0.8, linewidth=2, label='目标: 4.0%')
                elif indicator == "失业率":
                    ax.axhline(y=4.0, color=self.colors['success'], linestyle='--',
                               alpha=0.8, linewidth=2, label='目标: 4.0%')
                elif indicator == "基尼系数":
                    ax.axhline(y=0.35, color=self.colors['success'], linestyle='--',
                               alpha=0.8, linewidth=2, label='目标: 0.35')
                elif indicator == "碳排放指数":
                    ax.axhline(y=70.0, color=self.colors['success'], linestyle='--',
                               alpha=0.8, linewidth=2, label='目标: 70')

                # 添加图例 - 字体大小设置为20pt
                ax.legend(loc='best', facecolor=self.colors['bg_accent'],
                          edgecolor=self.colors['text_secondary'],
                          labelcolor=self.colors['text_secondary'],
                          fontsize=20)

        plt.tight_layout(pad=2.0)
        self.canvas.draw()

    def check_game_end(self):
        """检查游戏结束条件"""
        # 检查胜利条件
        completed_objectives = sum(1 for obj in self.objectives.values() if obj["completed"])

        if completed_objectives >= 3:
            messagebox.showinfo("🎉 胜利！",
                                f"恭喜！您已完成 {completed_objectives}/4 个主要目标，"
                                f"成功领导国家走向繁荣！")
            self.end_game()
            return

        # 检查失败条件
        failure_conditions = [
            ("经济崩溃", self.economic_data["GDP增长率"] <= -3.0),
            ("财政危机", self.economic_data["财政赤字率"] >= 15.0),
            ("社会动荡", self.economic_data["失业率"] >= 20.0),
            ("恶性通胀", self.economic_data["通胀率"] >= 10.0)
        ]

        for condition_name, condition in failure_conditions:
            if condition:
                messagebox.showinfo("💥 游戏结束",
                                    f"游戏结束！{condition_name}导致政府倒台。")
                self.end_game()
                return

    def end_game(self):
        """结束游戏"""
        self.apply_btn.configure(state=tk.DISABLED)
        self.next_turn_btn.configure(state=tk.DISABLED)

        # 显示最终得分
        score = self.calculate_final_score()
        completed = sum(1 for obj in self.objectives.values() if obj["completed"])

        result_msg = f"🏛️ 游戏结束！\n\n"
        result_msg += f"📊 完成目标: {completed}/4\n"
        result_msg += f"🏆 最终得分: {score:.1f}\n\n"
        result_msg += "🎯 目标完成情况：\n"

        for name, obj in self.objectives.items():
            status = "✅" if obj["completed"] else "❌"
            result_msg += f"{status} {name}\n"

        messagebox.showinfo("📋 游戏总结", result_msg)

    def calculate_final_score(self):
        """计算最终得分"""
        score = 0

        # 基础得分基于目标完成情况
        completed_objectives = sum(1 for obj in self.objectives.values() if obj["completed"])
        score += completed_objectives * 25

        # 各项指标的额外得分
        if self.economic_data["GDP增长率"] >= 3.0:
            score += 10
        if self.economic_data["失业率"] <= 5.0:
            score += 10
        if self.economic_data["财政赤字率"] <= 5.0:
            score += 10
        if self.economic_data["社会福利指数"] >= 70.0:
            score += 5
        if self.economic_data["创新指数"] >= 70.0:
            score += 5

        return score

    def reset_game(self):
        """重置游戏"""
        self.turn = 1
        self.budget = 100

        # 重置经济数据
        self.economic_data = {
            "GDP增长率": 2.5,
            "失业率": 6.0,
            "通胀率": 2.0,
            "财政赤字率": 3.0,
            "基尼系数": 0.45,
            "碳排放指数": 100.0,
            "社会福利指数": 65.0,
            "创新指数": 60.0,
            "教育水平": 70.0,
            "健康指数": 75.0
        }

        # 重置历史数据
        self.data_history = {key: [value] for key, value in self.economic_data.items()}
        self.budget_history = [self.budget]

        # 重置政策系统
        self.selected_policies = []
        self.policy_cooldowns = {}
        self.random_events = []

        # 重置目标
        for obj in self.objectives.values():
            obj["completed"] = False

        # 更新显示
        self.update_display()
        self.create_policy_widgets()

        # 重置按钮状态
        self.apply_btn.configure(state=tk.NORMAL)
        self.next_turn_btn.configure(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    game = EconomicSimulationGame(root)
    root.mainloop()