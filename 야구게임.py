import random
numbers = str(random.randrange(100,1000))
answer = [int(numbers[0]),int(numbers[1]),int(numbers[2])]
#print(answer)
a = 0
while True:
    Strike = 0
    Ball = 0 
    question = input()
    questions = [int(question[0]),int(question[1]),int(question[2])]
    for i in range(len(answer)):
        if i==2:
            a==1
        else:
            a=i
        for j in range(a,len(questions)):
            if answer[i]==questions[j] and i == j:
                #print(i, j)
                Strike +=1
            elif answer[i]==questions[j] and i != j :
                Ball += 1
    print("{} Strike {} Ball".format(Strike, Ball))
    if Strike == 3:
        print("Success")
        break

    
