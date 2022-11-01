import cv2
import face_recognition
import os 

path='Images/'
images=os.listdir(path)
face_image_encodings=[]
names=[]
for i in images:
    image = cv2.imread(path+i)
    face_loc = face_recognition.face_locations(image)[0]
    face_image_encodings.append(face_recognition.face_encodings(image, known_face_locations=[face_loc])[0])
    (name,ter)=i.split('.')
    names.append(name)

res = {names[i]: face_image_encodings[i] for i in range(len(names))}

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
     ret, frame = cap.read()
     if ret == False: break
     frame = cv2.flip(frame, 1)

     face_locations = face_recognition.face_locations(frame)
     if face_locations != []:
          for face_location in face_locations:
               face_frame_encodings = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]
               for x,y in res.items():  
                    result = face_recognition.compare_faces([y], face_frame_encodings)
               #print("Result:", result)
                    if result[0] == True:
                        text = x
                        color = (125, 220, 0)
                        break
                    else:
                        text = "Desconocido"
                        color = (50, 50, 255)
               cv2.rectangle(frame, (face_location[3], face_location[2]), (face_location[1], face_location[2] + 30), color, -1)
               cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color, 2)
               cv2.putText(frame, text, (face_location[3], face_location[2] + 20), 2, 0.7, (255, 255, 255), 1)

     cv2.imshow("Frame", frame)
     if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
