import torch

from cost import Cost

class CarSystemStateCost(Cost):
    def __init__(self, reward, name=""):
        """
        Initialize with dimension to add cost to and origin to center the
        quadratic cost about.

        :param dimension: dimension to add cost
        :type dimension: uint
        :param threshold: value along the specified dim where the cost is zero
        :type threshold: float
        """
        self.reward = reward
        super(CarSystemStateCost, self).__init__(name)

    def __call__(self, xu, k=0):
        """
        Evaluate this cost function on the given input, which might either be
        a state `x` or a control `u`. Hence the input is named `xu`.
        NOTE: `xu` should be a PyTorch tensor with `requires_grad` set `True`.
        NOTE: `xu` should be a column vector.

        :param xu: state of the system
        :type xu: torch.Tensor
        :return: scalar value of cost
        :rtype: torch.Tensor
        """
        #remember to change xu to a pytorch tensor
        return -self.reward.state_reward_torch(0, xu, None)
