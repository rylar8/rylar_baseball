from . import player


class Pitch():
    def __init__(self, data, inning, top_bottom, at_bat, pitch):
        self.game_data = data

        self.inning_data = self.game_data[self.game_data['Inning'] == inning]
        if top_bottom == 'top':
            self.half_inning_data = self.inning_data[self.inning_data['Top/Bottom'] == 'Top']
        elif top_bottom == 'bottom':
            self.half_inning_data = self.inning_data[self.inning_data['Top/Bottom'] == 'Bottom']
        else:
            raise ValueError(f"top_bottom parameter requires either 'top' or 'bottom' not '{top_bottom}'")

        self.at_bat_data = self.half_inning_data[self.half_inning_data['PAofInning'] == at_bat]
        self.data = self.at_bat_data[self.at_bat_data['PitchofPA'] == pitch]
        self.number = pitch

        if len(self.data) > 0:
            self.velocity = self.data['RelSpeed'].iloc[0]
            self.vertical = self.data['VertBreak'].iloc[0]
            self.induced = self.data['InducedVertBreak'].iloc[0]
            self.horizontal = self.data['HorzBreak'].iloc[0]
            self.spin = self.data['SpinRate'].iloc[0]
            self.axis = self.data['SpinAxis'].iloc[0]
            self.tilt = self.data['Tilt'].iloc[0]
            self.release_height = self.data['RelHeight'].iloc[0]
            self.release_side = self.data['RelSide'].iloc[0]
            self.release_extension = self.data['Extension'].iloc[0]
            self.auto_type = self.data['AutoPitchType'].iloc[0]
            self.tagged_type = self.data['TaggedPitchType'].iloc[0]
            self.call = self.data['PitchCall'].iloc[0]
            self.location_height = self.data['PlateLocHeight'].iloc[0]
            self.location_side = self.data['PlateLocSide'].iloc[0]
            self.exit_velocity = self.data['ExitSpeed'].iloc[0]
            self.launch_angle = self.data['Angle'].iloc[0]
            self.hit_direction = self.data['Direction'].iloc[0]
            self.hit_spin = self.data['HitSpinRate'].iloc[0]
            self.hit_type = self.data['TaggedHitType'].iloc[0]
            self.distance = self.data['Distance'].iloc[0]
            self.hang_time = self.data['HangTime'].iloc[0]
            self.hit_bearing = self.data['Bearing'].iloc[0]
            self.result = self.data['PlayResult'].iloc[0]
            self.outs_made = self.data['OutsOnPlay'].iloc[0]
            self.runs_scored = self.data['RunsScored'].iloc[0]
            self.catcher_velocity = self.data['ThrowSpeed'].iloc[0]
            self.catcher_pop = self.data['PopTime'].iloc[0]
            self.k_or_bb = self.data['KorBB'].iloc[0]
            self.vert_approach_angle = self.data['VertApprAngle'].iloc[0]
            self.horz_approach_angle = self.data['HorzApprAngle'].iloc[0]
            self.zone_speed = self.data['ZoneSpeed'].iloc[0]
            self.zone_time = self.data['ZoneTime'].iloc[0]
            self.pos_at_110x = self.data['PositionAt110X'].iloc[0]
            self.pos_at_110y = self.data['PositionAt110Y'].iloc[0]
            self.pos_at_110z = self.data['PositionAt110Z'].iloc[0]
            self.last_tracked_distance = self.data['LastTrackedDistance'].iloc[0]
            self.pfxx = self.data['pfxx'].iloc[0]
            self.pfxz = self.data['pfxz'].iloc[0]
            self.horz_loc_50 = self.data['x0'].iloc[0]
            self.from_home_loc_50 = self.data['y0'].iloc[0]
            self.vert_loc_50 = self.data['z0'].iloc[0]
            self.horz_velo_50 = self.data['vx0'].iloc[0]
            self.from_home_velo_50 = self.data['vy0'].iloc[0]
            self.vert_velo_50 = self.data['vz0'].iloc[0]
            self.horz_acc_50 = self.data['ax0'].iloc[0]
            self.from_home_acc_50 = self.data['ay0'].iloc[0]
            self.vert_acc_50 = self.data['az0'].iloc[0]
            self.con_pos_x = self.data['ContactPositionX'].iloc[0]
            self.con_pos_y = self.data['ContactPositionY'].iloc[0]
            self.con_pos_z = self.data['ContactPositionZ'].iloc[0]
            self.hit_spin_axis = self.data['HitSpinAxis'].iloc[0]

    def batter(self):
        return player.Batter(list(self.data['BatterId'])[0])

    def pitcher(self):
        return player.Pitcher(list(self.data['PitcherId'])[0])
    
    def catcher(self):
        return player.Catcher(list(self.data['CatcherId'])[0])

    def barreled(self, exit_velocity, launch_angle):

        barrel = False
        if exit_velocity >= 98.0:
            if exit_velocity <= 99.0:
                if launch_angle >= 26.0 and launch_angle <= 30.0:
                    barrel = True
            elif exit_velocity <= 100.0:
                if launch_angle >= 25.0 and launch_angle <= 31.0:
                    barrel = True
            #Not a perfect representation of a barrel, but pretty close
            else:
                range_growth = (exit_velocity - 100.0) * 1.2
                high_angle = min(31.0 + range_growth, 50.0)
                low_angle = max(25.0 - range_growth, 8.0)
                if launch_angle >= low_angle and launch_angle <= high_angle:
                    barrel = True

        return barrel