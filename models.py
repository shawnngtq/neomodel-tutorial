"""
Use the following commands to create these definitions in neo4j.
neomodel_install_labels --db bolt://neo4j:tester@localhost:7687 models.py
"""

from neomodel import (
    AliasProperty, config, EmailProperty, FloatProperty, IntegerProperty, Relationship, StringProperty, StructuredNode,
    StructuredRel, ZeroOrMore,
)

config.DATABASE_URL = "bolt://neo4j:tester@localhost:7687"


class Skill(StructuredNode):
    name = StringProperty(required=True, unique_index=True)


# structure to define relationship attributes between Team Member and Skill
class ProficiencyRel(StructuredRel):
    year = IntegerProperty(required=True)
    score = FloatProperty(required=True)
    name = AliasProperty(to="year")  # demonstrates alias creation for property


class TeamMember(StructuredNode):
    first_name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    name = StringProperty(required=True)
    email: object = EmailProperty(required=True, unique_index=True)

    # defines the relationship between Team Member and Skill, The type of relationship is "PROFICIENCY_FOR",
    # and the team member can have zero or more Skills.
    skill = Relationship(Skill, "PROFICIENCY_FOR", cardinality=ZeroOrMore, model=ProficiencyRel)

    # This demonstrates creation of email address based on provided first_name and last_name. The user doesn't have
    # to provide an email address while creating a team member.
    def pre_save(self):
        self.email = f"{self.first_name}.{self.last_name}@acme.com"
        self.name = f"{self.last_name},{self.first_name}"
