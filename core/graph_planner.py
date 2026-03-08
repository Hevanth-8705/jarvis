class GraphPlanner:

    def __init__(self, planner):
        self.planner = planner

    def generate_plan(self, user_request):

        prompt = f"""
Break the following task into numbered executable steps.

Task:
{user_request}

Rules:
- Keep steps short.
- Each step must be independently executable.
- Only return numbered steps.
"""

        plan_text = self.planner.plan(prompt)

        steps = []

        for line in plan_text.split("\n"):
            line = line.strip()
            if line and line[0].isdigit():
                step = line.split(".", 1)[-1].strip()
                steps.append(step)

        return steps