LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)

# Explicitly mark gdbserver as "eng" so that it doesn't
# get included in user or SDK builds. (GPL issues)
#
LOCAL_SRC_FILES := libnvram.so
LOCAL_MODULE := libnvram
LOCAL_MODULE_SUFFIX := .so
#LOCAL_PREBUILT_MODULE_FILE
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_MODULE_TAGS := debug
include $(BUILD_PREBUILT)

# Any prebuilt files with default TAGS can use the below:
#prebuilt_files := libnvram.so