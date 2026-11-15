output "steamos_vm_id" {
  value = proxmox_virtual_environment_vm.steamos.id
}

output "steamos_vm_name" {
  value = proxmox_virtual_environment_vm.steamos.name
}

output "steamos_gpu_mapping" {
  value = var.gpu_mapping
}
