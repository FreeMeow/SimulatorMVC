import math

def calculate_new_angle(p_src,p_dst):
    if p_dst.x == p_src.x:
        if p_dst.y > p_src.y:
            target_angle = math.pi * 0.5
        else:
            target_angle = math.pi * 1.5
    else:
        target_angle = math.atan((p_dst.y - p_src.y) / (p_dst.x - p_src.x))
        if p_dst.x < p_src.x:
            target_angle += math.pi
    return target_angle

def get_rotation_frames(old_angle,new_angle,position, rotation_speed):
    ang_src = old_angle % (math.pi*2) if old_angle else 0
    ang_dst = new_angle % (math.pi*2)
    if ang_src > ang_dst:
        if ang_src - ang_dst < math.pi:
            delta = ang_src - ang_dst
            sign = -1
        else:
            delta = ang_dst - ang_src + 2*math.pi
            sign = 1
    else:
        if ang_dst - ang_src < math.pi:
            delta = ang_dst - ang_src
            sign = 1
        else:
            delta = ang_src - ang_dst + 2*math.pi
            sign = -1

    frames = []
    for i in range(int(delta / rotation_speed)):
        frames.append({'angle':ang_src + i*rotation_speed * sign, 'position':position})
    frames.append({'angle':ang_dst,'position':position})
    return frames


