variable "proxmox_api_url" {
  type        = string
  description = "Proxmox VE API base URL, e.g. https://<proxmox-host>:8006/api2/json"
  default     = "https://<proxmox-host>:8006/api2/json"
}

variable "proxmox_api_token_id" {
  type        = string
  description = "Proxmox API token id, format: <user>@<realm>!<token_name>"
  sensitive   = true
}

variable "proxmox_api_token_secret" {
  type        = string
  description = "Proxmox API token secret"
  sensitive   = true
}

variable "proxmox_tls_insecure" {
  type        = bool
  description = "Skip TLS verification for the Proxmox API"
  default     = true
}

variable "proxmox_host" {
  type        = string
  description = "Proxmox host, used for SSH access during bootstrap"
  default     = "<proxmox-host>"
}

variable "proxmox_node" {
  type        = string
  description = "Proxmox node name"
  default     = "homelab"
}

variable "storage_pool" {
  type        = string
  description = "Proxmox storage pool for VM disks"
  default     = "vmstore"
}

variable "bridge_network" {
  type        = string
  description = "Proxmox network bridge for the VM"
  default     = "vmbr0"
}

variable "vm_id" {
  type        = number
  description = "Proxmox VM ID"
  default     = 110
}

variable "vm_name" {
  type        = string
  description = "Proxmox VM name"
  default     = "steamos-vm"
}

variable "vm_os_type" {
  type        = string
  description = "Proxmox guest OS type for the VM"
  default     = "l26"
}

variable "vm_cores" {
  type        = number
  description = "Number of vCPU cores for the SteamOS VM"
  default     = 8
}

variable "vm_memory" {
  type        = number
  description = "Dedicated memory in MB for the SteamOS VM"
  default     = 16384
}

variable "vm_disk_size" {
  type        = number
  description = "Disk size in GB for the SteamOS VM"
  default     = 500
}

variable "vm_iso" {
  type        = string
  description = "SteamOS / Bazzite ISO file name on the hdd-iso storage"
  default     = "bazzite-stable-amd64.iso"
}

variable "autoinstall_enabled" {
  type        = bool
  description = "Use the Packer-built SteamOS autoinstall ISO instead of the Bazzite release ISO"
  default     = false
}

variable "autoinstall_iso" {
  type        = string
  description = "SteamOS autoinstall ISO file name on the hdd-iso storage"
  default     = "bazzite-stable-amd64-autoinstall.iso"
}

variable "gpu_pci_ids" {
  type        = string
  description = "GPU PCI IDs in form '0000:xx:yy.0;0000:xx:yy.1' (GPU + audio function)"
  default     = "0000:01:00.0;0000:01:00.1"
}

variable "gpu_mapping" {
  type        = string
  description = "Named PCI mapping for the GPU, e.g. 'nvidia-gpu'"
  default     = "nvidia-gpu"
}

variable "gpu_pcie" {
  type        = bool
  description = "Use PCIe slot for the GPU (requires q35 machine type)"
  default     = false
}

variable "gpu_rombar" {
  type        = bool
  description = "Expose the GPU firmware ROM to the guest"
  default     = false
}

variable "gpu_xvga" {
  type        = bool
  description = "Mark the GPU as primary display of the VM"
  default     = true
}

variable "controller_enabled" {
  type        = bool
  description = "Enable Steam Controller 2 USB passthrough"
  default     = false
}

variable "controller_host" {
  type        = string
  description = "Steam Controller 2 USB device id in form '<MANUFACTURER>:<ID>'"
  default     = ""
}

variable "controller_mapping" {
  type        = string
  description = "Named USB mapping for the Steam Controller 2"
  default     = "steam-controller-2"
}

variable "controller_usb3" {
  type        = bool
  description = "Expose the Steam Controller 2 as USB3 device"
  default     = false
}
