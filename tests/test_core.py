from neuro_nav_lab.envs.worlds import scenario_specs
from neuro_nav_lab.envs.navigation_env import NeuroNavigationEnv
from neuro_nav_lab.controllers.baselines import ReactiveAvoidController
from neuro_nav_lab.evaluation.runner import run_study, summarise

def test_env_reset_and_step():
    spec = scenario_specs()[0]
    env = NeuroNavigationEnv(spec, seed=7, max_steps=25)
    obs = env.reset()
    ctrl = ReactiveAvoidController()
    action = ctrl.act(obs)
    obs2, reward, done, info = env.step(action)
    assert "state_vector" in obs2
    assert len(obs2["lidar"]) == 24
    assert isinstance(info["collision"], bool)

def test_main_study_smoke():
    records, trajectories = run_study(base_seed=5, repeats=1)
    summary = summarise(records)
    assert len(records) == 24
    assert "Reactive" in summary
    assert len(trajectories) >= 4
