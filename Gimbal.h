#include "Arduino.h"
#include <Servo.h>

const unsigned int MAX_MESSAGE_LENGTH = 15;
const unsigned int ANGLE_CMD_SIZE = 3;
typedef enum {CMD_TYPE_POSE, CMD_TYPE_VEL, CMD_TYPE_INVALID} CMD_TYPE;

struct State{
  double pitch;
  double yaw;
};

struct GimbalCommand{
  CMD_TYPE cmd_type; // 1 for pose and 2 for vel
  State state; // intigers in degrees
  bool arm;  // send serial 2 for true
  bool trigger; // send serial 2 for true
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
  GimbalCommand get_cmd_from_serial();
  void printCmd(GimbalCommand cmd);
};

