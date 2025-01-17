# Copyright 2021 Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import acl
from atlas_utils.constants import *
from atlas_utils.lib.atlasutil_so import libatlas

def check_ret(message, ret):
    if ret != ACL_ERROR_NONE:
        raise Exception("{} failed ret={}"
                        .format(message, ret))

def copy_data_device_to_host(device_data, data_size):
    host_buffer, ret = acl.rt.malloc_host(data_size)
    if ret != ACL_ERROR_NONE:
        print("Malloc host memory failed, error: ", ret)
        return None

    ret = acl.rt.memcpy(host_buffer, data_size,
                        device_data, data_size,
                        ACL_MEMCPY_DEVICE_TO_HOST)
    if ret != ACL_ERROR_NONE:
        print("Copy device data to host memory failed, error: ", ret)
        acl.rt.free_host(host_buffer)
        return None

    return host_buffer

def copy_data_device_to_device(device_data, data_size):
    device_buffer, ret = acl.rt.malloc(data_size, ACL_MEM_MALLOC_NORMAL_ONLY)
    if ret != ACL_ERROR_NONE:
        print("Malloc device memory failed, error: ", ret)
        return None

    ret = acl.rt.memcpy(device_buffer, data_size,
                        device_data, data_size,
                        ACL_MEMCPY_DEVICE_TO_DEVICE)
    if ret != ACL_ERROR_NONE:
        print("Copy device data to device memory failed, error: ", ret)
        acl.rt.free(device_buffer)
        return None

    return device_buffer

def copy_data_host_to_device(host_data, data_size):
    device_buffer, ret = acl.rt.malloc(data_size, ACL_MEM_MALLOC_NORMAL_ONLY)
    if ret != ACL_ERROR_NONE:
        print("Malloc device memory failed, error: ", ret)
        return None

    ret = acl.rt.memcpy(device_buffer, data_size,
                        host_data, data_size,
                        ACL_MEMCPY_HOST_TO_DEVICE)
    if ret != ACL_ERROR_NONE:
        print("Copy device data to device memory failed, error: ", ret)
        acl.rt.free(device_buffer)
        return None

    return device_buffer

def align_up(value, align):
    return int(int((value + align - 1) / align) * align)

def align_up16(value):
    return align_up(value, 16)

def align_up2(value):
    return align_up(value, 2)

def yuv420sp_size(width, height):
    return width * height * 3 // 2

def unpack_bytes(dest, dest_size, src, src_size):
    libatlas.UnpackFloatByteArray(dest, dest_size, src, src_size)
