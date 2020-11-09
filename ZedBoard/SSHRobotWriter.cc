#include <iostream>
#include <fstream>

int main(int argc, char *argv[]) {
	// Creates a filestream with positions.txt
	std::ofstream file ("positions.txt");
	if(file.is_open()) {
		for(int i = 1; i < argc; i++) {
			// Writes the current argument (followed by a space) to the file
			file << argv[i] << " ";
		}	
	}
}

