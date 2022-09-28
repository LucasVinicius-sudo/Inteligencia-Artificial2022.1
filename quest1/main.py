rules_file_path = "rules.txt" #arquivo com as regras da questão
facts_file_path = "facts.txt" #arquivo com os fatos da questão
hypothesis_file_path = "hypothesis.txt" #a hipotese

val = {} #
rules = {} #
facts = {} #
hypothesis = [] #
rule = [] #
used = [] #
query_item = "?" #

def check_item(item):
    if item not in val:
        val[item] = "?"
        rules[item] = []


def add_rule(item, index):
    check_item(item)
    rules[item].append(index)


def set_fact(fact, value):
    check_item(fact)
    val[fact] = value


def set_hypothesis(h, value):
    hypothesis.append((h, value))


def print_rules():#Regras que são estabelecidas no começo da questão
    print("Regras:")
    for item in rule:
        j = 0

        while j < len(item[0]):
            print(str(item[0][j][0]) + " = " + str(item[0][j][1]), end="")
            print("" if j == len(item[0]) - 1 else " e ", end="")
            j += 1

        print(" entao ", end="")
        print(str(item[1][0]) + " = " + str(item[1][1]))

    print()


def print_facts():#Gatos estabelecidos no começo da questão
    print("Fatos Iniciais:")
    for item in val.keys():
        if val[item] != "?":
            print(str(item) + " = " + str(val[item]))
    print()


def print_rule(r):
    print("Aplicando a regra " + str(r+1) + ": " +
          str(rule[r][1][0]) + " = " + str(rule[r][1][1]))



def parse_line(words):
    conditions = []
    conclusion = ("", "")
    i = 0

    while i < len(words):
        if words[i] == "se" or words[i] == "e":
            conditions.append((words[i + 1], words[i + 3]))
            i += 4
        else:
            conclusion = (words[i + 1], words[i + 3])
            i += 4

    return (conditions, conclusion)


def read_rules():
    lines = []

    with open(rules_file_path) as file:
        lines = file.readlines()

    index = 0

    for l in lines:
        parsed = parse_line(l.split())
        conditions = parsed[0]
        conclusion = parsed[1]
        rule.append((conditions, conclusion))

        for c in conditions:
            add_rule(c[0], index)

        check_item(conclusion[0])
        index += 1

    print_rules()


def read_facts():
    lines = []

    with open(facts_file_path) as file:
        lines = file.readlines()

    for l in lines:
        fact = l.split()
        set_fact(fact[0], fact[2])

    print_facts()


def read_hypothesis():
    lines = []

    with open(hypothesis_file_path) as file:
        lines = file.readlines()

    for l in lines:
        h = l.split()
        set_hypothesis(h[0], h[2])


def check_rule(r):
    result = True

    for item in rule[r][0]:
        if val[item[0]] == "?":
            global query_item
            query_item = item[0]

        if val[item[0]] != item[1]:
            result = False

    return result


def bfs():  # (busca em largura)
    global used #
    queue = [] #

    for item in val.keys():#
        if val[item] != "?": # ja sei o valor desse item
            queue.append(item) #

    while queue: #
        item = queue.pop(0) #
        for r in rules[item]: #
            if used[r]: #
                continue #

            if check_rule(r): #
                set_fact(rule[r][1][0], rule[r][1][1])#
                used[r] = 1#
                print_rule(r)#
                queue.append(rule[r][1][0])#


def answer(): #
    global used #
    global query_item#
    used = [False] * len(rule)#

    for item in hypothesis:
        result = "?"

        while result == "?":
            bfs()
            result = val[item[0]]

            if query_item == "?":
                query_item = item[0]

            if result == "?":  # indefinido, ainda nao consegui chegar em uma conclusao
                do_query()
            elif result == item[1]:
                print("\nHipotese (" + str(item[0]) +
                      " = " + str(item[1]) + ") é verdadeira!\n")
            else:
                print("\nHipotese (" + str(item[0]) +
                      " = " + str(item[1]) + ") é falsa!\n")


def main():
    read_rules()#ler as regras
    read_facts()#ler os fatos
    read_hypothesis()#ler a hipotese
    answer()#resposta hipotese verdadeira ou falsa


if __name__ == "__main__":
    main()
