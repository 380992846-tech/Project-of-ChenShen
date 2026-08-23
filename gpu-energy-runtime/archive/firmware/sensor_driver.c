// ============================================================
// IR 温度传感器驱动（示意）
// 实际接入：MLX90614 (I2C) / AMG8833 网格热电堆
// ============================================================
#include "sensor_driver.h"

float sensor_read_grill_c(void) {
    // 占位：读取 IR 热电堆，返回烤架表面温度 (°C)
    // 以 MLX90614 为例：
    //   float obj = mlx90614.readObjectTempC();
    return 0.0f;
}

float sensor_read_food_c(void) {
    // 食物核心温度（插入式探针）
    return 0.0f;
}

bool sensor_calibrate(float reference_temp) {
    // 用已知温度校准偏移
    return true;
}
