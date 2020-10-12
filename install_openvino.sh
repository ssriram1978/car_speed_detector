#!/bin/bash
echo "cd ~/Downloads/"
cd ~/Downloads/
echo "sudo mkdir -p /opt/intel/openvino"
sudo mkdir -p /opt/intel/openvino
echo "wget https://download.01.org/opencv/2020/openvinotoolkit/2020.1/l_openvino_toolkit_runtime_raspbian_p_2020.1.023.tgz"
wget https://download.01.org/opencv/2020/openvinotoolkit/2020.1/l_openvino_toolkit_runtime_raspbian_p_2020.1.023.tgz
echo "sudo tar -xf  l_openvino_toolkit_runtime_raspbian_p_*.tgz --strip 1 -C /opt/intel/openvino"
sudo tar -xf  l_openvino_toolkit_runtime_raspbian_p_*.tgz --strip 1 -C /opt/intel/openvino
echo "source /opt/intel/openvino/bin/setupvars.sh"
source /opt/intel/openvino/bin/setupvars.sh
echo "sudo usermod -a -G users \"$(whoami)\""
sudo usermod -a -G users "$(whoami)"
echo "source /opt/intel/openvino/bin/setupvars.sh"
source /opt/intel/openvino/bin/setupvars.sh
source "sh /opt/intel/openvino/install_dependencies/install_NCS_udev_rules.sh"
sh /opt/intel/openvino/install_dependencies/install_NCS_udev_rules.sh
