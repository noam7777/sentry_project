#include <Gimbal.h>
Gimbal gimbal(9, 10, 11);



void setup() {
  Serial.begin(9600);
  gimbal.begin();
  gimbal.goHome();
  Serial.flush();
}

void loop() {

 //Check to see if anything is available in the serial receive buffer
  GimbalCommand cmd = gimbal.get_cmd_from_serial(); 
  if(cmd.cmd_type == CMD_TYPE_POSE){
     gimbal.cmdPose(cmd.state);
  }
  else if(cmd.cmd_type == CMD_TYPE_VEL){
     gimbal.set_cmd_vel(cmd.state);
  }
  else{/*  */
    Serial.print("invalid cmd type: ");
    Serial.println(cmd.cmd_type);
  }
  gimbal.printCmd(cmd);
  delay(1);
 
}
