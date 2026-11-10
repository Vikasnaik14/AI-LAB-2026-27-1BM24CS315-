"""
VACUUM CLEANER AGENT
=====================
World: Two locations, A and B. Each can be 'Dirty' or 'Clean'.
The agent (vacuum) can be in either location and can:
  - Move Left
  - Move Right
  - Suck (clean the dirt)

Two agent types are shown:
  1. Simple Reflex Agent  -> decides using ONLY the current percept (no memory/goal).
  2. Goal-Based Agent     -> decides by checking if the GOAL (both rooms clean)
                              is satisfied, and picks actions that move it closer
                              to that goal.
"""

import random  # used to randomly set up the starting dirt state for the demo


# ---------------------------------------------------------
# 1. THE ENVIRONMENT
# ---------------------------------------------------------
class Environment:
    def __init__(self):
        # status: dictionary holding cleanliness of each location
        self.status = {
            'A': random.choice(['Clean', 'Dirty']),
            'B': random.choice(['Clean', 'Dirty'])
        }
        # agent starts randomly in room A or B
        self.location = random.choice(['A', 'B'])

    def percept(self):
        # The agent can only "see" its current location and that room's status
        return (self.location, self.status[self.location])

    def is_goal_state(self):
        # Goal: every room must be Clean
        return all(state == 'Clean' for state in self.status.values())

    def act(self, action):
        # Apply the chosen action to change the environment
        if action == 'Suck':
            self.status[self.location] = 'Clean'
        elif action == 'Right':
            self.location = 'B'
        elif action == 'Left':
            self.location = 'A'
        # 'NoOp' (no operation) changes nothing


# ---------------------------------------------------------
# 2. SIMPLE REFLEX AGENT
#    Rule: react only to the current percept, no planning ahead.
# ---------------------------------------------------------
def simple_reflex_agent(percept):
    location, status = percept          # unpack current location and its status

    if status == 'Dirty':
        return 'Suck'                   # rule 1: if dirty, clean it
    elif location == 'A':
        return 'Right'                  # rule 2: if clean and in A, go to B
    elif location == 'B':
        return 'Left'                   # rule 3: if clean and in B, go to A


# ---------------------------------------------------------
# 3. GOAL-BASED AGENT
#    Checks the GOAL (both rooms clean) before acting.
#    It "looks ahead" instead of just reacting to one room.
# ---------------------------------------------------------
def goal_based_agent(percept, env):
    location, status = percept

    if env.is_goal_state():
        return 'NoOp'                   # goal already achieved, do nothing

    if status == 'Dirty':
        return 'Suck'                   # clean current room first

    # current room is clean but goal isn't reached -> dirt must be elsewhere
    return 'Right' if location == 'A' else 'Left'


# ---------------------------------------------------------
# 4. RUNNER: simulate an agent acting in the environment
# ---------------------------------------------------------
def run_agent(agent_type='reflex', max_steps=10):
    env = Environment()
    print(f"\n--- Running {agent_type.upper()} agent ---")
    print(f"Start state: location={env.location}, status={env.status}")

    for step in range(1, max_steps + 1):
        percept = env.percept()

        if agent_type == 'reflex':
            action = simple_reflex_agent(percept)
        else:
            action = goal_based_agent(percept, env)

        print(f"Step {step}: percept={percept} -> action={action}")
        env.act(action)

        if env.is_goal_state():
            print(f"Goal reached! Final status: {env.status}")
            break


# ---------------------------------------------------------
# 5. DEMO
# ---------------------------------------------------------
if __name__ == "__main__":
    run_agent('reflex')
    run_agent('goal')