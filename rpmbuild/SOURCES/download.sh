#!/usr/bin/env bash

declare -A packages

packages["td"]="https://github.com/tdlib/td/archive/refs/tags/v1.8.0.tar.gz"
packages["pjproject"]="https://github.com/pjsip/pjproject/archive/refs/tags/2.12.tar.gz"
packages["spdlog"]="https://github.com/gabime/spdlog/archive/refs/tags/v1.9.2.tar.gz"
packages["tg2sip"]="https://github.com/Infactum/tg2sip/archive/refs/tags/v1.3.0.tar.gz"

echo "Downloading packages from Github"

for package in "${!package[@]}"; do
	echo "Start downloading ${package}"
	wget ${packages["${package}"]}
	echo "----------------------------"
done
