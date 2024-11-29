# **对比原始设计的改进**
1. 简化设计，更适合量产
1. 修改所有1.0mm的连接器为插针1.5mm，fix原版连接器容易脱落
1. 删除base板，将base板子集成到了主板上
1. 添加switching ldo，供电电流最大2A，fix原版mcu ldo电流过小，温度过高issue
1. 将led ring，buzzer 控制从ESP32 改到stm32 mcu
1. 更合理的布局
1. 降低量产成本


--原理图基于并且拥有者稚晖君，原理图修改版和PCB设计木子晓文。--

Based on ZhiHuiJun schematic, the oringal design owned by ZhiHuiJun. Schematic modified and PCB designed by Muzi Xiaowen. 
The schematic and PCB design are free and open, and comes with ABSOLUTELY NO WARRANTY, to the extent permitted by applicable law.

References
https://github.com/peng-zhihui/Dummy-Robot
