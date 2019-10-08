from ansible import context
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.playbook.play import Play
from ansible.module_utils.common.collections import ImmutableDict
from ansible.plugins.callback import CallbackBase


class MyCallBack(CallbackBase):
    """
    重写callbackBase类的部分方法
    """

    def __init__(self, *args, **kwargs):
        super(MyCallBack, self).__init__(*args, **kwargs)  # 初始化父类方法
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):  # result 为父类中获取所有执行结果信息的对象
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.host_failed[result._host.get_name()] = result


load = DataLoader()
inventory = InventoryManager(loader=load, sources="hosts")
variable_manager = VariableManager(loader=load, inventory=inventory)
# 执行参数选项 verbosity=0默认是0，应该不填也没关系，但实际缺少这个参数就会报错。
context.CLIARGS = ImmutableDict(listtags=False, listtasks=False,
                                listhosts=False, syntax=False,
                                connection="ssh", module_path=None,
                                forks=5, private_key_file=None,
                                ssh_common_args=None, ssh_extra_args=None,
                                sftp_extra_args=None, scp_extra_args=None,
                                become=False, become_method=None,
                                become_user=None, verbosity=0, check=False)
# Play 执行对象和模块
play_source = dict(
    name='Ansible Play ad-hoc test',  # 任务执行的名称
    hosts='192.168.*',  # 控制着任务执行的目标主机，可以通过逗号填入多台主机，或者正则匹配，或者主机组
    gather_facts="no",  # 执行任务之前去获取响应主机的相关信息，建议关闭，提高执行效率
    tasks=[
        # 以dict的方式实现，一个任务一个dict,可以写多个，module 为对应模块，args为传入的参数
        dict(action=dict(module='shell', args='ls'))
        # dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
    ]
)
play = Play().load(play_source, variable_manager=variable_manager, loader=load)
callback = MyCallBack()
# passwords没有实际作用，实际中密码已经写在文件中了
tqm = TaskQueueManager(inventory=inventory, variable_manager=variable_manager,
                       loader=load, passwords={}, stdout_callback=callback)
tqm.run(play)

result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}

for host, result in callback.host_ok.items():
    result_raw['success'][host] = result._result  # _result属性来获取任务执行的结果
for host, result in callback.host_failed.items():
    result_raw['failed'][host] = result._result
for host, result in callback.host_unreachable.items():
    result_raw['unreachable'][host] = result._result

print(result_raw)
