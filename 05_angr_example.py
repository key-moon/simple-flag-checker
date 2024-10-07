import subprocess
import angr

subprocess.run("gcc -o bin/05_angr_example 05_angr_example.c", shell=True)

proj = angr.Project("bin/05_angr_example")

state = proj.factory.entry_state()
simgr = proj.factory.simulation_manager(state)

simgr.explore(find=lambda state: b'Correct!' in state.posix.dumps(1)) # can be address
state = simgr.found[0]
print(state.posix.dumps(0))
