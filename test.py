import threading
import time

total = 0

# Function to simulate a task
def task1():
    global total
    print("Task 1 started")
    for i in range(2):
        total += 1
        print("TASK 1", i, total)
        time.sleep(1)
    #time.sleep(2)  # Simulating a task taking 2 seconds
    print("Task 1 completed")
    print("Total in TAsk 1", total)

def task2():
    global total
    print("Task 2 started")
    for i in range(3):
        total += 1
        print("TASK 2", i, total)
        time.sleep(1)
    # time.sleep(3)  # Simulating a task taking 3 seconds
    print("Task 2 completed")
    print("Total in task 2", total)

# Create thread objects for task1 and task2
thread1 = threading.Thread(target=task1)
thread2 = threading.Thread(target=task2)

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to complete
thread1.join()
thread2.join()

print("Both tasks are completed.")
print(total)