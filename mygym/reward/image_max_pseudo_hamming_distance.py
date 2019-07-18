import numpy as np
import cv2

from .core import BaseReward


class ImageMaxPseudoHammingDistanceReward(BaseReward):

    def __init__(self, target, mode):
        if mode is 'sum':
            self.func = np.sum
        elif mode is 'mean':
            self.func = np.mean
        else:
            raise ValueError('mode must be "sum" or "mean".')
        self.dist_target, self.mask_target = self._make_dist_mask(
            np.array(target)
        )

    def reset(self, env, state):
        pass

    def __call__(self, env, state, done):
        dist_image, mask_image = self._make_dist_mask(state[0])
        distance = (self.func(dist_image * self.mask_target, (1, 2)) +
                    self.func(self.dist_target * mask_image, (1, 2)))
        distance = -distance.min().item()
        return distance

    @staticmethod
    def _make_dist_mask(image):
        bin_image = np.where(image < 0.5, 1, 0).astype(np.uint8)
        if len(image.shape) == 3:
            dist_image = np.array([
                cv2.distanceTransform(im, cv2.DIST_L2, 5) for im in bin_image
            ])
        else:
            dist_image = cv2.distanceTransform(bin_image, cv2.DIST_L2, 5)
        mask_image = np.logical_not(bin_image)
        return dist_image, mask_image
