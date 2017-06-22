from random import choice

def random_walk(max_iters =1e12):
    walk = 0
    direction = [1, -1]
    try:
        for i in range(int(max_iters)):
            walk += choice(direction)
    except KeyboardInterrupt:
            print("Process Interrupted at Iteraction" + str(i))
    else:
            print("Process Completed")
    finally:
        return walk


class Contentfilter(object):
    def __init__(self, arg):
        if isinstance(arg,str):
            fname = arg + ".txt"
            with open(fname,"r") as f:
                self.contents = f.readlines()
                self.contents = [line.rstrip("\n") for line in self.contents]
                self.name = arg
        else:
            raise TypeError("Wrong Entry Type")

    def uniform(self,other,mode="w", case="upper"):
        if mode != "w" and mode != "a":
            raise ValueError("Wrong Mode to write file")
        out = other + ".txt"
        if case == "upper":
            with open(out,mode) as outfile:
                for lines in self.contents:
                    outfile.write(lines.upper() + "\n")
        elif case =="lower":
            with open(out,mode) as outfile:
                for lines in self.contents:
                    outfile.write(lines.lower() + "\n")
        else:
            raise ValueError("I need a proper case")

    def reverse(self, other, mode= "w", unit = "line"):
        if mode!= "w" and mode != "a":
            raise ValueError("Wrong Mode to write file")
        out = other + ".txt"
        if unit == "word":
            with open(out, mode) as outfile:
                for lines in self.contents:
                    words = lines.split()
                    rev = " ".join(words[::-1])
                    outfile.write(rev + "\n")
        elif unit =="line":
            with open(out, mode) as outfile:
                contents = self.contents[::-1]
                for lines in contents:
                    outfile.write(lines + "\n")
        else:
            raise ValueError("I need a proper unit")

    def transpose(self, other, mode="w"):
        if mode!= "w" and mode != "a":
            raise ValueError("Wrong Mode to write file")
        out = other + ".txt"
        length = len(self.contents[0].split())
        for lines in self.contents:
            if len(lines.split()) != length:
                raise ValueError("Not symmetric file")
        with open(out, mode) as outfile:
            for x in range(0,length):
                trans = [line.split()[x] for line in self.contents]
                line = " ".join(trans)
                outfile.write(line + "\n")

    def __str__(self):
        totaltext = " ".join(self.contents)
        # We stripped away all \n, but here we introduce a blank space
        # when recombining the text
        sp_count = sum(c.isspace() for c in totaltext)
        num_count = sum(c.isdigit() for c in totaltext)
        word_count = sum(c.isalpha() for c in totaltext)
        tot_count = len(totaltext)
        line_count = len(self.contents)
        return "Source File: \t" + self.name  + ".txt" + \
         "\nTotal Characters: \t" + str(tot_count) + \
         "\nAlphabetic Characters: \t" + str(word_count) + \
         "\nNumerical Characters: \t" + str(num_count) + \
         "\nWhitespace Characters: \t" + str(sp_count) + \
         "\nNumber of Lines: \t" + str(line_count)
