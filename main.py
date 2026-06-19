#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 家庭用电数据分析节能助手 - Python增强版
# 功能：
# 1. 根据电费计算用电数据
# 2. 输入数据分析给出建议
# 3. 输入数据计算当月电费
# 4. 分析各项电器用电情况
# 5. 电器管理(添加/删除/修改)
# 6. 用电习惯评分评级
# 7. 峰谷电价计算

import os
import sys
import time
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass, field

# 跨平台颜色控制
class ConsoleStyle:
   
    @staticmethod
    def init():
        if os.name == 'nt':
            os.system('')
    @staticmethod
    def set_color(color_code: str):
        print(f"\033[{color_code}m", end='')
    @staticmethod
    def reset():
        print("\033[0m", end='')
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def sleep(milliseconds: int):
        time.sleep(milliseconds / 1000)
    
    @staticmethod
    def green():
        ConsoleStyle.set_color("32")
    
    @staticmethod
    def red():
        ConsoleStyle.set_color("31")
    
    @staticmethod
    def yellow():
        ConsoleStyle.set_color("33")
    
    @staticmethod
    def blue():
        ConsoleStyle.set_color("34")
    
    @staticmethod
    def cyan():
        ConsoleStyle.set_color("36")
    
    @staticmethod
    def magenta():
        ConsoleStyle.set_color("35")
    
    @staticmethod
    def white():
        ConsoleStyle.set_color("37")


