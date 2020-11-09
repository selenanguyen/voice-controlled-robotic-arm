import sys
import time
import select
import paramiko
import speech_recognition as sr

# Robot related settings
currentBase = 90
currentBicep = 110
currentElbow = 110
currentWrist = 90
currentGripper = 0
keepRunning = True

# SSH related settings
host = '192.168.1.10'
user = "root"
password = "root"
port = 22

#Connect to the host
while True:
    print("Trying to connect")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, port=port, username=user, password=password)
        print("Connected to host")
        break
    except paramiko.AuthenticationException:
        print("Authentication failed")
        sys.exit(1)

# Navigate to proper directory
stdin, stdout, stderr = ssh.exec_command("cd /home/user103/FinalProject; ./SSHRobotReader &")

# Wait for the command to terminate
while not stdout.channel.exit_status_ready():
    # Only print data if there is data to read in the channel
    if stdout.channel.recv_ready():
        rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
        if len(rl) > 0:
            # Print data from stdout
            print(stdout.channel.recv(1024))

# Begin main loop
while(keepRunning):
    # obtain audio from the mic
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        speechToText = r.recognize_google(audio).split()
        print("You said: " + str(speechToText))
        if(len(speechToText) == 2):
            delta = 0;
            if(speechToText[1] == "left" or speechToText[1] == "down"):
                delta = -45
            elif(speechToText[1] == "right" or speechToText[1] == "up"):
                delta = 45
            if(speechToText[0] == "base" or speechToText[0] == "bass" or speechToText[0] == "face"):
                currentBase += delta
                if(currentBase >= 180):
                    currentBase = 175
                if(currentBase <= 0):
                    currentBase = 5
            if(speechToText[0] == "bicep"):
                currentBicep += delta
                if(currentBicep >= 180):
                    currentBicep = 175
                if(currentBicep <= 0):
                    currentBicep = 5
            if(speechToText[0] == "elbow"):
                currentElbow += delta
                if(currentElbow >= 180):
                    currentElbow = 175
                if(currentElbow <= 0):
                    currentElbow = 5
            if(speechToText[0] == "wrist"):
                currentWrist += delta
                if(currentWrist >= 180):
                    currentWrist = 175
                if(currentWrist <= 0):
                    currentWrist = 5
            if(speechToText[0] == "gripper"):
                currentGripper += delta
                if(currentGripper >= 180):
                    currentGripper = 175
                if(currentGripper <= 0):
                    currentGripper = 5
        if(speechToText[0] == "quit"):
            keepRunning = False
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Request Error; {0}".format(e))

    # Update user on SSH command
    print("Sending command with updated values;")
    print("Base: " + str(currentBase))
    print("Bicep: " + str(currentBicep))
    print("Elbow: " + str(currentElbow))
    print("Wrist: " + str(currentWrist))
    print("Gripper: " + str(currentGripper))

    # Send command to ZedBoard
    msg = "cd /home/user103/FinalProject; "
    msg += "./SSHRobotWriter " + str(currentBase) + " 60 " + str(currentBicep) + " 60 " + str(currentElbow) + " 60 " + str(currentWrist) + " 60 " + str(currentGripper) + " 60"
    stdin, stdout, stderr = ssh.exec_command(msg)

    # Wait for the command to terminate
    while not stdout.channel.exit_status_ready():
        # Only print data if there is data to read in the channel
        if stdout.channel.recv_ready():
            rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
            if len(rl) > 0:
                # Print data from stdout
                print(stdout.channel.recv(1024))
# Disconnect from the host
print("Voice session finished. Closing SSH connection. Goodbye!")
stdin, stdout, stderr = ssh.exec_command("killall SSHRobotReader")
ssh.close()
