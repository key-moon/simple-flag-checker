import angr
import claripy
from tqdm import tqdm
from extract_data import FLAG_LEN

proj = angr.Project("checker")

AT_CHR_LOAD = 0x401a08
AFTER_MEMCMP = 0x401a2f

t = tqdm(total=FLAG_LEN)
def step_func(lsm: angr.SimulationManager):
  def populate_next(state: angr.SimState):
    if state.addr != AT_CHR_LOAD: return False
    t.update()
    states = []
    for c in range(0x20, 0x80):
      new_state = state.copy()
      new_state.globals["flag"] += chr(c)
      next_flag = new_state.globals["flag"].encode()
      new_state.memory.store(state.regs.sp + 0x30, next_flag, len(next_flag))
      states.append(new_state)
    return states

  def remove_non_zero(state: angr.SimState):
    if state.addr != AFTER_MEMCMP: return False
    return state.regs.rax.concrete_value != 0

  lsm.apply(populate_next)
  lsm.drop(filter_func=remove_non_zero)
  
  return lsm

state = proj.factory.entry_state(
  stdin=claripy.BVV(b''),
  add_options={
    *angr.options.unicorn,
    "ZERO_FILL_UNCONSTRAINED_MEMORY",
    "ZERO_FILL_UNCONSTRAINED_REGISTERS",
  }
)
state.globals["flag"] = ""

# unicornでの実行は謎のクールダウンがあるので、それを無効化する
# https://github.com/angr/angr/blob/9005e7186952d20f7a71f49d35744896ff978313/angr/state_plugins/unicorn_engine.py#L606-L618
state.unicorn.cooldown_nonunicorn_blocks = 0

simgr = proj.factory.simulation_manager(state)
simgr.explore(
  step_func=step_func,
  find=lambda state: b'Correct!' in state.posix.dumps(1),
  # https://github.com/angr/angr/blob/9005e7186952d20f7a71f49d35744896ff978313/angr/engines/unicorn.py#L30
  extra_stop_points={
    AT_CHR_LOAD,
    AFTER_MEMCMP,
  }
)
t.close()

print(simgr.found[0].globals["flag"])
