class Analyzer(object):
    def __init__(self):
        self.trans = []
        self.endure = []
        self.beta1 = 0.9
        self.beta2 = 0.9

    def analyze(self, container, standard_frames):
        score = self.get_total_score(container)
        frames = [f[0] for f in container.matched_frame]
        reasons = []
        for frame_x, frame_y in zip(frames, standard_frames):
            standard_angles = frame_y.get_angles()
            angles = frame_x.get_angles()

            diffs = {key: abs(standard_angles[key] - angles[key]) for key in angles if key in standard_angles}
            k = sorted(diffs.keys(), key=lambda k: diffs[k], reverse=True)[0]
            reason = [k, standard_angles[k], angles[k]]
            reasons.append(reason)
        for idx in self.endure:
            reasons[idx].append('动作持续时间较短')

        for idx, idy in self.trans:
            reasons[idx].append('与第%d个动作切换时间太快'%idy)
            reasons[idy].append('与第%d个动作切换时间太快' % idx)
        return score, reasons

    def get_total_score(self, container):
        scores = [t[1] for t in container.matched_frame]
        if len(container.action_endure) > 0:
            frame_endure = container.endure_analysis()
            for i in range(len(frame_endure)):
                edr_time, need_time = frame_endure[i]
                if need_time:
                    portion = edr_time / need_time if edr_time < need_time else 1
                    eta = self.beta1 + (1 - self.beta1) * portion
                    scores[i] *= eta
                    self.endure.append(i)
        if len(container.time_transfer_require) > 0:
            transfer_times = container.transfer_analysis()
            for t in transfer_times:
                for idx, idy, dur_time, real_time in t:
                    portion = real_time / dur_time if real_time < dur_time else 1
                    eta = self.beta2 + (1 - self.beta2) * portion
                    scores[idx] *= eta
                    scores[idy] *= eta
                    self.trans.append((idx, idy))

        return sum(scores) / len(scores)

    def clear(self):
        self.trans.clear()
        self.endure.clear()