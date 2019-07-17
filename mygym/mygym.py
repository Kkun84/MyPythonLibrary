import typing
import dataclasses as dc
import numpy as np
import pandas as pd

import torch
from torch import nn
from torch.nn import functional as F

from mygym.transition import Transition


@dc.dataclass
class History:
    step: typing.List[int] = dc.field(
        default_factory=list)
    lr: typing.List[float] = dc.field(
        default_factory=list)
    epsilon: typing.List[float] = dc.field(
        default_factory=list)
    reward: typing.List[float] = dc.field(
        default_factory=list)
    loss: typing.List[float] = dc.field(
        default_factory=list)
    update: typing.List[bool] = dc.field(
        default_factory=list)
    report: typing.List[str] = dc.field(
        default_factory=list)

    def append(self, **kwargs):
        for key in kwargs.keys():
            self.__dict__[key].append(kwargs[key])

    def to_dict(self):
        return dc.asdict(self)

    def save_csv(self, path):
        src = pd.DataFrame(self.__dict__)
        src.to_csv(path, index=False)

    @staticmethod
    def load_csv(path):
        dst = pd.read_csv(path)
        dst = History(**dst.to_dict('list'))
        return dst

    @classmethod
    def buffer(cls):
        changes = {key: value.__args__[0]() for key, value in
                   cls.__annotations__.items()}
        replaced = dc.replace(cls(), **changes)
        return replaced


class DQN(nn.Module):

    def select_action(self, state, eps, return_q=False):
        if eps <= np.random.rand():
            with torch.no_grad():
                q = self(state)
            action = q.max(1)[1].item()
        else:
            action = np.random.randint(self.output_shape)
            q = None
        if return_q:
            if q is not None:
                q = q.tolist()
            return action, q
        return action


def optimize_model(memory, batch_size, gamma, policy_net, target_net, optimizer):
    device = next(policy_net.parameters()).device

    transitions = memory(batch_size)
    batch = Transition.from_transitions(transitions)

    state = torch.stack(batch.state)
    action = torch.stack(batch.action)
    next_state = torch.stack(batch.next_state)
    reward = torch.stack(batch.reward)
    done = torch.stack(batch.done)

    with torch.no_grad():
        next_action = policy_net(next_state).max(1, keepdim=True)[1]
        next_state_values = torch.zeros(batch_size, 1).to(device).float()

        mask = (done == False)[:, 0]
        next_state_values[mask] = target_net(
            next_state[mask]).gather(1, next_action[mask])
        expected_state_action_values = reward + gamma * next_state_values

    state_action_values = policy_net(state).gather(1, action)
    loss = F.smooth_l1_loss(state_action_values,
                            expected_state_action_values.detach())

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss.item()
