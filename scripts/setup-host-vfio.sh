#!/bin/bash
# Enable IOMMU + VFIO on the Proxmox host.
# Run ON THE PROXMOX HOST before `terraform apply`.
#
# Set the GPU + audio function IDs for your card (find them with `lspci -nn`,
# they look like 10de:xxxx / 10de:yyyy):
#   GPU_IDS="10de:xxxx,10de:yyyy" sudo -E bash scripts/setup-host-vfio.sh

set -e

GPU_IDS="${GPU_IDS:?set GPU_IDS to your GPU and audio device IDs, see lspci -nn}"

echo "==> Setting GRUB cmdline (IOMMU + VFIO)"
sudo sed -i 's|GRUB_CMDLINE_LINUX_DEFAULT=.*|GRUB_CMDLINE_LINUX_DEFAULT="quiet amd_iommu=on iommu=pt"|' /etc/default/grub

echo "==> Loading vfio-pci module"
echo "vfio-pci" | sudo tee /etc/modules-load.d/vfio.conf >/dev/null

echo "==> Blacklisting nouveau / nvidiafb"
echo "blacklist nouveau" | sudo tee /etc/modprobe.d/vfio.conf >/dev/null
echo "blacklist nvidiafb" | sudo tee -a /etc/modprobe.d/vfio.conf >/dev/null
echo "options vfio-pci ids=${GPU_IDS}" | sudo tee -a /etc/modprobe.d/vfio.conf >/dev/null

echo "==> Rebuilding GRUB / initramfs"
sudo update-grub
sudo update-initramfs -u

echo "==> Rebooting into IOMMU/VFIO mode"
sudo reboot
