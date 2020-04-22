import inquirer


def inquire(name, desc, choice):
    questions = [
        inquirer.List(
            name,
            message=desc,
            choices=choice,
        ),
    ]
    selection = inquirer.prompt(questions)

    return selection
