from frame import Frame


class StandardAction(object):

    def __init__(self, name, cfg):
        self.name = name
        self.size = cfg['size']
        self.frames = [[], []]
        angles = [cfg['0_angle'], cfg['1_angle']]
        for aspect in (0, 1):
            if len(angles[aspect]) == 0: continue
            frames = self.frames[aspect]
            for i in range(self.size):
                bone_points = cfg['0'][i] if aspect == 0 else cfg['1'][i]
                frame_angles = angles[aspect][i]
                frames.append(Frame(i, bone_points, frame_angles, aspect, cfg))

        # self.aspect_weight = cfg['aspect_weight']
        self.repeat = cfg['repeat']

        states = list(range(self.size))
        last_end_id = -1
        end_id = -1
        for start_id, end_id, rep_num in self.repeat:
            self.states = states[last_end_id + 1: start_id] + states[start_id: end_id + 1] * rep_num
            last_end_id = end_id
        self.states += states[end_id + 1: ]

        # self.transfer_time_required = cfg['transition']
        self.updown = cfg['updown']
        self.rotate = cfg['rotate']