class UIComponents:
    
    @staticmethod
    def print_header(title: str):
        ConsoleStyle.cyan()
        print("\n╔════════════════════════════════════════════════════════════╗")
        print("║", end='')
        ConsoleStyle.yellow()
        print(f"{title:^48}", end='')
        ConsoleStyle.cyan()
        print("║")
        print("╚════════════════════════════════════════════════════════════╝")
        ConsoleStyle.reset()
    
    @staticmethod
    def print_section(title: str):
        ConsoleStyle.blue()
        print("\n┌────────────────────────────────────────────────────────────┐")
        print(f"│ {title:<58}│")
        print("└────────────────────────────────────────────────────────────┘")
        ConsoleStyle.reset()
    
    @staticmethod
    def print_success(message: str):
        ConsoleStyle.green()
        print(f"✅ {message}")
        ConsoleStyle.reset()
    
    @staticmethod
    def print_warning(message: str):
        ConsoleStyle.yellow()
        print(f"⚠️  {message}")
        ConsoleStyle.reset()
    
    @staticmethod
    def print_error(message: str):
        ConsoleStyle.red()
        print(f"❌ {message}")
        ConsoleStyle.reset()
    
    @staticmethod
    def print_info(message: str):
        ConsoleStyle.cyan()
        print(f"💡 {message}")
        ConsoleStyle.reset()
    
    @staticmethod
    def progress_bar(task: str, duration: int = 1000):
        ConsoleStyle.blue()
        print(f"\n{task}")
        print("[", end='')
        ConsoleStyle.reset()
        
        steps = 20
        for i in range(steps + 1):
            ConsoleStyle.green()
            print("█", end='', flush=True)
            ConsoleStyle.reset()
            ConsoleStyle.sleep(duration // steps)
        print("] 完成！")
    
    @staticmethod
    def print_table_header(headers: List[str]):
        ConsoleStyle.magenta()
        print("┌", end='')
        for i, _ in enumerate(headers):
            print("──────────────────", end='')
            if i < len(headers) - 1:
                print("┬", end='')
        print("┐")
        
        print("│", end='')
        for header in headers:
            print(f" {header:<18}│", end='')
        print()
        
        print("├", end='')
        for i, _ in enumerate(headers):
            print("──────────────────", end='')
            if i < len(headers) - 1:
                print("┼", end='')
        print("┤")
        ConsoleStyle.reset()
    
    @staticmethod
    def print_table_row(cells: List[str]):

        print("│", end='')
        for cell in cells:
            print(f" {cell:<18}│", end='')
        print()
    
    @staticmethod
    def print_table_footer(columns: int):

        ConsoleStyle.magenta()
        print("└", end='')
        for i in range(columns):
            print("──────────────────", end='')
            if i < columns - 1:
                print("┴", end='')
        print("┘")
        ConsoleStyle.reset()


@dataclass
class HabitScore:

    total_score: float = 0.0
    grade: str = ""
    title: str = ""
    sub_scores: Dict[str, float] = field(default_factory=dict)
    suggestions: List[str] = field(default_factory=list)


class EnergyAnalyzer:

    
    def __init__(self):

        self.appliance_data = {
            "空调": 1.2,
            "冰箱": 0.15,
            "电视机": 0.08,
            "洗衣机": 0.5,
            "热水器": 2.0,
            "电脑": 0.1,
            "照明": 0.06,
            "微波炉": 1.0
        }
    
    def animate_number(self, target: float, label: str, unit: str = ""):

        step = target / 20.0
        
        ConsoleStyle.green()
        print(label, end='')
        ConsoleStyle.reset()
        
        for i in range(20):
            current = step * (i + 1)
            if current > target:
                current = target
            
            print(f"\r{label}{current:.2f}{unit}   ", end='', flush=True)
            ConsoleStyle.sleep(50)
        print()
    
    def calculate_usage_from_bill(self):
        """功能1: 根据电费计算用电数据"""
        UIComponents.print_header("根据电费计算用电量")
        
        try:
            bill = float(input("请输入当月电费金额(元): "))
        except ValueError:
            UIComponents.print_error("请输入有效的数字！")
            return
        
        if bill <= 0:
            UIComponents.print_error("电费金额必须大于0")
            return
        
        UIComponents.progress_bar("计算中...", 800)
        
        usage = bill / 0.6  # 假设平均电价0.6元/kWh
        carbon_emission = usage * 0.785
        
        UIComponents.print_section("计算结果")
        
        self.animate_number(usage, "📊 当月用电量: ", " kWh")
        self.animate_number(carbon_emission, "🌿 碳排放量: ", " kg CO₂")
        self.animate_number(bill, "💰 平均电价: ", " 元/kWh")
        
        self.display_usage_chart(usage)
        self.provide_basic_suggestions(usage)
    
    def analyze_and_suggest(self):
        """功能2: 输入数据分析给出建议"""
        UIComponents.print_header("用电数据分析与建议")
        
        try:
            days = int(input("请输入要分析的天数: "))
        except ValueError:
            UIComponents.print_error("请输入有效的整数！")
            return
        
        if days <= 0 or days > 31:
            UIComponents.print_error("天数必须在1-31之间")
            return
        
        daily_data = []
        total = 0.0
        
        UIComponents.print_info("请输入每日用电量(kWh):")
        for i in range(1, days + 1):
            try:
                usage = float(input(f"第{i}天: "))
                daily_data.append(usage)
                total += usage
            except ValueError:
                UIComponents.print_error("请输入有效的数字！")
                return
        
        UIComponents.progress_bar("分析数据中...", 1000)
        
        self.analyze_daily_data(daily_data, total)
    
    def calculate_monthly_bill(self):
        """功能3: 输入数据计算当月电费"""
        UIComponents.print_header("当月电费计算")
        
        try:
            monthly_usage = float(input("请输入当月总用电量(kWh): "))
        except ValueError:
            UIComponents.print_error("请输入有效的数字！")
            return
        
        if monthly_usage <= 0:
            UIComponents.print_error("用电量必须大于0")
            return
        
        UIComponents.progress_bar("计算电费中...", 600)
        
        bill = self.calculate_tiered_bill(monthly_usage)
        carbon_emission = monthly_usage * 0.785
        avg_price = bill / monthly_usage
        
        UIComponents.print_section("电费详情")
        
        self.animate_number(monthly_usage, "⚡ 总用电量: ", " kWh")
        self.animate_number(bill, "💰 总电费: ", " 元")
        self.animate_number(carbon_emission, "🌍 碳排放: ", " kg CO₂")
        self.animate_number(avg_price, "📈 平均电价: ", " 元/kWh")
        
        self.display_bill_analysis(monthly_usage, bill)
    
    def analyze_appliances(self):
        """功能4: 分析电器运行时长"""
        UIComponents.print_header("电器用电分析")
        
        UIComponents.print_info("当前电器库:")
        self.display_appliances_table()
        
        usage_hours = {}
        total_daily_usage = 0.0
        
        UIComponents.print_section("输入使用时长")
        print("请输入各电器每日使用时长(小时):")
        
        for appliance, power in self.appliance_data.items():
            try:
                hours = float(input(f"{appliance} ({power}kW): "))
                usage_hours[appliance] = hours
                total_daily_usage += power * hours
            except ValueError:
                UIComponents.print_error("请输入有效的数字！")
                return
        
        UIComponents.progress_bar("分析电器用电...", 1200)
        self.display_appliance_analysis(usage_hours, total_daily_usage)
    
    # ==================== 新增功能3: 电器管理扩展 ====================
    
    def manage_appliances(self):
        """电器管理主菜单"""
        while True:
            ConsoleStyle.clear_screen()
            UIComponents.print_header("电器管理")
            
            ConsoleStyle.cyan()
            print("请选择操作:")
            ConsoleStyle.reset()
            
            print("┌───────────────┬────────────────────────────────────────────┐")
            print("│   选项        │                功能描述                    │")
            print("├───────────────┼────────────────────────────────────────────┤")
            print("│      1        │ 📋 查看所有电器                           │")
            print("│      2        │ ➕ 添加新电器                             │")
            print("│      3        │ ➖ 删除电器                               │")
            print("│      4        │ ✏️  修改电器功率                          │")
            print("│      5        │ 🔙 返回主菜单                             │")
            print("└───────────────┴────────────────────────────────────────────┘")
            
            ConsoleStyle.yellow()
            choice = input("\n请输入选择 (1-5): ")
            ConsoleStyle.reset()
            
            if choice == '1':
                self.display_appliances_table()
            elif choice == '2':
                self.add_appliance()
            elif choice == '3':
                self.remove_appliance()
            elif choice == '4':
                self.modify_appliance()
            elif choice == '5':
                UIComponents.print_info("返回主菜单...")
                break
            else:
                UIComponents.print_error("无效选择，请重新输入！")
                ConsoleStyle.sleep(1000)
                continue
            
            if choice != '5':
                ConsoleStyle.yellow()
                input("\n⏎ 按回车键继续...")
                ConsoleStyle.reset()
    
    def add_appliance(self):
        """添加新电器"""
        UIComponents.print_header("添加新电器")
        
        name = input("请输入电器名称: ").strip()
        
        if not name:
            UIComponents.print_error("电器名称不能为空！")
            return
        
        if name in self.appliance_data:
            UIComponents.print_error("该电器已存在！")
            return
        
        try:
            power = float(input("请输入电器功率(kW): "))
        except ValueError:
            UIComponents.print_error("请输入有效的数字！")
            return
        
        if power <= 0:
            UIComponents.print_error("功率必须大于0！")
            return
        
        self.appliance_data[name] = power
        UIComponents.print_success("电器添加成功！")
        
        print()
        headers = ["电器名称", "功率(kW)", "状态"]
        UIComponents.print_table_header(headers)
        UIComponents.print_table_row([name, f"{power:.2f}", "✅ 新增"])
        UIComponents.print_table_footer(len(headers))
    
    def remove_appliance(self):
        """删除电器"""
        UIComponents.print_header("删除电器")
        
        self.display_appliances_table()
        
        name = input("\n请输入要删除的电器名称: ").strip()
        
        if name not in self.appliance_data:
            UIComponents.print_error("未找到该电器！")
            return
        
        del self.appliance_data[name]
        UIComponents.print_success("电器删除成功！")
    
    def modify_appliance(self):
        """修改电器功率"""
        UIComponents.print_header("修改电器功率")
        
        self.display_appliances_table()
        
        name = input("\n请输入要修改的电器名称: ").strip()
        
        if name not in self.appliance_data:
            UIComponents.print_error("未找到该电器！")
            return
        
        print(f"当前功率: {self.appliance_data[name]} kW")
        
        try:
            new_power = float(input("请输入新功率(kW): "))
        except ValueError:
            UIComponents.print_error("请输入有效的数字！")
            return
        
        if new_power <= 0:
            UIComponents.print_error("功率必须大于0！")
            return
        
        self.appliance_data[name] = new_power
        UIComponents.print_success("电器功率修改成功！")
    
    
    def evaluate_habit(self):
        """用电习惯评分评级"""
        UIComponents.print_header("用电习惯评分评级")
        
        UIComponents.print_info("请回答以下问题，系统将评估您的用电习惯")
        
        try:
            days = int(input("\n请输入要评估的天数(建议7-30天): "))
        except ValueError:
            UIComponents.print_error("请输入有效的整数！")
            return
        
        if days <= 0 or days > 31:
            UIComponents.print_error("天数必须在1-31之间")
            return
        
        daily_data = []
        total = 0.0
        
        UIComponents.print_section("输入用电数据")
        
        for i in range(1, days + 1):
            try:
                usage = float(input(f"第{i}天用电量(kWh): "))
                daily_data.append(usage)
                total += usage
            except ValueError:
                UIComponents.print_error("请输入有效的数字！")
                return
        
        try:
            print(f"\n过去{days}天中，有多少天在峰时段(8:00-22:00)大量用电: ", end='')
            peak_hours_count = int(input())
            
            print("估算的待机功耗(W): ", end='')
            standby_power = float(input())
            
            print("家中节能电器数量: ", end='')
            energy_saving_appliances = int(input())
        except ValueError:
            UIComponents.print_error("请输入有效的数字！")
            return
        
        UIComponents.progress_bar("评估用电习惯中...", 1500)
        
        score = self.calculate_habit_score(
            daily_data, total, days, 
            peak_hours_count, standby_power, energy_saving_appliances
        )
        
        self.display_habit_score(score)
    
    def calculate_habit_score(self, daily_data: List[float], total: float, days: int,
                               peak_hours_count: int, standby_power: float, 
                               energy_saving_appliances: int) -> HabitScore:
        """计算用电习惯评分"""
        score = HabitScore()
        
        avg = total / days
        max_usage = max(daily_data)
        min_usage = min(daily_data)
        
        # 计算标准差
        variance = sum((usage - avg) ** 2 for usage in daily_data) / days
        std_dev = math.sqrt(variance)
        
        # 1. 用电量评分 (30分)
        if avg > 20:
            usage_score = 5
        elif avg > 15:
            usage_score = 10
        elif avg > 10:
            usage_score = 20
        elif avg > 5:
            usage_score = 25
        else:
            usage_score = 30
        score.sub_scores["用电量"] = usage_score
        
        # 2. 用电稳定性评分 (25分)
        cv = (std_dev / avg) if avg > 0 else 0
        if cv > 0.5:
            stability_score = 5
        elif cv > 0.3:
            stability_score = 15
        elif cv > 0.15:
            stability_score = 20
        else:
            stability_score = 25
        score.sub_scores["用电稳定性"] = stability_score
        
        # 3. 峰谷用电评分 (20分)
        peak_ratio = peak_hours_count / days
        if peak_ratio > 0.8:
            peak_valley_score = 5
        elif peak_ratio > 0.6:
            peak_valley_score = 10
        elif peak_ratio > 0.4:
            peak_valley_score = 15
        else:
            peak_valley_score = 20
        score.sub_scores["峰谷用电"] = peak_valley_score
        
        # 4. 待机功耗评分 (15分)
        if standby_power > 50:
            standby_score = 3
        elif standby_power > 30:
            standby_score = 7
        elif standby_power > 15:
            standby_score = 10
        elif standby_power > 5:
            standby_score = 12
        else:
            standby_score = 15
        score.sub_scores["待机功耗"] = standby_score
        
        # 5. 节能设备评分 (10分)
        appliance_score = min(10.0, energy_saving_appliances * 2.0)
        score.sub_scores["节能设备"] = appliance_score
        
        # 计算总分
        score.total_score = (usage_score + stability_score + peak_valley_score + 
                            standby_score + appliance_score)
        
        # 确定等级
        if score.total_score >= 90:
            score.grade = "S"
            score.title = "节能王者"
        elif score.total_score >= 80:
            score.grade = "A"
            score.title = "节能大师"
        elif score.total_score >= 70:
            score.grade = "B"
            score.title = "节能好手"
        elif score.total_score >= 60:
            score.grade = "C"
            score.title = "节能新手"
        else:
            score.grade = "D"
            score.title = "急需改进"
        
        # 生成建议
        if usage_score < 20:
            score.suggestions.append("日均用电量偏高，建议检查高耗电设备")
        if stability_score < 15:
            score.suggestions.append("用电波动较大，建议均衡每日用电")
        if peak_valley_score < 15:
            score.suggestions.append("峰时段用电过多，建议错峰用电")
        if standby_score < 10:
            score.suggestions.append("待机功耗过高，建议关闭不用的电器")
        if appliance_score < 6:
            score.suggestions.append("建议购买更多节能认证电器")
        
        if not score.suggestions:
            score.suggestions.append("您的用电习惯非常优秀，请继续保持！")
        
        return score
    
    def display_habit_score(self, score: HabitScore):
        """显示用电习惯评分结果"""
        UIComponents.print_section("评分结果")
        
        # 显示等级徽章
        ConsoleStyle.cyan()
        print("\n    ╔═══════════════════════════════════════╗")
        print("      ║                                       ║")
        print("      ║           用电习惯评级                 ║")
        print("      ║                                       ║")
        
        # 根据等级显示不同颜色
        if score.grade == "S":
            ConsoleStyle.magenta()
        elif score.grade == "A":
            ConsoleStyle.green()
        elif score.grade == "B":
            ConsoleStyle.cyan()
        elif score.grade == "C":
            ConsoleStyle.yellow()
        else:
            ConsoleStyle.red()
        
        print(f"   ║              等级: {score.grade}       ║")
        ConsoleStyle.cyan()
        print(f"   ║              {score.title:^14}        ║")
        print("    ║                                       ║")
        print("    ╚═══════════════════════════════════════╝")
        ConsoleStyle.reset()
        
        # 显示总分
        ConsoleStyle.yellow()
        print(f"\n📊 总评分: {score.total_score:.1f} / 100")
        ConsoleStyle.reset()
        
        # 显示进度条
        bars = int(score.total_score / 2.5)
        print("[", end='')
        if score.total_score >= 80:
            ConsoleStyle.green()
        elif score.total_score >= 60:
            ConsoleStyle.yellow()
        else:
            ConsoleStyle.red()
        for _ in range(bars):
            print("█", end='')
        ConsoleStyle.reset()
        for _ in range(40 - bars):
            print("─", end='')
        print("]")
        
        # 显示分项得分
        UIComponents.print_section("分项评分")
        
        headers = ["评分项目", "得分", "满分", "评价"]
        UIComponents.print_table_header(headers)
        
        max_points_map = {
            "用电量": 30,
            "用电稳定性": 25,
            "峰谷用电": 20,
            "待机功耗": 15,
            "节能设备": 10
        }
        
        for item_name, points in score.sub_scores.items():
            max_points = max_points_map.get(item_name, 10)
            
            if points >= max_points * 0.9:
                evaluation = "优秀"
            elif points >= max_points * 0.7:
                evaluation = "良好"
            elif points >= max_points * 0.5:
                evaluation = "一般"
            else:
                evaluation = "需改进"
            
            UIComponents.print_table_row([
                item_name,
                str(int(points)),
                str(int(max_points)),
                evaluation
            ])
        
        UIComponents.print_table_footer(len(headers))
        
        # 显示改进建议
        UIComponents.print_section("改进建议")
        for suggestion in score.suggestions:
            if score.total_score >= 80:
                UIComponents.print_success(suggestion)
            elif score.total_score >= 60:
                UIComponents.print_info(suggestion)
            else:
                UIComponents.print_warning(suggestion)
    
    
    def calculate_peak_valley_bill(self):
        """峰谷电价计算"""
        UIComponents.print_header("峰谷电价计算")
        
        UIComponents.print_info("峰谷电价说明:")
        print("• 峰时段(8:00-22:00): 电价较高")
        print("• 谷时段(22:00-8:00): 电价较低")
        print("• 合理利用谷时段用电可节省电费")
        
        UIComponents.print_section("输入用电数据")
        
        try:
            peak_usage = float(input("峰时段用电量(kWh): "))
            valley_usage = float(input("谷时段用电量(kWh): "))
        except ValueError:
            UIComponents.print_error("请输入有效的数字！")
            return
        
        if peak_usage < 0 or valley_usage < 0:
            UIComponents.print_error("用电量不能为负数！")
            return
        
        UIComponents.print_section("输入电价")
        
        peak_input = input("峰时段电价(元/kWh)[默认按照0.58元/kWh计算]: ").strip()
        peak_price = 0.58 if peak_input == "" else float(peak_input)
        
        valley_input = input("谷时段电价(元/kWh)[默认按照0.33元/kWh计算]: ").strip()
        valley_price = 0.33 if valley_input == "" else float(valley_input)
        
        UIComponents.progress_bar("计算中...", 800)
        
        peak_bill = peak_usage * peak_price
        valley_bill = valley_usage * valley_price
        total_bill = peak_bill + valley_bill
        total_usage = peak_usage + valley_usage
        avg_price = total_bill / total_usage if total_usage > 0 else 0
        
        normal_bill = total_usage * 0.6
        savings = normal_bill - total_bill
        
        UIComponents.print_section("峰谷电价计算结果")
        
        headers = ["时段", "用电量(kWh)", "电价(元)", "电费(元)"]
        UIComponents.print_table_header(headers)
        
        rows = [
            ["峰时段", f"{peak_usage:.2f}", f"{peak_price:.2f}", f"{peak_bill:.2f}"],
            ["谷时段", f"{valley_usage:.2f}", f"{valley_price:.2f}", f"{valley_bill:.2f}"],
            ["合计", f"{total_usage:.2f}", "-", f"{total_bill:.2f}"]
        ]
        
        for row in rows:
            UIComponents.print_table_row(row)
        
        UIComponents.print_table_footer(len(headers))
        
        ConsoleStyle.cyan()
        print(f"\n📊 平均电价: {avg_price:.3f} 元/kWh")
        ConsoleStyle.reset()
        
        # 显示节省分析
        UIComponents.print_section("节省分析")
        
        if savings > 0:
            UIComponents.print_success(f"使用峰谷电价可节省: {savings:.2f} 元")
            
            peak_ratio = peak_usage / total_usage if total_usage > 0 else 0
            ConsoleStyle.green()
            print(f"峰电占比: {peak_ratio * 100:.1f}%")
            
            if peak_ratio < 0.5:
                print("✨ 您的谷电使用率很高，节能效果显著！")
            elif peak_ratio < 0.7:
                print("💡 还有优化空间，可进一步增加谷时段用电")
            else:
                print("⚠️  峰电占比较高，建议调整用电时间")
            ConsoleStyle.reset()
        elif savings < 0:
            UIComponents.print_warning(f"当前用电模式使用峰谷电价多支出: {-savings:.2f} 元")
            ConsoleStyle.yellow()
            print("建议: 将部分用电转移到谷时段(22:00-8:00)")
            ConsoleStyle.reset()
        else:
            UIComponents.print_info("使用峰谷电价与常规电价费用相同")
        
        # 显示优化建议
        UIComponents.print_section("用电优化建议")
        
        print("适合转移到谷时段的用电行为:")
        print("• 🌙 洗衣机: 晚上10点后使用")
        print("• 🌙 热水器: 设置定时在谷时段加热")
        print("• 🌙 洗碗机: 预约谷时段运行")
        print("• 🌙 电动汽车充电: 尽量在夜间充电")
        print("• 🌙 储能设备: 谷时段充电，峰时段放电")
    
    
    def calculate_tiered_bill(self, usage: float) -> float:
        """计算阶梯电价"""
        if usage <= 200:
            return usage * 0.5
        elif usage <= 400:
            return 100 + (usage - 200) * 0.6
        else:
            return 220 + (usage - 400) * 0.8
    
    def display_usage_chart(self, usage: float):
        """显示用电量图表"""
        UIComponents.print_section("用电量图示")
        
        bars = min(40, int(usage / 5))
        ConsoleStyle.cyan()
        print(f"用电量: {usage:.1f} kWh")
        print("[", end='')
        ConsoleStyle.green()
        for _ in range(bars):
            print("█", end='')
        ConsoleStyle.reset()
        for _ in range(40 - bars):
            print("─", end='')
        print("]")
        
        ConsoleStyle.yellow()
        print("参考线: ", end='')
        ConsoleStyle.white()
        print("│节能(150) ", end='')
        ConsoleStyle.yellow()
        print("│适中(300) ", end='')
        ConsoleStyle.red()
        print("│偏高(450)│")
        ConsoleStyle.reset()
    
    def provide_basic_suggestions(self, usage: float):
        """提供基本节能建议"""
        UIComponents.print_section("节能建议")
        
        if usage > 450:
            UIComponents.print_error("用电量偏高！急需节能措施")
            print("• 🎯 空调温度设定26℃以上")
            print("• 🎯 减少大功率电器同时使用")
            print("• 🎯 检查是否有电器待机耗电")
        elif usage > 300:
            UIComponents.print_warning("用电量适中，可进一步优化")
            print("• 💡 使用定时插座控制热水器")
            print("• 💡 选择能效等级高的家电")
            print("• 💡 合理规划电器使用时间")
        elif usage > 150:
            UIComponents.print_info("用电习惯良好")
            print("• 🌟 继续保持节能习惯")
            print("• 🌟 可以考虑使用太阳能")
        else:
            UIComponents.print_success("优秀！您是节能典范")
            print("• 🏆 您的用电习惯值得学习")
            print("• 🏆 考虑分享您的节能经验")
    
    def analyze_daily_data(self, data: List[float], total: float):
        """分析每日数据"""
        avg = total / len(data)
        max_usage = max(data)
        min_usage = min(data)
        
        variance = sum((usage - avg) ** 2 for usage in data) / len(data)
        std_dev = math.sqrt(variance)
        
        UIComponents.print_section("统计分析")
        
        headers = ["指标", "数值", "单位", "评价"]
        UIComponents.print_table_header(headers)
        
        rows = [
            ["总用电量", f"{total:.2f}", "kWh", "偏高" if total > 300 else "良好"],
            ["日均用电", f"{avg:.2f}", "kWh", "偏高" if avg > 10 else "良好"],
            ["最高用电", f"{max_usage:.2f}", "kWh", "注意" if max_usage > 20 else "正常"],
            ["最低用电", f"{min_usage:.2f}", "kWh", "优秀" if min_usage < 2 else "正常"],
            ["波动程度", f"{std_dev:.2f}", "-", "较大" if std_dev > 5 else "稳定"]
        ]
        
        for row in rows:
            UIComponents.print_table_row(row)
        
        UIComponents.print_table_footer(len(headers))
        
        self.display_daily_trend(data)
        self.provide_detailed_suggestions(avg, std_dev)
    
    def display_daily_trend(self, data: List[float]):
        """显示每日趋势图"""
        UIComponents.print_section("用电趋势图")
        
        max_val = max(data)
        if max_val == 0:
            max_val = 1
        
        for i, usage in enumerate(data):
            ConsoleStyle.cyan()
            print(f"第{i+1:2d}天: ", end='')
            ConsoleStyle.reset()
            
            height = int((usage / max_val) * 30)
            ConsoleStyle.green()
            for _ in range(height):
                print("█", end='')
            ConsoleStyle.reset()
            print(f" {usage:.1f} kWh")
    
    def provide_detailed_suggestions(self, avg: float, std_dev: float):
        """提供详细建议"""
        UIComponents.print_section("个性化建议")
        
        if std_dev > 5:
            UIComponents.print_warning("用电波动较大")
            print("• 📅 建议均衡每日用电")
            print("• ⏰ 避免集中使用大功率电器")
        
        if avg > 15:
            UIComponents.print_error("日均用电量偏高")
            print("• 🔌 检查是否有待机耗电")
            print("• 🌡️  优化空调使用策略")
        elif avg < 5:
            UIComponents.print_success("优秀的节能习惯")
            print("• 🌟 继续保持绿色生活方式")
    
    def display_bill_analysis(self, usage: float, bill: float):
        """显示电费构成分析"""
        UIComponents.print_section("电费构成分析")
        
        tiers = []
        if usage > 400:
            tiers = [
                ("第一阶梯(0-200)", 100),
                ("第二阶梯(201-400)", 120),
                ("第三阶梯(400+)", (usage - 400) * 0.8)
            ]
        elif usage > 200:
            tiers = [
                ("第一阶梯(0-200)", 100),
                ("第二阶梯(200+)", (usage - 200) * 0.6)
            ]
        else:
            tiers = [("第一阶梯", usage * 0.5)]
        
        for tier_name, tier_bill in tiers:
            percentage = (tier_bill / bill) * 100
            print(f"{tier_name}: ¥{tier_bill:.2f} ({percentage:.1f}%)")
            
            bars = int(percentage / 2)
            print("  ", end='')
            ConsoleStyle.green()
            for _ in range(bars):
                print("█", end='')
            ConsoleStyle.reset()
            print()
    
    def display_appliances_table(self):
        """显示电器表格"""
        headers = ["电器名称", "功率(kW)", "建议时长", "状态"]
        UIComponents.print_table_header(headers)
        
        suggestions = {
            "空调": "4-6小时", "冰箱": "24小时", "电视机": "2-4小时",
            "洗衣机": "1小时", "热水器": "2-3小时", "电脑": "3-5小时",
            "照明": "5-8小时", "微波炉": "0.5小时"
        }
        
        for appliance, power in self.appliance_data.items():
            UIComponents.print_table_row([
                appliance,
                f"{power:.2f}",
                suggestions.get(appliance, "自定义"),
                "✅ 可用"
            ])
        
        UIComponents.print_table_footer(len(headers))
    
    def display_appliance_analysis(self, usage_hours: Dict[str, float], total_usage: float):
        """显示电器用电分析"""
        UIComponents.print_section("电器用电分析")
        
        self.animate_number(total_usage, "📊 日总用电量: ", " kWh")
        
        UIComponents.print_info("各电器用电占比:")
        
        sorted_appliances = []
        for appliance, power in self.appliance_data.items():
            usage = power * usage_hours[appliance]
            sorted_appliances.append((appliance, usage))
        
        sorted_appliances.sort(key=lambda x: x[1], reverse=True)
        
        for appliance, usage in sorted_appliances:
            percentage = (usage / total_usage) * 100 if total_usage > 0 else 0
            
            print(f"{appliance}: {usage:.1f} kWh ({percentage:.1f}%)")
            
            bars = int(percentage)
            print("  ", end='')
            ConsoleStyle.green()
            for _ in range(bars):
                print("█", end='')
            ConsoleStyle.reset()
            print()
        
        self.provide_appliance_suggestions(usage_hours)
    
    def provide_appliance_suggestions(self, usage_hours: Dict[str, float]):
        """提供电器使用建议"""
        UIComponents.print_section("电器使用建议")
        
        for appliance, hours in usage_hours.items():
            if appliance == "空调" and hours > 8:
                UIComponents.print_warning("空调使用时间过长")
                print("• 建议使用定时功能，避免整夜运行")
            
            if appliance == "热水器" and hours > 4:
                UIComponents.print_info("热水器可优化")
                print("• 建议使用前1小时开启，使用后关闭")
            
            if appliance == "冰箱":
                UIComponents.print_success("冰箱使用合理")


def print_welcome():
    """打印欢迎界面"""
    ConsoleStyle.clear_screen()
    
    ConsoleStyle.green()
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║         🌿 家庭用电节能分析系统 🌿                          ║
    ║                                                            ║
    ║             绿色中国 · 智慧生活 · 节能环保                   ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    ConsoleStyle.reset()
    
    UIComponents.progress_bar("系统初始化", 800)


def print_menu():
    """打印主菜单"""
    UIComponents.print_header("主菜单")
    
    ConsoleStyle.cyan()
    print("请选择功能:")
    ConsoleStyle.reset()
    
    print("┌───────────────┬────────────────────────────────────────────┐")
    print("│   选项        │                功能描述                     │")
    print("├───────────────┼────────────────────────────────────────────┤")
    print("│      1        │ 💰 根据电费计算用电数据                     │")
    print("│      2        │ 📊 输入数据分析给出建议                     │")
    print("│      3        │ ⚡ 输入数据计算当月电费                     │")
    print("│      4        │ 🔌 分析各项电器用电情况                     │")
    print("│      5        │ 🏠 电器管理(添加/删除/修改)                 │")
    print("│      6        │ ⭐ 用电习惯评分评级                         │")
    print("│      7        │ 🌙 峰谷电价计算                             │")
    print("│      8        │ 🚪 退出程序                                 │")
    print("└───────────────┴────────────────────────────────────────────┘")


def main():
    """主函数"""
    ConsoleStyle.init()
    analyzer = EnergyAnalyzer()
    
    print_welcome()
    
    while True:
        ConsoleStyle.clear_screen()
        print_menu()
        
        ConsoleStyle.yellow()
        choice = input("\n请输入选择 (1-8): ")
        ConsoleStyle.reset()
        
        if choice == '1':
            analyzer.calculate_usage_from_bill()
        elif choice == '2':
            analyzer.analyze_and_suggest()
        elif choice == '3':
            analyzer.calculate_monthly_bill()
        elif choice == '4':
            analyzer.analyze_appliances()
        elif choice == '5':
            analyzer.manage_appliances()
        elif choice == '6':
            analyzer.evaluate_habit()
        elif choice == '7':
            analyzer.calculate_peak_valley_bill()
        elif choice == '8':
            UIComponents.print_header("感谢使用")
            ConsoleStyle.green()
            print("💚 节约用电，共建绿色中国！")
            print("🌍 保护环境，从点滴做起！")
            print('🌟 愿您的生活更加节能环保，享受绿色生活！')
            print('版权声明：本程序由徐晨凯编码完成，刘慕阳策划完成，持有国家版权登记证（数字版），仅可用于学习使用，转载请注明出处，若作者发现侵权行为，将追究法律责任。')
            ConsoleStyle.reset()
            # 增加退出等待时间
            time.sleep(3)  # 等待3秒
            break
        else:
            UIComponents.print_error("无效选择，请重新输入！")
            ConsoleStyle.sleep(1000)
            continue
        
        if choice != '8':
            ConsoleStyle.yellow()
            input("\n⏎ 按回车键返回主菜单...")
            ConsoleStyle.reset()


if __name__ == "__main__":
    main()
