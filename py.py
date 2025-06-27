average_score=int(input('Enter the student average score:'))
if average_score>=0 and average_score<=69:
    print('Result is fail')
elif average_score>=70 and average_score<=84:
    print('Result is Second class')
elif average_score>=85 and average_score<=95:
    print('Result is first class')
else:
    print('Result is Excellent')