packer {
  required_version = ">= 1.9.0"
}

variable "iso_input" {
  type    = string
  default = "iso/bazzite-stable-amd64.iso"
}

variable "iso_output" {
  type    = string
  default = "output/bazzite-autoinstall.iso"
}

variable "kickstart_file" {
  type    = string
  default = "../autoinstall/kickstart/steamos-ks.cfg"
}

source "null" "steamos_iso" {
  communicator = "none"
}

build {
  name    = "steamos-autoinstall-iso"
  sources = ["source.null.steamos_iso"]

  provisioner "shell-local" {
    inline = [
      "bash ../scripts/build-linux-iso.sh ${var.iso_input} ${var.iso_output} ${var.kickstart_file} 'inst.ks=cdrom:/steamos-ks.cfg'"
    ]
  }
}
