// ============================================================
// GPU BBQ System  —  ESP32 烤架温控 + 自动翻面固件
// PID 恒温（60-80°C） + 每 N 秒翻面 90 度
// 警告：仅供受控实验台使用，勿接真实机柜。
// ============================================================
#include <Servo.h>

// --- 硬件引脚 ---
const int SERVO_PIN  = 13;    // 翻面舵机
const int IR_SENSOR  = 34;    // IR 热电堆（模拟输入）
const int HEATER_PIN = 25;    // 加热控制（PWM，接到外部固态继电器/风机）

// --- PID 参数 ---
double setpoint   = 72.0;     // 目标烤架温度 °C
double Kp = 8.0, Ki = 0.2, Kd = 0.5;
double errSum = 0, lastErr = 0;

// --- 翻面 ---
const unsigned long FLIP_MS = 45000UL; // 每 45s 翻面
unsigned long lastFlip = 0;
const int FLIP_ANGLE = 90;

Servo flipServo;

double readGrillTemp() {
  // 将 ADC 0-4095 映射到 0-100°C 的粗略校准
  int raw = analogRead(IR_SENSOR);
  return (double)raw / 4095.0 * 100.0;
}

void pidTick(double input) {
  double error = setpoint - input;
  errSum = constrain(errSum + error, -100.0, 100.0);
  double dErr = error - lastErr;
  lastErr = error;
  double out = Kp * error + Ki * errSum + Kd * dErr;
  out = constrain(out, 0.0, 255.0);
  analogWrite(HEATER_PIN, (int)out);
}

void setup() {
  Serial.begin(115200);
  flipServo.attach(SERVO_PIN);
  flipServo.write(0);
  Serial.println("GPU BBQ System firmware 已启动 (ESP32)");
}

void loop() {
  double gpuTemp = readGrillTemp();
  pidTick(gpuTemp);

  unsigned long now = millis();
  if (now - lastFlip >= FLIP_MS && gpuTemp >= 60.0) {
    flipServo.write(FLIP_ANGLE);
    delay(300);
    flipServo.write(0);
    lastFlip = now;
    Serial.println("🔄 自动翻面 90°");
  }

  // 过热保护：>85°C 关闭加热
  if (gpuTemp > 85.0) analogWrite(HEATER_PIN, 0);

  Serial.printf("🌡️  %.1f °C  |  setpoint %.1f\n", gpuTemp, setpoint);
  delay(1000);
}
