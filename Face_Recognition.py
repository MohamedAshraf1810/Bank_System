# Train multiple images per person
# Find and recognize faces in an image using a SVC with scikit-learn
import face_recognition
import pickle
import time

def FaceRec_Model(username,pos_L):
        
    try:
        accuracyList=[]
        
        for k in range(0,3):
            print(f"Processing {pos_L[k]} Face")
            # Load the test image with unknown faces into a numpy array
            test_image = face_recognition.load_image_file(f'face_Recognition_Utilities/SVC_Testimgs/Users_Photos/{username}/{pos_L[k]}.png')
            # Find all the faces in the test image using the default HOG-based model
            dettime = time.time()
            face_locations = face_recognition.face_locations(test_image ,model='cnn')
            detendtime = time.time()
            detectionTime = detendtime-dettime
            print("=========Detection Time========")
            print(f"{detectionTime}For Image {k}")
            print("===============================")
            no = len(face_locations)
            print("Number of faces detected: ", no)
            # Predict all the faces in the test image using the trained classifier
            print("Found:")
            for i in range(no):
                classtime = time.time()
                test_image_enc = face_recognition.face_encodings(test_image,face_locations)[i]
                # print("image incoding is ",test_image_enc)
                 # Get pk File
                with open(f'face_Recognition_Utilities/Dumbed_Model/Trained_Model/MAIN/{username}/{pos_L[k]}.pk', 'rb') as f:
                    mypickle = pickle.load(f)
                propa_name = mypickle.predict_proba([test_image_enc])
                # Getting Model Accuracy
                max_acc = propa_name.max()*100
                name = mypickle.predict([test_image_enc])
                predictedName = name[0]
                if (max_acc < 96 or predictedName == 'other'):
                    predictedName = 'UnKnown'
                    print('The Predicted Person Is : ', predictedName)
                    print("The Model Accuracy Is = " , round(max_acc,2) , "%")
                    accuracyList.append(0)
                else:
                    print("The Predicted Person Is : " , predictedName)
                    print("The Model Accuracy Is = " , round(max_acc,2) , "%")
                    accuracyList.append(max_acc)
                    
                classendtime  =time.time()
                print("***************Classification Time*************")
                print(f"{classendtime-classtime} From image {k}")
                print("***********************************************")
                
        print("***************")
        print(" Accuracy List : " , accuracyList)
        print("***************")
        # AverageScore = sum(accuracyList)/len(accuracyList)
        AverageScore = sum(accuracyList)/3
        print("Average Score Is :" , AverageScore)
        if AverageScore > 96:
            return True
        else:
            return False

    except Exception as e:
        print(e)
