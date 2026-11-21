LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)

subdirs := $(addprefix $(LOCAL_PATH)/,$(addsuffix /Android.mk, \
		libnvram_daemon_callback \
		libnvram \
	))

include $(subdirs)

