# Voice Controlled Robotic Arm
## Selena Nguyen and Ryan Corkery | 4/18/2019
#### Project Description
Our group has taken on a challenge for our final project – integrating a microphone component into communication with the robotic arm. At first, we did not have the necessary software, tools, or libraries installed onto our lab equipment to make this happen. Many of our features therefore involve the communication standard we had to develop to allow for voice recognition.
- Robotic Arm – The first component of our project is the arm itself. The 5 servos on this arm are
connected to the ZedBoard and controlled via hardware Synthesis.
- Laptop – The laptop played a major role in voice recognition. Since our personal laptops had a
working network connection and administrative rights, we could install various libraries
to enable SSH communication with the ZedBoard, as well as API calls to Google’s
speech recognition cloud servers, to properly translate audio into text that we could map
to servo angles in our code. This was all processed via python. These changes could then
be relayed via SSH to the board and processed further there.
- ZedBoard – The board was responsible for two components of our project:
  1. Hardware Synthesis – The servo controller design from Lab 11 was synthesized to the ZedBoard’s FPGA. This allows for some locations in memory on the board to be mapped to each PWM signal’s speed and angle signals (used in the circuit design).
  2. SSH communication – On the software side, the ZedBoard needed to manipulate the values in memory as requested to move the robotic arm accordingly. Due to the nature of the SSH connection, our group ran into an issue where we needed to be able to continuously update the values of the servos, which involved starting, killing, and restarting our control program repeatedly. However, when it was killed, the memory values to which the robot arm was mapped were unallocated. So during the time between the program being killed and being relaunched again, these memory addresses could be reallocated and filled with new values. This would cause robot arm to act sporadically. To fix this, our group came up with a unique solution: using two programs, with one running in the background.
    - SSHRobotReader: To keep the vital memory values from being deallocated, this program could not be ended. As a result, this program would run in the background (by appending the launch command with ‘&’) and continuously read the servo values from a text file (named ‘positions.txt’) in the working directory. These values were then converted into integers and written into the correct memory locations to which the robot could respond.
    - SSHRobotWriter: This program was the executable, which was continuously called upon via the laptop via SSH. The program simply would write the values that were passed to it as arguments into the text file (‘positions.txt’) previously mentioned. This way, the values that the SSHRobotReader are using can change, without the program ever terminating.
#### Relevance in this Course:
<table>
  <tr>
<td>SSHRobotReader.cc
SSHRobotWriter.cc
RoboticArm.cc
RoboticArm.h
  Makefile</td>
    <td>
[Unit 1]: Using vi, Understanding linux commands and its filesystem structure<br />
[Unit 2]: Input/Output and Strings, Arithmetic Operators, Selection control Structures, Functions, Arrays<br />
[Unit 3]: Classes, Object oriented Design, Header files, Makefiles
      </td>
  </tr>
  <tr>
    <td>
      FPGA Synthesis
    </td>
    <td>
[Unit 5]: Boolean Algebra/Logic Gates (used during design of circuits)<br />
[Unit 6]: Combinational Logic<br />
[Unit 7]: Sequential Logic<br />
[Lab 8]: How to synthesize to FPGA<br />
[Lab 11]: Servo Controller
    </td>
  </tr>
  <tr>
    <td>
Laptop
    </td>
    <td>
[Learned]: Python programming syntax, Library installation, Static IP configuration (of network adapter), API programming<br />
[Unit 1/Lab1]: SSH communication
    </td>
  </tr>
</table>

#### Roles
Ryan Corkery:
- Wrote majority of speech recognition code
o Researched SpeechRecognition library (specifically using google API)
- Figured out how to set static IP addresses to ZedBoard to connect via SSH
- Wrote makefile
- Wrote SSHRobotWriter.cc
- Debugged SSHRobotReader.cc
- Wrote majority of report
- Helped finalize and look over video<br />
Selena Nguyen:
- Developed communication standard between laptop and ZedBoard
- Researched Paramiko library (to implement SSH connection)
- Helped debug and tweak speech recognition code
- Resynthesized Lab 11 hardware design to board
o Used RoboticArm.cc and RoboticArm.h to create SSHRobotReader.cc
- Debugged SSHRobotWriter.cc
- Edited majority of video
- Helped finalize and look over report prior to submission
YouTube Link: https://youtu.be/DPbz_761SLo
