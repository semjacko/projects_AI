from itertools import product
from tkinter import *
import re


class GUI:

    def __init__(self, root, backend):
        self.backend = backend

        # hlavne okno
        root.title("Jednoduchy dopredny produkcny system")
        root.minsize(900, 625)
        root.maxsize(900, 625)
        root.config(bg="#5A6B6C")

        # top a bottom frame
        top_frame = Frame(root, bg='#5A6B6C')
        top_frame.grid(row=0, column=0, sticky=W)
        bottom_frame = Frame(root, width=500, height=400, bg='#5A6B6C')
        bottom_frame.grid(row=1, column=0, pady=5, sticky=W)

        # labely k toolbarom
        Label(top_frame, text="Iniciaizacia:", bg='#5A6B6C', font="Helvetica 12 bold", fg="#DCDADA").grid(row=0, column=0, padx=3, pady=5)
        Label(top_frame, text="Inferencia:", bg='#5A6B6C', font="Helvetica 12 bold", fg="#DCDADA").grid(row=1, column=0, padx=3, pady=5, sticky=E)

        # toolbar1
        tool_bar = Frame(top_frame, bg='#5A6B6C')
        tool_bar.grid(row=0, column=1, padx=5, pady=5)
        Button(tool_bar, text="Pracovna pamat", relief=RAISED, command=self.memory).grid(row=0, column=0, padx=5, ipadx=10)
        Button(tool_bar, text="Rodinne vztahy", relief=RAISED, command=self.family).grid(row=0, column=1, padx=5, ipadx=10)
        Button(tool_bar, text="Faktorial", relief=RAISED, command=self.factorial).grid(row=0, column=2, padx=5, ipadx=10)
        Button(tool_bar, text="Fibonacci", relief=RAISED, command=self.fibonacci).grid(row=0, column=3, padx=5, ipadx=10)

        # toolbar2
        tool_bar = Frame(top_frame, bg='#5A6B6C')
        tool_bar.grid(row=1, column=1, padx=5, pady=5, sticky=W)
        Button(tool_bar, text="Jeden krok", relief=RAISED, command=self.launch_step).grid(row=1, column=0, padx=5, ipadx=10)
        Button(tool_bar, text="Do konca", relief=RAISED, command=self.launch_all).grid(row=1, column=1, padx=5, ipadx=10)

        # labely k textom
        Label(bottom_frame, text="Pracovna pamat:", bg='#5A6B6C', font="Helvetica 10 bold", fg="#DCDADA").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        Label(bottom_frame, text="Baza pravidiel:", bg='#5A6B6C', font="Helvetica 10 bold", fg="#DCDADA").grid(row=0, column=1, padx=5, pady=5, sticky=W)
        Label(bottom_frame, text="Pomocny vystup:", bg='#5A6B6C', font="Helvetica 10 bold", fg="#DCDADA").grid(row=2, column=1, padx=5, pady=5, sticky=W)
        Label(bottom_frame, text="Vystup sprav:", bg='#5A6B6C', font="Helvetica 10 bold", fg="#DCDADA").grid(row=4, column=1, padx=5, pady=5, sticky=W)

        # scrollbary
        scrollbar_rules = Scrollbar(bottom_frame)
        scrollbar_rules.grid(row=1, column=2, sticky=(N, S, W))
        scrollbar_temporarytext = Scrollbar(bottom_frame)
        scrollbar_temporarytext.grid(row=3, column=2, sticky=(N, S, W))
        scrollbar_message = Scrollbar(bottom_frame)
        scrollbar_message.grid(row=5, column=2, sticky=(N, S, W))

        # textfieldy
        self.facts_text = Text(bottom_frame, bg='white', width=30, height=31, wrap=WORD)
        self.facts_text.grid(row=1, column=0, padx=(8, 0), rowspan=5)
        self.rules_text = Text(bottom_frame, bg='white', width=77, height=11, wrap=WORD, yscrollcommand=scrollbar_rules.set)
        self.rules_text.grid(row=1, column=1, padx=(8, 0), sticky=N)
        scrollbar_rules.config(command=self.rules_text.yview)
        self.temporary_text = Text(bottom_frame, bg='white', width=77, height=12, wrap=WORD, yscrollcommand=scrollbar_temporarytext.set)
        self.temporary_text.grid(row=3, column=1, padx=(8, 0), sticky=N)
        scrollbar_temporarytext.config(command=self.temporary_text.yview)
        self.message_text = Text(bottom_frame, bg='white', width=77, height=3, wrap=WORD, yscrollcommand=scrollbar_message.set)
        self.message_text.grid(row=5, column=1, padx=(8, 0), sticky=N)
        scrollbar_message.config(command=self.message_text.yview)

    def memory(self):
        facts = self.facts_text.get(1.0, END)
        rules = self.rules_text.get(1.0, END)
        self.backend.set_facts("", facts)
        self.backend.set_rules("", rules)
        self.facts_show()
        self.rules_show()

    def family(self):
        self.backend.set_facts("family")
        self.backend.set_rules("family")
        self.facts_show()
        self.rules_show()

    def factorial(self):
        self.backend.set_facts("factorial")
        self.backend.set_rules("factorial")
        self.facts_show()
        self.rules_show()

    def fibonacci(self):
        self.backend.set_facts("fibonacci")
        self.backend.set_rules("fibonacci")
        self.facts_show()
        self.rules_show()

    def facts_show(self):
        facts = self.backend.facts
        s = ""
        for f in facts:
            s += f + "\n"
        s = s[:-1]  # posledny enter
        self.facts_text.delete(1.0, END)
        self.facts_text.insert(1.0, s)

    def rules_show(self):
        rules = self.backend.rules
        s = ""
        for r in rules:
            s += str(r) + "\n"
        s = s[:-2]  # posledne entery
        self.rules_text.delete(1.0, END)
        self.rules_text.insert(1.0, s)

    def temporary_show(self):
        applicable_instances = self.backend.applicable_instances
        s = ""
        for ai in applicable_instances:
            s += ai + "\n"
        s = s[:-1]
        self.temporary_text.delete(1.0, END)
        self.temporary_text.insert(1.0, s)

    def message_show(self):
        messages = self.backend.messages
        s = ""
        for m in messages:
            s += m + "\n"
        s = s[:-1]
        self.message_text.delete(1.0, END)
        self.message_text.insert(1.0, s)

    def launch_step(self):
        self.backend.one_step()
        self.facts_show()
        self.rules_show()
        self.temporary_show()
        self.message_show()

    def launch_all(self):
        self.backend.all_steps()
        self.facts_show()
        self.rules_show()
        self.message_show()


