#include <Gimbal.h>
Gimbal::Gimbal(int pin_pitch, int pin_yaw, int pin_triger){
	this->pin_pitch = pin_pitch;
	this->pin_yaw = pin_yaw;
	this->pin_triger = pin_triger;
}

void Gimbal::goHome(){
	servo_pitch.write(90);
	servo_yaw.write(90);
	servo_triger.write(10);
	pose.pitch = 0;
	pose.yaw = 0;
	vel.pitch = 0;
	vel.yaw = 0;
}
void Gimbal::cmdPose(State cmd_pose){
	servo_pitch.write(cmd_pose.pitch);
	servo_yaw.write(cmd_pose.yaw);
	pose = cmd_pose;
}
void Gimbal::begin(){
	servo_pitch.attach(pin_pitch);
	servo_yaw.attach(pin_yaw);
	servo_triger.attach(pin_triger);
}
void Gimbal::cmdPullTriger(){
	servo_triger.write(100);
	delay(500);
	servo_triger.write(10);
}

void Gimbal::set_cmd_vel(State cmd_vel)
{
	this->cmd_vel = cmd_vel;
}

void Gimbal::motors_step(double dt){
	State pose_cmd;
	pose_cmd.pitch = pose.pitch + pose_cmd.pitch * dt;
	pose_cmd.yaw = pose.yaw + pose_cmd.yaw * dt;
	cmdPose(pose_cmd);
}