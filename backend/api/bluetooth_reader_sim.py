# import serial - get this with the real bluetooth connection
import threading # get this with the real bluetooth connection
import csv
import time
# TODO for me, is to test all of this stuff

class BluetoothReaderSimulation:

    # initiailizes the reader object - this we would still have to make as versatiole
    def __init__(self,  filename="", port="/dev/rfcomm0", baud_rate=9600, timeout=1):
        """
        Actual: Bluetooth reader constructor where serial_connection is a Serial object.
        Simulation: Port, baud_rate, timeout stay the same. Serial_connection and running are booleans that 
            are manually flipped as different bluetooth methods are called.
        """
        # bluetooth processing
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.serial_connection = False # this would be a serial object instead
        self.running = False
        
        # data values -> possibly make this another object (like a data something something)
        self.buffer = []
        self.last_recording = []
        self.ride_statistics = {"speed": 0}

        #simulation values
        self.csv_name = filename
        self.data = [] # data that csv file is sent to
        self.data_index = 0

 
    # change this so that it has pairing information (as shown by the bluetooth ready)
    def connect_sim(self):
        """
        Actual: Establishes a connection with the HC-05 module - uses a try catch block and proper error handling
            - Can return an error/exception.
        Simulation: Flip serial_connection bool and doesn't actually return an error.
            - Flips serial_connection boolean.
            - Prints a connect/disconnection message. 
- 
        """
        self.serial_connection = True

        # open csv and store into data list
        with open(self.csv_name, newline="", encoding='utf-8') as file:
            reader = csv.reader(file)
            self.data = list(reader)
        
        self.data.pop(0)

        # connection statements
        if (self.serial_connection == True):
            print(f"Connected to HC-05 on {self.port} at {self.baud_rate} baud.")
            return True
        else:
            print(f"Unable to connect to HC-05. Please try connecting again or connecting to a different device.")
            return False
    
    def process_buffer_endpoint(self, endpoint): # TODO

        print("Popped value from sliding window")
        # self.ride_statistics[self.data_index] = endpoint;            

    def process_ride_statistics(self):
        # do a check to see that the bluetooth indeed has not been disconnected

        if self.serial_connection or self.running:
            print("Need to disconnect first. Please click stop recording")
            return
        
        print("Processing ride statistics... ")
        self.ride_statistics["speed"] = self.ride_statistics["speed"]/len(self.data)
        print(self.ride_statistics)

    # realisitically, this would be actually calling the serial connection
    def read_data_sim(self): # TODO
        """
        Actual: Continuously reads data from HC-05 and processes it.
        Simulation: Loops through an imported csv file through buffers of 8 rows at a time, and sends it to process data.

        """
        # print("Entered read_data_sim")
        # check to see if connect has been called yet
        if not self.serial_connection:
            print("No serial connection. Call connect() first.")
            return
        
        print("Populating sliding window...")
        print()
        while self.running and self.data_index < len(self.data) and len(self.buffer) <= 20: # 30 because its supposed to be 15 min * twice
            self.buffer.append(self.data[self.data_index])
             
            self.ride_statistics["speed"] += abs(float(self.data[self.data_index][4]))


            self.data_index += 1
            time.sleep(0.5)
        
        # basically this means that we have reach the buffer capacity, but we are
        # still recording
        print("Sliding window reached max capacity.")
        print("Implementing sliding window...")
        print()
        while self.running and self.data_index < len(self.data):
            self.process_buffer_endpoint(self.buffer[-1]) # process the last value
            self.buffer.pop() # pop last value
            self.buffer.append(self.data[self.data_index]) # insert at beginnging
            
            self.ride_statistics["speed"] += abs(float(self.data[self.data_index][4]))

            self.data_index += 1
            time.sleep(0.5)
    

    def process_final_buffer(self):
        """
        Actual: Processes the received Bluetooth data.
        Simulation: Processes the 'received' Bluetooth data in buffers. Ideally make some kind of DB call.
            - Final buffer (partially populated if ride < 15 minutes) (fully populated if ride if >= 15 minutes)
            - This is the buffer used to develop the crash report
        """
        # do a check to see that the bluetooth indeed has not been disconnected
        if self.serial_connection or self.running:
            print("Need to disconnect first. Please click stop recording")
            return
        
        print("Uploading final buffer to cloud...")

    def start_sim(self):
        """
        Actual: Starts the Bluetooth reading in a separate thread.
        Simulation: Same. Only read_data is changed for simulation.
            - Flips the boolean running.
            - Flips the boolean serial_connection.
            - Instead of reading data on a seperate thread, we are calling it in the start function

        """
        self.running = True
        if self.running:
            print("Bluetooth reader thread starting....")
            self.read_data_sim()

    def stop_sim(self):
        """
        Actual: Stops the Bluetooth connection using Serial object.
        Simulation: 
            - Flips the boolean running.
            - Flips the boolean serial_connection.
            - Calls the process_data() function, which processes the 
                most recent buffer. If ride <= 15 min, then this is a
                partially filled buffer. If ride > 15 min, then the 
                sliding window functionality will have been implenented.

        """
        print()
        self.running = False

        if self.serial_connection:
            self.serial_connection = False
            print("Bluetooth connection closed.")
        
        # print("ProcesFinal sliding window")
        self.process_final_buffer() # crash report
        # print("Sending data to process ride statistics")
        self.process_ride_statistics() # user statistics

        print("Completed data processing.")


        """
        - database processing: go through each line 
        - extract the first 6 values of each row
        - go through each row 

        Statistics:
        - average distance (per trip)
        - total distance (across all trips)
        - average speed

        Crash Report:

        """

if __name__ == "__main__":

        # create a bluetooth reader
    bts = BluetoothReaderSimulation(".sim13.csv", "COM5")
    # print("CALLING CONNECT")
    # print()
    bts.connect_sim()
    # print("CALLING START")
    print()
    bts.start_sim()
    #print()
    #print("CALLING STOP")
    #print()
    bts.stop_sim()

