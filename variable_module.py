from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager

loader = DataLoader()
inventory = InventoryManager(loader=loader, sources='hosts')
variable_manager = VariableManager(loader=loader, inventory=inventory)
host = inventory.get_host('192.168.10.150')
print(variable_manager.get_vars(host=host))
variable_manager.set_host_variable(host=host, varname="ansible_ssh_pass", value="1111111")
print(variable_manager.get_vars(host=host))
print(variable_manager.__dict__)
variable_manager._extra_vars = {'mysite': "ys.blog.com"}
print(variable_manager.get_vars(host=host))