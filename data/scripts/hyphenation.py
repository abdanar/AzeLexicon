# under construction - ignore this file

sait = ['a', 'ə', 'i', 'o', 'ö', 'u', 'ü']

def is_samit(char):
    return char not in sait
def is_sait(char):
    return char in sait

word = "kitabxana"


def hyphenate(word):
    string = ""
    while len(string.replace("-", "")) < len(word):
        print(len(string.replace("-", "")) < len(word))
        print(word)
        if len(word) == 1:
            string += word
            break
        elif len(word) == 2:
            string += word
            break
        elif len(word) == 3:
            if is_samit(word[0]) and is_sait(word[1]) and is_samit(word[2]):
                string += word[:2] + "-" + word[2]
                break
            else:
                string += word
                break
        else:
            if is_samit(word[2]):
                if is_sait(word[3]):
                    string += word[:2] + "-"
                    word = word[2:]
                    print("case 1")
                else:
                    string += word[:3] + "-"
                    word = word[3:]
                    print("case 2")
            else:
                string += word[0] + "-"
                word = word[1:]
                print("case 3")
    return string
print(hyphenate(word))