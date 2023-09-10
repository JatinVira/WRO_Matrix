/*
   Rosserial serial_node to subscribe to cmd_vel and generate PWM signals for
   the motor speed controller
   Also publishes the PWM values to the chatter topic
   Also turns the robot by moving the servo
*/

// Import all the Header Files
#include <Servo.h>

/* Pin Configuration */
// Color sensor pins
#define S0 13
#define S1 12
#define S2 11
#define S3 10
#define sensorOut 9

// Servo PWM Pin
#define servo_pin 5

// Motor Config
#define max_pwm 255
#define motor_pwm_pin 3
#define motor_in1_pin 2
#define motor_in2_pin 4

// Ultrasonic Sensor Pins
#define trigger_us_left A0
#define echo_us_left A1
#define trigger_us_right A4
#define echo_us_right A5

// Velocity Parameters
#define max_linear_vel 0.22   // Range: 0-1
#define max_angular_vel 0.80  // Range: 0-1

/* Calibrated sensor values */
// Define the color thresholds here
#define O_lowerRed 27
#define O_upperRed 65
#define O_lowerGreen 65
#define O_upperGreen 105
#define O_lowerBlu 65
#define O_upperBlu 105

#define B_lowerRed 70
#define B_upperRed 165
#define B_lowerGreen 25
#define B_upperGreen 110
#define B_lowerBlu 15
#define B_upperBlu 80

/* Global Variables */
// Distance calculation
long timeElapsed = 0;
float distance = 0;

// Define the number of elements in the array
#define max_array_size 10

// Define the distance threshold
#define distance_extreme_right 25
#define distance_extreme_left 25
#define distance_center 30
#define distance_max 255

// Stores frequency read by the photodiodes
int redFrequency = 0;
int greenFrequency = 0;
int blueFrequency = 0;
String color = "";

// Command angle for the servo
int servo_angle_pos = 90;

// Global iterator to iterate through the array
int global_iterator = 0;

// Arrays to store the distance values
int prox_sensor_left[max_array_size];
int prox_sensor_right[max_array_size];

// Variables to store the average of the array
int prox_sensor_left_avg = 0;
int prox_sensor_right_avg = 0;

Servo servo;

int get_distance_from_sensor(const int trigger_pin, const int echo_pin) {
  // Function to get the distance from the ultrasonic sensor
  // Trigger the ultrasonic sensor
  digitalWrite(trigger_pin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigger_pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger_pin, LOW);

  // Get the time elapsed for the ultrasonic sensor to send and receive the
  // signal
  timeElapsed = pulseIn(echo_pin, HIGH);

  // Calculate the distance from the time elapsed
  distance = (timeElapsed * 0.034) / 2;

  // Distance has to be returned in integer, so ensure overflow doesnt happen
  return distance > 255 ? 255 : distance;
}

void redRead() {
  digitalWrite(S2, LOW);
  digitalWrite(S3, LOW);
  redFrequency = pulseIn(sensorOut, LOW);
}
void greenRead() {
  digitalWrite(S2, HIGH);
  digitalWrite(S3, HIGH);
  greenFrequency = pulseIn(sensorOut, LOW);
}
void blueRead() {
  digitalWrite(S2, LOW);
  digitalWrite(S3, HIGH);
  blueFrequency = pulseIn(sensorOut, LOW);
}

void colorSense() {
  redRead();
  greenRead();
  blueRead();
  // Condition to check if the color is orange
  if (O_lowerRed < redFrequency && redFrequency < O_upperRed &&
      O_lowerGreen < greenFrequency && greenFrequency < O_upperGreen &&
      O_lowerBlu < blueFrequency && blueFrequency < O_upperBlu) {
    color = "orange";
  }
  // Condition to check if the color is blue
  else if (B_lowerRed < redFrequency && redFrequency < B_upperRed &&
           B_lowerGreen < greenFrequency && greenFrequency < B_upperGreen &&
           B_lowerBlu < blueFrequency && blueFrequency < B_upperBlu) {
    color = "blue";
  } else {
    color = "none";
  }
}

int get_average(int array[]) {
  int sum = 0;
  for (int i = 0; i < max_array_size; i++) {
    sum += array[i];
  }
  return int(sum / max_array_size);
}

