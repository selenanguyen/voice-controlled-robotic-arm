all: SSHRobotReader SSHRobotWriter
SSHRobotReader: SSHRobotReader.o RoboticArm.o
	g++ SSHRobotReader.o RoboticArm.o -o SSHRobotReader
SSHRobotWriter: SSHRobotWriter.cc
	g++ SSHRobotWriter.cc -o SSHRobotWriter
SSHRobotReader.o: SSHRobotReader.cc RoboticArm.h
	g++ -c SSHRobotReader.cc
RoboticArm.o: RoboticArm.cc RoboticArm.h
	g++ -c RoboticArm.cc
clean:
	rm -f RoboticArm.o
	rm -f SSHRobotReader.o
