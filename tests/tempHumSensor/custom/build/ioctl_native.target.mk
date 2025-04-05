# This file is generated by gyp; do not edit.

TOOLSET := target
TARGET := ioctl_native
DEFS_Debug := \
	'-DNODE_GYP_MODULE_NAME=ioctl_native' \
	'-DUSING_UV_SHARED=1' \
	'-DUSING_V8_SHARED=1' \
	'-DV8_DEPRECATION_WARNINGS=1' \
	'-D_GLIBCXX_USE_CXX11_ABI=1' \
	'-D_LARGEFILE_SOURCE' \
	'-D_FILE_OFFSET_BITS=64' \
	'-D__STDC_FORMAT_MACROS' \
	'-DOPENSSL_NO_PINSHARED' \
	'-DOPENSSL_THREADS' \
	'-DBUILDING_NODE_EXTENSION' \
	'-DDEBUG' \
	'-D_DEBUG'

# Flags passed to all source files.
CFLAGS_Debug := \
	-fPIC \
	-pthread \
	-Wall \
	-Wextra \
	-Wno-unused-parameter \
	-g \
	-O0

# Flags passed to only C files.
CFLAGS_C_Debug :=

# Flags passed to only C++ files.
CFLAGS_CC_Debug := \
	-fno-rtti \
	-fno-exceptions \
	-fno-strict-aliasing \
	-std=gnu++17

INCS_Debug := \
	-I/home/windy/.cache/node-gyp/22.14.0/include/node \
	-I/home/windy/.cache/node-gyp/22.14.0/src \
	-I/home/windy/.cache/node-gyp/22.14.0/deps/openssl/config \
	-I/home/windy/.cache/node-gyp/22.14.0/deps/openssl/openssl/include \
	-I/home/windy/.cache/node-gyp/22.14.0/deps/uv/include \
	-I/home/windy/.cache/node-gyp/22.14.0/deps/zlib \
	-I/home/windy/.cache/node-gyp/22.14.0/deps/v8/include

DEFS_Release := \
	'-DNODE_GYP_MODULE_NAME=ioctl_native' \
	'-DUSING_UV_SHARED=1' \
	'-DUSING_V8_SHARED=1' \
	'-DV8_DEPRECATION_WARNINGS=1' \
	'-D_GLIBCXX_USE_CXX11_ABI=1' \
	'-D_LARGEFILE_SOURCE' \
	'-D_FILE_OFFSET_BITS=64' \
	'-D__STDC_FORMAT_MACROS' \
	'-DOPENSSL_NO_PINSHARED' \
	'-DOPENSSL_THREADS' \
	'-DBUILDING_NODE_EXTENSION'

# Flags passed to all source files.
CFLAGS_Release := \
	-fPIC \
	-pthread \
	-Wall \
	-Wextra \
	-Wno-unused-parameter \
	-O3 \
	-fno-omit-frame-pointer

# Flags passed to only C files.
CFLAGS_C_Release :=

# Flags passed to only C++ files.
CFLAGS_CC_Release := \
	-fno-rtti \
	-fno-exceptions \
	-fno-strict-aliasing \
	-std=gnu++17

INCS_Release := \
	-I/home/windy/.cache/node-gyp/22.14.0/include/node \
	-I/home/windy/.cache/node-gyp/22.14.0/src \
	-I/home/windy/.cache/node-gyp/22.14.0/deps/openssl/config \
	-I/home/windy/.cache/node-gyp/22.14.0/deps/openssl/openssl/include \
	-I/home/windy/.cache/node-gyp/22.14.0/deps/uv/include \
	-I/home/windy/.cache/node-gyp/22.14.0/deps/zlib \
	-I/home/windy/.cache/node-gyp/22.14.0/deps/v8/include

OBJS := \
	$(obj).target/$(TARGET)/ioctl_native.o

# Add to the list of files we specially track dependencies for.
all_deps += $(OBJS)

# CFLAGS et al overrides must be target-local.
# See "Target-specific Variable Values" in the GNU Make manual.
$(OBJS): TOOLSET := $(TOOLSET)
$(OBJS): GYP_CFLAGS := $(DEFS_$(BUILDTYPE)) $(INCS_$(BUILDTYPE))  $(CFLAGS_$(BUILDTYPE)) $(CFLAGS_C_$(BUILDTYPE))
$(OBJS): GYP_CXXFLAGS := $(DEFS_$(BUILDTYPE)) $(INCS_$(BUILDTYPE))  $(CFLAGS_$(BUILDTYPE)) $(CFLAGS_CC_$(BUILDTYPE))

# Suffix rules, putting all outputs into $(obj).

$(obj).$(TOOLSET)/$(TARGET)/%.o: $(srcdir)/%.cc FORCE_DO_CMD
	@$(call do_cmd,cxx,1)

# Try building from generated source, too.

$(obj).$(TOOLSET)/$(TARGET)/%.o: $(obj).$(TOOLSET)/%.cc FORCE_DO_CMD
	@$(call do_cmd,cxx,1)

$(obj).$(TOOLSET)/$(TARGET)/%.o: $(obj)/%.cc FORCE_DO_CMD
	@$(call do_cmd,cxx,1)

# End of this set of suffix rules
### Rules for final target.
LDFLAGS_Debug := \
	-pthread \
	-rdynamic

LDFLAGS_Release := \
	-pthread \
	-rdynamic

LIBS :=

$(obj).target/ioctl_native.node: GYP_LDFLAGS := $(LDFLAGS_$(BUILDTYPE))
$(obj).target/ioctl_native.node: LIBS := $(LIBS)
$(obj).target/ioctl_native.node: TOOLSET := $(TOOLSET)
$(obj).target/ioctl_native.node: $(OBJS) FORCE_DO_CMD
	$(call do_cmd,solink_module)

all_deps += $(obj).target/ioctl_native.node
# Add target alias
.PHONY: ioctl_native
ioctl_native: $(builddir)/ioctl_native.node

# Copy this to the executable output path.
$(builddir)/ioctl_native.node: TOOLSET := $(TOOLSET)
$(builddir)/ioctl_native.node: $(obj).target/ioctl_native.node FORCE_DO_CMD
	$(call do_cmd,copy)

all_deps += $(builddir)/ioctl_native.node
# Short alias for building this executable.
.PHONY: ioctl_native.node
ioctl_native.node: $(obj).target/ioctl_native.node $(builddir)/ioctl_native.node

# Add executable to "all" target.
.PHONY: all
all: $(builddir)/ioctl_native.node

