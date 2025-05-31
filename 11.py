import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams['axes.unicode_minus'] = False


class EconomicSimulationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("经济模拟游戏")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f5f9")

        # 确保中文显示正常
        self.title_font = ("SimHei", 18, "bold")
        self.header_font = ("SimHei", 14, "bold")
        self.normal_font = ("SimHei", 12)

        # 经济数据初始化
        self.turn = 1
        self.max_turns = 10
        self.policies = []
        self.selected_policies = []
        self.economic_data = {
            "GDP增长率": 0.0,
            "财政赤字率": 0.0,
            "失业率": 5.0,
            "碳排放量": 100.0,
            "社会稳定指数": 75.0,
            "基尼系数": 0.40,
            "中产阶级比例": 50.0,
            "税收收入": 0.0,
            "企业投资": 50.0,
            "消费者信心": 70.0
        }
        self.data_history = {key: [value] for key, value in self.economic_data.items()}

        # 创建UI组件
        self.create_widgets()

        # 初始化政策
        self.initialize_policies()

        # 更新显示
        self.update_economic_display()

    def create_widgets(self):
        # 顶部标题区域
        self.header_frame = ttk.Frame(self.root, padding="10", style="Header.TFrame")
        self.header_frame.pack(fill=tk.X)

        self.title_label = ttk.Label(self.header_frame, text="经济模拟游戏", font=self.title_font, style="Title.TLabel")
        self.title_label.pack(side=tk.LEFT, padx=20)

        self.turn_label = ttk.Label(self.header_frame, text=f"回合: {self.turn}/{self.max_turns}",
                                    font=self.header_font, style="Turn.TLabel")
        self.turn_label.pack(side=tk.RIGHT, padx=20)

        # 主内容区域
        self.main_frame = ttk.Frame(self.root, padding="10", style="Main.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧政策区域
        self.policy_frame = ttk.LabelFrame(self.main_frame, text="政策选项", padding="10", style="Policy.TLabelframe")
        self.policy_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # 政策滚动区域
        self.policy_canvas = tk.Canvas(self.policy_frame, bg="white", highlightthickness=0)
        self.policy_scrollbar = ttk.Scrollbar(self.policy_frame, orient="vertical", command=self.policy_canvas.yview)
        self.policy_scrollable_frame = ttk.Frame(self.policy_canvas, style="PolicyScroll.TFrame")

        self.policy_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.policy_canvas.configure(
                scrollregion=self.policy_canvas.bbox("all")
            )
        )

        self.policy_canvas.create_window((0, 0), window=self.policy_scrollable_frame, anchor="nw")
        self.policy_canvas.configure(yscrollcommand=self.policy_scrollbar.set)

        self.policy_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.policy_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 右侧信息区域
        self.info_frame = ttk.Frame(self.main_frame, padding="10", style="Info.TFrame")
        self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 经济指标区域
        self.indicators_frame = ttk.LabelFrame(self.info_frame, text="经济指标", padding="10",
                                               style="Indicators.TLabelframe")
        self.indicators_frame.pack(fill=tk.X, pady=(0, 10))

        self.indicator_labels = {}
        for i, (name, value) in enumerate(self.economic_data.items()):
            frame = ttk.Frame(self.indicators_frame)
            frame.grid(row=i // 2, column=i % 2, sticky="ew", pady=5)

            label = ttk.Label(frame, text=f"{name}:", font=self.normal_font, style="IndicatorName.TLabel")
            label.pack(side=tk.LEFT, padx=(0, 10))

            value_label = ttk.Label(frame, text=f"{value:.2f}" if isinstance(value, float) else f"{value}",
                                    font=self.normal_font, style="IndicatorValue.TLabel")
            value_label.pack(side=tk.LEFT)

            self.indicator_labels[name] = value_label

        # 图表区域
        self.chart_frame = ttk.LabelFrame(self.info_frame, text="经济趋势", padding="10", style="Chart.TLabelframe")
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

        self.fig, self.axes = plt.subplots(2, 2, figsize=(8, 6), dpi=100)
        self.fig.patch.set_facecolor('#f0f5f9')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 底部按钮区域
        self.button_frame = ttk.Frame(self.root, padding="10", style="Button.TFrame")
        self.button_frame.pack(fill=tk.X)

        self.select_button = ttk.Button(self.button_frame, text="实施政策", command=self.apply_policies,
                                        style="Select.TButton")
        self.select_button.pack(side=tk.RIGHT, padx=(0, 10))

        self.next_turn_button = ttk.Button(self.button_frame, text="下一回合", command=self.next_turn,
                                           style="Next.TButton", state=tk.DISABLED)
        self.next_turn_button.pack(side=tk.RIGHT, padx=(0, 10))

        self.reset_button = ttk.Button(self.button_frame, text="重新开始", command=self.reset_game,
                                       style="Reset.TButton")
        self.reset_button.pack(side=tk.LEFT, padx=(10, 0))

    def initialize_policies(self):
        # 定义更多政策选项
        self.policies = [
            {
                "name": "提高最低工资",
                "description": "提高最低工资标准，改善低收入群体生活水平，但可能增加企业成本。",
                "effects": {
                    "GDP增长率": 0.2,
                    "失业率": -0.5,
                    "基尼系数": -0.03,
                    "社会稳定指数": 2.0,
                    "企业投资": -1.0,
                    "消费者信心": 3.0
                }
            },
            {
                "name": "研发补贴",
                "description": "为企业研发提供补贴，促进技术创新和长期经济增长。",
                "effects": {
                    "GDP增长率": 0.5,
                    "碳排放量": -2.0,
                    "企业投资": 5.0,
                    "财政赤字率": 0.8
                }
            },
            {
                "name": "遗产税",
                "description": "对大额遗产征收税收，减少财富不平等，增加公共收入。",
                "effects": {
                    "基尼系数": -0.05,
                    "税收收入": 2.0,
                    "社会稳定指数": 1.5,
                    "消费者信心": -1.0
                }
            },
            {
                "name": "教育券制度",
                "description": "提供教育券，提高教育公平性和质量，长期提升人力资本。",
                "effects": {
                    "GDP增长率": 0.3,
                    "基尼系数": -0.02,
                    "社会稳定指数": 1.0,
                    "中产阶级比例": 1.0,
                    "财政赤字率": 0.5
                }
            },
            {
                "name": "反垄断法",
                "description": "加强反垄断监管，促进市场竞争，提高效率和创新。",
                "effects": {
                    "GDP增长率": 0.4,
                    "基尼系数": -0.01,
                    "企业投资": 2.0,
                    "消费者信心": 2.0
                }
            },
            {
                "name": "累进所得税",
                "description": "提高高收入群体税率，降低低收入群体负担，减少不平等。",
                "effects": {
                    "基尼系数": -0.04,
                    "税收收入": 1.5,
                    "社会稳定指数": 1.5,
                    "企业投资": -1.0,
                    "消费者信心": -0.5
                }
            },
            {
                "name": "全民基本收入",
                "description": "为所有公民提供基本收入，消除贫困，但增加财政负担。",
                "effects": {
                    "失业率": -0.3,
                    "基尼系数": -0.06,
                    "社会稳定指数": 3.0,
                    "消费者信心": 4.0,
                    "财政赤字率": 2.0
                }
            },
            {
                "name": "慈善税收抵扣",
                "description": "鼓励慈善捐赠，支持社会福利项目，减轻企业和个人税负。",
                "effects": {
                    "社会稳定指数": 1.0,
                    "税收收入": -0.5,
                    "企业投资": 0.5
                }
            },
            {
                "name": "基础设施投资",
                "description": "大规模投资基础设施，创造就业，促进长期经济增长。",
                "effects": {
                    "GDP增长率": 0.6,
                    "失业率": -1.0,
                    "企业投资": 3.0,
                    "碳排放量": 1.0,
                    "财政赤字率": 1.5
                }
            },
            {
                "name": "绿色能源补贴",
                "description": "补贴可再生能源，减少碳排放，促进可持续发展。",
                "effects": {
                    "碳排放量": -3.0,
                    "GDP增长率": 0.2,
                    "企业投资": 2.0,
                    "财政赤字率": 0.7
                }
            },
            {
                "name": "放松移民政策",
                "description": "吸引更多移民，增加劳动力供给，促进文化多样性。",
                "effects": {
                    "GDP增长率": 0.3,
                    "失业率": 0.2,
                    "基尼系数": 0.01,
                    "社会稳定指数": -1.0,
                    "消费者信心": 0.5
                }
            },
            {
                "name": "降低公司税",
                "description": "降低企业税率，刺激投资和经济增长。",
                "effects": {
                    "GDP增长率": 0.4,
                    "企业投资": 4.0,
                    "税收收入": -1.0,
                    "基尼系数": 0.02
                }
            }
        ]

        # 创建政策选择UI
        self.policy_vars = []
        for i, policy in enumerate(self.policies):
            frame = ttk.Frame(self.policy_scrollable_frame, padding="5", style="PolicyItem.TFrame")
            frame.grid(row=i, column=0, sticky="ew", pady=2)

            var = tk.BooleanVar()
            self.policy_vars.append(var)

            checkbox = ttk.Checkbutton(
                frame,
                text=policy["name"],
                variable=var,
                compound=tk.LEFT
            )
            checkbox.pack(anchor="w")

            description_label = ttk.Label(
                frame,
                text=policy["description"],
                font=("SimHei", 10),
                wraplength=300
            )
            description_label.pack(anchor="w", padx=(20, 0))

    def apply_policies(self):
        selected_indices = [i for i, var in enumerate(self.policy_vars) if var.get()]
        if len(selected_indices) != 3:
            messagebox.showwarning("警告", "请选择三项政策。")
            return

        self.selected_policies = [self.policies[i] for i in selected_indices]
        self.update_economic_indicators()
        self.update_economic_display()
        self.select_button.config(state=tk.DISABLED)
        self.next_turn_button.config(state=tk.NORMAL)

    def update_economic_indicators(self):
        for policy in self.selected_policies:
            for key, effect in policy["effects"].items():
                new_value = self.economic_data[key] + effect
                self.economic_data[key] = max(min(new_value, 100), 0)  # 防止超过范围
                self.data_history[key].append(self.economic_data[key])

        self.turn += 1

    def update_economic_display(self):
        for name, value_label in self.indicator_labels.items():
            value_label.config(text=f"{self.economic_data[name]:.2f}" if isinstance(self.economic_data[name],
                                                                                    float) else f"{self.economic_data[name]}")

        self.turn_label.config(text=f"回合: {self.turn}/{self.max_turns}")
        self.update_charts()

        if self.check_victory_conditions():
            messagebox.showinfo("恭喜", "您赢得了游戏！")
            self.end_game()
        elif self.check_failure_conditions():
            messagebox.showinfo("遗憾", "游戏结束，未能达成目标。")
            self.end_game()

    def update_charts(self):
        x = range(len(self.data_history["GDP增长率"]))
        indicators_to_plot = {
            "GDP增长率": (0, 0),
            "财政赤字率": (0, 1),
            "失业率": (1, 0),
            "碳排放量": (1, 1),
            "社会稳定指数": (0, 0),
            "基尼系数": (0, 1),
            "中产阶级比例": (1, 0),
            "税收收入": (1, 1)
        }

        for ax in self.axes.flat:
            ax.clear()

        plotted = set()
        for indicator, (row, col) in indicators_to_plot.items():
            if indicator not in plotted:
                self.axes[row, col].plot(x, self.data_history[indicator], label=indicator)
                self.axes[row, col].set_title(indicator)
                self.axes[row, col].legend(loc='best')
                plotted.add(indicator)

        self.fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        self.canvas.draw()

    def next_turn(self):
        if self.turn < self.max_turns:
            self.select_button.config(state=tk.NORMAL)
            self.next_turn_button.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("游戏结束", "已达到最大回合数。")
            self.end_game()

    def reset_game(self):
        self.turn = 1
        self.economic_data = {
            "GDP增长率": 0.0,
            "财政赤字率": 0.0,
            "失业率": 5.0,
            "碳排放量": 100.0,
            "社会稳定指数": 75.0,
            "基尼系数": 0.40,
            "中产阶级比例": 50.0,
            "税收收入": 0.0,
            "企业投资": 50.0,
            "消费者信心": 70.0
        }
        self.data_history = {key: [value] for key, value in self.economic_data.items()}
        self.update_economic_display()
        self.select_button.config(state=tk.NORMAL)
        self.next_turn_button.config(state=tk.DISABLED)
        self.turn_label.config(text=f"回合: {self.turn}/{self.max_turns}")
        self.update_charts()

    def check_victory_conditions(self):
        return (
                self.economic_data["基尼系数"] <= 0.3 and self.economic_data["中产阶级比例"] >= 70 or
                self.economic_data["GDP增长率"] >= 8 and self.economic_data["财政赤字率"] <= 2 or
                self.economic_data["碳排放量"] <= 50 and self.economic_data["社会稳定指数"] >= 80
        )

    def check_failure_conditions(self):
        return (
                self.economic_data["基尼系数"] > 0.6 or
                self.economic_data["财政赤字率"] > 10
        )

    def end_game(self):
        self.select_button.config(state=tk.DISABLED)
        self.next_turn_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    game = EconomicSimulationGame(root)
    root.mainloop()