void move_robot(const float linear_vel, const float angular_vel) {
  // Linear velocity is the velocity of the robot in the forward direction
  // Angular velocity is the velocity of the robot in the angular direction
  // linear_vel and angular_vel are in the range of -1 to 1
  // Makes the motor drive in only forward direction with a PWM value of 0-255
  int pwm = linear_vel * max_pwm;
  int in1 = LOW;
  int in2 = HIGH;

  if (pwm < 0) {
    in1 = HIGH;
    in2 = LOW;
    pwm = pwm * -1;
  }

  // Write the values to the motor
  analogWrite(motor_pwm_pin, pwm);
  digitalWrite(motor_in1_pin, in1);
  digitalWrite(motor_in2_pin, in2);

  // Refactor the below code
  if (angular_vel > 0) {
    servo_angle_pos = 90 + (angular_vel * 10);
  } else if (angular_vel < 0) {
    servo_angle_pos = 90 + (angular_vel * 10);
  } else {
    servo_angle_pos = 90;
  }

  // Convert the servo angle position to the int
  servo_angle_pos = int(servo_angle_pos);
  // Write the servo angle position
  servo.write(servo_angle_pos);
}

void hard_coded_left_turn() {
  // Function to turn the robot left
  // Turn the robot left by 90 degrees
  move_robot(1, 0);
  delay(1000);
  move_robot(1, 1);
  delay(1000);
  move_robot(0, 0);
}

void hard_coded_right_turn() {
  // Function to turn the robot right
  // Turn the robot right by 90 degrees
  move_robot(1, 0);
  delay(1000);
  move_robot(1, -1);
  delay(1000);
  move_robot(0, 0);
}

void take_action() {
  // Function to take action based on the color sensed and the distance
  // calculated
  // If the color is none, check the distance
  // Condition to check if the robot is in the center of the path
  if (prox_sensor_left_avg < distance_max &&
      prox_sensor_left_avg > distance_center &&
      prox_sensor_right_avg < distance_max &&
      prox_sensor_right_avg > distance_center) {
    move_robot(max_linear_vel, 0);
    return;
  }
  // Condition to check if the robot is in the extreme left of the path
  else if (prox_sensor_left_avg < distance_extreme_left &&
           prox_sensor_right_avg > distance_center) {
    move_robot(max_linear_vel, max_angular_vel);
    return;
  }
  // Condition to check if the robot is in the extreme right of the path
  else if (prox_sensor_left_avg > distance_center &&
           prox_sensor_right_avg < distance_extreme_right) {
    move_robot(max_linear_vel, -max_angular_vel);
    return;
  }
  // Condition to check if the robot is in open left space
  else if (prox_sensor_left_avg >= distance_max &&
           prox_sensor_right_avg > distance_extreme_right) {
    // Insert a harcoded left turn here
    hard_coded_left_turn();
    return;
  }
  // Condition to check if the robot is in open right space
  else if (prox_sensor_left_avg > distance_extreme_left &&
           prox_sensor_right_avg >= distance_max) {
    // Insert a harcoded right turn here
    hard_coded_right_turn();
    return;
  }
}

void setup() {
  // Setup the color sensor pins
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT);
  // Setting frequency scaling to 20%
  digitalWrite(S0, HIGH);
  digitalWrite(S1, LOW);

  // Setup the motor pins
  pinMode(motor_pwm_pin, OUTPUT);
  pinMode(motor_in1_pin, OUTPUT);
  pinMode(motor_in2_pin, OUTPUT);

  // Set the motor to stop
  digitalWrite(motor_in1_pin, LOW);
  digitalWrite(motor_in2_pin, LOW);

  // Setup the ultrasonic sensor pins
  pinMode(trigger_us_left, OUTPUT);
  pinMode(trigger_us_right, OUTPUT);
  pinMode(echo_us_left, INPUT);
  pinMode(echo_us_right, INPUT);

  // Setup the servo
  servo.attach(servo_pin);
  servo.write(servo_angle_pos);
  delay(100);

  // Setup the serial communication
  Serial.begin(9600);
  Serial.println("Robot is ready");
}

void loop() {
  // Get the color values from the color sensor and publish them
  colorSense();

  if (global_iterator < max_array_size) {
    prox_sensor_left[global_iterator] =
        get_distance_from_sensor(trigger_us_left, echo_us_left);
    prox_sensor_right[global_iterator] =
        get_distance_from_sensor(trigger_us_right, echo_us_right);
    global_iterator++;
  }
  // If the array is full, calculate the average of the array and take action
  else if (global_iterator == max_array_size) {
    // Print the contents of array
    Serial.println("Left Array: ");
    for (int i = 0; i < max_array_size; i++) {
      Serial.print(prox_sensor_left[i]);
      Serial.print(" ");
    }
    Serial.println();
    Serial.println("Right Array: ");
    for (int i = 0; i < max_array_size; i++) {
      Serial.print(prox_sensor_right[i]);
      Serial.print(" ");
    }
    Serial.println();
    prox_sensor_left_avg = get_average(prox_sensor_left);
    prox_sensor_right_avg = get_average(prox_sensor_right);
    // Reset the global iterator
    global_iterator = 0;
    take_action();
  }
}
