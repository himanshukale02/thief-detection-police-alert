import cv2
import requests

def send_video(client_id, server_ip, server_port=5000):
    video_capture = cv2.VideoCapture(0)  

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame")
            break
        

        _, img_encoded = cv2.imencode('.jpg', frame)
        

        try:
            response = requests.post(f'http://{server_ip}:{server_port}/upload_frame/{client_id}', files={'frame': img_encoded.tobytes()})
            if response.status_code != 200:
                print(f"Failed to send frame: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending frame: {e}")
            break
        

        cv2.imshow(f'Client {client_id} - Captured Frame', frame)
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    client_id = 'client2'  
    server_ip = '192.168.45.207'  
    send_video(client_id, server_ip)