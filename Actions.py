import logging

logging.basicConfig(filename='log/demo.log', level=logging.INFO)

class SimpleAction(object):

    def __init__(self, name, cfg, angles, output, analyse_output):
        self.name = name
        self.bone_points = [cfg['0'], cfg['1']]
        self.angles = [angles, []]
        self.size = len(self.bone_points[0])
        self.current_states = [-1, -1]
        self.next_states = [[0], [0]]
        self.matched = [[], []]
        self.reasons = [[], []]
        self.angle_weights = [cfg['0_angle_weights'], cfg['1_angle_weights']]
        self.frame_weights = [cfg['0_frame_weights'], cfg['1_frame_weights']]
        self.angle_thresholds = [cfg['0_angle_thresholds'], cfg['1_angle_thresholds']]
        # self.aspect_weight = cfg['aspect_weight']
        self.repeat = cfg['repeat']
        self.hold = cfg['hold']
        self.updown = cfg['updown']
        self.rotate = cfg['rotate']
        self.output = output
        self.analyse_output = analyse_output

    def match(self, ankles, frame_idx):

        for aspect in [0, 1]:
            if not self.angles[aspect]:
                continue
            for state in self.next_states[aspect]:
                self.update_matched(ankles, frame_idx, aspect)

                matched, score, reason = self.match_frame(ankles, aspect, state)
                if matched:
                    reason = (frame_idx, *reason)
                    print('当前帧号为: %d, 失误位置:%s, 标准角度: %f, 错误角度: %f, 与关键帧: %d匹配,得分为: %f'%(*reason, state, score))

                    self.append_and_report(score, reason, frame_idx, aspect, state)
                    break


    def update_matched(self, ankles, frame_idx, aspect):
        cur_state = self.current_states[aspect]
        matched, score, reason = self.match_frame(ankles, aspect, cur_state)

        if matched and score < self.matched[aspect][cur_state][1]:
            reason = (frame_idx, *reason)
            print('当前帧号: %d, 失误位置:%s, 标准角度: %f, 错误角度: %f, 更新关键帧: %d, 新的得分: %f'%(*reason, cur_state, score))

            self.matched[aspect][cur_state] = (frame_idx, score)
            self.reasons[aspect][cur_state] = reason

    def match_frame(self, bones, aspect, frame_ind):
        weights = self.angle_weights[aspect]
        frame_to_match = self.angles[aspect][frame_ind]

        thresholds = self.angle_thresholds[aspect]

        diffs = {key: abs(frame_to_match[key] - bones[key]) for key in bones if key in frame_to_match}
        matched = all(diffs[key] < thresholds[key] for key in diffs)
        score = None
        reason = None
        if matched:
            values = {key: diffs[key] / thresholds[key] * weights[key] for key in diffs}
            score = sum(values.values())
            reason = self.analyse(values, frame_to_match, bones)
        return matched, score, reason

    def append_and_report(self, score, reason, frame_idx, aspect, matched_id):
        matched_frames = self.matched[aspect]
        matched_reason = self.reasons[aspect]
        self.state_change(matched_id, aspect)
        matched_frames.append((frame_idx, score))
        matched_reason.append(reason)
        if self.current_states[aspect] == self.repeat[1]:
            self.report(aspect)

    def state_change(self, matched_id, aspect):
        self.current_states[aspect] = matched_id

        start_id, end_id = self.repeat
        if matched_id == end_id:
            self.next_states[aspect] = [start_id, (matched_id + 1) % self.size]
        else:
            self.next_states[aspect] = [(matched_id + 1) % self.size]


    def analyse(self, values, standard_bones, bones):
        k = sorted(values.keys(), key=lambda k: values[k], reverse=True)[0]
        reason = (k, standard_bones[k], bones[k])
        return reason

    def report(self, aspect):
        weights = self.frame_weights[aspect]
        total_score = sum(score * weight for (_, score), weight in zip(self.matched[aspect], weights.values()))
        self.output.append((self.name, total_score))
        self.analyse_output.append(self.reasons[aspect])
        start_id = self.repeat[0]
        matched_frames = self.matched[aspect]
        matched_frames = matched_frames[:start_id]
        reasons = self.reasons[aspect]
        reasons = reasons[:start_id]

    def clear(self):
        self.current_states = [-1, -1]
        self.next_states = [[0], [0]]
        self.matched = [[], []]

    @staticmethod
    def face_towards(eye_points, ear_points):
        pass
