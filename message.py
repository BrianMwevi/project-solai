import sys
import time
message = sys.argv[1]
is_deployment = sys.argv[2]
print(f"\n\n{message}! Have fun coding... :)\n\n")

if is_deployment:
    print("Opening the deployed app in browser.........")
time.sleep(2.5)
