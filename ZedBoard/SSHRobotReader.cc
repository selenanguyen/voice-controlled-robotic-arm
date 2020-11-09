#include <iostream>
#include <fstream>
#include <string>
#include <unistd.h>
#include "RoboticArm.h"
#include <sstream>

int main() {
	std::string line;
	RoboticArm robotic_arm;
	while(true) {
		std::ifstream file ("positions.txt");
		if(file.is_open()) {
			while(getline(file, line)) {
				std::cout << line << '\n';
			}
		}
		else {
			std::cout << "Cannot open file.";
		}
		file.close();
		
		// Determine the values within the array
		std::istringstream stream(line);
		std::string word;
		int values[10];
		int index = 0;
		
		// Parse each value into an integer
		while(stream >> word) {
			std::stringstream intstream(word);
			int val = 0;
			intstream >> val;
			values[index] = val;
			index += 1;
		}
		
		// Update all of the servos
		for(int i = 0; i < 5; i++)
			robotic_arm.MoveServo(i, values[2*i], values[(2*i)+1]);
		sleep(1);
	}
}

