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


GimbalCommand Gimbal::get_cmd_from_serial(){
 GimbalCommand cmd;
 while (Serial.available() > 0)
 {
   //Create a place to hold the incoming message
   static char message[MAX_MESSAGE_LENGTH];
   static unsigned int message_pos = 0;

   //Read the next available byte in the serial receive buffer
   char inByte = Serial.read();

   //Message coming in (check not terminating character) and guard for over message size
   if ( inByte != '\n' && (message_pos < MAX_MESSAGE_LENGTH - 1) )
   {
     //Add the incoming byte to our message
     message[message_pos] = inByte;
     message_pos++;
   }
   //Full message received...
   else
   {
      //Add null character to string
      message[message_pos] = '\0';
      Serial.println(message);

        // parse the serial message:
      char cmd_type_c;
      char pitch_c[4];
      char yaw_c[4];
      char arm_c;
      char trigger_c;
      cmd_type_c = message[0];
      for(int i=0;i<3;i++){
        pitch_c[i] = message[i+2];
        yaw_c[i] = message[i+6];
      }
      pitch_c[ANGLE_CMD_SIZE] = '\0';
      yaw_c[ANGLE_CMD_SIZE] = '\0';

      arm_c = message[10];
      trigger_c = message[12];

        //convert to int
      if(cmd_type_c == 1)
        cmd.cmd_type = CMD_TYPE_POSE;
      else if(cmd_type_c == 2)
        cmd.cmd_type = CMD_TYPE_VEL;
      else 
        cmd.cmd_type = CMD_TYPE_INVALID;

      State state;
      state.pitch = atoi(pitch_c);
      state.yaw = atoi(yaw_c);
      cmd.state.pitch = atoi(pitch_c);
      cmd.state.yaw = atoi(yaw_c);

      cmd.arm = arm_c == '2' ? true : false;
      cmd.trigger = arm_c == '2' ? true : false;
      
      message_pos = 0;

   }
 }
 return cmd;

}

void Gimbal::printCmd(cmd){
  Serial.print("CMD_TYPE: ");
  Serial.print(cmd.cmd_type);
  Serial.print("| pitch_c: ");
  Serial.print(cmd.state.pitch);
  Serial.print("| yaw_c: ");
  Serial.print(cmd.state.yaw);
  Serial.print("| arm_c: ");
  Serial.print(cmd.arm);
  Serial.print("| trigger_c: ");
  Serial.print(cmd.trigger);
  Serial.println("");
}