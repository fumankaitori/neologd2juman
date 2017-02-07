import os


def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)


def find_jumanrc_file(jumanrc_file='.jumanrc', parent_dir='/'):
    """* What you can do
    - You find jumanrc file from you system
    """
    seq_jumanrc_candidate = []
    for file in fild_all_files(parent_dir):
        if file == jumanrc_file:
            seq_jumanrc_candidate.append(file)

    if len(seq_jumanrc_candidate) >= 2:
        raise Exception('It found more than 2 .jumanrc files. It can not decide which file should be used. End.')
    elif len(seq_jumanrc_candidate)==0:
        return None
    else:
        return seq_jumanrc_candidate[0]

usr_result = find_jumanrc_file(parent_dir='/usr')
if not usr_result is None:
    print(usr_result)
else:
    User_result = find_jumanrc_file(parent_dir='/Users')
    print(User_result)