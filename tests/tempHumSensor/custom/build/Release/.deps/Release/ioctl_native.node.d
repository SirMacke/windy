cmd_Release/ioctl_native.node := ln -f "Release/obj.target/ioctl_native.node" "Release/ioctl_native.node" 2>/dev/null || (rm -rf "Release/ioctl_native.node" && cp -af "Release/obj.target/ioctl_native.node" "Release/ioctl_native.node")
