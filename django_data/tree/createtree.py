import io
import uuid
from pathlib import Path
from collections import deque

from django.conf import settings
from graphviz import Digraph

from persons.models import Person


class Tree:
    """Single children get one node too much"""

    def __init__(self, filetype="svg"):
        self.stack = deque()
        self.filename = Path(settings.BASE_DIR, "static", "images", "output")
        self.graph = Digraph(filename=self.filename, node_attr={
            'shape': "box"}, edge_attr={"dir": "none"}, format=filetype)
        self.male_color = "deepskyblue"
        self.female_color = "pink"

    def build_tree(self, oldest_ancestor):
        with self.graph.subgraph() as s:
            s1 = Digraph()
            s2 = Digraph()
            self.add_person(oldest_ancestor, s1, s2)
            self.add_to_stack(oldest_ancestor)
            self.graph.subgraph(s1)
            self.graph.subgraph(s2)
        while self.stack:
            self.add_family(self.stack.popleft())

    def add_spouse(self, person):
        with self.graph.subgraph() as s:
            s.attr(rank='same')
            spouse = person.get_spouse()
            if spouse:
                color = self.get_color(spouse)
            else:
                color = self.get_color(person, reverse=True)
                spouse = self.get_unknown_spouse()
            s.attr("node", color=color, style="filled",
                   width="2", shape="box")
            s.node(f"{spouse.id}", self.get_person_string(spouse))
            s.attr("node", shape="circle", color="black",
                   style="filled", width="0.05", fixedsize="true")
            s.node(f"spouse_con{person.id}", "")
            if person.gender == "Male":
                s.edge(f"{person.id}", f"spouse_con{person.id}")
                s.edge(f"spouse_con{person.id}", f"{spouse.id}")
            else:
                s.edge(f"{spouse.id}", f"spouse_con{person.id}")
                s.edge(f"spouse_con{person.id}", f"{person.id}")

    def add_children(self, person):
        children = person.get_children()

        s1 = Digraph()
        s2 = Digraph()
        for child in children:
            self.add_person(child, s1, s2)
        self.graph.subgraph(s1)
        self.graph.subgraph(s2)

        s = Digraph()
        s.attr(rank='same')
        children = list(children)
        for i in range(len(children)):
            if children[i] != children[-1]:
                s.edge(f"sibling_con{children[i].id}",
                       f"sibling_con{children[i+1].id}")
        self.graph.subgraph(s)

        s = Digraph()
        s.attr(rank='')

        s.edge(f"spouse_con{person.id}", f"sibling_con{children[0].id}")
        self.graph.subgraph(s)

    def add_person(self, person, s1, s2):
        s1.attr(rank='same')
        s2.attr(rank='same')
        color = self.get_color(person)
        s1.attr("node", color=color, style="filled", width="", shape="box")
        s1.node(f"{person.id}", self.get_person_string(person))
        s2.attr("node", shape="circle", color="black",
                style="filled", width="0.05", fixedsize="true")
        s2.node(f"sibling_con{person.id}", "")
        s2.attr(rank='')
        s2.edge(f"sibling_con{person.id}", f"{person.id}")

    def add_family(self, person):
        children = person.get_children()
        if children:
            self.add_spouse(person)
            self.add_children(person)
            self.add_to_stack(children)

    def add_to_stack(self, elements):
        if type(elements) == list:
            for element in elements:
                self.stack.append(element)
        else:
            self.stack.append(elements)

    def get_person_string(self, person):
        text = f"{person.first_name} {person.last_name}\n"
        date_of_birth = person.date_of_birth
        date_of_death = person.date_of_death
        hometown = person.hometown
        if date_of_birth:
            text += f"{date_of_birth}\n"
        if date_of_death:
            text += f"† {date_of_death}\n"
        if hometown:
            text += f"{hometown}"
        return text

    def get_color(self, person, reverse=False):
        if person.gender == "Male":
            if reverse == False:
                return self.male_color
            else:
                return self.female_color
        else:
            if reverse == False:
                return self.female_color
            else:
                return self.male_color

    def get_unknown_spouse(self):
        return Person(
            id=uuid.uuid4(),
            first_name="Unknown",
            last_name="Spouse",
            maiden_name=None,
            gender=None,
            date_of_birth=None,
            date_of_death=None,
            mother=None,
            father=None,
            hometown=None,
            infos=None
        )

    def show(self):
        self.graph.render(self.filename, view=True)

    def get_svg(self):
        return self.graph.pipe().decode("utf-8")

    def get_file(self):
        return self.graph.pipe()
