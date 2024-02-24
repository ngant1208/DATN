import time

# timeout variable can be omitted, if you use specific value in the while condition
timeout = 2   # [seconds]

timeout_start = time.time()
print(f'start_time {timeout_start}')
test=0
while time.time() < timeout_start + timeout:
    #test = 0
    # if test == 5:
    #     break
    test += 1
print(time.time())
print("done")