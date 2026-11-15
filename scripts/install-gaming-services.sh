#!/bin/bash
# Install Moonlight + Sunshine inside the SteamOS gaming VM.
# Run from the Proxmox host via terraform bootstrap, or manually inside the VM.

set -e

echo "[steam-gpu] Installing Moonlight + Sunshine + EmuDeck"

# --- EmuDeck (emulated consoles: Dolphin, PCSX2, RetroArch) ---
echo "==> Installing EmuDeck"
if command -v flatpak >/dev/null 2>&1; then
  flatpak remote-add --if-not-exists flathub https://flathub.org/flathub.flatpakrepo
  flatpak install -y flathub org.EmuDeck.EmuDeck
else
  curl -fsSL https://emudeck.org | bash
fi

# --- Sunshine (host streaming server) ---
SUNSHINE_TAG=$(curl -fsSL https://api.github.com/repos/LizardByte/Sunshine/releases/latest | grep -oP '"tag_name":\s*"\K[^"]+')
SUNSHINE_FILE="Sunshine_${SUNSHINE_TAG}_amd64.deb"
SUNSHINE_URL="https://github.com/LizardByte/Sunshine/releases/download/${SUNSHINE_TAG}/${SUNSHINE_FILE}"

if [ ! -f "/tmp/${SUNSHINE_FILE}" ]; then
  curl -fsSL -o "/tmp/${SUNSHINE_FILE}" "${SUNSHINE_URL}"
fi

if command -v dnf >/dev/null 2>&1; then
  sudo rpm -U "/tmp/${SUNSHINE_FILE}"
else
  sudo dpkg -i "/tmp/${SUNSHINE_FILE}"
fi

sudo systemctl enable --now sunshine

# --- Moonlight (client streamer) ---
MOONLIGHT_TAG=$(curl -fsSL https://api.github.com/repos/moonlight-stream/moonlight-installer/releases/latest | grep -oP '"tag_name":\s*"\K[^"]+')
MOONLIGHT_FILE="moonlight-installer_${MOONLIGHT_TAG}_amd64.deb"
MOONLIGHT_URL="https://github.com/moonlight-stream/moonlight-installer/releases/download/${MOONLIGHT_TAG}/${MOONLIGHT_FILE}"

if [ ! -f "/tmp/${MOONLIGHT_FILE}" ]; then
  curl -fsSL -o "/tmp/${MOONLIGHT_FILE}" "${MOONLIGHT_URL}"
fi

if command -v dnf >/dev/null 2>&1; then
  sudo rpm -U "/tmp/${MOONLIGHT_FILE}"
else
  sudo dpkg -i "/tmp/${MOONLIGHT_FILE}"
fi

sudo systemctl enable --now moonlight

echo "[steam-gpu] Moonlight + Sunshine + EmuDeck installed"
echo "[steam-gpu] Sunshine API: http://<proxmox-host>:47989"