class Backend:
    def __init__(self):
        self.facts = []
        self.rules = []
        self.applicable_instances = []
        self.messages = []

    def set_facts(self, input_file, input_facts=None):
        if input_facts is not None:
            self.facts = input_facts.split('\n')[:-1]
        else:
            f = open(input_file, "r")
            buf = f.read()
            # oddelia sa fakty a pravidla, potom sa rozdelia fakty, posledny je prazdny
            self.facts = buf.split('$\n')[0].split('\n')[:-1]

    def set_rules(self, input_file, input_rules=None):
        self.rules = []
        rules_raw = []
        if input_rules is not None:
            rules_raw = input_rules.split('\n\n')
        else:
            f = open(input_file, "r")
            buf = f.read()
            rules_raw = buf.split('$\n')[1].split('\n\n')
        for rw in rules_raw:
            self.rules.append(Rule(rw))

    def one_step(self):
        def get_values(facts):
            vals = []
            for f in facts:
                vals_in_fact = re.findall(r"\b[A-Z0-9]\S*", f)
                for vif in vals_in_fact:
                    if vif not in vals:
                        vals.append(vif)
            return vals

        def get_variables(conditions):
            vars = []
            for c in conditions:
                vars_in_condition = re.findall(r"\?\S+", c)
                for vic in vars_in_condition:
                    if vic not in vars:
                        vars.append(vic)
            return vars

        def is_true(condition, facts):
            if '<>' in condition:
                words = condition.split(" ")
                x = words[1]
                y = words[2]
                if x.isnumeric() and y.isnumeric():
                    return int(x) != int(y)
                else:
                    return x != y
            if '<' in condition:
                words = condition.split(" ")
                x = words[1]
                y = words[2]
                if x.isnumeric() and y.isnumeric():
                    return int(x) < int(y)
                else:
                    return x < y
            if '>' in condition:
                words = condition.split(" ")
                x = words[1]
                y = words[2]
                if x.isnumeric() and y.isnumeric():
                    return int(x) > int(y)
                else:
                    return x > y
            else:
                return condition in facts

        def get_applicable_instances(rule, variables, values_combinations, facts):
            applicable_instances = []
            for i in range(len(values_combinations)):
                flag = True
                for c in rule.conditions:
                    substitute_condition = c[:]
                    for j in range(len(variables)):
                        substitute_condition = substitute_condition.replace(variables[j], values_combinations[i][j])
                    if not is_true(substitute_condition, facts):
                        flag = False
                        break
                if flag:
                    s = ""
                    for a in rule.actions:
                        s += a + ","
                    s = s[:-1]
                    for j in range(len(variables)):
                        s = s.replace(variables[j], values_combinations[i][j])
                    s = rule.name + ", " + s
                    applicable_instances.append(s)
            return applicable_instances

        def filtrate(raw, facts):
            applicable = []
            for r in raw:
                actions_raw = r.split(", ")[1]   # oddelenie mena od akcii
                actions = actions_raw.split(',')  # rozdelenie jednotlivych akcii
                s = ""
                only_msg = True
                impossible_cmd = False
                for a in actions:
                    command = a.split(" ")[0]  # typ akcie je na 0tej pozicii
                    content = a.replace(command, "")[1:]  # po nahradeni este ostane medzera preto [1:]
                    if command == 'pridaj':
                        if content not in facts:
                            s += a + ","
                            only_msg = False
                        else:
                            impossible_cmd = True
                    elif command == 'vymaz':
                        if content in facts:
                            s += a + ","
                            only_msg = False
                        else:
                            impossible_cmd = True
                    elif command == 'sprava':
                        s += a + ","
                if not only_msg and not impossible_cmd:
                    s = s[:-1]
                    applicable.append(s)
            return applicable

        def calculate_formulas(text):
            new_text = text
            formulas = re.findall(r"\{ ([^}]*)\ }", text)
            for f in formulas:
                if len(f) > 0:
                    num = eval(f)
                    new_text = new_text.replace("{ " + f + " }", str(num))
            return new_text

        def execute(applicable, facts):
            new_facts = facts
            messages = []
            if len(applicable) == 0:
                return new_facts
            actions = applicable[0].split(",")    # vyberie sa 0ta instania, akcie sa rozdelia podla ciarky
            for a in actions:
                command = a.split(" ")[0]  # typ akcie je na 0tej pozicii
                content = a.replace(command, "")[1:]  # po nahradeni este ostane medzera preto [1:]
                content = calculate_formulas(content)
                if command == 'pridaj':
                    new_facts.append(content)
                elif command == 'vymaz':
                    new_facts.remove(content)
                elif command == 'sprava':
                    messages.append(content)
            return new_facts, messages

        values = get_values(self.facts)
        applicable_instances_raw = []
        for r in self.rules:
            variables = get_variables(r.conditions)
            values_combinations = list(product(values, repeat=len(variables)))
            applicable_instances_raw += get_applicable_instances(r, variables, values_combinations, self.facts)

        self.applicable_instances = filtrate(applicable_instances_raw, self.facts)
        if len(self.applicable_instances) <= 0:
            return 0
        self.facts, self.messages = execute(self.applicable_instances, self.facts)
        return 1

    def all_steps(self):
        status = 1
        while status == 1:
            status = self.one_step()


class Rule:
    def __init__(self, rule_raw):
        self.name = re.findall(r"Meno: (.*)", rule_raw)[0]
        self.conditions = re.findall(r"AK\s{4}(.*)", rule_raw)[0].split(",")
        self.actions = re.findall("POTOM (.*)", rule_raw)[0].split(",")

    def __repr__(self):
        s = "Meno: " + self.name + "\nAK    "
        for c in self.conditions:
            s += c + ","
        s = s[:-1] + "\nPOTOM "
        for a in self.actions:
            s += a + ","
        s = s[:-1] + "\n"
        return s


root = Tk()  # create root window
backend = Backend()
gui = GUI(root, backend)
root.mainloop()
