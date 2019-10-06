from ansible import context
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.playbook.play import Play
from ansible.module_utils.common.collections import ImmutableDict

load = DataLoader()
inventory = InventoryManager(loader=load, sources="hosts")
variable_manager = VariableManager(loader=load, inventory=inventory)
# 执行参数选项
context.CLIARGS = ImmutableDict(listtags=False, listtasks=False,
                                listhosts=False, syntax=False,
                                connection="smart", module_path=None,
                                forks=5, private_key_file=None,
                                ssh_common_args=None, ssh_extra_args=None,
                                sftp_extra_args=None, scp_extra_args=None,
                                become=False, become_method=None,
                                become_user=None,
                                verbosity=None, check=False)
# Play 执行对象和模块
play_source = dict(
    name='Ansible Play ad-hoc test',  # 任务执行的名称
    hosts='192.168.*',  # 控制着任务执行的目标主机，可以通过逗号填入多台主机，或者正则匹配，或者主机组
    gather_facts="no",  # 执行任务之前去获取响应主机的相关信息，建议关闭，提高执行效率
    tasks=[
        # 以dict的方式实现，一个任务一个dict,可以写多个，module 为对应模块，args为传入的参数
        dict(action=dict(module='shell', args='ls'), register='shell_out')
        # dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
    ]
)
play = Play().load(play_source, variable_manager=variable_manager, loader=load)
# passwords没有实际作用，实际中密码已经写在文件中了
tqm = TaskQueueManager(inventory=inventory, variable_manager=variable_manager,
                       loader=load, passwords={})
result = tqm.run(play)
print(result)
