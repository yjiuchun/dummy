import mujoco
import mujoco.viewer
import os
import numpy as np
from pid import PID
try:
    # 获取XML文件的绝对路径
    xml_path = os.path.join(os.path.expanduser("~"), "dummy/src/dummy_mujoco/dummy_xml/dummy.xml")

    # 加载模型
    model = mujoco.MjModel.from_xml_path(xml_path)
    data = mujoco.MjData(model)
    j1_pid = PID(kp=20, ki=0.0, kd=10, ki_limit=1)
    j2_pid = PID(kp=10, ki=0.0, kd=2.5, ki_limit=1)
    j3_pid = PID(kp=8, ki=0.0, kd=3.5, ki_limit=1)
    j4_pid = PID(kp=5, ki=0.0, kd=3.5, ki_limit=1)
    j5_pid = PID(kp=3, ki=0.0, kd=3.5, ki_limit=1)

    js_target = np.array([0, 0, 0, 0, 0])
    js_T = np.array([0, 0, 0, 0, 0])

    # 打开查看器并运行模拟
    with mujoco.viewer.launch_passive(model, data) as viewer:
        # 模拟循环
        while viewer.is_running():
            js_current_pos = data.qpos[0:5]
            js_current_vel = data.qvel[0:5]
            js_T[0] = j1_pid.out(js_current_pos[0], js_current_vel[0], js_target[0])
            js_T[1] = j2_pid.out(js_current_pos[1], js_current_vel[1], js_target[1])
            js_T[2] = j3_pid.out(js_current_pos[2], js_current_vel[2], js_target[2])
            js_T[3] = j4_pid.out(js_current_pos[3], js_current_vel[3], js_target[3])
            js_T[4] = j5_pid.out(js_current_pos[4], js_current_vel[4], js_target[4])  
            data.ctrl[0:5] = js_T

            # 步进模拟
            mujoco.mj_step(model, data)
            
            # 同步查看器
            viewer.sync()
            
except Exception as e:
    print(f"错误: {e}")