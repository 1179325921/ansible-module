from ansible import context
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor

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
                                become_user=None,
                                verbosity=None, check=False)
# PlaybookExecutor执行playbook
playbook = PlaybookExecutor(loader=loader, inventory=inventory,
                            passwords={}, variable_manager=variable_manager,
                            playbooks=['/etc/ansible/playbooks/test_ping.yml'])
playbook.run()