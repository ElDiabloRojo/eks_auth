def yes_or_no(question):
    answer = input(question + " (y/n): ")
    while not(answer == "y" or answer == "yes" or \
    answer == "n" or answer == "no"):
        print("\ninput yes or no\n")
        answer = input(question + " (y/n): ")
    if answer[0] == "y":
        return True
    else:
        return False

def request_value(request):
    response = input('%s: ' % request)
    return str(response)
