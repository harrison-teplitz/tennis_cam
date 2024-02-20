import subprocess
import time

def capture_image(image_number):
    filename = f"/home/harrison/tennis/data/image_{image_number}.jpg"
    command = f"libcamera-still -o {filename}"
    subprocess.run(command, shell=True)
    print(f"Captured {filename}")
    
def main():
        image_number = 1
        while image_number <= 10:
            capture_image(image_number)
            time.sleep(10)
            image_number +=1
            
if __name__ == "__main__":
    main()