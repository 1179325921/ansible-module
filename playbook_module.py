from ansible import context
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor


class MyCallBack(CallbackBase):
    """
    重写callbackBase类的部分方法
    """

    def __init__(self, *args, **kwargs):
        super(MyCallBack, self).__init__(*args, **kwargs)  # 初始化父类方法
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}

    def v2_runner_on_unreachable(self, result):  # result 为父类中获取所有执行结果信息的对象
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result):
        self.task_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.task_failed[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        self.task_ok[result._host.get_name()] = result

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                "ok": t['ok'],
                "changed": t['changed'],
                "unreachable": t['unreachable'],
                "skipped": t['skipped'],
                "failed": t['failures']
            }


loader = DataLoader()
inventory = InventoryManager(loader=loader, sources="/etc/ansible/hosts")
variable_manager = VariableManager(loader=loader, inventory=inventory)
context.CLIARGS = ImmutableDict(listtags=False, listtasks=False,
                                listhosts=False, syntax=False,
                                connection="smart", module_path=None,
                                forks=5, private_key_file=None,
                                ssh_common_args=None, ssh_extra_args=None,
                                sftp_extra_args=None, scp_extra_args=None,
                                become=False, become_method=None,
                                become_user=None, start_at_task=None,
                                verbosity=None, check=False)
# PlaybookExecutor执行playbook
playbook = PlaybookExecutor(loader=loader, inventory=inventory,
                            passwords={}, variable_manager=variable_manager,
                            playbooks=['/etc/ansible/playbooks/test_ping.yml'])
callback = MyCallBack()
playbook._tqm._stdout_callback = callback
playbook.run()

results_raw = {'skipped': {}, 'failed': {}, 'success': {}, "status": {}, 'unreachable': {}, "changed": {}}


for host, result in callback.task_ok.items():
    results_raw['success'][host] = result._result # _result属性来获取任务执行的结果
for host, result in callback.task_failed.items():
    results_raw['failed'][host] = result._result
for host, result in callback.task_unreachable.items():
    results_raw['unreachable'][host] = result._result
print(results_raw)
