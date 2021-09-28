import logging

from analyzer import Analyzer
from attribute_container import AttributeContainer
from state_machine import ChainStateMachine
from standard_action import StandardAction
from static_similarity import angle_similarity, angle_similarity_almost


log_path = 'log/demo.log'
file_handler = logging.FileHandler(log_path, encoding='utf8')
logging.basicConfig(handlers={file_handler}, level=logging.INFO)


class ActionRecognizer(object):

    def __init__(self, name, cfg):
        self.standard_action = StandardAction(name, cfg)
        self.analyzer = Analyzer()
        self.time_limiter = None
        self.matched = [AttributeContainer(cfg), AttributeContainer(cfg)]
        self.reasons = [[], []]
        self.state_machines = [ChainStateMachine(self.standard_action.states),
                               ChainStateMachine(self.standard_action.states)]
        # self.output = []
        # self.analyse_output = []

    def match(self, frame):
        for aspect in [0, 1]:
            if not self.standard_action.frames[aspect]:
                continue

            self.update_preframe(frame, aspect)
            next_frame_id = self.state_machines[aspect].get_next_frame_id()
            standard_frame = self.standard_action.frames[aspect][next_frame_id]
            matched, score = angle_similarity_almost(frame, standard_frame)
            if not matched:
                continue
            logging.info('[当前状态首次匹配]当前帧号为: %d, 与视频%s的第%d个关键帧进行匹配, 得分为: %f'
                         %(frame.order, self.standard_action.name, next_frame_id, score))

            self.append_matched(score, frame, aspect, next_frame_id)
            break

    def update_preframe(self, frame, aspect):
        cur_frame_id = self.state_machines[aspect].get_cur_frame_id()
        cur_state = self.state_machines[aspect].cur_state
        if cur_frame_id is None: return
        matched, score = angle_similarity_almost(frame, self.standard_action.frames[aspect][cur_frame_id])
        # 设置动作起始帧的帧号
        if (len(self.output) == 0
            and self.time_limiter is not None
            and len(self.matched[aspect].matched_frame) == 1
            and matched):
            self.time_limiter.set_start_time(self.matched[aspect].matched_frame[0][0].order)

        if matched:
            self.matched[aspect].update_endure(frame)
            if score > self.matched[aspect].matched_frame[cur_state][1]:
                logging.info('[更新前一个状态的匹配帧]当前帧号为: %d, 更新视频%s的第%d个关键帧, 得分为: %f'
                             % (frame.order, self.standard_action.name, cur_frame_id, score))
                self.matched[aspect].update(frame, score, cur_frame_id)

    def append_matched(self, score, frame, aspect, matched_id):
        if self.state_machines[aspect].cur_state == self.state_machines[aspect].length - 1:
            self.report(aspect)
            self.clear()
            self.matched[aspect].base = frame.order - 1
        added = self.matched[aspect].add(frame, score, matched_id)
        if added:
            self.state_machines[aspect].state_change()

    def add_to_output_queue(self, aspect):
        # weights = self.frame_weights[aspect]
        # total_score = sum(score * weight for (_, score), weight in zip(self.matched[aspect], weights.values()))

        standard_frames = map(lambda ind: self.standard_action.frames[aspect][ind], self.standard_action.states)
        score, reasons = self.analyzer.analyze(self.matched[aspect], standard_frames)
        self.output.append((self.standard_action.name, score))
        self.analyse_output.append(reasons)

    def set_time_limiter(self, limiter):
        self.time_limiter = limiter

    def set_output(self, output):
        self.output = output

    def clear(self):
        self.analyzer.clear()
        for aspect in [0, 1]:
            self.state_machines[aspect].reinitialize()
            self.matched[aspect].clear()



