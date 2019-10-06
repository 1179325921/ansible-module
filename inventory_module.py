from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

#  实例化一个DataLoader对象，用户json，yaml解析
loader = DataLoader()
inventory_manager = InventoryManager(loader=loader, sources='hosts')

# get_hosts()获取所有主机资源
print(inventory_manager.get_hosts())
# get_groups_dict()方法，查看主机组资源
print(inventory_manager.get_groups_dict())
# add_group()添加组
inventory_manager.add_group("node")
# add_host()方法，添加主机到指定的主机组
inventory_manager.add_host("192.168.1.110", "node", 22)
print(inventory_manager.get_groups_dict())
# get_host() 获取指定的主机对象
print(inventory_manager.get_host(hostname="192.168.1.110"))
