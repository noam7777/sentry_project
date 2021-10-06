#include "Arduino.h"
#include <Servo.h>


struct State{
  double pitch;
  double yaw;
};

class Gimbal
{
  private:
  int pin_pitch, pin_yaw, pin_triger;
  Servo servo_pitch;
  Servo servo_yaw;
  Servo servo_triger;
  State pose;
  State vel;
  State cmd_vel;
  
  public:
  Gimbal(int pin_pitch, int pin_yaw, int pin_trigger);
  void cmdPose(State cmd_pose);
  void set_cmd_vel(State cmd_vel);
  void cmdLinearTraj(State cmd_pose, State cmd_vel);
  void cmdPullTriger(); 
  void goHome();
  void begin();
  void motors_step(double dt);
  enum Mode {E_POSE, E_VEL, E_LINE_TRAJ};
};

