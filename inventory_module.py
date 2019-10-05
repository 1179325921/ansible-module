from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager


loader = DataLoader()
inventory_manager = InventoryManager(loader=loader, sources='hosts')

print(inventory_manager.get_hosts())
print(inventory_manager.get_groups_dict())
inventory_manager.add_group("node")
inventory_manager.add_host("192.168.1.110", "node", 22)
print(inventory_manager.get_groups_dict())
print(inventory_manager.get_host(hostname="192.168.1.110"))
