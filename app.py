from typing import (
    Any, Union,
)

from neomodel import (
    db, Q,
)

from models import (
    Skill, TeamMember, ProficiencyRel,
)


def create_sample_data():
    """creation of nodes and relationship between those"""
    # create skills
    python: Union[Skill, Any] = Skill(name="Python").save()
    fim_process = Skill(name="FIM Process").save()
    neo4j = Skill(name="neo4j").save()
    data_engineering = Skill(name="Data Engineering").save()
    data_visualization = Skill(name="Data Visualization").save()

    # create team members and connect to skill
    tom = TeamMember(first_name="Tom", last_name="Holiday").save()
    tom.skill.connect(python, {"year": 2019, "score": 4.0})
    tom.skill.connect(fim_process, {"year": 2019, "score": 5.0})
    tom.skill.connect(python, {"year": 2020, "score": 5.0})
    tom.skill.connect(fim_process, {"year": 2020, "score": 5.0})
    tran = TeamMember(first_name="Tran", last_name="Charismatic").save()
    tran.skill.connect(python, {"year": 2019, "score": 3.0})
    ron = TeamMember(first_name="Ron", last_name="Paradise").save()
    ron.skill.connect(neo4j, {"year": 2019, "score": 2.0})
    ron.skill.connect(python, {"year": 2019, "score": 3.0})
    ron.skill.connect(data_engineering, {"year": 2019, "score": 5.0})
    dev = TeamMember(first_name="Dev", last_name="Global").save()
    dev.skill.connect(data_engineering, {"year": 2019, "score": 4.0})
    dev.skill.connect(data_visualization, {"year": 2019, "score": 3.0})
    aqua = TeamMember(first_name="Aqua", last_name="Gloss").save()
    aqua.skill.connect(data_visualization, {"year": 2019, "score": 2.0})
    aqua.skill.connect(python, {"year": 2019, "score": 2.0})
    prem = TeamMember(first_name="Prem", last_name="Chopra").save()
    prem.skill.connect(fim_process, {"year": 2019, "score": 3.0})
    print("Created sample data ...")


def sample_describe_graph():
    """this demonstrates use of cypher query and interpretation of result returned from the query"""
    rows, cols = db.cypher_query(
        "MATCH (t:TeamMember)-[p:PROFICIENCY_FOR]-(s:Skill) RETURN t, p, s"
    )
    # cols {0: TeamMember, 1: Proficiency, 2: Skill}
    for r in rows:
        team_member = TeamMember.inflate(r[0])
        proficiency = ProficiencyRel.inflate(r[1])
        skill = Skill.inflate(r[2])
        print(
            f"Team member {team_member.name} is proficient in skill {skill.name} with a score {proficiency.score} "
            f"in year {proficiency.year}\n"
        )


def sample_queries():
    """sample queries, using both techniques provided by neomodel and cypher query"""

    # use object graph mapping (OGM) to query for information
    print(f"Skill Python: {Skill.nodes.get_or_none(name='Python')}")
    print(f"Skill Java that doesn't exist: {Skill.nodes.get_or_none(name='Java')}")
    print("All team members name that starts with T:\n")
    team_members = TeamMember.nodes.filter(Q(first_name__startswith="T"))
    for n in team_members:
        print(f"\tTeam member: {n}\n")

    print("All team members name that starts with T with proficiencies more than 3 in:\n")
    excellencies = team_members.skill.match(score__gt=4.0)
    for ex in excellencies:
        print(f"\t Skills: {ex}\n")

    # use cypher queries
    print("Current graph description:")
    sample_describe_graph()

    print("The skills in which team member first name starting with T has score more than 3 in any year")
    rows, cols = db.cypher_query(
        "MATCH(t: TeamMember)-[p: PROFICIENCY_FOR]-(s:Skill) "
        "WHERE t.first_name STARTS WITH 'T' AND p.score > 3.0 "
        "RETURN DISTINCT (s)"
    )
    # cols: {0: Skill}
    for r in rows:
        skill = Skill.inflate(r[0])
        print(f"Skill name {skill.name}")

    print("For each of the available skills, find out the list of team members who has proficiency in it\n")
    skills = Skill.nodes.all()
    for skill in skills:
        rows, cols = db.cypher_query(
            "MATCH (s:Skill)-[p:PROFICIENCY_FOR]-(t:TeamMember) "
            "WHERE s.name = $name RETURN DISTINCT (t)", params={"name": skill.name}
        )
        print(f"\nSkill name: {skill.name}")
        for r in rows:
            team_member = TeamMember.inflate(r[0])  # cols: {0: TeamMember}
            print(f"Team member name {team_member.name}")
    print("Queried sample queries ...")


if __name__ == "__main__":
    # delete existing data prior to loading
    results, meta = db.cypher_query("MATCH (s:Skill) DETACH DELETE (s)")
    print("Deleted existing Skill nodes ...")
    results, meta = db.cypher_query("MATCH (t:TeamMember) DETACH DELETE (t)")
    print("Deleted existing TeamMember nodes ...")
    # load sample data
    create_sample_data()
    # sample queries
    sample_queries()
