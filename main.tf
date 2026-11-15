# SteamOS gaming VM on Proxmox VE with NVIDIA GPU passthrough and
# Steam Controller 2 USB passthrough, streamed via Sunshine + Moonlight.

provider "proxmox" {
  endpoint  = var.proxmox_api_url
  api_token = "${var.proxmox_api_token_id}=${var.proxmox_api_token_secret}"
  insecure  = var.proxmox_tls_insecure

  ssh {
    agent    = true
    username = "root"
  }
}

resource "proxmox_virtual_environment_vm" "steamos" {
  name        = var.vm_name
  node_name   = var.proxmox_node
  vm_id       = var.vm_id
  description = "SteamOS gaming VM - NVIDIA GPU passthrough + Steam Controller 2"

  machine = "pc"
  bios    = "ovmf"

  cpu {
    cores   = var.vm_cores
    sockets = 1
    type    = "host"
  }

  memory {
    dedicated = var.vm_memory
  }

  disk {
    datastore_id = var.storage_pool
    file_format  = "raw"
    interface    = "virtio0"
    size         = var.vm_disk_size
  }

  network_device {
    bridge = var.bridge_network
  }

  hostpci {
    device  = "hostpci0"
    id      = var.gpu_pci_ids
    mapping = var.gpu_mapping
    pcie    = var.gpu_pcie
    rombar  = var.gpu_rombar
    xvga    = var.gpu_xvga
  }

  vga {
    type = "std"
  }

  efi_disk {
    datastore_id      = var.storage_pool
    file_format       = "raw"
    type              = "4m"
    pre_enrolled_keys = true
  }

  tpm_state {
    datastore_id = var.storage_pool
    version      = "v2.0"
  }

  dynamic "usb" {
    for_each = var.controller_enabled ? ["hostusb0"] : []
    content {
      host    = var.controller_host
      mapping = var.controller_mapping
      usb3    = var.controller_usb3
    }
  }

  cdrom {
    file_id   = var.autoinstall_enabled ? "hdd-iso:iso/${var.autoinstall_iso}" : "hdd-iso:iso/${var.vm_iso}"
    interface = "ide0"
  }

  boot_order = ["ide0", "virtio0"]

  operating_system {
    type = var.vm_os_type
  }

  tags = ["steamos", "linux", "gaming", "terraform"]

  started = true
}

resource "null_resource" "steamos_bootstrap" {
  depends_on = [proxmox_virtual_environment_vm.steamos]

  provisioner "local-exec" {
    command = <<-EOT
      echo "Waiting for SteamOS VM (${var.vm_name}, ID ${var.vm_id}) to boot..."
      VM_IP=""
      for i in $(seq 1 60); do
        VM_IP=$(ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@${var.proxmox_host} \
          "qm guest cmd ${var.vm_id} network-get-interfaces" 2>/dev/null \
          | grep -oP '"ip-address": "\K[0-9.]+' | head -1)
        if [ -n "$${VM_IP}" ]; then
          echo "SteamOS VM IP found: $${VM_IP} (after $((i * 10)) seconds)"
          break
        fi
        sleep 10
      done
      if [ -z "$${VM_IP}" ]; then
        echo "ERROR: SteamOS VM IP not found"
        exit 1
      fi
      SSH_READY=false
      for i in $(seq 1 30); do
        if nc -zw 3 "$${VM_IP}" 22 2>/dev/null; then
          SSH_READY=true
          break
        fi
        sleep 5
      done
      if [ "$${SSH_READY}" != "true" ]; then
        echo "ERROR: SSH not reachable on SteamOS VM"
        exit 1
      fi
      echo "Uploading gaming services install script..."
      scp -o StrictHostKeyChecking=no ${path.module}/scripts/install-gaming-services.sh root@$${VM_IP}:/tmp/install-gaming-services.sh
      ssh -o StrictHostKeyChecking=no root@$${VM_IP} "bash /tmp/install-gaming-services.sh"
    EOT
  }

  triggers = {
    vm_id = proxmox_virtual_environment_vm.steamos.id
  }
}
